#!/usr/bin/env python3
"""
render_end_sketch_video.py
Renders the 4-second Trump telephone video (VN20261104_232855.mp4) inside the
animated hand-drawn sketch box with fast, creative documentary kinetic subtitles
displayed directly on the video inside the box.
"""

import os, sys, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
INPUT_VIDEO = "/home/rashid/.gemini/antigravity/brain/1e5be721-c9b4-4d36-8f45-30a2f3a82e22/.user_uploaded/media_1793815278120_bfff079e.mp4"
OUTPUT_MP4 = os.path.join(PROJECT_DIR, "assets/titles/ending_trump_phone_clip.mp4")
OUTPUT_WAV = os.path.join(PROJECT_DIR, "assets/titles/ending_trump_phone_clip.wav")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MARKER = os.path.join(PROJECT_DIR, "assets/fonts/PermanentMarker.ttf")

WIDTH, HEIGHT = 1920, 1080
FPS = 30

# Fast small short subtitles with exact word timestamps
SUBTITLES = [
    {"start": 0.05, "end": 0.55, "text": "IN FACT...", "color": (255, 255, 255), "hl": False},
    {"start": 0.55, "end": 1.25, "text": "if people ever got...", "color": (230, 235, 245), "hl": False},
    {"start": 1.25, "end": 2.35, "text": "TIRED OF ME IN THE U.S.", "color": (255, 230, 0), "hl": True},
    {"start": 2.35, "end": 3.20, "text": "I'll move to Israel,", "color": (255, 255, 255), "hl": False},
    {"start": 3.20, "end": 4.05, "text": "BECOME PRIME MINISTER.", "color": (255, 220, 0), "hl": True},
]

