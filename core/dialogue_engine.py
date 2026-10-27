"""
core/dialogue_engine.py - Animated Roblox Character Dialogue Compositor
Creates viral character drama Shorts with 2 talking avatars,
dynamic speaking focus, animated speech bubbles, and custom voices.
"""

import os
import sys
import shutil
import subprocess
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageOps
import edge_tts

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(ROOT_DIR, "assets", "fonts")
FONT_ANTON = os.path.join(FONTS_DIR, "Anton-Regular.ttf")
FONT_BOLD = os.path.join(FONTS_DIR, "Montserrat-ExtraBold.ttf")

AVATAR_BACON = os.path.join(ROOT_DIR, "assets", "avatars", "bacon.png")
AVATAR_PREPPY = os.path.join(ROOT_DIR, "assets", "avatars", "preppy.png")
DEFAULT_BG = os.path.join(ROOT_DIR, "assets", "backgrounds", "satisfying_bg.mp4")

# Binary resolution
FFMPEG_BIN = shutil.which("ffmpeg") or "/Users/aliaf/.local/bin/ffmpeg"
FFPROBE_BIN = shutil.which("ffprobe") or "/Users/aliaf/.local/bin/ffprobe"

W, H = 1080, 1920
FPS = 30

CHARACTERS = {
    "preppy": {
        "name": "👑 PREPPY",
        "voice": "en-US-AvaNeural",
        "rate": "+10%",
        "avatar_path": AVATAR_PREPPY,
        "side": "right",
        "theme_color": (236, 72, 153), # Hot Pink
        "bg_badge": (236, 72, 153, 230),
        "bubble_border": (244, 114, 182, 255)
    },
    "bacon": {
        "name": "🥓 BACON",
        "voice": "en-US-AndrewMultilingualNeural",
        "rate": "+6%",
        "avatar_path": AVATAR_BACON,
        "side": "left",
        "theme_color": (16, 185, 129), # Emerald Green
        "bg_badge": (16, 185, 129, 230),
        "bubble_border": (52, 211, 153, 255)
    }
}

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def get_audio_duration(file_path: str) -> float:
    cmd = [
        FFPROBE_BIN, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        return float(res.stdout.strip())
    except Exception:
        return 3.0

async def render_tts_line(text: str, voice: str, rate: str, out_file: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    for attempt in range(1, 4):
        try:
            comm = edge_tts.Communicate(text, voice, rate=rate)
            await comm.save(out_file)
            return out_file
        except Exception as e:
            if attempt == 3:
                raise e
            await asyncio.sleep(0.8)

def wrap_text(text: str, font: ImageFont.ImageFont, max_width: int):
    words = text.split(" ")
    lines = []
    curr = []
    for w in words:
        test = " ".join(curr + [w])
        bbox = font.getbbox(test)
        if bbox[2] - bbox[0] <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def render_dialogue_frame(active_speaker: str, speech_text: str, out_frame_path: str):
    """Draws the composite 1080x1920 Short frame with active and inactive avatars."""
    base = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)

    # 1. Subtle top and bottom dark gradients for contrast
    for y in range(450):
        alpha = int(140 * (1 - y / 450.0))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    for y in range(H - 600, H):
        alpha = int(180 * ((y - (H - 600)) / 600.0))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))

    # 2. Channel Header
    header_w, header_h = 420, 65
    hx = (W - header_w) // 2
    draw.rounded_rectangle([hx, 130, hx + header_w, 130 + header_h], radius=32, fill=(225, 29, 72, 230), outline=(255, 255, 255), width=2)
    h_font = get_font(FONT_ANTON, 32)
    h_text = "🚨 SECRETBLOX STORIES 🚨"
    h_bbox = h_font.getbbox(h_text)
    draw.text((hx + (header_w - (h_bbox[2] - h_bbox[0])) // 2, 130 + (header_h - (h_bbox[3] - h_bbox[1])) // 2 - 2), h_text, font=h_font, fill=(255, 255, 255))

    # 3. Speech Bubble Dialog Box (Center-Top)
    speaker_cfg = CHARACTERS[active_speaker]
    bx1, by1, bx2, by2 = 80, 240, W - 80, 560
    # Background card
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=28, fill=(15, 23, 42, 235), outline=speaker_cfg["bubble_border"], width=4)

    # Speaker Badge Pill
    badge_w, badge_h = 240, 50
    draw.rounded_rectangle([bx1 + 30, by1 - 25, bx1 + 30 + badge_w, by1 + 25], radius=25, fill=speaker_cfg["bg_badge"], outline=(255, 255, 255), width=2)
    b_font = get_font(FONT_ANTON, 28)
    b_bbox = b_font.getbbox(speaker_cfg["name"])
    draw.text((bx1 + 30 + (badge_w - (b_bbox[2] - b_bbox[0])) // 2, by1 - 25 + (badge_h - (b_bbox[3] - b_bbox[1])) // 2 - 2), speaker_cfg["name"], font=b_font, fill=(255, 255, 255))

    # Dialog Text
    text_font = get_font(FONT_BOLD, 42)
    lines = wrap_text(speech_text, text_font, max_width=bx2 - bx1 - 80)
    line_h = 52
    total_text_h = len(lines) * line_h
    start_y = by1 + (by2 - by1 - total_text_h) // 2 + 10

    for idx, line in enumerate(lines):
        line_bbox = text_font.getbbox(line)
        lw = line_bbox[2] - line_bbox[0]
        lx = bx1 + (bx2 - bx1 - lw) // 2
        ly = start_y + idx * line_h
        # Drop shadow
        draw.text((lx + 2, ly + 2), line, font=text_font, fill=(0, 0, 0, 200))
        draw.text((lx, ly), line, font=text_font, fill=(255, 255, 255, 255))

    # 4. Draw Characters (Bottom Section)
    bacon_img = Image.open(AVATAR_BACON).convert("RGBA")
    # Mirror bacon so he faces right towards Preppy
    bacon_img = ImageOps.mirror(bacon_img)
    preppy_img = Image.open(AVATAR_PREPPY).convert("RGBA")

    # Dynamic scaling: Active speaker is larger (540px), inactive is smaller (430px)
    bacon_is_active = (active_speaker == "bacon")
    bacon_h = 560 if bacon_is_active else 450
    bacon_w = int(bacon_img.width * (bacon_h / bacon_img.height))
    bacon_resized = bacon_img.resize((bacon_w, bacon_h), Image.Resampling.LANCZOS)

    preppy_is_active = (active_speaker == "preppy")
    preppy_h = 560 if preppy_is_active else 450
    preppy_w = int(preppy_img.width * (preppy_h / preppy_img.height))
    preppy_resized = preppy_img.resize((preppy_w, preppy_h), Image.Resampling.LANCZOS)

    # Inactive character opacity dim
    if not bacon_is_active:
        # Dim bacon to 65% opacity
        r, g, b, a = bacon_resized.split()
        a = a.point(lambda p: int(p * 0.65))
        bacon_resized = Image.merge("RGBA", (r, g, b, a))

    if not preppy_is_active:
        # Dim preppy to 65% opacity
        r, g, b, a = preppy_resized.split()
        a = a.point(lambda p: int(p * 0.65))
        preppy_resized = Image.merge("RGBA", (r, g, b, a))

    # Position avatars side-by-side on bottom stage
    bacon_x = 40
    bacon_y = H - bacon_h - 100
    base.alpha_composite(bacon_resized, (bacon_x, bacon_y))

    preppy_x = W - preppy_w - 40
    preppy_y = H - preppy_h - 100
    base.alpha_composite(preppy_resized, (preppy_x, preppy_y))

    # Speaking indicator glow rings
    if bacon_is_active:
        draw.ellipse([bacon_x + 120, H - 95, bacon_x + bacon_w - 120, H - 75], fill=(16, 185, 129, 140))
    if preppy_is_active:
        draw.ellipse([preppy_x + 120, H - 95, preppy_x + preppy_w - 120, H - 75], fill=(236, 72, 153, 140))

    base.save(out_frame_path, "PNG")
    return out_frame_path

def create_character_dialogue_video(dialogue_turns: list, output_mp4: str, bg_video: str = DEFAULT_BG):
    """
    Renders an entire character dialogue sequence:
    1. Generates speech for each turn
    2. Builds animated overlay per turn
    3. Renders segment clips with FFmpeg
    4. Concatenates into final Full HD Short
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_mp4)), exist_ok=True)
    temp_dir = os.path.join(os.path.dirname(output_mp4), "temp_dialogue")
    os.makedirs(temp_dir, exist_ok=True)

    segment_files = []

    print(f"🎬 Producing {len(dialogue_turns)} character dialogue turns...")

    for i, turn in enumerate(dialogue_turns):
        speaker = turn["speaker"]
        text = turn["text"]
        cfg = CHARACTERS[speaker]

        turn_audio = os.path.join(temp_dir, f"turn_{i}_{speaker}.mp3")
        turn_frame = os.path.join(temp_dir, f"frame_{i}_{speaker}.png")
        turn_video = os.path.join(temp_dir, f"segment_{i}.mp4")

        # 1. Voice
        print(f" [{i+1}/{len(dialogue_turns)}] Generating {cfg['name']} voice: '{text[:35]}...'")
        asyncio.run(render_tts_line(text, cfg["voice"], cfg["rate"], turn_audio))
        duration = get_audio_duration(turn_audio)

        # 2. Frame overlay
        render_dialogue_frame(speaker, text, turn_frame)

        # 3. Composite segment
        cmd = [
            FFMPEG_BIN, "-y",
            "-i", bg_video,
            "-i", turn_frame,
            "-i", turn_audio,
            "-filter_complex",
            "[0:v]loop=loop=-1:size=2:start=0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
            "[bg][1:v]overlay=0:0[outv]",
            "-map", "[outv]",
            "-map", "2:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "19",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-shortest",
            turn_video
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg segment {i} error: {res.stderr[-300:]}")
        segment_files.append(turn_video)

    # 4. Concatenate segments
    concat_list = os.path.join(temp_dir, "concat.txt")
    with open(concat_list, "w") as f:
        for seg in segment_files:
            f.write(f"file '{seg}'\n")

    print(f"🎬 Merging {len(segment_files)} dialogue scenes into final Short...")
    concat_cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        output_mp4
    ]
    res = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg concat error: {res.stderr[-300:]}")

    print(f"✅ SUCCESS! Created Character Dialogue Video: {output_mp4}")
    return output_mp4
