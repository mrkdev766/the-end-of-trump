#!/usr/bin/env python3
"""
generate_audio.py
Synthesizes Christopher Neural TTS for every line, measures exact durations,
writes scenes.json, and masters the voiceover with ducked dark cinematic BGM.
"""

import os, json, subprocess

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
AUDIO_DIR = os.path.join(PROJECT_DIR, "assets/audio/segments")
OUTPUT_AUDIO_DIR = os.path.join(PROJECT_DIR, "assets/audio")
BGM_FILE = os.path.join(PROJECT_DIR, "assets/music/dark_cinematic_bgm.mp3")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICE = "en-US-ChristopherNeural"

STORYBOARD = [
    # New Hook: Midterm Election & Viral Video Prediction
    {
        "id": "scene_hook_01",
        "type": "video",
        "asset": "assets/video/democrat_victory_celebration_opening.mp4",
        "text": "Hi, while checking midterm election results, I came across a crazy video. Just watch this...",
        "motion": "cut"
    },
    {
        "id": "scene_hook_02_video",
        "type": "title_card",
        "asset": "assets/titles/hook_viral_clip_3s.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_hook_03",
        "type": "image",
        "asset": "assets/images_enhanced/47_trump_night_capitol_look_up.jpg",
        "text": "That was crazy, right? Let’s see if his prediction comes true or not. But in the meantime, let’s look into what is really going to happen to Donald Trump under these unprecedented circumstances.",
        "motion": "zoom_in"
    },
    # 0. Title Card Intro
    {
        "id": "scene_00_title",
        "type": "title_card",
        "asset": "assets/titles/title_00_intro.mp4",
        "text": "",
        "pause_after": 0.2
    },
    # Opening
    {
        "id": "scene_01",
        "type": "image",
        "asset": "assets/images_enhanced/01_trump_butler_fist.jpg",
        "text": "He survived assassination attempts.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_02",
        "type": "image",
        "asset": "assets/images_enhanced/02_trump_flag_crane_rally.jpg",
        "text": "He defeated political opponents.",
        "motion": "pan_up"
    },
    {
        "id": "scene_03",
        "type": "image",
        "asset": "assets/images_enhanced/03_trump_inauguration_oath.jpg",
        "text": "He returned to the White House after one of the most controversial elections in American history.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_04",
        "type": "image",
        "asset": "assets/images_enhanced/46_white_house_dark_storm_clouds.jpg",
        "text": "But now, Donald Trump is facing a series of challenges that could reshape the rest of his presidency.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_05",
        "type": "image",
        "asset": "assets/images_enhanced/05_capitol_lightning_night.jpg",
        "text": "His party has suffered a major setback in Congress.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_06",
        "type": "image",
        "asset": "assets/images_enhanced/18_iran_3d_glowing_map.jpg",
        "text": "His administration is dealing with an escalating confrontation with Iran.",
        "motion": "pan_right"
    },
    {
        "id": "scene_07",
        "type": "image",
        "asset": "assets/images_enhanced/34_sniper_rooftop_city_dusk.jpg",
        "text": "And behind the political crisis, there are reports of threats against his own life.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_08",
        "type": "image",
        "asset": "assets/images_enhanced/09_trump_close_up_portrait.jpg",
        "text": "For a president who built his political identity around strength, control, and victory, the situation is becoming increasingly complicated.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_09",
        "type": "image",
        "asset": "assets/images_enhanced/45_trump_resolute_desk_prayer.jpg",
        "text": "But is this really the beginning of the end for Donald Trump?",
        "motion": "zoom_in"
    },
    {
        "id": "scene_10",
        "type": "image",
        "asset": "assets/images_enhanced/39_trump_low_angle_flag_sky.jpg",
        "text": "Or is this just another crisis he could survive?",
        "motion": "pan_up"
    },

    # Chapter 1 Title Card
    {
        "id": "scene_11_ch1_title",
        "type": "title_card",
        "asset": "assets/titles/title_01_chapter1.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_12",
        "type": "video",
        "asset": "assets/titles/date_scene_12.mp4",
        "text": "November 3, 2026. America's midterm elections delivered a major political setback for Donald Trump.",
        "motion": "cut"
    },
    {
        "id": "scene_13",
        "type": "image",
        "asset": "assets/images_enhanced/10_abc_news_election_night_desk.jpg",
        "text": "The Democrats regained control of both chambers of Congress, the House of Representatives and the Senate.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_14",
        "type": "image",
        "asset": "assets/images_enhanced/12_empty_committee_hearing_dais.jpg",
        "text": "And this matters far more than just losing an election.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_15",
        "type": "image",
        "asset": "assets/images_enhanced/14_signing_eo_resolute_mike_johnson.jpg",
        "text": "For the first two years of his second presidency, Trump had the advantage of a Republican-controlled Congress.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_16",
        "type": "image",
        "asset": "assets/images_enhanced/11_house_chamber_joint_session.jpg",
        "text": "That meant his administration could move forward with legislation, appointments, and major policy decisions with support from his own party.",
        "motion": "pan_right"
    },
    {
        "id": "scene_17",
        "type": "image",
        "asset": "assets/images_enhanced/05_capitol_lightning_night.jpg",
        "text": "But that political advantage has now changed.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_18",
        "type": "image",
        "asset": "assets/images_enhanced/15_press_photographers_hearing_scrum.jpg",
        "text": "Beginning in January 2027, Democrats will have greater power to investigate his administration, challenge his policies, and block important legislative priorities.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_19",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "Trump will still be president.",
        "motion": "pan_down"
    },
    {
        "id": "scene_20",
        "type": "image",
        "asset": "assets/images_enhanced/41_trump_marine_one_chopper_talk.jpg",
        "text": "But governing America could become considerably more difficult.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_21",
        "type": "image",
        "asset": "assets/images_enhanced/16_white_house_south_portico.jpg",
        "text": "And this is happening at a particularly sensitive moment. Because the biggest challenge facing his administration isn't even inside America.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_22",
        "type": "image",
        "asset": "assets/images_enhanced/33_generals_holographic_mideast_map.jpg",
        "text": "It's thousands of miles away, in Iran.",
        "motion": "zoom_in"
    },

    # Chapter 2 Title Card
    {
        "id": "scene_23_ch2_title",
        "type": "title_card",
        "asset": "assets/titles/title_02_chapter2.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_24",
        "type": "video",
        "asset": "assets/video/dod_carrier_night_ops.mp4",
        "text": "For months, the United States has been caught in a dangerous confrontation with Iran.",
        "motion": "cut"
    },
    {
        "id": "scene_25",
        "type": "video",
        "asset": "assets/video/dod_airstrike_ir_drone.mp4",
        "text": "What began as military operations has developed into a conflict with consequences far beyond the Middle East.",
        "motion": "cut"
    },
    {
        "id": "scene_26",
        "type": "image",
        "asset": "assets/images_enhanced/21_strait_of_hormuz_tankers_aerial.jpg",
        "text": "One of the biggest concerns is the Strait of Hormuz.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_27",
        "type": "image",
        "asset": "assets/images_enhanced/06_uss_eisenhower_carrier.jpg",
        "text": "A narrow waterway through which a significant portion of the world's oil supply travels.",
        "motion": "pan_left"
    },
    {
        "id": "scene_28",
        "type": "image",
        "asset": "assets/images_enhanced/22_oil_refinery_storage_tanks_night.jpg",
        "text": "Any disruption here can affect global energy markets, fuel prices, and economies around the world.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_29",
        "type": "image",
        "asset": "assets/images_enhanced/37_tanker_flags_tearing_tug_of_war.jpg",
        "text": "And the consequences are not limited to America's foreign policy.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_30",
        "type": "image",
        "asset": "assets/images_enhanced/23_gas_station_price_board.jpg",
        "text": "They are increasingly becoming a domestic political issue for Trump.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_31",
        "type": "image",
        "asset": "assets/images_enhanced/43_wall_street_crude_oil_panic.jpg",
        "text": "The longer the conflict continues, the more difficult it becomes for his administration to explain its costs and objectives to the American public.",
        "motion": "pan_right"
    },
    {
        "id": "scene_32",
        "type": "image",
        "asset": "assets/images_enhanced/13_cabinet_meeting_rubio_hegseth.jpg",
        "text": "Trump has repeatedly suggested that the conflict could end soon.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_33",
        "type": "image",
        "asset": "assets/images_enhanced/27_khamenei_speech_blue_stage.jpg",
        "text": "But Iran has continued to issue warnings against further American military action.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_34",
        "type": "video",
        "asset": "assets/titles/date_scene_34.mp4",
        "text": "On November 4, Iran's Supreme Leader warned that another American attack could trigger a wider retaliation.",
        "motion": "cut"
    },
    {
        "id": "scene_35",
        "type": "video",
        "asset": "assets/video/tanker_boarding.webm",
        "text": "And that brings us to another, much more personal dimension of this conflict. Because Iran's hostility towards Trump is not just about American military policy.",
        "motion": "cut"
    },
    {
        "id": "scene_36",
        "type": "image",
        "asset": "assets/images_enhanced/20_orbital_strike_escalation_map.jpg",
        "text": "It is also connected to events dating back to 2020.",
        "motion": "zoom_in"
    },

    # Chapter 3 Title Card
    {
        "id": "scene_37_ch3_title",
        "type": "title_card",
        "asset": "assets/titles/title_03_chapter3.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_38",
        "type": "video",
        "asset": "assets/titles/date_scene_38.mp4",
        "text": "January 2020. A US drone strike near Baghdad International Airport killed Iranian military commander Qassem Soleimani.",
        "motion": "cut"
    },
    {
        "id": "scene_39",
        "type": "video",
        "asset": "assets/video/mq9_reaper_drone.webm",
        "text": "The operation was ordered by Donald Trump during his first presidency.",
        "motion": "cut"
    },
    {
        "id": "scene_40",
        "type": "image",
        "asset": "assets/images_enhanced/30_trump_national_address_milley_2020.jpg",
        "text": "Iran promised retaliation.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_41",
        "type": "image",
        "asset": "assets/images_enhanced/31_soleimani_funeral_tehran_crowd.jpg",
        "text": "And Trump became a potential target in that confrontation.",
        "motion": "pan_up"
    },
    {
        "id": "scene_42",
        "type": "video",
        "asset": "assets/titles/date_scene_42.mp4",
        "text": "In August 2026, Reuters reported that Israel had repeatedly warned American officials about alleged Iranian assassination plots targeting Trump.",
        "motion": "cut"
    },
    {
        "id": "scene_43",
        "type": "image",
        "asset": "assets/images_enhanced/36_top_secret_classified_folder.jpg",
        "text": "The reported possibilities included attacks involving snipers and other methods.",
        "motion": "pan_down"
    },
    {
        "id": "scene_44",
        "type": "image",
        "asset": "assets/images_enhanced/42_diplomatic_talks_us_iran_table.jpg",
        "text": "However, American intelligence officials could not independently verify some of those specific allegations.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_45",
        "type": "image",
        "asset": "assets/images_enhanced/08_trump_oval_window_flag_back.jpg",
        "text": "That distinction is important.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_46",
        "type": "image",
        "asset": "assets/images_enhanced/07_trump_police_officers_escort.jpg",
        "text": "These reports do not establish that Iran has an active, confirmed assassination operation against Trump. But they reveal how far the hostility between the two sides has escalated.",
        "motion": "pan_left"
    },
    {
        "id": "scene_47",
        "type": "image",
        "asset": "assets/images_enhanced/32_butler_secret_service_stairs_rush.jpg",
        "text": "And with the conflict continuing, Trump's personal security has become another issue surrounding his presidency.",
        "motion": "zoom_in"
    },

    # Chapter 4 Title Card
    {
        "id": "scene_48_ch4_title",
        "type": "title_card",
        "asset": "assets/titles/title_04_chapter4.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_49",
        "type": "image",
        "asset": "assets/images_enhanced/40_senate_chamber_trial_debate.jpg",
        "text": "Now comes the biggest political question. With Democrats controlling Congress, could Trump actually lose his presidency?",
        "motion": "zoom_in"
    },
    {
        "id": "scene_50",
        "type": "image",
        "asset": "assets/images_enhanced/04_trump_resolute_desk_seated.jpg",
        "text": "The answer is more complicated than it appears. Winning control of Congress does not automatically remove a president. Trump remains constitutionally entitled to serve his full term.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_51",
        "type": "image",
        "asset": "assets/images_enhanced/24_trump_briefing_room_podium_blue_tie.jpg",
        "text": "However, Democrats will have greater authority to conduct congressional investigations and potentially begin impeachment proceedings.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_52",
        "type": "image",
        "asset": "assets/images_enhanced/38_trump_the_beast_dusk_wave.jpg",
        "text": "But impeachment itself does not remove a president. The Senate must also convict him with the required two-thirds majority. And that remains a significant constitutional obstacle.",
        "motion": "pan_right"
    },
    {
        "id": "scene_53",
        "type": "image",
        "asset": "assets/images_enhanced/25_trump_podium_warning_red_tie.jpg",
        "text": "In other words, the midterm results have weakened Trump's political position, but they have not ended his presidency.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_54",
        "type": "image",
        "asset": "assets/images_enhanced/19_carrier_vs_patrol_boats_standoff.jpg",
        "text": "The bigger question is what happens next. Can Trump bring the Iran conflict to an end?",
        "motion": "pan_left"
    },
    {
        "id": "scene_55",
        "type": "image",
        "asset": "assets/images_enhanced/21_strait_of_hormuz_tankers_aerial.jpg",
        "text": "Can he prevent further economic damage?",
        "motion": "zoom_in"
    },
    {
        "id": "scene_56",
        "type": "image",
        "asset": "assets/images_enhanced/02_trump_flag_crane_rally.jpg",
        "text": "And can his administration regain public confidence before the next presidential election?",
        "motion": "pan_up"
    },

    # Ending Title Card
    {
        "id": "scene_57_ending_title",
        "type": "title_card",
        "asset": "assets/titles/title_05_verdict.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_58",
        "type": "image",
        "asset": "assets/images_enhanced/01_trump_butler_fist.jpg",
        "text": "Donald Trump has already experienced political defeats, legal battles, public controversies, and even assassination attempts.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_59",
        "type": "image",
        "asset": "assets/images_enhanced/03_trump_inauguration_oath.jpg",
        "text": "Yet he returned to the White House.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_60",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "Now, as his second presidency enters another difficult chapter, he faces a different kind of challenge.",
        "motion": "pan_down"
    },
    {
        "id": "scene_61",
        "type": "image",
        "asset": "assets/images_enhanced/11_house_chamber_joint_session.jpg",
        "text": "A divided Congress.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_62",
        "type": "image",
        "asset": "assets/images_enhanced/20_orbital_strike_escalation_map.jpg",
        "text": "An increasingly complicated international conflict.",
        "motion": "pan_right"
    },
    {
        "id": "scene_63",
        "type": "image",
        "asset": "assets/images_enhanced/45_trump_resolute_desk_prayer.jpg",
        "text": "And a political future that is no longer entirely in his own hands.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_64",
        "type": "image",
        "asset": "assets/images_enhanced/09_trump_close_up_portrait.jpg",
        "text": "So, is this the end of Donald Trump? Not yet.",
        "motion": "zoom_out"
    },
    {
        "id": "scene_65",
        "type": "image",
        "asset": "assets/images_enhanced/47_trump_night_capitol_look_up.jpg",
        "text": "But the next two years could determine how his presidency is remembered.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_66",
        "type": "image",
        "asset": "assets/images_enhanced/46_white_house_dark_storm_clouds.jpg",
        "text": "And perhaps, how his political story finally ends.",
        "motion": "zoom_out"
    },
    # Ending Outro + Bonus Video in Animated Sketch Box
    {
        "id": "scene_67_outro",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "That's all for today, see you—bye! ...Oh, actually wait, there is something more.",
        "motion": "zoom_in"
    },
    {
        "id": "scene_68_ending_video",
        "type": "title_card",
        "asset": "assets/titles/ending_trump_phone_clip.mp4",
        "text": "",
        "pause_after": 0.2
    }
]