def generate_sketch_lines(box, rng, jitter=2.6, passes=3):
    x0, y0, x1, y1 = box
    strokes = []
    n_pts = 8

    for p in range(passes):
        # Top
        over_l, over_r = rng.uniform(16, 32), rng.uniform(16, 32)
        sx, ex = x0 - over_l, x1 + over_r
        yv = y0 + rng.uniform(-jitter, jitter)
        pts = [(sx + (i/n_pts)*(ex - sx), yv + rng.uniform(-jitter, jitter)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Bottom
        over_l, over_r = rng.uniform(16, 32), rng.uniform(16, 32)
        sx, ex = x0 - over_l, x1 + over_r
        yv = y1 + rng.uniform(-jitter, jitter)
        pts = [(sx + (i/n_pts)*(ex - sx), yv + rng.uniform(-jitter, jitter)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Left
        over_t, over_b = rng.uniform(16, 32), rng.uniform(16, 32)
        sy, ey = y0 - over_t, y1 + over_b
        xv = x0 + rng.uniform(-jitter, jitter)
        pts = [(xv + rng.uniform(-jitter, jitter), sy + (i/n_pts)*(ey - sy)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Right
        over_t, over_b = rng.uniform(16, 32), rng.uniform(16, 32)
        sy, ey = y0 - over_t, y1 + over_b
        xv = x1 + rng.uniform(-jitter, jitter)
        pts = [(xv + rng.uniform(-jitter, jitter), sy + (i/n_pts)*(ey - sy)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

    # Cross-hatch shadow
    shadow_strokes = []
    for y_pos in range(int(y0 + 20), int(y1 + 40), 16):
        hx0 = x1 + rng.uniform(4, 7)
        hy0 = y_pos + rng.uniform(-2, 2)
        shadow_strokes.append(([(hx0, hy0), (hx0 + rng.uniform(18, 28), hy0 + rng.uniform(10, 16))], rng.uniform(1.8, 2.4), 160))

    for x_pos in range(int(x0 + 20), int(x1 + 35), 18):
        hx0 = x_pos + rng.uniform(-2, 2)
        hy0 = y1 + rng.uniform(4, 7)
        shadow_strokes.append(([(hx0, hy0), (hx0 + rng.uniform(12, 18), hy0 + rng.uniform(16, 24))], rng.uniform(1.8, 2.4), 160))

    return strokes, shadow_strokes

def precompute_sketch_variants(card_box, inner_box):
    seeds = [111, 222, 333, 444]
    variants = []
    for s in seeds:
        rng = random.Random(s)
        strokes, shadows = generate_sketch_lines(card_box, rng, jitter=2.4, passes=3)
        inner_strokes, _ = generate_sketch_lines(inner_box, rng, jitter=1.4, passes=2)
        variants.append({
            "strokes": strokes,
            "shadows": shadows,
            "inner": inner_strokes,
            "rng": rng
        })
    return variants

def main():
    print("=== Rendering Trump Phone Clip in Sketch Box with Kinetic Subtitles ===")
    os.makedirs(os.path.dirname(OUTPUT_MP4), exist_ok=True)
    
    # 1. Inspect source video frames count & dimensions
    probe_cmd = f'ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets,width,height -of json "{INPUT_VIDEO}"'
    info = subprocess.check_output(probe_cmd, shell=True).decode().strip()
    import json
    info_json = json.loads(info)
    stream_info = info_json["streams"][0]
    in_w = int(stream_info["width"])
    in_h = int(stream_info["height"])
    nb_frames = int(stream_info.get("nb_read_packets", 122))
    print(f"Source: {in_w}x{in_h}, total frames: {nb_frames}")
    
    # 2. Extract frames pipe from ffmpeg
    pipe_in_cmd = [
        "ffmpeg", "-i", INPUT_VIDEO,
        "-f", "image2pipe",
        "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo", "-"
    ]
    pipe_in = subprocess.Popen(pipe_in_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
    
    # 3. Output pipe to ffmpeg for encoding
    temp_video_only = "/tmp/end_sketch_vonly.mp4"
    pipe_out_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        temp_video_only
    ]
    pipe_out = subprocess.Popen(pipe_out_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    
    # Dimensions on 1080p canvas
    vh = 920
    vw = int(vh * (in_w / in_h))
    vx0 = (WIDTH - vw) // 2
    vy0 = (HEIGHT - vh) // 2
    vx1 = vx0 + vw
    vy1 = vy0 + vh
    
    pad = 14
    card_x0, card_y0 = vx0 - pad, vy0 - pad
    card_x1, card_y1 = vx1 + pad, vy1 + pad
    card_box = (card_x0, card_y0, card_x1, card_y1)
    inner_box = (vx0, vy0, vx1, vy1)
    
    variants = precompute_sketch_variants(card_box, inner_box)
    
    frame_size_in = in_w * in_h * 3
    
    font_sub_reg = ImageFont.truetype(FONT_BOLD, 32)
    font_sub_hl = ImageFont.truetype(FONT_BOLD, 36)
    
    # Base background
    bg_canvas = Image.new("RGBA", (WIDTH, HEIGHT), (14, 17, 23, 255))
    grid_draw = ImageDraw.Draw(bg_canvas)
    for gx in range(0, WIDTH, 80):
        grid_draw.line([(gx, 0), (gx, HEIGHT)], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, HEIGHT, 80):
        grid_draw.line([(0, gy), (WIDTH, gy)], fill=(255, 255, 255, 10), width=1)

    print("Rendering frames with animated line boil & kinetic subtitle overlay...")
    
    for f in range(nb_frames):
        raw_frame = pipe_in.stdout.read(frame_size_in)
        if not raw_frame:
            break
            
        v_img = Image.frombytes("RGB", (in_w, in_h), raw_frame)
        t_sec = f / FPS
        
        # Stop-motion line-boil cycle (every 3 frames)
        v_idx = (f // 3) % 4
        var = variants[v_idx]
        rng = var["rng"]
        
        # Background: blurred from video + dimmed + grid
        canvas = bg_canvas.copy()
        v_bg = v_img.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=28))
        canvas.paste(v_bg, (0, 0))
        dark_dim = Image.new("RGBA", (WIDTH, HEIGHT), (12, 15, 20, 225))
        canvas.alpha_composite(dark_dim)
        
        g_draw = ImageDraw.Draw(canvas)
        for gx in range(0, WIDTH, 90):
            g_draw.line([(gx, 0), (gx, HEIGHT)], fill=(255, 255, 255, 8), width=1)
        for gy in range(0, HEIGHT, 90):
            g_draw.line([(0, gy), (WIDTH, gy)], fill=(255, 255, 255, 8), width=1)
            
        # Draw paper shadow
        shadow_draw = ImageDraw.Draw(canvas)
        for pts, width, alpha in var["shadows"]:
            shadow_draw.line(pts, fill=(0, 0, 0, alpha), width=int(width))
            
        # Cream paper backing
        paper = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(paper)
        paper_poly = [
            (card_x0 + rng.uniform(-2, 2), card_y0 + rng.uniform(-2, 2)),
            (card_x1 + rng.uniform(-2, 2), card_y0 + rng.uniform(-2, 2)),
            (card_x1 + rng.uniform(-2, 2), card_y1 + rng.uniform(-2, 2)),
            (card_x0 + rng.uniform(-2, 2), card_y1 + rng.uniform(-2, 2)),
        ]
        p_draw.polygon(paper_poly, fill=(245, 243, 238, 255))
        canvas.alpha_composite(paper)
        
        # Scale & paste video frame
        v_scaled = v_img.resize((vw, vh), Image.Resampling.BILINEAR).convert("RGBA")
        canvas.alpha_composite(v_scaled, (vx0, vy0))
        
        # Sketch strokes layer
        stroke_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(stroke_layer)
        
        # Outer card strokes
        for pts, width, alpha in var["strokes"]:
            s_draw.line(pts, fill=(22, 24, 30, int(alpha)), width=max(1, int(round(width))))
            
        # Inner video strokes
        for pts, width, alpha in var["inner"]:
            s_draw.line(pts, fill=(45, 48, 56, int(alpha * 0.7)), width=max(1, int(round(width - 1))))
            
        # Corner brackets
        corner_s = 28
        s_draw.line([(card_x0 - 10, card_y0 + corner_s), (card_x0 - 10, card_y0 - 10), (card_x0 + corner_s, card_y0 - 10)], fill=(230, 70, 70, 220), width=3)
        s_draw.line([(card_x1 + 10, card_y1 - corner_s), (card_x1 + 10, card_y1 + 10), (card_x1 - corner_s, card_y1 + 10)], fill=(230, 70, 70, 220), width=3)
        
        # Yellow tape at top center
        tw, th = 140, 36
        tx0 = (WIDTH - tw) // 2 + rng.uniform(-2, 2)
        ty0 = card_y0 - th // 2 + rng.uniform(-1, 1)
        t_poly = [
            (tx0, ty0), (tx0 + tw, ty0),
            (tx0 + tw - 4, ty0 + th), (tx0 + 4, ty0 + th)
        ]
        s_draw.polygon(t_poly, fill=(245, 215, 65, 210))
        s_draw.line(t_poly + [t_poly[0]], fill=(180, 150, 30, 180), width=2)
        
        # === KINETIC SUBTITLE OVERLAY (ON THE VIDEO IN THE BOX ONLY) ===
        # Find active subtitle
        active_sub = None
        for s in SUBTITLES:
            if s["start"] <= t_sec <= s["end"]:
                active_sub = s
                break
                
        if active_sub:
            sub_text = active_sub["text"]
            f_sub = font_sub_hl if active_sub["hl"] else font_sub_reg
            
            # Subtle bounce scale at word entry
            entry_prog = min(1.0, (t_sec - active_sub["start"]) / 0.12)
            # Measure text
            bbox = f_sub.getbbox(sub_text)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            
            # Center horizontally inside the video frame: [vx0, vx1]
            sub_x = vx0 + (vw - tw) // 2
            # Lower-third of the video frame
            sub_y = vy1 - 120
            
            # Draw sleek translucent documentary badge / pill backing
            pill_pad_x, pill_pad_y = 16, 8
            pill_box = [
                sub_x - pill_pad_x, sub_y - pill_pad_y,
                sub_x + tw + pill_pad_x, sub_y + th + pill_pad_y + 4
            ]
            s_draw.rounded_rectangle(pill_box, radius=8, fill=(10, 12, 16, 215), outline=(255, 230, 0, 180) if active_sub["hl"] else (255, 255, 255, 60), width=2 if active_sub["hl"] else 1)
            
            # Drop shadow for text
            s_draw.text((sub_x + 2, sub_y + 2), sub_text, font=f_sub, fill=(0, 0, 0, 230))
            # Text fill
            s_draw.text((sub_x, sub_y), sub_text, font=f_sub, fill=active_sub["color"] + (255,))

        canvas.alpha_composite(stroke_layer)
        rgb_frame = canvas.convert("RGB").tobytes()
        pipe_out.stdin.write(rgb_frame)
        
        if f % 30 == 0 or f == nb_frames - 1:
            print(f"Rendered ending clip frame {f}/{nb_frames} ({(f/nb_frames)*100:.1f}%)")

    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()
    print("Video track finished rendering.")

    # 4. Mux Audio: Original audio from VN20261104_232855.mp4 + whoosh at t=0
    print("Muxing audio with tactile entrance whoosh...")
    sfx_whoosh = os.path.join(PROJECT_DIR, "assets/audio/whoosh_fast.wav")
    
    cmd_audio_mix = (
        f'ffmpeg -y '
        f'-i "{INPUT_VIDEO}" '
        f'-i "{sfx_whoosh}" '
        f'-filter_complex "[0:a]volume=1.4[vorig];[1:a]volume=0.5[w];'
        f'[vorig][w]amix=inputs=2:duration=first:dropout_transition=0[aout]" '
        f'-map "[aout]" -c:a pcm_s16le -ar 44100 -ac 2 -t 4.066 "{OUTPUT_WAV}"'
    )
    subprocess.run(cmd_audio_mix, shell=True, check=True)
    
    # 5. Final Mux: Video + Audio into OUTPUT_MP4
    cmd_mux = (
        f'ffmpeg -y '
        f'-i "{temp_video_only}" '
        f'-i "{OUTPUT_WAV}" '
        f'-map 0:v -map 1:a '
        f'-c:v copy -c:a aac -b:a 192k '
        f'-t 4.066 "{OUTPUT_MP4}"'
    )
    subprocess.run(cmd_mux, shell=True, check=True)
    if os.path.exists(temp_video_only):
        os.remove(temp_video_only)
        
    print(f"=== Successfully Created Ending Video Clip: {OUTPUT_MP4} ===")

if __name__ == "__main__":
    main()

