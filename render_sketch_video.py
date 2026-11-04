#!/usr/bin/env python3
"""
render_sketch_video.py
Renders the viral social media video inside an animated, hand-drawn sketch box
with stop-motion line boil and original audio (no distracting side text boxes).
"""

import os, sys, math, random, subprocess
from PIL import Image, ImageDraw, ImageFilter

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
INPUT_VIDEO = "/home/rashid/.gemini/antigravity/brain/1e5be721-c9b4-4d36-8f45-30a2f3a82e22/.user_uploaded/media_1793811465006_1c8e16bb.mp4"
OUTPUT_MP4 = os.path.join(PROJECT_DIR, "assets/titles/hook_viral_clip.mp4")
OUTPUT_WAV = os.path.join(PROJECT_DIR, "assets/titles/hook_viral_clip.wav")

WIDTH, HEIGHT = 1920, 1080
FPS = 30

def generate_sketch_lines(box, rng, jitter=2.8, passes=3):
    x0, y0, x1, y1 = box
    strokes = []
    n_pts = 8

    for p in range(passes):
        # Top
        over_l, over_r = rng.uniform(18, 35), rng.uniform(18, 35)
        sx, ex = x0 - over_l, x1 + over_r
        yv = y0 + rng.uniform(-jitter, jitter)
        pts = [(sx + (i/n_pts)*(ex - sx), yv + rng.uniform(-jitter, jitter)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Bottom
        over_l, over_r = rng.uniform(18, 35), rng.uniform(18, 35)
        sx, ex = x0 - over_l, x1 + over_r
        yv = y1 + rng.uniform(-jitter, jitter)
        pts = [(sx + (i/n_pts)*(ex - sx), yv + rng.uniform(-jitter, jitter)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Left
        over_t, over_b = rng.uniform(18, 35), rng.uniform(18, 35)
        sy, ey = y0 - over_t, y1 + over_b
        xv = x0 + rng.uniform(-jitter, jitter)
        pts = [(xv + rng.uniform(-jitter, jitter), sy + (i/n_pts)*(ey - sy)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

        # Right
        over_t, over_b = rng.uniform(18, 35), rng.uniform(18, 35)
        sy, ey = y0 - over_t, y1 + over_b
        xv = x1 + rng.uniform(-jitter, jitter)
        pts = [(xv + rng.uniform(-jitter, jitter), sy + (i/n_pts)*(ey - sy)) for i in range(n_pts + 1)]
        strokes.append((pts, rng.uniform(2.5, 3.8), rng.randint(215, 255)))

    # Cross-hatch shadow along right & bottom
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

def precompute_sketch_variants():
    """Precompute 4 line-boil variants for smooth animated sketching."""
    seeds = [101, 202, 303, 404]
    variants = []
    
    vh = 920
    vw = int(vh * (720 / 1280))
    vx0 = (WIDTH - vw) // 2
    vy0 = (HEIGHT - vh) // 2
    vx1 = vx0 + vw
    vy1 = vy0 + vh
    
    pad = 14
    card_box = (vx0 - pad, vy0 - pad, vx1 + pad, vy1 + pad)
    inner_box = (vx0, vy0, vx1, vy1)
    
    for s in seeds:
        rng = random.Random(s)
        strokes, shadows = generate_sketch_lines(card_box, rng, jitter=2.5, passes=3)
        inner_strokes, _ = generate_sketch_lines(inner_box, rng, jitter=1.4, passes=2)
        variants.append({
            "strokes": strokes,
            "shadows": shadows,
            "inner": inner_strokes,
            "card_box": card_box,
            "video_box": inner_box,
            "rng": rng
        })
    return variants

def main():
    print("=== Rendering Viral Video in Clean Animated Hand-Drawn Sketch Box ===")
    os.makedirs(os.path.dirname(OUTPUT_MP4), exist_ok=True)
    
    # 1. Inspect source video frames count
    probe_cmd = f'ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of default=nokey=1:noprint_wrappers=1 "{INPUT_VIDEO}"'
    nb_frames = int(subprocess.check_output(probe_cmd, shell=True).decode().strip())
    print(f"Total video frames to process: {nb_frames}")
    
    # 2. Extract frames pipe from ffmpeg
    pipe_in_cmd = [
        "ffmpeg", "-i", INPUT_VIDEO,
        "-f", "image2pipe",
        "-pix_fmt", "rgb24",
        "-vcodec", "rawvideo", "-"
    ]
    pipe_in = subprocess.Popen(pipe_in_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
    
    # 3. Output pipe to ffmpeg for encoding
    temp_video_only = "/tmp/hook_sketch_vonly.mp4"
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
    
    variants = precompute_sketch_variants()
    
    frame_size_in = 720 * 1280 * 3
    
    vh = 920
    vw = int(vh * (720 / 1280))
    vx0 = (WIDTH - vw) // 2
    vy0 = (HEIGHT - vh) // 2
    vx1 = vx0 + vw
    vy1 = vy0 + vh
    
    pad = 14
    card_x0, card_y0 = vx0 - pad, vy0 - pad
    card_x1, card_y1 = vx1 + pad, vy1 + pad
    
    # Static base background
    bg_canvas = Image.new("RGBA", (WIDTH, HEIGHT), (14, 17, 23, 255))
    grid_draw = ImageDraw.Draw(bg_canvas)
    for gx in range(0, WIDTH, 80):
        grid_draw.line([(gx, 0), (gx, HEIGHT)], fill=(255, 255, 255, 10), width=1)
    for gy in range(0, HEIGHT, 80):
        grid_draw.line([(0, gy), (WIDTH, gy)], fill=(255, 255, 255, 10), width=1)

    print("Processing frames with animated line boil...")
    
    for f in range(nb_frames):
        raw_frame = pipe_in.stdout.read(frame_size_in)
        if not raw_frame:
            break
            
        v_img = Image.frombytes("RGB", (720, 1280), raw_frame)
        
        # Pick line-boil variant (cycles every 3 frames = 10fps stop-motion)
        v_idx = (f // 3) % 4
        var = variants[v_idx]
        rng = var["rng"]
        
        # Canvas
        canvas = bg_canvas.copy()
        
        # Dynamic blurred background from this video frame
        v_bg = v_img.resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(radius=28))
        canvas.paste(v_bg, (0, 0))
        dark_dim = Image.new("RGBA", (WIDTH, HEIGHT), (12, 15, 20, 225))
        canvas.alpha_composite(dark_dim)
        
        # Redraw subtle grid over dimmed bg
        g_draw = ImageDraw.Draw(canvas)
        for gx in range(0, WIDTH, 90):
            g_draw.line([(gx, 0), (gx, HEIGHT)], fill=(255, 255, 255, 8), width=1)
        for gy in range(0, HEIGHT, 90):
            g_draw.line([(0, gy), (WIDTH, gy)], fill=(255, 255, 255, 8), width=1)

        # Entrance animation for first 15 frames (0.5s)
        scale = 1.0
        v_alpha = 255
        if f < 15:
            prog = f / 15.0
            scale = 0.92 + 0.08 * math.sin(prog * math.pi / 2)
            v_alpha = int(255 * min(1.0, max(0.0, (f - 3) / 12.0)))
            
        # Draw paper backing & shadow
        shadow_draw = ImageDraw.Draw(canvas)
        for pts, width, alpha in var["shadows"]:
            shadow_draw.line(pts, fill=(0, 0, 0, alpha), width=int(width))
            
        # Cream paper card
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
        
        # Video paste
        v_scaled = v_img.resize((vw, vh), Image.Resampling.BILINEAR).convert("RGBA")
        if v_alpha < 255:
            alpha_mask = Image.new("L", (vw, vh), v_alpha)
            v_scaled.putalpha(alpha_mask)
        canvas.alpha_composite(v_scaled, (vx0, vy0))
        
        # Sketch strokes layer
        stroke_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(stroke_layer)
        
        # Outer card sketch strokes
        for pts, width, alpha in var["strokes"]:
            s_draw.line(pts, fill=(22, 24, 30, int(alpha)), width=max(1, int(round(width))))
            
        # Inner video sketch strokes
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
        
        canvas.alpha_composite(stroke_layer)
        rgb_frame = canvas.convert("RGB").tobytes()
        pipe_out.stdin.write(rgb_frame)
        
        if f % 75 == 0 or f == nb_frames - 1:
            print(f"Rendered frame {f}/{nb_frames} ({(f/nb_frames)*100:.1f}%)")

    pipe_in.stdout.close()
    pipe_in.wait()
    pipe_out.stdin.close()
    pipe_out.wait()
    print("Video track finished rendering.")

    # 4. Mix Audio: Original video audio + subtle paper whoosh at t=0
    print("Muxing audio with tactile whoosh SFX...")
    sfx_whoosh = os.path.join(PROJECT_DIR, "assets/audio/whoosh_fast.wav")
    sfx_marker = os.path.join(PROJECT_DIR, "assets/audio/marker_streak.wav")
    
    cmd_audio_mix = (
        f'ffmpeg -y '
        f'-i "{INPUT_VIDEO}" '
        f'-i "{sfx_whoosh}" '
        f'-i "{sfx_marker}" '
        f'-filter_complex "[0:a]volume=1.0[vorig];[1:a]volume=0.6[w];[2:a]volume=0.5[m];'
        f'[vorig][w][m]amix=inputs=3:duration=first:dropout_transition=0[aout]" '
        f'-map "[aout]" -c:a pcm_s16le -ar 44100 -ac 2 -t 14.866 "{OUTPUT_WAV}"'
    )
    subprocess.run(cmd_audio_mix, shell=True, check=True)
    
    # 5. Final Mux: Video + Audio into OUTPUT_MP4
    cmd_mux = (
        f'ffmpeg -y '
        f'-i "{temp_video_only}" '
        f'-i "{OUTPUT_WAV}" '
        f'-map 0:v -map 1:a '
        f'-c:v copy -c:a aac -b:a 192k '
        f'-t 14.866 "{OUTPUT_MP4}"'
    )
    subprocess.run(cmd_mux, shell=True, check=True)
    if os.path.exists(temp_video_only):
        os.remove(temp_video_only)
        
    print(f"=== Successfully Created Hook Viral Clip: {OUTPUT_MP4} ===")

if __name__ == "__main__":
    main()
