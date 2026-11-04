#!/usr/bin/env python3
"""
test_sketch_frame.py
Tests rendering a hand-drawn sketch box around the video frame using PIL and numpy.
"""

import os, random, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_PATH = "/tmp/test_sketch_frame.jpg"
VIDEO_PATH = "/home/rashid/.gemini/antigravity/brain/1e5be721-c9b4-4d36-8f45-30a2f3a82e22/.user_uploaded/media_1793811465006_1c8e16bb.mp4"
FONT_CAVEAT = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc/assets/fonts/Caveat.ttf"
FONT_MARKER = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc/assets/fonts/PermanentMarker.ttf"

def generate_sketch_lines(box, rng, jitter=3.0, passes=3):
    """
    box: (x0, y0, x1, y1)
    Generates hand-drawn strokes with overshoot and jitter.
    """
    x0, y0, x1, y1 = box
    strokes = []
    
    # 4 sides: top, right, bottom, left
    for p in range(passes):
        # Top side (x0 - overshoot to x1 + overshoot)
        over_l = rng.uniform(15, 35)
        over_r = rng.uniform(15, 35)
        start_x = x0 - over_l
        end_x = x1 + over_r
        y_val = y0 + rng.uniform(-jitter, jitter)
        
        # generate 6-8 segmented points for a natural wavy hand-drawn stroke
        pts = []
        n_pts = 8
        for i in range(n_pts + 1):
            t = i / n_pts
            px = start_x + t * (end_x - start_x)
            py = y_val + rng.uniform(-jitter, jitter)
            pts.append((px, py))
        strokes.append((pts, rng.uniform(2.5, 4.0), rng.randint(210, 245)))
        
        # Bottom side
        over_l = rng.uniform(15, 35)
        over_r = rng.uniform(15, 35)
        start_x = x0 - over_l
        end_x = x1 + over_r
        y_val = y1 + rng.uniform(-jitter, jitter)
        pts = []
        for i in range(n_pts + 1):
            t = i / n_pts
            px = start_x + t * (end_x - start_x)
            py = y_val + rng.uniform(-jitter, jitter)
            pts.append((px, py))
        strokes.append((pts, rng.uniform(2.5, 4.0), rng.randint(210, 245)))
        
        # Left side
        over_t = rng.uniform(15, 35)
        over_b = rng.uniform(15, 35)
        start_y = y0 - over_t
        end_y = y1 + over_b
        x_val = x0 + rng.uniform(-jitter, jitter)
        pts = []
        for i in range(n_pts + 1):
            t = i / n_pts
            px = x_val + rng.uniform(-jitter, jitter)
            py = start_y + t * (end_y - start_y)
            pts.append((px, py))
        strokes.append((pts, rng.uniform(2.5, 4.0), rng.randint(210, 245)))
        
        # Right side
        over_t = rng.uniform(15, 35)
        over_b = rng.uniform(15, 35)
        start_y = y0 - over_t
        end_y = y1 + over_b
        x_val = x1 + rng.uniform(-jitter, jitter)
        pts = []
        for i in range(n_pts + 1):
            t = i / n_pts
            px = x_val + rng.uniform(-jitter, jitter)
            py = start_y + t * (end_y - start_y)
            pts.append((px, py))
        strokes.append((pts, rng.uniform(2.5, 4.0), rng.randint(210, 245)))

    # Cross-hatch shadow along bottom and right
    shadow_strokes = []
    # Right edge hatch
    for y_pos in range(int(y0 + 20), int(y1 + 40), 16):
        hx0 = x1 + rng.uniform(4, 8)
        hy0 = y_pos + rng.uniform(-2, 2)
        hx1 = hx0 + rng.uniform(20, 32)
        hy1 = hy0 + rng.uniform(12, 18)
        shadow_strokes.append(([(hx0, hy0), (hx1, hy1)], rng.uniform(1.8, 2.5), 160))
        
    # Bottom edge hatch
    for x_pos in range(int(x0 + 20), int(x1 + 35), 18):
        hx0 = x_pos + rng.uniform(-2, 2)
        hy0 = y1 + rng.uniform(4, 8)
        hx1 = hx0 + rng.uniform(14, 22)
        hy1 = hy0 + rng.uniform(18, 26)
        shadow_strokes.append(([(hx0, hy0), (hx1, hy1)], rng.uniform(1.8, 2.5), 160))

    return strokes, shadow_strokes


