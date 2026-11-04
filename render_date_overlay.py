#!/usr/bin/env python3
"""
render_date_overlay.py
Renders clean, cinematic documentary-style animated date stamps directly on photos:
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
    temp_dir = f"/tmp/date_frames_{os.path.basename(output_clip_path).replace('.mp4','')}"
    os.makedirs(temp_dir, exist_ok=True)
    
    total_frames = int(duration * fps)
    
    font_tag = ImageFont.truetype(FONT_PATH_BOLD, 22)
    font_date = ImageFont.truetype(FONT_PATH_BOLD, 54)
    font_sub = ImageFont.truetype(FONT_PATH_BOLD, 26)
    
    # Load base enhanced image (2560x1440 16:9)
    base_img = Image.open(image_path).convert("RGB")
    bw, bh = base_img.size
    
    # Card configuration (positioned lower-left: x=100, y=780)
    card_x = 90
    card_y = 740
    card_w = 880
    card_h = 240
    
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
        frame_bg = base_img.crop(crop_box).resize((width, height), Image.Resampling.LANCZOS)
        
        # Subtle vignette / film darkening around edges
        draw = ImageDraw.Draw(frame_bg, "RGBA")
        
        # 2. Card Animation Timing
        # Card slides up / fades in from t=0.2s to t=0.6s
        if t < 0.2:
            card_alpha = 0
            card_offset_y = 60
        elif t < 0.6:
            c_prog = (t - 0.2) / 0.4
            card_alpha = int(c_prog * 235)
            card_offset_y = int((1.0 - c_prog) * 60)
        else:
            card_alpha = 235
            card_offset_y = 0
            
        cur_card_y = card_y + card_offset_y
        
        if card_alpha > 0:
            # Draw semi-transparent frosted card backing
            card_poly = [
                (card_x, cur_card_y),
                (card_x + card_w, cur_card_y),
                (card_x + card_w, cur_card_y + card_h),
                (card_x, cur_card_y + card_h)
            ]
            # Deep shadow
            draw.rectangle(
                [card_x + 8, cur_card_y + 12, card_x + card_w + 8, cur_card_y + card_h + 12],
                fill=(0, 0, 0, int(card_alpha * 0.6))
            )
            # Charcoal card body
            draw.rectangle(
                [card_x, cur_card_y, card_x + card_w, cur_card_y + card_h],
                fill=(12, 14, 18, card_alpha)
            )
            # Electric yellow accent border bar on left side (6px)
            draw.rectangle(
                [card_x, cur_card_y, card_x + 8, cur_card_y + card_h],
                fill=(255, 230, 0, card_alpha)
            )
            
            # Tag pill (e.g. "[ DECLASSIFIED STRIKE ]")
            tag_box = font_tag.getbbox(tag_text)
            tw = tag_box[2] - tag_box[0]
            th = tag_box[3] - tag_box[1]
            tx = card_x + 36
            ty = cur_card_y + 28
            draw.rounded_rectangle([tx - 10, ty - 5, tx + tw + 10, ty + th + 7], radius=6, fill=(255, 230, 0, card_alpha))
            draw.text((tx, ty), tag_text, font=font_tag, fill=(12, 14, 18, card_alpha))
            
            # Typewriter Date Writing (starts at t=0.6s to 1.6s)
            if t >= 0.6:
                write_prog = min(1.0, (t - 0.6) / 1.0)
                visible_chars = int(len(date_text) * write_prog)
                current_date_str = date_text[:visible_chars]
                
                # Blinking cursor (2Hz)
                cursor = " |" if (int(t * 4) % 2 == 0 and write_prog < 1.0) else ""
                
                dx = card_x + 36
                dy = ty + th + 24
                draw.text((dx, dy), current_date_str + cursor, font=font_date, fill=(255, 255, 255, card_alpha))
                
            # Subtitle line (fades in at t=1.6s)
            if t >= 1.5:
                sub_prog = min(1.0, (t - 1.5) / 0.5)
                sub_alpha = int(sub_prog * card_alpha)
                sx = card_x + 36
                sy = dy + 70
                # Accent divider dot
                draw.text((sx, sy), sub_text, font=font_sub, fill=(200, 205, 215, sub_alpha))

        # Save frame
        frame_bg.save(os.path.join(temp_dir, f"frame_{f:04d}.png"))
        
    # Compile to MP4 with synchronized typewriter sound effect!
    sfx_type = os.path.join(AUDIO_DIR, "typewriter_burst.wav")
    sfx_slam = os.path.join(AUDIO_DIR, "paper_slam.wav")
    
    cmd = (
        f'ffmpeg -y -framerate {fps} -i "{temp_dir}/frame_%04d.png" '
        f'-itsoffset 0.2 -i "{sfx_slam}" -itsoffset 0.6 -i "{sfx_type}" '
        f'-filter_complex "[1:a]volume=0.9[a1];[2:a]volume=1.2[a2];[a1][a2]amix=inputs=2:dropout_transition=0[aout]" '
        f'-map 0:v -map "[aout]" -c:v libx264 -preset fast -pix_fmt yuv420p -t {duration} "{output_clip_path}"'
    )
    subprocess.run(cmd, shell=True, check=True)
    
    # Clean up frames
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)
    print(f"Generated animated date stamp clip: {output_clip_path}")

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
