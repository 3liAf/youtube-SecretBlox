"""
scripts/render_deadly_grass.py - Renders 3D In-Engine Roblox Machinima Short
Story: "In This World, Touching GRASS Deletes Your Account..."
Features:
- Real 3D scene rendered directly from Roblox Studio
- 3 dynamic cinematic camera angles (establishing, confrontation, low-angle)
- High-stakes dystopian rule narrative
- Popping yellow kinetic captions with black drop shadow
"""

import os
import sys
import shutil
import subprocess
import asyncio
import edge_tts

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG_BIN = shutil.which("ffmpeg") or "/Users/aliaf/.local/bin/ffmpeg"
FFPROBE_BIN = shutil.which("ffprobe") or "/Users/aliaf/.local/bin/ffprobe"

SCENE_DIR = os.path.join(ROOT_DIR, "assets", "scenes", "deadly_grass")
SHOT1 = os.path.join(SCENE_DIR, "shot1.jpg")
SHOT2 = os.path.join(SCENE_DIR, "shot2.jpg")
SHOT3 = os.path.join(SCENE_DIR, "shot3.jpg")

OUT_DIR = os.path.join(ROOT_DIR, "output", "deadly_grass")
FINAL_MP4 = os.path.join(OUT_DIR, "deadly_grass_story.mp4")

SCRIPT = (
    "In this world, touching grass doesn't just hurt you... it permanently deletes your entire Roblox account. "
    "For five years, everyone stayed strictly on concrete pavements. Concrete was safe, but lawns were forbidden death zones. "
    "At school today, the richest bully pushed me right to the sidewalk edge. He laughed, held my backpack over the lawn, and said: 'Touch the grass, or I drop your entire inventory.' "
    "I looked down, smiled, and whispered: 'You forgot one thing.' I activated my hover boots, grabbed his arm, and pushed HIM onto the lawn. "
    "His avatar started glitching... and within three seconds, his account vanished forever. "
    "Subscribe to SecretBlox if you would have pushed the bully into the grass!"
)

async def generate_voice(text: str, out_file: str):
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    comm = edge_tts.Communicate(text, "en-US-AndrewMultilingualNeural", rate="+8%")
    submaker = edge_tts.SubMaker()
    
    with open(out_file, "wb") as f:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)
                
    srt_path = os.path.splitext(out_file)[0] + ".srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())
    return out_file, srt_path

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
        return 32.0

def build_scene_clip(image_path: str, duration: float, out_clip: str, zoom_type: str = "in"):
    """Creates a 1080x1920 video clip with subtle cinematic camera movement from a 3D shot."""
    frames = int(duration * 30)
    
    # Zoom in or out filter
    if zoom_type == "in":
        z_expr = "min(zoom+0.0012,1.25)"
    else:
        z_expr = "max(1.2-0.001,1.0)"
        
    vf = (
        f"scale=1920:1080,zoompan=z='{z_expr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s=1080x1920:fps=30"
    )
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-loop", "1",
        "-i", image_path,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        out_clip
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return out_clip

def render():
    os.makedirs(OUT_DIR, exist_ok=True)
    audio_file = os.path.join(OUT_DIR, "narration.mp3")
    
    print("🎙️ Generating suspenseful narration with Andrew Neural...")
    asyncio.run(generate_voice(SCRIPT, audio_file))
    
    srt_file = os.path.splitext(audio_file)[0] + ".srt"
    total_dur = get_audio_duration(audio_file)
    print(f"🎬 Narration duration: {total_dur:.2f}s")
    
    # Divide duration across the 3 cinematic 3D shots
    d1 = total_dur * 0.35  # Establishing shot
    d2 = total_dur * 0.35  # Bully confrontation close-up
    d3 = total_dur - d1 - d2 + 0.5  # Low-angle dramatic revenge
    
    clip1 = os.path.join(OUT_DIR, "clip1.mp4")
    clip2 = os.path.join(OUT_DIR, "clip2.mp4")
    clip3 = os.path.join(OUT_DIR, "clip3.mp4")
    
    print("🎥 Rendering 3D Camera Shot 1 (Establishing)...")
    build_scene_clip(SHOT1, d1, clip1, zoom_type="in")
    
    print("🎥 Rendering 3D Camera Shot 2 (Confrontation)...")
    build_scene_clip(SHOT2, d2, clip2, zoom_type="out")
    
    print("🎥 Rendering 3D Camera Shot 3 (Dramatic Low-Angle)...")
    build_scene_clip(SHOT3, d3, clip3, zoom_type="in")
    
    # Concatenate clips
    concat_list = os.path.join(OUT_DIR, "concat.txt")
    with open(concat_list, "w") as f:
        f.write(f"file '{clip1}'\nfile '{clip2}'\nfile '{clip3}'\n")
        
    combined_video = os.path.join(OUT_DIR, "bg_combined.mp4")
    cmd_concat = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        combined_video
    ]
    subprocess.run(cmd_concat, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("✨ Applying Popping Yellow Subtitles and Sound Design...")
    # Exact style from viral screenshot: Bold yellow text, thick black outline, centered
    sub_filter = (
        f"subtitles='{srt_file}':force_style='"
        "FontName=Anton,FontSize=28,Bold=1,PrimaryColour=&H0000FFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=3.5,Shadow=1.5,"
        "Alignment=2,MarginV=360'"
    )
    
    cmd_final = [
        FFMPEG_BIN, "-y",
        "-i", combined_video,
        "-i", audio_file,
        "-filter_complex", f"[0:v]{sub_filter}[outv]",
        "-map", "[outv]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg final render failed: {res.stderr[-300:]}")
        
    print(f"🎉 SUCCESS! Rendered 3D In-Engine Short: {FINAL_MP4}")
    return FINAL_MP4

if __name__ == "__main__":
    render()
