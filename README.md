# 🚨 SecretBlox — Multi-Language Automated Roblox Shorts Engine

> An automated content pipeline generating high-retention Roblox mystery, secret, and story Shorts across 4 high-CPM languages: **English**, **German**, **Spanish**, and **French**.

---

## 🌟 Channel Network

| Channel | Language | Target Audience | CPM Potential | Voice Engine |
| :--- | :--- | :--- | :--- | :--- |
| **SecretBlox** | English (`en`) | US, UK, CA, AU | $4.00 – $8.00+ | `en-US-AndrewMultilingualNeural` |
| **SecretBlox Deutsch** | German (`de`) | Germany, Austria, Switzerland | $5.00 – $12.00+ | `de-DE-FlorianMultilingualNeural` |
| **SecretBlox Español** | Spanish (`es`) | Mexico, Spain, Argentina, LATAM | Viral Scale + Tier 1 Spain | `es-MX-JorgeNeural` |
| **SecretBlox Français** | French (`fr`) | France, Belgium, Canada, Switzerland | $4.00 – $8.00+ | `fr-FR-RemyMultilingualNeural` |

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.9+
- [FFmpeg](https://ffmpeg.org/) installed and available in PATH.

### 2. Setup
```bash
git clone https://github.com/3liAf/youtube-SecretBlox.git
cd youtube-SecretBlox

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🎬 Generating Videos

Render any story from `data/stories.json`:

```bash
# Render single story in English:
python3 scripts/render.py --story secret_room_brookhaven --lang en

# Render single story in German:
python3 scripts/render.py --story secret_room_brookhaven --lang de

# Render single story across ALL 4 languages at once:
python3 scripts/render.py --story secret_room_brookhaven --lang all

# Render the entire story catalog in all languages:
python3 scripts/render.py --all
```

Rendered outputs are saved to `output/<lang>/<story_id>/` in **Full HD 1080x1920 (Vertical Short)** format with:
- Word-synced animated high-contrast yellow subtitles
- Top branded pill badge (`🚨 SECRETBLOX 🚨`)
- Cinematic vignette & dark contrast gradients
- Companion `<story_id>_<lang>_meta.json` containing title, description, and hashtags.

---

## 📤 Uploading to YouTube

### 1. Add your OAuth credentials
Place your Google Cloud OAuth 2.0 Desktop credentials in:
```
config/credentials/client_secret.json
```
*(Reference `config/credentials/client_secret.example.json` for format).*

### 2. Upload a video
```bash
# Upload to English channel:
python3 scripts/upload_to_youtube.py output/en/secret_room_brookhaven/secret_room_brookhaven_en.mp4 --lang en

# Upload to German channel:
python3 scripts/upload_to_youtube.py output/de/secret_room_brookhaven/secret_room_brookhaven_de.mp4 --lang de

# Upload to Spanish channel:
python3 scripts/upload_to_youtube.py output/es/secret_room_brookhaven/secret_room_brookhaven_es.mp4 --lang es

# Upload to French channel:
python3 scripts/upload_to_youtube.py output/fr/secret_room_brookhaven/secret_room_brookhaven_fr.mp4 --lang fr
```
*On first upload for each language, a browser window will open asking you to sign in to that language's YouTube channel. The token will be saved automatically to `config/credentials/youtube_token_<lang>.json`.*

---

## ⏰ Optimal Upload Windows

| Channel | Timezone | Slot 1 | Slot 2 |
| :--- | :--- | :--- | :--- |
| **English** | EST (US Eastern) | 2:30 PM EST | 7:00 PM EST |
| **German** | CET (Central Europe) | 15:30 CET | 19:30 CET |
| **Spanish** | CST (Mexico / LATAM) | 1:00 PM CST | 6:30 PM CST |
| **French** | CET (France) | 16:00 CET | 20:00 CET |

---

## 🎮 Roblox Game Conversion Roadmap

When you are ready to launch your own Roblox game:
1. Frame the video as an unsolved mystery or challenge: *"I found an unreleased game with only 5 players... and it's terrifying"*
2. Direct viewers to the pinned comment and bio: *"Game link is in pinned comment. Can you beat stage 10?"*
3. Because your audience is already hooked on exploring secret games, they will instantly convert into active players.

---

## 📜 License
MIT License
