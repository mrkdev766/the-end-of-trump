#!/usr/bin/env python3
"""
generate_title_cards.py
Generates highly animated papercraft title cards:
- Paper cutout with jagged edges and drop shadow
- Crisp white typography + high-voltage golden yellow (#FFE600) highlighter banners
- Kinetic pop-in bounce, yellow marker sweep, and subtle 12fps stop-motion paper wiggle
- Professional television-grade tactile sound design:
  * 0.0s: Fast whoosh (whoosh_fast.wav)
  * 0.35s: Heavy paper slam + sub-bass thud (paper_slam.wav + sub_boom.wav)
  * 0.45s: Felt-tip yellow highlighter squeak/streak (marker_streak.wav)
  * 0.65s: Mechanical typewriter clicks (typewriter_burst.wav)
"""

import os, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "assets/titles")
SFX_DIR = os.path.join(PROJECT_DIR, "assets/audio")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_PATH_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLES = [
    {
        "id": "title_00_intro",
        "tag": "SPECIAL INVESTIGATION",
        "main": "THE END OF TRUMP?",
        "question": "Is This the Beginning of the End for Donald Trump?",
        "highlight": "TRUMP?"
    },
    {
        "id": "title_01_chapter1",
        "tag": "CHAPTER 01",
        "main": "THE POLITICAL SETBACK",
        "question": "Can Democrats Paralyze the Second Term?",
        "highlight": "POLITICAL SETBACK"
    },
    {
        "id": "title_02_chapter2",
        "tag": "CHAPTER 02",
        "main": "THE IRAN CONFLICT",
        "question": "The Chokepoint of World Oil & Naval War",
        "highlight": "IRAN CONFLICT"
    },
    {
        "id": "title_03_chapter3",
        "tag": "CHAPTER 03",
        "main": "THE THREAT AGAINST TRUMP",
        "question": "Vows of Revenge & Covert Plots",
        "highlight": "THREAT AGAINST TRUMP"
    },
    {
        "id": "title_04_chapter4",
        "tag": "CHAPTER 04",
        "main": "CAN TRUMP BE REMOVED?",
        "question": "Impeachment vs The Senate Two-Thirds Barrier",
        "highlight": "REMOVED?"
    },
    {
        "id": "title_05_verdict",
        "tag": "THE VERDICT",
        "main": "SURVIVAL OR COLLAPSE?",
        "question": "How Will Donald Trump's Story Finally End?",
        "highlight": "SURVIVAL"
    }
]

def create_torn_paper_polygon(x, y, w, h, seed=42):
    random.seed(seed)
    points = []
    # Top edge
    steps = 40
    for i in range(steps + 1):
        px = x + (w * i) / steps
        py = y + random.uniform(-4, 4)
        points.append((px, py))
    # Right edge
    for i in range(steps + 1):
        px = x + w + random.uniform(-4, 4)
        py = y + (h * i) / steps
        points.append((px, py))
    # Bottom edge
    for i in range(steps, -1, -1):
        px = x + (w * i) / steps
        py = y + h + random.uniform(-4, 4)
        points.append((px, py))
    # Left edge
    for i in range(steps, -1, -1):
        px = x + random.uniform(-4, 4)
        py = y + (h * i) / steps
        points.append((px, py))
    return points

