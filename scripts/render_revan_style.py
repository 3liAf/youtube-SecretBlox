"""
channels/secretblox/render_revan_style.py - Revan-Style Roblox Story Video Engine
Renders a high-retention Short matching the exact style of @RevanRants:
- Authentic vertical Roblox gameplay background
- Deep, suspenseful storytelling voice
- Centered, high-contrast dynamic subtitle phrasing
- No clunky 2D stickers or fake cardboard cutouts
"""

import os
import sys
import shutil
import subprocess
import asyncio
import edge_tts

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

FFMPEG_BIN = shutil.which("ffmpeg") or "/Users/aliaf/.local/bin/ffmpeg"
FFPROBE_BIN = shutil.which("ffprobe") or "/Users/aliaf/.local/bin/ffprobe"

BG_GAMEPLAY = "/Users/aliaf/youtube-SecretBlox/assets/backgrounds/roblox_gameplay_dark.mp4"
OUTPUT_DIR = "/Users/aliaf/youtube-SecretBlox/output/revan_style"

STORY = {
    "title": "The Rule You Must NEVER Break in Roblox #shorts",
    "voice": "en-US-AndrewMultilingualNeural",
    "rate": "+8%",
    "text": (
        "In this school, there is only one rule: never open the janitor's closet after 3 PM. "
        "Everyone thought it was just a stupid legend... until Jake decided to test it. "
        "He picked the lock and stepped inside, but instead of brooms, there was an elevator leading deep underground. "
        "At the bottom was a dark server room with a single glowing monitor. "
        "And on the screen, a message appeared: 'Welcome Jake. Your account will be permanently deleted in five seconds.' "
        "He tried to turn around, but the doors had completely vanished. "
        "Subscribe to SecretBlox if you would have opened that door!"
    )
}

async def generate_speech_and_srt(text: str, voice: str, rate: str, out_audio: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_audio)), exist_ok=True)
    comm = edge_tts.Communicate(text, voice, rate=rate)
    submaker = edge_tts.SubMaker()
    
    with open(out_audio, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)
                
    srt_path = os.path.splitext(out_audio)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())
    return out_audio, srt_path

def get_duration(file_path: str) -> float:
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
        return 28.0

def render():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    audio_path = os.path.join(OUTPUT_DIR, "story_audio.mp3")
    final_output = os.path.join(OUTPUT_DIR, "the_secret_rule_short.mp4")
    
    print("🎙️ Generating suspenseful narration with Andrew Neural...")
    asyncio.run(generate_speech_and_srt(STORY["text"], STORY["voice"], STORY["rate"], audio_path))
    
    srt_path = os.path.splitext(audio_path)[0] + ".srt"
    duration = get_duration(audio_path)
    total_duration = duration + 0.5
    print(f"🎬 Narration duration: {duration:.2f}s. Compositing onto authentic Roblox gameplay...")
    
    # Format subtitles like Revan:
    # Font Anton, clean bright white, thick black border, placed in lower-center
    sub_filter = (
        f"subtitles='{srt_path}':force_style='"
        "FontName=Anton,FontSize=26,Bold=1,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=3.5,Shadow=1.5,"
        "Alignment=2,MarginV=380'"
    )
    
    # Scale gameplay to fill 1080x1920 with high-contrast slight vignette
    filter_complex = (
        f"[0:v]loop=loop=-1:size=2:start=0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
        f"[bg]{sub_filter}[outv]"
    )
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", "0", "-t", str(total_duration),
        "-i", BG_GAMEPLAY,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render error: {res.stderr[-300:]}")
        
    print(f"✅ SUCCESS! Rendered Revan-Style Short: {final_output}")
    return final_output

if __name__ == "__main__":
    render()
