#!/usr/bin/env python3
"""
render_date_overlay.py
Fast, high-fidelity documentary animated date stamp generator:
- Pipes raw frames directly to ffmpeg (RAM-speed rendering, zero disk I/O bottleneck)
- Frosted dark charcoal container with yellow accent marker line
- Category tag pill (e.g., "[ DECLASSIFIED STRIKE ]")
- Typewriter character-by-character date revelation with blinking cursor
- Subtitle location/event description
- Muxed with mechanical typewriter and tactile impact sound effects
"""

import os, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
AUDIO_DIR = os.path.join(PROJECT_DIR, "assets/audio")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output/date_overlays")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def render_date_stamp_clip(
    image_path,
    tag_text,
    date_text,
    sub_text,
    output_clip_path,
    duration=5.0,
    fps=30,
    motion="zoom_in"
):
    width, height = 1920, 1080
    total_frames = int(round(duration * fps))
    
    font_tag = ImageFont.truetype(FONT_PATH_BOLD, 22)
    font_date = ImageFont.truetype(FONT_PATH_BOLD, 54)
    font_sub = ImageFont.truetype(FONT_PATH_BOLD, 26)
    
    # Load base enhanced image (e.g. 2560x1440 or 8000x4500)
    base_img = Image.open(image_path).convert("RGB")
    bw, bh = base_img.size
    
    # Card configuration (positioned lower-left: x=90, y=740)
    card_x = 90
    card_y = 740
    card_w = 880
    card_h = 240

    sfx_type = os.path.join(AUDIO_DIR, "typewriter_burst.wav")
    sfx_slam = os.path.join(AUDIO_DIR, "paper_slam.wav")
    
    # ffmpeg command to accept raw RGB frames from stdin and mux with audio SFX
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}",
        "-r", str(fps),
        "-i", "pipe:0",
        "-i", sfx_slam,
        "-i", sfx_type,
        "-filter_complex",
        "[1:a]adelay=200:all=1,volume=1.4[a1];"
        "[2:a]adelay=600:all=1,volume=2.2[a2];"
        "[a1][a2]amix=inputs=2:normalize=0:dropout_transition=0,alimiter=limit=0.95[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        output_clip_path
    ]
    
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    for f in range(total_frames):
        t = f / fps
        progress = f / max(1, total_frames - 1)
        
        # 1. Ken Burns camera motion on base image
        if motion == "zoom_in":
            scale = 1.0 + 0.12 * progress
            cw = int(bw / scale)
            ch = int(bh / scale)
            cx = (bw - cw) // 2
            cy = (bh - ch) // 2
        elif motion == "zoom_out":
            scale = 1.12 - 0.12 * progress
            cw = int(bw / scale)
            ch = int(bh / scale)
            cx = (bw - cw) // 2
            cy = (bh - ch) // 2
        else: # pan_left
            cw = int(bw / 1.1)
            ch = int(bh / 1.1)
            cx = int((bw - cw) * (1.0 - progress))
            cy = (bh - ch) // 2
            
        crop_box = (cx, cy, cx + cw, cy + ch)
        frame_bg = base_img.crop(crop_box).resize((width, height), Image.Resampling.BILINEAR)
        
        # Subtle vignette / film darkening around edges
        draw = ImageDraw.Draw(frame_bg, "RGBA")
        draw.rectangle([0, 0, width, 120], fill=(0, 0, 0, 70))
        draw.rectangle([0, height - 160, width, height], fill=(0, 0, 0, 90))
        
        # 2. Date Card Animation
        # Entrance: 0.2s slide in from bottom-left
        if t < 0.2:
            card_alpha = int((t / 0.2) * 230)
            cur_card_y = card_y + int((1.0 - (t / 0.2)) * 60)
        else:
            card_alpha = 230
            cur_card_y = card_y

        # Draw frosted dark charcoal card
        card_rect = [card_x, cur_card_y, card_x + card_w, cur_card_y + card_h]
        # Shadow
        draw.rectangle([card_x + 8, cur_card_y + 10, card_x + card_w + 8, cur_card_y + card_h + 10], fill=(0, 0, 0, 110))
        # Card body
        draw.rectangle(card_rect, fill=(16, 18, 24, card_alpha))
        # Left golden highlight stripe
        draw.rectangle([card_x, cur_card_y, card_x + 8, cur_card_y + card_h], fill=(255, 230, 0, min(255, card_alpha + 25)))
        
        if t >= 0.2:
            # Tag Pill (e.g. [ DECLASSIFIED STRIKE ])
            tag_bbox = font_tag.getbbox(tag_text)
            ptw = tag_bbox[2] - tag_bbox[0]
            pth = tag_bbox[3] - tag_bbox[1]
            pill_x = card_x + 36
            pill_y = cur_card_y + 26
            
            draw.rounded_rectangle([pill_x - 12, pill_y - 4, pill_x + ptw + 12, pill_y + pth + 6], radius=6, fill=(255, 230, 0, card_alpha))
            draw.text((pill_x, pill_y), tag_text, font=font_tag, fill=(16, 18, 24, card_alpha))
            
            # Typewriter Date Text (starts at 0.5s to 1.4s)
            dy = pill_y + pth + 24
            if t >= 0.5:
                type_prog = min(1.0, (t - 0.5) / 0.9)
                num_chars = int(len(date_text) * type_prog)
                disp_date = date_text[:num_chars]
                draw.text((card_x + 36, dy), disp_date, font=font_date, fill=(255, 255, 255, card_alpha))
                
                # Blinking cursor while typing
                if type_prog < 1.0 and (int(t * 8) % 2 == 0):
                    c_bbox = font_date.getbbox(disp_date) if disp_date else [0, 0, 0, 0]
                    cursor_x = card_x + 36 + (c_bbox[2] - c_bbox[0]) + 6
                    draw.rectangle([cursor_x, dy + 6, cursor_x + 4, dy + 48], fill=(255, 230, 0, card_alpha))
                    
            # Subtitle (location/event) fades in at 1.5s
            if t >= 1.5:
                sub_prog = min(1.0, (t - 1.5) / 0.5)
                sub_alpha = int(sub_prog * card_alpha)
                sx = card_x + 36
                sy = dy + 70
                draw.text((sx, sy), sub_text, font=font_sub, fill=(200, 205, 215, sub_alpha))

        # Write raw bytes to ffmpeg pipe
        proc.stdin.write(frame_bg.tobytes())

    proc.stdin.close()
    stderr = proc.stderr.read()
    proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"FFmpeg failed with code {proc.returncode}: {stderr.decode()}")
    print(f"Generated animated date stamp clip in RAM: {output_clip_path}")

def main():
    print("=== Testing Animated Documentary Date Overlay Generator ===")
    test_img = os.path.join(PROJECT_DIR, "assets/images_enhanced/28_baghdad_airport_tarmac_night.jpg")
    out_test = os.path.join(OUTPUT_DIR, "scene_38_date_test.mp4")
    render_date_stamp_clip(
        image_path=test_img,
        tag_text="DECLASSIFIED OPERATION",
        date_text="JANUARY 3, 2020",
        sub_text="BAGHDAD INTERNATIONAL AIRPORT — TARGET: SOLEIMANI",
        output_clip_path=out_test,
        duration=6.5,
        fps=30,
        motion="zoom_in"
    )

if __name__ == "__main__":
    main()
