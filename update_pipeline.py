#!/usr/bin/env python3
"""
update_pipeline.py
Updates generate_audio.py to:
1. Use enhanced 16:9 images (assets/images_enhanced/)
2. Use animated date overlays (date_scene_12, 34, 38, 42)
3. Use authentic B-roll video footage (MQ-9 drone, carrier, tanker)
4. Preserve tactile title card audio in the master track
5. Mix typewriter & slam SFX into date narration segments
"""

import re

SRC_PATH = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc/generate_audio.py"

with open(SRC_PATH, "r") as f:
    content = f.read()

# 1. Update image directory in assets
content = content.replace('"assets/images/', '"assets/images_enhanced/')

# 2. Update specific scenes
# scene_12 -> date_scene_12.mp4
content = re.sub(
    r'\{\s*"id":\s*"scene_12",\s*"type":\s*"image",\s*"asset":\s*"assets/images_enhanced/44_voter_lines_polling_station\.jpg",\s*"text":\s*"([^"]+)",\s*"motion":\s*"[^"]+"\s*\}',
    r'{\n        "id": "scene_12",\n        "type": "video",\n        "asset": "assets/titles/date_scene_12.mp4",\n        "text": "\1",\n        "motion": "cut"\n    }',
    content
)

# scene_34 -> date_scene_34.mp4
content = re.sub(
    r'\{\s*"id":\s*"scene_34",\s*"type":\s*"image",\s*"asset":\s*"assets/images_enhanced/26_khamenei_irgc_generals_salute\.jpg",\s*"text":\s*"([^"]+)",\s*"motion":\s*"[^"]+"\s*\}',
    r'{\n        "id": "scene_34",\n        "type": "video",\n        "asset": "assets/titles/date_scene_34.mp4",\n        "text": "\1",\n        "motion": "cut"\n    }',
    content
)

# scene_38 -> date_scene_38.mp4
content = re.sub(
    r'\{\s*"id":\s*"scene_38",\s*"type":\s*"image",\s*"asset":\s*"assets/images_enhanced/28_baghdad_airport_tarmac_night\.jpg",\s*"text":\s*"([^"]+)",\s*"motion":\s*"[^"]+"\s*\}',
    r'{\n        "id": "scene_38",\n        "type": "video",\n        "asset": "assets/titles/date_scene_38.mp4",\n        "text": "\1",\n        "motion": "cut"\n    }',
    content
)

# scene_39 -> mq9_reaper_drone.webm
content = re.sub(
    r'\{\s*"id":\s*"scene_39",\s*"type":\s*"image",\s*"asset":\s*"assets/images_enhanced/29_qasem_soleimani_portrait\.jpg",\s*"text":\s*"([^"]+)",\s*"motion":\s*"[^"]+"\s*\}',
    r'{\n        "id": "scene_39",\n        "type": "video",\n        "asset": "assets/video/mq9_reaper_drone.webm",\n        "text": "\1",\n        "motion": "cut"\n    }',
    content
)

# scene_42 -> date_scene_42.mp4
content = re.sub(
    r'\{\s*"id":\s*"scene_42",\s*"type":\s*"image",\s*"asset":\s*"assets/images_enhanced/35_cyber_intel_command_center\.jpg",\s*"text":\s*"([^"]+)",\s*"motion":\s*"[^"]+"\s*\}',
    r'{\n        "id": "scene_42",\n        "type": "video",\n        "asset": "assets/titles/date_scene_42.mp4",\n        "text": "\1",\n        "motion": "cut"\n    }',
    content
)

# 3. Update generate_tts_for_scene to use title card audio and mix date SFX
title_code_old = """    if item["type"] == "title_card":
        # Duration comes from pre-rendered video
        full_path = os.path.join(PROJECT_DIR, item["asset"])
        dur = get_media_duration(full_path)
        item["duration"] = round(dur, 2)
        # Create silent audio matching title card length
        silent_audio = os.path.join(AUDIO_DIR, f"{sid}_silent.wav")
        subprocess.run(f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {dur} "{silent_audio}"', shell=True, check=True)
        item["audio_file"] = f"assets/audio/segments/{sid}_silent.wav"
        print(f"[{sid}] Title card duration: {item['duration']}s")
        return item"""

title_code_new = """    if item["type"] == "title_card":
        # Duration comes from pre-rendered video
        full_path = os.path.join(PROJECT_DIR, item["asset"])
        dur = get_media_duration(full_path)
        item["duration"] = round(dur, 2)
        # Use tactile title card sound design!
        title_wav = full_path.replace(".mp4", ".wav")
        title_seg_wav = os.path.join(AUDIO_DIR, f"{sid}_title.wav")
        if os.path.exists(title_wav):
            subprocess.run(f'ffmpeg -y -i "{title_wav}" -ar 44100 -ac 2 -t {dur} "{title_seg_wav}"', shell=True, check=True)
            item["audio_file"] = f"assets/audio/segments/{sid}_title.wav"
        else:
            silent_audio = os.path.join(AUDIO_DIR, f"{sid}_silent.wav")
            subprocess.run(f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {dur} "{silent_audio}"', shell=True, check=True)
            item["audio_file"] = f"assets/audio/segments/{sid}_silent.wav"
        print(f"[{sid}] Title card duration: {item['duration']}s (with tactile SFX)")
        return item"""

content = content.replace(title_code_old, title_code_new)

# Add SFX mixing for date scenes
sfx_mix_target = """    dur = get_media_duration(out_wav)
    item["duration"] = round(dur, 2)
    item["audio_file"] = f"assets/audio/segments/{sid}.wav"
    print(f"[{sid}] TTS: {dur}s -> {text[:45]}...")
    return item"""

sfx_mix_replacement = """    # If this is an animated date event scene, mix typewriter clicks & paper slam
    if sid in ["scene_12", "scene_34", "scene_38", "scene_42"]:
        sfx_type = os.path.join(PROJECT_DIR, "assets/audio/typewriter_burst.wav")
        sfx_slam = os.path.join(PROJECT_DIR, "assets/audio/paper_slam.wav")
        temp_mix = out_wav + ".mixed.wav"
        subprocess.run(
            f'ffmpeg -y -i "{out_wav}" -itsoffset 0.2 -i "{sfx_slam}" -itsoffset 0.6 -i "{sfx_type}" '
            f'-filter_complex "[0:a]volume=1.0[a0];[1:a]volume=1.1[a1];[2:a]volume=1.2[a2];[a0][a1][a2]amix=inputs=3:dropout_transition=0,volume=1.05[aout]" '
            f'-map "[aout]" -ar 44100 -ac 2 "{temp_mix}"',
            shell=True, check=True
        )
        os.replace(temp_mix, out_wav)

    dur = get_media_duration(out_wav)
    item["duration"] = round(dur, 2)
    item["audio_file"] = f"assets/audio/segments/{sid}.wav"
    print(f"[{sid}] TTS: {dur}s -> {text[:45]}...")
    return item"""

content = content.replace(sfx_mix_target, sfx_mix_replacement)

with open(SRC_PATH, "w") as f:
    f.write(content)

print("Updated generate_audio.py successfully!")