def get_media_duration(path):
    cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{path}"'
    res = subprocess.check_output(cmd, shell=True).decode().strip()
    return float(res)

def generate_tts_for_scene(item):
    sid = item["id"]
    text = item.get("text", "").strip()
    
    if item["type"] == "title_card":
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
        return item
    
    # Generate edge-tts with cache and retry
    out_mp3 = os.path.join(AUDIO_DIR, f"{sid}.mp3")
    out_wav = os.path.join(AUDIO_DIR, f"{sid}.wav")
    
    if os.path.exists(out_wav) and os.path.getsize(out_wav) > 1000:
        dur = get_media_duration(out_wav)
        item["duration"] = round(dur, 2)
        item["audio_file"] = f"assets/audio/segments/{sid}.wav"
        print(f"[{sid}] (Cached) TTS: {dur}s")
        return item

    import time
    for attempt in range(5):
        try:
            cmd_tts = f'edge-tts --voice "{VOICE}" --rate="-2%" --text "{text}" --write-media "{out_mp3}"'
            subprocess.run(cmd_tts, shell=True, check=True)
            break
        except Exception as e:
            print(f"[{sid}] Attempt {attempt+1} failed: {e}. Retrying in 1.5s...")
            time.sleep(1.5)
            
    cmd_conv = f'ffmpeg -y -i "{out_mp3}" -af "apad=pad_dur=0.25" -ar 44100 -ac 2 "{out_wav}"'
    subprocess.run(cmd_conv, shell=True, check=True)
    
    # If this is an animated date event scene, mix typewriter clicks & paper slam
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
    return item