def create_sketch_frame(video_frame_img, seed=42):
    rng = random.Random(seed)
    W, H = 1920, 1080
    canvas = Image.new("RGBA", (W, H), (14, 17, 23, 255))
    
    # Background texture: blurred darkened background from video frame
    bg = video_frame_img.copy().resize((W, H), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=35))
    # Dark overlay
    dark = Image.new("RGBA", (W, H), (12, 15, 20, 220))
    canvas.paste(bg, (0, 0))
    canvas.alpha_composite(dark)
    
    # Draw subtle background vignette / editorial paper grid
    grid_draw = ImageDraw.Draw(canvas)
    for gx in range(0, W, 80):
        grid_draw.line([(gx, 0), (gx, H)], fill=(255, 255, 255, 8), width=1)
    for gy in range(0, H, 80):
        grid_draw.line([(0, gy), (W, gy)], fill=(255, 255, 255, 8), width=1)
        
    # Video Placement
    # 720x1280 scaled to H=900 -> W=506
    vh = 900
    vw = int(vh * (720 / 1280))
    vx0 = (W - vw) // 2
    vy0 = (H - vh) // 2
    vx1 = vx0 + vw
    vy1 = vy0 + vh
    
    # Paper / Card backing behind video
    pad = 12
    card_x0, card_y0 = vx0 - pad, vy0 - pad
    card_x1, card_y1 = vx1 + pad, vy1 + pad
    
    # Sketched drop shadow layer
    draw = ImageDraw.Draw(canvas)
    strokes, shadow_strokes = generate_sketch_lines((card_x0, card_y0, card_x1, card_y1), rng, jitter=2.5, passes=3)
    
    for pts, width, alpha in shadow_strokes:
        draw.line(pts, fill=(0, 0, 0, alpha), width=int(width))
        
    # Sketched white/cream paper backing
    # draw slight off-white paper fill with sketched rough edge
    paper = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    paper_draw = ImageDraw.Draw(paper)
    paper_poly = [
        (card_x0 + rng.uniform(-2, 2), card_y0 + rng.uniform(-2, 2)),
        (card_x1 + rng.uniform(-2, 2), card_y0 + rng.uniform(-2, 2)),
        (card_x1 + rng.uniform(-2, 2), card_y1 + rng.uniform(-2, 2)),
        (card_x0 + rng.uniform(-2, 2), card_y1 + rng.uniform(-2, 2)),
    ]
    paper_draw.polygon(paper_poly, fill=(245, 243, 238, 255))
    canvas.alpha_composite(paper)
    
    # Paste video frame
    v_scaled = video_frame_img.resize((vw, vh), Image.Resampling.LANCZOS).convert("RGBA")
    canvas.alpha_composite(v_scaled, (vx0, vy0))
    
    # Draw sketch strokes over the frame and paper edge
    stroke_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stroke_layer)
    
    for pts, width, alpha in strokes:
        # Draw dark charcoal sketch lines
        s_draw.line(pts, fill=(20, 22, 28, int(alpha)), width=max(1, int(round(width))))
        
    # Inner sketch line right around video border
    inner_strokes, _ = generate_sketch_lines((vx0, vy0, vx1, vy1), rng, jitter=1.5, passes=2)
    for pts, width, alpha in inner_strokes:
        s_draw.line(pts, fill=(40, 44, 52, int(alpha * 0.7)), width=max(1, int(round(width - 1))))
        
    # Sketched corner tabs / brackets
    corner_size = 28
    # Top-Left corner
    s_draw.line([(card_x0 - 10, card_y0 + corner_size), (card_x0 - 10, card_y0 - 10), (card_x0 + corner_size, card_y0 - 10)], fill=(230, 70, 70, 220), width=3)
    # Bottom-Right corner
    s_draw.line([(card_x1 + 10, card_y1 - corner_size), (card_x1 + 10, card_y1 + 10), (card_x1 - corner_size, card_y1 + 10)], fill=(230, 70, 70, 220), width=3)

    # Sketched yellow tape at top center
    tape_w, tape_h = 130, 34
    tape_x0 = (W - tape_w) // 2 + rng.uniform(-3, 3)
    tape_y0 = card_y0 - tape_h // 2 + rng.uniform(-2, 2)
    tape_poly = [
        (tape_x0, tape_y0 + rng.uniform(-1, 1)),
        (tape_x0 + tape_w, tape_y0 + rng.uniform(-1, 1)),
        (tape_x0 + tape_w - 4, tape_y0 + tape_h + rng.uniform(-1, 1)),
        (tape_x0 + 4, tape_y0 + tape_h + rng.uniform(-1, 1))
    ]
    s_draw.polygon(tape_poly, fill=(245, 215, 65, 210))
    s_draw.line(tape_poly + [tape_poly[0]], fill=(180, 150, 30, 180), width=2)

    # Handwritten Typography using downloaded Google Fonts
    font_title = ImageFont.truetype(FONT_MARKER, 38)
    font_hand = ImageFont.truetype(FONT_CAVEAT, 36)
    font_bold = ImageFont.truetype(FONT_CAVEAT, 44)
    font_small = ImageFont.truetype(FONT_CAVEAT, 28)

    # Left-side editorial sticky note / sketch annotations
    note_x, note_y = 110, 280
    # Sketched card for note
    s_draw.rectangle([note_x - 15, note_y - 15, note_x + 480, note_y + 360], outline=(255, 255, 255, 40), width=1)
    s_draw.text((note_x, note_y), "EVIDENCE / ARCHIVE", font=font_title, fill=(255, 215, 65, 240))
    s_draw.line([(note_x, note_y + 50), (note_x + 420, note_y + 50)], fill=(255, 215, 65, 180), width=3)
    
    s_draw.text((note_x, note_y + 75), "• Source: Viral Social Media Clip", font=font_hand, fill=(230, 235, 245, 230))
    s_draw.text((note_x, note_y + 125), "• Claim: Specific date prediction for Trump", font=font_hand, fill=(230, 235, 245, 230))
    s_draw.text((note_x, note_y + 175), "• Date Cited: December 22, 2026", font=font_bold, fill=(255, 90, 90, 255))
    s_draw.text((note_x, note_y + 235), "• Status: Internet Phenomenon / Unverified", font=font_small, fill=(180, 190, 205, 200))
    
    # Sketched arrow pointing from note to video
    arrow_pts = [
        (note_x + 450, note_y + 185),
        (note_x + 510, note_y + 195),
        (vx0 - 35, note_y + 220)
    ]
    s_draw.line(arrow_pts, fill=(255, 215, 65, 220), width=3)
    # arrow head
    ax, ay = vx0 - 35, note_y + 220
    s_draw.line([(ax - 18, ay - 12), (ax, ay), (ax - 18, ay + 12)], fill=(255, 215, 65, 220), width=3)

    # Right side: Sketched context card
    rx, ry = vx1 + 55, 340
    s_draw.rectangle([rx - 15, ry - 15, rx + 490, ry + 300], outline=(255, 255, 255, 40), width=1)
    s_draw.text((rx, ry), "THE REALITY CHECK", font=font_title, fill=(255, 255, 255, 240))
    s_draw.line([(rx, ry + 50), (rx + 420, ry + 50)], fill=(255, 255, 255, 120), width=2)
    s_draw.text((rx, ry + 75), "While viral predictions flood feeds,", font=font_hand, fill=(220, 225, 235, 220))
    s_draw.text((rx, ry + 120), "Donald Trump faces concrete, real-world", font=font_hand, fill=(220, 225, 235, 220))
    s_draw.text((rx, ry + 165), "crises: Midterm loss, Iran confrontation,", font=font_hand, fill=(220, 225, 235, 220))
    s_draw.text((rx, ry + 210), "and verified national security threats.", font=font_hand, fill=(220, 225, 235, 220))

    # Bottom Banner under Video
    s_draw.text((vx0 + 15, card_y1 + 18), "[ FULL PLAYBACK: ORIGINAL AUDIO ]", font=font_hand, fill=(245, 215, 65, 220))

    canvas.alpha_composite(stroke_layer)
    return canvas.convert("RGB")

if __name__ == "__main__":
    # Load frame 2 from the video
    v_img = Image.open("/tmp/vid_frame_02.jpg")
    result = create_sketch_frame(v_img, seed=77)
    result.save(OUTPUT_PATH, quality=95)
    print(f"Saved test sketch frame to {OUTPUT_PATH}")

