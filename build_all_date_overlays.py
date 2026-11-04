#!/usr/bin/env python3
"""
build_all_date_overlays.py
Generates the 4 animated documentary date overlays directly on enhanced images:
- Scene 12: November 3, 2026 (Midterm elections)
- Scene 34: November 4, 2026 (Khamenei warning)
- Scene 38: January 3, 2020 (Soleimani Baghdad strike)
- Scene 42: August 2026 (Israel-US assassination plot intel)
"""

import os, sys
from render_date_overlay import render_date_stamp_clip

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
IMAGES_DIR = os.path.join(PROJECT_DIR, "assets/images_enhanced")
TITLES_DIR = os.path.join(PROJECT_DIR, "assets/titles")
os.makedirs(TITLES_DIR, exist_ok=True)

DATE_SCENES = [
    {
        "id": "date_scene_12",
        "image": os.path.join(IMAGES_DIR, "44_voter_lines_polling_station.jpg"),
        "tag": "ELECTION TIMELINE",
        "date": "NOVEMBER 3, 2026",
        "sub": "U.S. MIDTERMS — CONGRESSIONAL POWER SHIFTS",
        "duration": 8.99,
        "motion": "zoom_in"
    },
    {
        "id": "date_scene_34",
        "image": os.path.join(IMAGES_DIR, "26_khamenei_irgc_generals_salute.jpg"),
        "tag": "TEHRAN WARNING",
        "date": "NOVEMBER 4, 2026",
        "sub": "SUPREME LEADER WARNS OF WIDER RETALIATION",
        "duration": 7.50,
        "motion": "zoom_out"
    },
    {
        "id": "date_scene_38",
        "image": os.path.join(IMAGES_DIR, "28_baghdad_airport_tarmac_night.jpg"),
        "tag": "DECLASSIFIED STRIKE",
        "date": "JANUARY 3, 2020",
        "sub": "BAGHDAD INTL AIRPORT — TARGET: QASSEM SOLEIMANI",
        "duration": 9.90,
        "motion": "zoom_in"
    },
    {
        "id": "date_scene_42",
        "image": os.path.join(IMAGES_DIR, "35_cyber_intel_command_center.jpg"),
        "tag": "INTELLIGENCE DOSSIER",
        "date": "AUGUST 2026",
        "sub": "REUTERS REPORT — THREAT ASSESSMENT DECLASSIFIED",
        "duration": 9.78,
        "motion": "zoom_out"
    }
]

def main():
    print("=== Generating 4 Animated Documentary Date Overlays ===")
    for ds in DATE_SCENES:
        out_path = os.path.join(TITLES_DIR, f"{ds['id']}.mp4")
        print(f"\nRendering {ds['id']} ({ds['date']})...")
        render_date_stamp_clip(
            image_path=ds["image"],
            tag_text=ds["tag"],
            date_text=ds["date"],
            sub_text=ds["sub"],
            output_clip_path=out_path,
            duration=ds["duration"],
            fps=30,
            motion=ds["motion"]
        )
        print(f"✅ Generated: {out_path}")

if __name__ == "__main__":
    main()

