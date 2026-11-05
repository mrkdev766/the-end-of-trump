#!/usr/bin/env python3
"""
generate_audio.py
Masters the complete documentary soundtrack using the user's newly provided voiceover narration:
- Slices user-recorded master narration takes with microsecond precision for every scene
- Sets exact scene durations in scenes.json
- Attaches tactical sound design to all chapter title cards (whoosh, paper slam, highlighter squeak, typewriter)
- Masters continuous voiceover track with ducked dark cinematic BGM:
  * Deep ducking (0.02) during both viral sketch videos
  * Tactical ducking (0.04) during all chapter title cards for maximum SFX punch and clarity
  * Atmospheric cinematic bed (0.18) during narrative scenes
"""

import os, json, subprocess

PROJECT_DIR = "/home/rashid/.gemini/antigravity/scratch/trump-iran-doc"
AUDIO_DIR = os.path.join(PROJECT_DIR, "assets/audio/segments")
OUTPUT_AUDIO_DIR = os.path.join(PROJECT_DIR, "assets/audio")
BGM_FILE = os.path.join(PROJECT_DIR, "assets/music/dark_cinematic_bgm.mp3")
os.makedirs(AUDIO_DIR, exist_ok=True)

# User's Master Audio Tracks
USER_UPLOAD_DIR = os.path.join(PROJECT_DIR, "assets/audio/user_narration")
if not os.path.exists(USER_UPLOAD_DIR):
    USER_UPLOAD_DIR = "/home/rashid/.gemini/antigravity/brain/1e5be721-c9b4-4d36-8f45-30a2f3a82e22/.user_uploaded"
SRC_HOOK_01 = os.path.join(USER_UPLOAD_DIR, "uploaded_media_1_1793835656984.wav")
SRC_HOOK_03 = os.path.join(USER_UPLOAD_DIR, "uploaded_media_0_1793835656984.wav")
SRC_INTRO   = os.path.join(USER_UPLOAD_DIR, "uploaded_media_4_1793835656984.wav")
SRC_CH1     = os.path.join(USER_UPLOAD_DIR, "uploaded_media_3_1793835656984.wav")
SRC_CH2     = os.path.join(USER_UPLOAD_DIR, "uploaded_media_2_1793835656984.wav")
SRC_CH3     = os.path.join(USER_UPLOAD_DIR, "uploaded_media_2_1793835688213.wav")
SRC_CH4     = os.path.join(USER_UPLOAD_DIR, "uploaded_media_1_1793835688213.wav")
SRC_VERDICT = os.path.join(USER_UPLOAD_DIR, "uploaded_media_0_1793835688213.wav")