def master_soundtrack(scenes, total_duration):
    print("=== Mastering Continuous Soundtrack & Ducked BGM ===")
    # 1. Create concat list of all segment WAV files
    concat_list = os.path.join(AUDIO_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for s in scenes:
            wav_path = os.path.join(PROJECT_DIR, s["audio_file"])
            f.write(f"file '{wav_path}'\n")
            
    # Concatenate voiceover track
    raw_vo_wav = os.path.join(OUTPUT_AUDIO_DIR, "full_voiceover.wav")
    subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{raw_vo_wav}"', shell=True, check=True)
    
    vo_dur = get_media_duration(raw_vo_wav)
    print(f"Full Voiceover Duration: {vo_dur:.2f}s ({vo_dur/60:.2f} min)")
    
    # 2. Mix with dark_cinematic_bgm.mp3 with ducking
    # Calculate start and end timestamps of both viral video scenes for deep ducking
    clip1_start = 0.0
    clip1_end = 0.0
    clip2_start = 0.0
    clip2_end = 0.0
    cur_t = 0.0
    for s in scenes:
        if s["id"] == "scene_hook_02_video":
            clip1_start = cur_t
            clip1_end = cur_t + s["duration"]
        elif s["id"] == "scene_68_ending_video":
            clip2_start = cur_t
            clip2_end = cur_t + s["duration"]
        cur_t += s["duration"]
        
    print(f"Hook viral clip timing: {clip1_start:.2f}s to {clip1_end:.2f}s")
    print(f"Ending Trump phone clip timing: {clip2_start:.2f}s to {clip2_end:.2f}s")
    
    final_mix_wav = os.path.join(OUTPUT_AUDIO_DIR, "voiceover_with_bgm.wav")
    final_mix_mp3 = os.path.join(OUTPUT_AUDIO_DIR, "voiceover_with_bgm.mp3")
    
    # Duck BGM down to 0.02 during both viral video clips so their audio is front and center
    bgm_vol_expr = (
        f"if(between(t\\,{clip1_start-0.2:.2f}\\,{clip1_end+0.2:.2f})\\,0.02\\,"
        f"if(between(t\\,{clip2_start-0.2:.2f}\\,{clip2_end+0.2:.2f})\\,0.02\\,0.18))"
    )
    filter_complex = (
        f"[0:a]volume=1.25,alimiter=limit=0.95[vo];"
        f"[1:a]aloop=loop=-1:size=2e+09,volume='{bgm_vol_expr}':eval=frame,afade=t=in:ss=0:d=2.0,afade=t=out:st={vo_dur-3.0}:d=3.0[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=0[outa]"
    )
    
    cmd_mix = (
        f'ffmpeg -y -i "{raw_vo_wav}" -i "{BGM_FILE}" '
        f'-filter_complex "{filter_complex}" -map "[outa]" -t {vo_dur} "{final_mix_wav}"'
    )
    subprocess.run(cmd_mix, shell=True, check=True)
    subprocess.run(f'ffmpeg -y -i "{final_mix_wav}" -c:a libmp3lame -q:a 2 "{final_mix_mp3}"', shell=True, check=True)
    print(f"Mastered final soundtrack: {final_mix_wav} and {final_mix_mp3}")
    return final_mix_wav, vo_dur

def main():
    print("=== Generating Audio & Storyboard Manifest ===")
    processed_scenes = []
    total_time = 0.0
    for idx, item in enumerate(STORYBOARD):
        processed = generate_tts_for_scene(item)
        processed_scenes.append(processed)
        total_time += processed["duration"]
        
    manifest_path = os.path.join(PROJECT_DIR, "scenes.json")
    with open(manifest_path, "w") as f:
        json.dump(processed_scenes, f, indent=2)
    print(f"Saved storyboard manifest: {manifest_path} ({len(processed_scenes)} scenes, {total_time:.2f}s total)")
    
    master_soundtrack(processed_scenes, total_time)

if __name__ == "__main__":
    main()
