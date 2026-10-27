"""
scripts/render.py - Command Line Video Generator
Renders individual stories or batch processes across all 4 languages.
Usage:
    python3 scripts/render.py --story secret_room_brookhaven --lang en
    python3 scripts/render.py --story secret_room_brookhaven --lang all
    python3 scripts/render.py --all
"""

import os
import sys
import json
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from config.languages import LANGUAGES
from core.tts import generate_speech
from core.renderer import generate_overlay_image, render_short_video

DATA_FILE = os.path.join(ROOT_DIR, "data", "stories.json")
OUTPUT_BASE = os.path.join(ROOT_DIR, "output")
FONT_TITLE = os.path.join(ROOT_DIR, "assets", "fonts", "Anton-Regular.ttf")
DEFAULT_BG = os.path.join(ROOT_DIR, "assets", "backgrounds", "satisfying_bg.mp4")

def load_stories():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def render_story_lang(story: dict, lang: str, bg_video: str = DEFAULT_BG):
    if lang not in LANGUAGES:
        print(f"Error: Unknown language {lang}")
        return None
        
    cfg = LANGUAGES[lang]
    if lang not in story:
        print(f"Error: Story {story.get('id')} has no translation for {lang}")
        return None
        
    story_id = story["id"]
    data = story[lang]
    full_script = f"{data['hook']} {data['body']} {data['cta']}"
    
    out_dir = os.path.join(OUTPUT_BASE, lang, story_id)
    os.makedirs(out_dir, exist_ok=True)
    
    audio_path = os.path.join(out_dir, "narration.mp3")
    overlay_path = os.path.join(out_dir, "overlay.png")
    final_video = os.path.join(out_dir, f"{story_id}_{lang}.mp4")
    meta_json = os.path.join(out_dir, f"{story_id}_{lang}_meta.json")
    
    print(f"[{lang.upper()}] 🎙️  Generating narration ({cfg['voice']})...")
    _, srt_path = generate_speech(full_script, audio_path, cfg["voice"], cfg["voice_rate"])
    
    print(f"[{lang.upper()}] 🎨 Generating branding badge ({cfg['channel_name']})...")
    generate_overlay_image(cfg["channel_name"], FONT_TITLE, overlay_path)
    
    print(f"[{lang.upper()}] 🎬 Compositing 1080x1920 Short video...")
    render_short_video(bg_video, overlay_path, audio_path, srt_path, final_video)
    
    # Save metadata for YouTube uploader
    meta_data = {
        "id": story_id,
        "lang": lang,
        "channel_name": cfg["channel_name"],
        "title": f"{data['title']} 🚨 #shorts",
        "description": f"{data['hook']}\n\n{data['body']}\n\n{cfg['cta_template'].format(keyword=data['keyword'])}\n\n" + " ".join(cfg["default_tags"]),
        "tags": [t.replace("#", "") for t in cfg["default_tags"]],
        "video_path": final_video
    }
    with open(meta_json, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2, ensure_ascii=False)
        
    print(f"[{lang.upper()}] ✅ Done: {final_video}")
    return final_video

def main():
    parser = argparse.ArgumentParser(description="SecretBlox Short Video Generator")
    parser.add_argument("--story", default="secret_room_brookhaven", help="Story ID to render")
    parser.add_argument("--lang", default="en", help="Language code (en, de, es, fr, or all)")
    parser.add_argument("--all", action="store_true", help="Render all stories in all languages")
    parser.add_argument("--bg", default=DEFAULT_BG, help="Custom vertical background video path")
    args = parser.parse_args()
    
    stories = load_stories()
    
    if args.all:
        print("🚀 Rendering ALL stories in ALL languages...")
        for s in stories:
            for l in LANGUAGES.keys():
                render_story_lang(s, l, args.bg)
    else:
        story = next((s for s in stories if s["id"] == args.story), None)
        if not story:
            print(f"Story {args.story} not found. Available stories:")
            for s in stories:
                print(f" - {s['id']}")
            sys.exit(1)
            
        if args.lang == "all":
            for l in LANGUAGES.keys():
                render_story_lang(story, l, args.bg)
        else:
            render_story_lang(story, args.lang, args.bg)

if __name__ == "__main__":
    main()