def render_title_clip(card_info, duration=3.2, fps=30):
    width, height = 1920, 1080
    temp_frames_dir = f"/tmp/frames_{card_info['id']}"
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    total_frames = int(duration * fps)
    
    font_tag = ImageFont.truetype(FONT_PATH_BOLD, 36)
    font_main = ImageFont.truetype(FONT_PATH_BOLD, 76)
    font_q = ImageFont.truetype(FONT_PATH_BOLD, 42)

    for f in range(total_frames):
        t = f / fps
        
        # Background: Dark textured charcoal
        im = Image.new("RGBA", (width, height), (16, 18, 22, 255))
        draw = ImageDraw.Draw(im)
        
        # Subtle vignette / grid lines
        for gx in range(0, width, 120):
            draw.line([(gx, 0), (gx, height)], fill=(28, 32, 40, 255), width=1)
        for gy in range(0, height, 120):
            draw.line([(0, gy), (width, gy)], fill=(28, 32, 40, 255), width=1)

        # Kinetic pop-in: 0.0s to 0.35s bounce
        if t < 0.35:
            progress = t / 0.35
            scale = 0.3 + 0.7 * (math.sin(progress * math.pi * 0.7) / math.sin(math.pi * 0.7))
            y_offset = (1.0 - progress) * 220
            alpha = int(min(255, progress * 350))
        else:
            scale = 1.0
            wiggle_step = int((t - 0.35) * 12)
            random.seed(wiggle_step + 100)
            y_offset = random.uniform(-3, 3)
            alpha = 255

        # Paper Card dimensions
        card_w = 1400 * scale
        card_h = 560 * scale
        cx = (width - card_w) / 2
        cy = (height - card_h) / 2 + y_offset

        # Drop shadow for paper
        shadow_pts = create_torn_paper_polygon(cx + 18, cy + 22, card_w, card_h, seed=int(f // 4))
        draw.polygon(shadow_pts, fill=(0, 0, 0, 160))

        # White Torn Paper Body
        paper_pts = create_torn_paper_polygon(cx, cy, card_w, card_h, seed=int(f // 4))
        draw.polygon(paper_pts, fill=(245, 245, 248, 255))
        
        # Inner subtle paper outline
        draw.line(paper_pts + [paper_pts[0]], fill=(210, 212, 218, 255), width=3)

        # Tape in the corners (Washi tape aesthetic)
        tape_w = 160 * scale
        tape_h = 44 * scale
        draw.rectangle([cx + 60, cy - 20, cx + 60 + tape_w, cy - 20 + tape_h], fill=(255, 230, 0, 220)) # Top-left yellow tape
        draw.rectangle([cx + card_w - 220, cy - 20, cx + card_w - 220 + tape_w, cy - 20 + tape_h], fill=(255, 230, 0, 220)) # Top-right yellow tape

        # Tag Banner: Black pill with golden yellow text
        tag_text = card_info["tag"]
        tag_bbox = font_tag.getbbox(tag_text)
        tag_tw = tag_bbox[2] - tag_bbox[0]
        tag_th = tag_bbox[3] - tag_bbox[1]
        tag_x = (width - tag_tw) / 2
        tag_y = cy + 60 * scale
        
        # Tag pill
        draw.rounded_rectangle([tag_x - 24, tag_y - 8, tag_x + tag_tw + 24, tag_y + tag_th + 14], radius=12, fill=(18, 20, 26, 255))
        draw.text((tag_x, tag_y), tag_text, font=font_tag, fill=(255, 230, 0, 255))

        # Main Title (Bold crisp text)
        main_text = card_info["main"]
        main_bbox = font_main.getbbox(main_text)
        main_tw = main_bbox[2] - main_bbox[0]
        main_th = main_bbox[3] - main_bbox[1]
        main_x = (width - main_tw) / 2
        main_y = tag_y + tag_th + 55 * scale

        # Animated Highlighter Sweep (starts at t=0.45s to 0.9s)
        if t >= 0.45:
            hl_prog = min(1.0, (t - 0.45) / 0.42)
            hl_w = (main_tw + 60) * hl_prog
            hl_h = main_th + 30
            # Draw bold yellow marker streak
            draw.rectangle([main_x - 30, main_y - 5, main_x - 30 + hl_w, main_y - 5 + hl_h], fill=(255, 230, 0, 210))

        # Main text (Charcoal black on white/yellow paper)
        draw.text((main_x, main_y), main_text, font=font_main, fill=(18, 20, 26, 255))

        # Subtitle / Question with animated typewriter (starts at t=0.65s)
        if t >= 0.65:
            q_prog = min(1.0, (t - 0.65) / 0.45)
            q_text = card_info["question"]
            visible_chars = int(len(q_text) * q_prog)
            disp_q = q_text[:visible_chars]
            
            q_bbox = font_q.getbbox(q_text)
            q_tw = q_bbox[2] - q_bbox[0]
            q_th = q_bbox[3] - q_bbox[1]
            q_x = (width - q_tw) / 2
            q_y = main_y + main_th + 65 * scale
            
            # Subtle pencil accent line under question
            draw.line([(q_x - 40, q_y + q_th + 16), (q_x + q_tw + 40, q_y + q_th + 16)], fill=(255, 230, 0, 255), width=5)
            draw.text((q_x, q_y), disp_q, font=font_q, fill=(50, 55, 65, 255))

        # Save frame
        frame_path = os.path.join(temp_frames_dir, f"frame_{f:04d}.png")
        im.save(frame_path)

    # Compile frames to MP4 using ffmpeg + attach tactical television-grade SFX!
    out_mp4 = os.path.join(OUTPUT_DIR, f"{card_info['id']}.mp4")
    out_wav = os.path.join(OUTPUT_DIR, f"{card_info['id']}.wav")
    
    sfx_whoosh = os.path.join(SFX_DIR, "whoosh_fast.wav")
    sfx_slam = os.path.join(SFX_DIR, "paper_slam.wav")
    sfx_boom = os.path.join(SFX_DIR, "sub_boom.wav")
    sfx_marker = os.path.join(SFX_DIR, "marker_streak.wav")
    sfx_type = os.path.join(SFX_DIR, "typewriter_burst.wav")
    
    # Generate standalone audio mix for this title card (duration seconds)
    # Visual Keyframes:
    # 0.00s: Card flies in -> Whoosh
    # 0.35s: Card slams desk & bounces -> Paper slam + Sub boom
    # 0.45s: Yellow highlighter marker streaks across main title -> Marker squeak
    # 0.65s: Typewriter types out question text -> Typewriter mechanical bursts
    cmd_audio = (
        f'ffmpeg -y '
        f'-i "{sfx_whoosh}" '
        f'-i "{sfx_slam}" '
        f'-i "{sfx_boom}" '
        f'-i "{sfx_marker}" '
        f'-i "{sfx_type}" '
        f'-filter_complex "'
        f'[0:a]volume=0.85[a0];'
        f'[1:a]adelay=350:all=1,volume=1.4[a1];'
        f'[2:a]adelay=350:all=1,volume=1.1[a2];'
        f'[3:a]adelay=450:all=1,volume=1.3[a3];'
        f'[4:a]adelay=650:all=1,volume=1.1[a4];'
        f'[a0][a1][a2][a3][a4]amix=inputs=5:dropout_transition=0,apad[aout]" '
        f'-map "[aout]" -ar 44100 -ac 2 -t {duration} "{out_wav}"'
    )
    subprocess.run(cmd_audio, shell=True, check=True)
    
    # Mux frames with the audio mix
    cmd_mux = (
        f'ffmpeg -y -framerate {fps} -i "{temp_frames_dir}/frame_%04d.png" '
        f'-i "{out_wav}" -map 0:v -map 1:a -c:v libx264 -preset fast -pix_fmt yuv420p -t {duration} "{out_mp4}"'
    )
    subprocess.run(cmd_mux, shell=True, check=True)
    
    # Clean up frames
    for f in os.listdir(temp_frames_dir):
        os.remove(os.path.join(temp_frames_dir, f))
    os.rmdir(temp_frames_dir)
    print(f"Generated animated title card with tactile sound: {out_mp4}")

def main():
    print("=== Re-generating Animated Papercraft Chapter Cards with Documentary Sound Design ===")
    for title in TITLES:
        print(f"Building {title['id']}...")
        render_title_clip(title)

if __name__ == "__main__":
    main()