STORYBOARD = [
    # New Hook: Midterm Election & Viral Video Prediction
    {
        "id": "scene_hook_01",
        "type": "video",
        "asset": "assets/video/democrat_victory_celebration_opening.mp4",
        "text": "Hi, while checking midterm election results, I came across a crazy video. Just watch this...",
        "audio_src": SRC_HOOK_01,
        "slice": (0.00, 6.68),
        "motion": "cut"
    },
    {
        "id": "scene_hook_02_video",
        "type": "title_card",
        "asset": "assets/titles/hook_viral_clip.mp4",
        "text": "",
        "pause_after": 0.2
    },
    {
        "id": "scene_hook_03",
        "type": "image",
        "asset": "assets/images_enhanced/47_trump_night_capitol_look_up.jpg",
        "text": "That was crazy, right? Let’s see if his prediction comes true or not. But in the meantime, let’s look into what is really going to happen to Donald Trump under these unprecedented circumstances.",
        "audio_src": SRC_HOOK_03,
        "slice": (0.00, 11.84),
        "motion": "zoom_in",
        "focus_y": 0.30
    },
    # 0. Title Card Intro
    {
        "id": "scene_00_title",
        "type": "title_card",
        "asset": "assets/titles/title_00_intro.mp4",
        "text": "",
        "pause_after": 0.2
    },
    # Opening Intro
    {
        "id": "scene_01",
        "type": "image",
        "asset": "assets/images_enhanced/01_trump_butler_fist.jpg",
        "text": "He survived assassination attempts.",
        "audio_src": SRC_INTRO,
        "slice": (0.00, 2.69),
        "motion": "zoom_in"
    },
    {
        "id": "scene_02",
        "type": "image",
        "asset": "assets/images_enhanced/02_trump_flag_crane_rally.jpg",
        "text": "He defeated political opponents.",
        "audio_src": SRC_INTRO,
        "slice": (2.69, 5.07),
        "motion": "pan_up"
    },
    {
        "id": "scene_03",
        "type": "image",
        "asset": "assets/images_enhanced/03_trump_inauguration_oath.jpg",
        "text": "He returned to the White House after one of the most controversial elections in American history.",
        "audio_src": SRC_INTRO,
        "slice": (5.07, 10.83),
        "motion": "zoom_in"
    },
    {
        "id": "scene_04",
        "type": "image",
        "asset": "assets/images_enhanced/46_white_house_dark_storm_clouds.jpg",
        "text": "But now, Donald Trump is facing a series of challenges that could reshape the rest of his presidency.",
        "audio_src": SRC_INTRO,
        "slice": (10.83, 16.98),
        "motion": "zoom_out"
    },
    {
        "id": "scene_05",
        "type": "image",
        "asset": "assets/images_enhanced/05_capitol_lightning_night.jpg",
        "text": "His party has suffered a major setback in Congress.",
        "audio_src": SRC_INTRO,
        "slice": (16.98, 19.87),
        "motion": "zoom_in"
    },
    {
        "id": "scene_06",
        "type": "image",
        "asset": "assets/images_enhanced/18_iran_3d_glowing_map.jpg",
        "text": "His administration is dealing with an escalating confrontation with Iran.",
        "audio_src": SRC_INTRO,
        "slice": (19.87, 23.88),
        "motion": "pan_right"
    },
    {
        "id": "scene_07",
        "type": "image",
        "asset": "assets/images_enhanced/34_sniper_rooftop_city_dusk.jpg",
        "text": "And behind the political crisis, there are reports of threats against his own life.",
        "audio_src": SRC_INTRO,
        "slice": (23.88, 29.23),
        "motion": "zoom_in"
    },
    {
        "id": "scene_08",
        "type": "image",
        "asset": "assets/images_enhanced/09_trump_close_up_portrait.jpg",
        "text": "For a president who built his political identity around strength, control, and victory, the situation is becoming increasingly complicated.",
        "audio_src": SRC_INTRO,
        "slice": (29.23, 37.54),
        "motion": "zoom_out"
    },
    {
        "id": "scene_09",
        "type": "image",
        "asset": "assets/images_enhanced/45_trump_resolute_desk_prayer.jpg",
        "text": "But is this really the beginning of the end for Donald Trump?",
        "audio_src": SRC_INTRO,
        "slice": (37.54, 40.86),
        "motion": "zoom_in"
    },
    {
        "id": "scene_10",
        "type": "image",
        "asset": "assets/images_enhanced/39_trump_low_angle_flag_sky.jpg",
        "text": "Or is this just another crisis he could survive?",
        "audio_src": SRC_INTRO,
        "slice": (40.86, 44.40),
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
        "audio_src": SRC_CH1,
        "slice": (0.00, 7.30),
        "motion": "cut"
    },
    {
        "id": "scene_13",
        "type": "image",
        "asset": "assets/images_enhanced/10_abc_news_election_night_desk.jpg",
        "text": "The Democrats regained control of both chambers of Congress, the House of Representatives and the Senate.",
        "audio_src": SRC_CH1,
        "slice": (7.30, 13.18),
        "motion": "zoom_in"
    },
    {
        "id": "scene_14",
        "type": "image",
        "asset": "assets/images_enhanced/12_empty_committee_hearing_dais.jpg",
        "text": "And this matters far more than just losing an election.",
        "audio_src": SRC_CH1,
        "slice": (13.18, 16.59),
        "motion": "zoom_out"
    },
    {
        "id": "scene_15",
        "type": "image",
        "asset": "assets/images_enhanced/14_signing_eo_resolute_mike_johnson.jpg",
        "text": "For the first two years of his second presidency, Trump had the advantage of a Republican-controlled Congress.",
        "audio_src": SRC_CH1,
        "slice": (16.59, 22.52),
        "motion": "zoom_in"
    },
    {
        "id": "scene_16",
        "type": "image",
        "asset": "assets/images_enhanced/11_house_chamber_joint_session.jpg",
        "text": "That meant his administration could move forward with legislation, appointments, and major policy decisions with support from his own party.",
        "audio_src": SRC_CH1,
        "slice": (22.52, 30.27),
        "motion": "pan_right"
    },
    {
        "id": "scene_17",
        "type": "image",
        "asset": "assets/images_enhanced/05_capitol_lightning_night.jpg",
        "text": "But that political advantage has now changed.",
        "audio_src": SRC_CH1,
        "slice": (30.27, 33.01),
        "motion": "zoom_in"
    },
    {
        "id": "scene_18",
        "type": "image",
        "asset": "assets/images_enhanced/15_press_photographers_hearing_scrum.jpg",
        "text": "Beginning in January 2027, Democrats will have greater power to investigate his administration, challenge his policies, and block important legislative priorities.",
        "audio_src": SRC_CH1,
        "slice": (33.01, 42.94),
        "motion": "zoom_in"
    },
    {
        "id": "scene_19",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "Trump will still be president.",
        "audio_src": SRC_CH1,
        "slice": (42.94, 44.78),
        "motion": "pan_down"
    },
    {
        "id": "scene_20",
        "type": "image",
        "asset": "assets/images_enhanced/41_trump_marine_one_chopper_talk.jpg",
        "text": "But governing America could become considerably more difficult.",
        "audio_src": SRC_CH1,
        "slice": (44.78, 48.49),
        "motion": "zoom_in"
    },
    {
        "id": "scene_21",
        "type": "image",
        "asset": "assets/images_enhanced/16_white_house_south_portico.jpg",
        "text": "And this is happening at a particularly sensitive moment. Because the biggest challenge facing his administration isn't even inside America.",
        "audio_src": SRC_CH1,
        "slice": (48.49, 56.90),
        "motion": "zoom_out"
    },
    {
        "id": "scene_22",
        "type": "image",
        "asset": "assets/images_enhanced/20_orbital_strike_escalation_map.jpg",
        "text": "It's thousands of miles away, in Iran.",
        "audio_src": SRC_CH1,
        "slice": (56.90, 60.00),
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
        "audio_src": SRC_CH2,
        "slice": (0.00, 4.73),
        "motion": "cut"
    },
    {
        "id": "scene_25",
        "type": "video",
        "asset": "assets/video/dod_airstrike_ir_drone.mp4",
        "text": "What began as military operations has developed into a conflict with consequences far beyond the Middle East.",
        "audio_src": SRC_CH2,
        "slice": (4.73, 11.14),
        "motion": "cut"
    },
    {
        "id": "scene_26",
        "type": "image",
        "asset": "assets/images_enhanced/21_strait_of_hormuz_tankers_aerial.jpg",
        "text": "One of the biggest concerns is the Strait of Hormuz.",
        "audio_src": SRC_CH2,
        "slice": (11.14, 14.39),
        "motion": "zoom_out"
    },
    {
        "id": "scene_27",
        "type": "image",
        "asset": "assets/images_enhanced/06_uss_eisenhower_carrier.jpg",
        "text": "A narrow waterway through which a significant portion of the world's oil supply travels.",
        "audio_src": SRC_CH2,
        "slice": (14.39, 19.57),
        "motion": "pan_left"
    },
    {
        "id": "scene_28",
        "type": "image",
        "asset": "assets/images_enhanced/22_oil_refinery_storage_tanks_night.jpg",
        "text": "Any disruption here can affect global energy markets, fuel prices, and economies around the world.",
        "audio_src": SRC_CH2,
        "slice": (19.57, 25.83),
        "motion": "zoom_in"
    },
    {
        "id": "scene_29",
        "type": "image",
        "asset": "assets/images_enhanced/37_tanker_flags_tearing_tug_of_war.jpg",
        "text": "And the consequences are not limited to America's foreign policy.",
        "audio_src": SRC_CH2,
        "slice": (25.83, 29.49),
        "motion": "pan_down"
    },
    {
        "id": "scene_30",
        "type": "image",
        "asset": "assets/images_enhanced/24_trump_briefing_room_podium_blue_tie.jpg",
        "text": "They are increasingly becoming a domestic political issue for Trump.",
        "audio_src": SRC_CH2,
        "slice": (29.49, 33.38),
        "motion": "zoom_in"
    },
    {
        "id": "scene_31",
        "type": "image",
        "asset": "assets/images_enhanced/25_trump_podium_warning_red_tie.jpg",
        "text": "The longer the conflict continues, the more difficult it becomes for his administration to explain its costs and objectives to the American public.",
        "audio_src": SRC_CH2,
        "slice": (33.38, 41.53),
        "motion": "pan_right"
    },
    {
        "id": "scene_32",
        "type": "image",
        "asset": "assets/images_enhanced/26_khamenei_irgc_generals_salute.jpg",
        "text": "Trump has repeatedly suggested that the conflict could end soon.",
        "audio_src": SRC_CH2,
        "slice": (41.53, 45.82),
        "motion": "zoom_out"
    },
    {
        "id": "scene_33",
        "type": "image",
        "asset": "assets/images_enhanced/27_khamenei_speech_blue_stage.jpg",
        "text": "But Iran has continued to issue warnings against further American military action.",
        "audio_src": SRC_CH2,
        "slice": (45.82, 50.83),
        "motion": "zoom_in"
    },
    {
        "id": "scene_34",
        "type": "video",
        "asset": "assets/titles/date_scene_34.mp4",
        "text": "On November 4, Iran's Supreme Leader warned that another American attack could trigger a wider retaliation.",
        "audio_src": SRC_CH2,
        "slice": (50.83, 57.96),
        "motion": "cut"
    },
    {
        "id": "scene_35",
        "type": "video",
        "asset": "assets/video/tanker_boarding.webm",
        "text": "And that brings us to another, much more personal dimension of this conflict. Because Iran's hostility towards Trump is not just about American military policy.",
        "audio_src": SRC_CH2,
        "slice": (57.96, 67.34),
        "motion": "cut"
    },
    {
        "id": "scene_36",
        "type": "image",
        "asset": "assets/images_enhanced/28_baghdad_airport_tarmac_night.jpg",
        "text": "It is also connected to events dating back to 2020.",
        "audio_src": SRC_CH2,
        "slice": (67.34, 70.76),
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
        "audio_src": SRC_CH3,
        "slice": (0.00, 7.64),
        "motion": "cut"
    },
    {
        "id": "scene_39",
        "type": "video",
        "asset": "assets/video/mq9_reaper_drone.webm",
        "text": "The operation was ordered by Donald Trump during his first presidency.",
        "audio_src": SRC_CH3,
        "slice": (7.64, 11.50),
        "motion": "cut"
    },
    {
        "id": "scene_40",
        "type": "image",
        "asset": "assets/images_enhanced/30_trump_national_address_milley_2020.jpg",
        "text": "Iran promised retaliation.",
        "audio_src": SRC_CH3,
        "slice": (11.50, 13.66),
        "motion": "zoom_out"
    },
    {
        "id": "scene_41",
        "type": "image",
        "asset": "assets/images_enhanced/31_soleimani_funeral_tehran_crowd.jpg",
        "text": "And Trump became a potential target in that confrontation.",
        "audio_src": SRC_CH3,
        "slice": (13.66, 17.53),
        "motion": "pan_up"
    },
    {
        "id": "scene_42",
        "type": "video",
        "asset": "assets/titles/date_scene_42.mp4",
        "text": "In August 2026, Reuters reported that Israel had repeatedly warned American officials about alleged Iranian assassination plots targeting Trump.",
        "audio_src": SRC_CH3,
        "slice": (17.53, 26.06),
        "motion": "cut"
    },
    {
        "id": "scene_43",
        "type": "image",
        "asset": "assets/images_enhanced/36_top_secret_classified_folder.jpg",
        "text": "The reported possibilities included attacks involving snipers and other methods.",
        "audio_src": SRC_CH3,
        "slice": (26.06, 30.52),
        "motion": "pan_down"
    },
    {
        "id": "scene_44",
        "type": "image",
        "asset": "assets/images_enhanced/42_diplomatic_talks_us_iran_table.jpg",
        "text": "However, American intelligence officials could not independently verify some of those specific allegations.",
        "audio_src": SRC_CH3,
        "slice": (30.52, 36.16),
        "motion": "zoom_out"
    },
    {
        "id": "scene_45",
        "type": "image",
        "asset": "assets/images_enhanced/08_trump_oval_window_flag_back.jpg",
        "text": "That distinction is important.",
        "audio_src": SRC_CH3,
        "slice": (36.16, 38.12),
        "motion": "zoom_in"
    },
    {
        "id": "scene_46",
        "type": "image",
        "asset": "assets/images_enhanced/07_trump_police_officers_escort.jpg",
        "text": "These reports do not establish that Iran has an active, confirmed assassination operation against Trump. But they reveal how far the hostility between the two sides has escalated.",
        "audio_src": SRC_CH3,
        "slice": (38.12, 47.98),
        "motion": "pan_left"
    },
    {
        "id": "scene_47",
        "type": "image",
        "asset": "assets/images_enhanced/32_butler_secret_service_stairs_rush.jpg",
        "text": "And with the conflict continuing, Trump's personal security has become another issue surrounding his presidency.",
        "audio_src": SRC_CH3,
        "slice": (47.98, 53.68),
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
        "audio_src": SRC_CH4,
        "slice": (0.00, 6.96),
        "motion": "zoom_in"
    },
    {
        "id": "scene_50",
        "type": "image",
        "asset": "assets/images_enhanced/04_trump_resolute_desk_seated.jpg",
        "text": "The answer is more complicated than it appears. Winning control of Congress does not automatically remove a president. Trump remains constitutionally entitled to serve his full term.",
        "audio_src": SRC_CH4,
        "slice": (6.96, 18.41),
        "motion": "zoom_out"
    },
    {
        "id": "scene_51",
        "type": "image",
        "asset": "assets/images_enhanced/24_trump_briefing_room_podium_blue_tie.jpg",
        "text": "However, Democrats will have greater authority to conduct congressional investigations and potentially begin impeachment proceedings.",
        "audio_src": SRC_CH4,
        "slice": (18.41, 25.18),
        "motion": "zoom_in"
    },
    {
        "id": "scene_52",
        "type": "image",
        "asset": "assets/images_enhanced/38_trump_the_beast_dusk_wave.jpg",
        "text": "But impeachment itself does not remove a president. The Senate must also convict him with the required two-thirds majority. And that remains a significant constitutional obstacle.",
        "audio_src": SRC_CH4,
        "slice": (25.18, 36.28),
        "motion": "pan_right"
    },
    {
        "id": "scene_53",
        "type": "image",
        "asset": "assets/images_enhanced/25_trump_podium_warning_red_tie.jpg",
        "text": "In other words, the midterm results have weakened Trump's political position, but they have not ended his presidency.",
        "audio_src": SRC_CH4,
        "slice": (36.28, 41.15),
        "motion": "zoom_in"
    },
    {
        "id": "scene_54",
        "type": "image",
        "asset": "assets/images_enhanced/19_carrier_vs_patrol_boats_standoff.jpg",
        "text": "The bigger question is what happens next. Can Trump bring the Iran conflict to an end?",
        "audio_src": SRC_CH4,
        "slice": (41.15, 46.75),
        "motion": "pan_left"
    },
    {
        "id": "scene_55",
        "type": "image",
        "asset": "assets/images_enhanced/21_strait_of_hormuz_tankers_aerial.jpg",
        "text": "Can he prevent further economic damage?",
        "audio_src": SRC_CH4,
        "slice": (46.75, 49.18),
        "motion": "zoom_in"
    },
    {
        "id": "scene_56",
        "type": "image",
        "asset": "assets/images_enhanced/02_trump_flag_crane_rally.jpg",
        "text": "And can his administration regain public confidence before the next presidential election?",
        "audio_src": SRC_CH4,
        "slice": (49.18, 54.36),
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
        "audio_src": SRC_VERDICT,
        "slice": (0.00, 8.90),
        "motion": "zoom_in"
    },
    {
        "id": "scene_59",
        "type": "image",
        "asset": "assets/images_enhanced/03_trump_inauguration_oath.jpg",
        "text": "Yet he returned to the White House.",
        "audio_src": SRC_VERDICT,
        "slice": (8.90, 11.58),
        "motion": "zoom_out"
    },
    {
        "id": "scene_60",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "Now, as his second presidency enters another difficult chapter, he faces a different kind of challenge.",
        "audio_src": SRC_VERDICT,
        "slice": (11.58, 18.17),
        "motion": "pan_down"
    },
    {
        "id": "scene_61",
        "type": "image",
        "asset": "assets/images_enhanced/11_house_chamber_joint_session.jpg",
        "text": "A divided Congress.",
        "audio_src": SRC_VERDICT,
        "slice": (18.17, 19.81),
        "motion": "zoom_in"
    },
    {
        "id": "scene_62",
        "type": "image",
        "asset": "assets/images_enhanced/20_orbital_strike_escalation_map.jpg",
        "text": "An increasingly complicated international conflict.",
        "audio_src": SRC_VERDICT,
        "slice": (19.81, 23.03),
        "motion": "pan_right"
    },
    {
        "id": "scene_63",
        "type": "image",
        "asset": "assets/images_enhanced/45_trump_resolute_desk_prayer.jpg",
        "text": "And a political future that is no longer entirely in his own hands.",
        "audio_src": SRC_VERDICT,
        "slice": (23.03, 27.36),
        "motion": "zoom_in"
    },
    {
        "id": "scene_64",
        "type": "image",
        "asset": "assets/images_enhanced/09_trump_close_up_portrait.jpg",
        "text": "So, is this the end of Donald Trump? Not yet.",
        "audio_src": SRC_VERDICT,
        "slice": (27.36, 31.24),
        "motion": "zoom_out"
    },
    {
        "id": "scene_65",
        "type": "image",
        "asset": "assets/images_enhanced/47_trump_night_capitol_look_up.jpg",
        "text": "But the next two years could determine how his presidency is remembered.",
        "audio_src": SRC_VERDICT,
        "slice": (31.24, 36.10),
        "motion": "zoom_in",
        "focus_y": 0.30
    },
    {
        "id": "scene_66",
        "type": "image",
        "asset": "assets/images_enhanced/46_white_house_dark_storm_clouds.jpg",
        "text": "And perhaps, how his political story finally ends.",
        "audio_src": SRC_VERDICT,
        "slice": (36.10, 39.03),
        "motion": "zoom_out"
    },
    # Ending Outro + Bonus Video in Animated Sketch Box
    {
        "id": "scene_67_outro",
        "type": "image",
        "asset": "assets/images_enhanced/17_trump_red_carpet_hallway_alone.jpg",
        "text": "That's all for today, see you—bye! ...Oh, actually wait, there is something more.",
        "audio_src": SRC_VERDICT,
        "slice": (39.03, 45.00),
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

def process_scene_audio(item):
    sid = item["id"]
    
    # 1. Title cards & Pre-rendered video clips
    if item["type"] == "title_card":
        full_path = os.path.join(PROJECT_DIR, item["asset"])
        dur = get_media_duration(full_path)
        item["duration"] = round(dur, 2)
        
        title_wav = full_path.replace(".mp4", ".wav")
        title_seg_wav = os.path.join(AUDIO_DIR, f"{sid}_title.wav")
        if os.path.exists(title_wav):
            subprocess.run(
                f'ffmpeg -y -i "{title_wav}" -af "apad=whole_dur={dur}" -ar 44100 -ac 2 -t {dur} "{title_seg_wav}" -v error',
                shell=True, check=True
            )
            item["audio_file"] = f"assets/audio/segments/{sid}_title.wav"
        else:
            silent_audio = os.path.join(AUDIO_DIR, f"{sid}_silent.wav")
            subprocess.run(
                f'ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=stereo -t {dur} "{silent_audio}" -v error',
                shell=True, check=True
            )
            item["audio_file"] = f"assets/audio/segments/{sid}_silent.wav"
        print(f"[{sid}] Title card duration: {item['duration']}s (tactile SFX synchronized)")
        return item

    # 2. Extract slice directly from user's custom narration WAV
    audio_src = item.get("audio_src")
    t_start, t_end = item.get("slice", (0.0, 0.0))
    dur = round(t_end - t_start, 2)
    out_wav = os.path.join(AUDIO_DIR, f"{sid}.wav")
    
    cmd_extract = (
        f'ffmpeg -y -i "{audio_src}" -ss {t_start} -to {t_end} '
        f'-af "volume=1.35,alimiter=limit=0.98,apad=whole_dur={dur}" -ar 44100 -ac 2 -t {dur} "{out_wav}" -v error'
    )
    subprocess.run(cmd_extract, shell=True, check=True)
    
    # 3. For animated date overlay scenes, mix tactile card slide + typewriter keystroke clicks
    if sid in ["scene_12", "scene_34", "scene_38", "scene_42"]:
        sfx_slam = os.path.join(PROJECT_DIR, "assets/audio/paper_slam.wav")
        sfx_type = os.path.join(PROJECT_DIR, "assets/audio/typewriter_burst.wav")
        temp_mix = out_wav + ".mixed.wav"
        subprocess.run(
            f'ffmpeg -y -i "{out_wav}" -i "{sfx_slam}" -i "{sfx_type}" '
            f'-filter_complex "[0:a]volume=1.35[vo];[1:a]adelay=150:all=1,volume=0.85[s1];[2:a]adelay=450:all=1,volume=1.1[s2];[vo][s1][s2]amix=inputs=3:normalize=0:dropout_transition=0,alimiter=limit=0.98,apad=whole_dur={dur}[aout]" '
            f'-map "[aout]" -ar 44100 -ac 2 -t {dur} "{temp_mix}" -v error',
            shell=True, check=True
        )
        os.replace(temp_mix, out_wav)
        print(f"[{sid}] Mixed tactile card slide & typewriter clicks into date overlay audio")
    
    actual_dur = round(get_media_duration(out_wav), 2)
    item["duration"] = actual_dur
    item["audio_file"] = f"assets/audio/segments/{sid}.wav"
    print(f"[{sid}] User Narration Slice: {actual_dur}s ({t_start:.2f}s -> {t_end:.2f}s)")
    return item

def master_soundtrack(scenes, total_duration):
    print("\n=== Mastering Continuous Soundtrack & Ducked BGM ===")
    
    # 1. Create concat list of all segment WAV files
    concat_list = os.path.join(AUDIO_DIR, "concat_list.txt")
    with open(concat_list, "w") as f:
        for s in scenes:
            wav_path = os.path.join(PROJECT_DIR, s["audio_file"])
            f.write(f"file '{wav_path}'\n")
            
    raw_vo_wav = os.path.join(OUTPUT_AUDIO_DIR, "full_voiceover.wav")
    subprocess.run(f'ffmpeg -y -f concat -safe 0 -i "{concat_list}" -c copy "{raw_vo_wav}" -v error', shell=True, check=True)
    
    vo_dur = get_media_duration(raw_vo_wav)
    print(f"Full Voiceover Track Duration: {vo_dur:.2f}s ({vo_dur/60:.2f} min)")
    
    # 2. Identify ducking time ranges:
    # Viral video clips duck deep to 0.02
    viral_ranges = []
    # Title card scenes duck to 0.04 for punchy tactile SFX
    title_ranges = []
    
    cur_t = 0.0
    for s in scenes:
        dur = s["duration"]
        if s["id"] in ["scene_hook_02_video", "scene_68_ending_video"]:
            viral_ranges.append((cur_t, cur_t + dur))
        elif s["id"] in [
            "scene_00_title", "scene_11_ch1_title", "scene_23_ch2_title",
            "scene_37_ch3_title", "scene_48_ch4_title", "scene_57_ending_title"
        ]:
            title_ranges.append((cur_t, cur_t + dur))
        cur_t += dur
        
    print(f"Viral video ranges (BGM -> 0.02): {viral_ranges}")
    print(f"Title card ranges (BGM -> 0.04): {title_ranges}")
    
    final_mix_wav = os.path.join(OUTPUT_AUDIO_DIR, "voiceover_with_bgm.wav")
    final_mix_mp3 = os.path.join(OUTPUT_AUDIO_DIR, "voiceover_with_bgm.mp3")
    
    # Build volume expression:
    expr = "0.18"
    for st, en in title_ranges:
        expr = f"if(between(t\\,{st:.2f}\\,{en:.2f})\\,0.04\\,{expr})"
    for st, en in viral_ranges:
        expr = f"if(between(t\\,{st-0.2:.2f}\\,{en+0.2:.2f})\\,0.02\\,{expr})"
        
    filter_complex = (
        f"[0:a]volume=1.05,alimiter=limit=0.98[vo];"
        f"[1:a]aloop=loop=-1:size=2e+09,volume='{expr}':eval=frame,afade=t=in:ss=0:d=1.5,afade=t=out:st={vo_dur-3.0}:d=3.0[bgm];"
        f"[vo][bgm]amix=inputs=2:duration=first:dropout_transition=0[outa]"
    )
    
    cmd_mix = (
        f'ffmpeg -y -i "{raw_vo_wav}" -i "{BGM_FILE}" '
        f'-filter_complex "{filter_complex}" -map "[outa]" -t {vo_dur} "{final_mix_wav}" -v error'
    )
    subprocess.run(cmd_mix, shell=True, check=True)
    subprocess.run(f'ffmpeg -y -i "{final_mix_wav}" -c:a libmp3lame -q:a 2 "{final_mix_mp3}" -v error', shell=True, check=True)
    print(f"Mastered final soundtrack: {final_mix_wav} and {final_mix_mp3}")
    return final_mix_wav, vo_dur

def main():
    print("=== Generating Audio & Storyboard Manifest with User Narration ===")
    processed_scenes = []
    total_time = 0.0
    for idx, item in enumerate(STORYBOARD):
        processed = process_scene_audio(item)
        processed_scenes.append(processed)
        total_time += processed["duration"]
        
    manifest_path = os.path.join(PROJECT_DIR, "scenes.json")
    with open(manifest_path, "w") as f:
        json.dump(processed_scenes, f, indent=2)
    print(f"\nSaved storyboard manifest: {manifest_path} ({len(processed_scenes)} scenes, {total_time:.2f}s total)")
    
    master_soundtrack(processed_scenes, total_time)

if __name__ == "__main__":
    main()
