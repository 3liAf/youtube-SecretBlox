"""
core/renderer.py - High-Retention Short Video Compositor
Composites background gameplay, dark cinematic vignettes, branded badges,
and styled bold captions into a finished 1080x1920 Short.
"""

import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

# Local bin path search
for p in ["/Users/aliaf/.local/bin", "/opt/homebrew/bin", "/usr/local/bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{p}:{os.environ.get('PATH', '')}"

FFMPEG_BIN = shutil.which("ffmpeg") or "/Users/aliaf/.local/bin/ffmpeg"
FFPROBE_BIN = shutil.which("ffprobe") or "/Users/aliaf/.local/bin/ffprobe"

def get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def get_media_duration(file_path: str) -> float:
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
        return 30.0

def generate_overlay_image(channel_name: str, font_path: str, out_overlay: str):
    """Draws top & bottom cinematic dark gradients and an eye-catching branded badge."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Gradients
    for y in range(450):
        alpha = int(160 * (1 - y / 450.0))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
    for y in range(H - 500, H):
        alpha = int(200 * ((y - (H - 500)) / 500.0))
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, alpha))
        
    # 2. Pill Badge
    pill_w, pill_h = 480, 80
    x1 = (W - pill_w) // 2
    y1 = 180
    x2 = x1 + pill_w
    y2 = y1 + pill_h
    
    draw.rounded_rectangle([x1, y1, x2, y2], radius=40, fill=(225, 29, 72, 235), outline=(255, 255, 255, 255), width=3)
    
    font = get_font(font_path, 40)
    text = f"🚨 {channel_name.upper()} 🚨"
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x1 + (pill_w - tw) // 2, y1 + (pill_h - th) // 2 - 4), text, font=font, fill=(255, 255, 255))
    
    os.makedirs(os.path.dirname(os.path.abspath(out_overlay)), exist_ok=True)
    img.save(out_overlay, "PNG")
    return out_overlay

def render_short_video(bg_video: str, overlay_img: str, audio_file: str, srt_file: str, out_video: str) -> str:
    """Invokes FFmpeg to composite the Full HD short video."""
    os.makedirs(os.path.dirname(os.path.abspath(out_video)), exist_ok=True)
    duration = get_media_duration(audio_file)
    total_duration = duration + 0.8
    
    # Subtitle styling with ASS filter: bright yellow (#00FFFF in BGR), thick black outline, centered
    sub_filter = (
        f"subtitles='{srt_file}':force_style='"
        "FontName=Anton,FontSize=26,Bold=1,PrimaryColour=&H0000FFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=3,Shadow=0,"
        "Alignment=2,MarginV=280'"
    )
    
    filter_complex = (
        f"[0:v]loop=loop=-1:size=2:start=0,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
        f"[bg][1:v]overlay=0:0[with_overlay];"
        f"[with_overlay]{sub_filter}[outv]"
    )
    
    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", "0", "-t", str(total_duration),
        "-i", bg_video,
        "-i", overlay_img,
        "-i", audio_file,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "2:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg render failed:\n{res.stderr[-400:]}")
        
    return out_video
