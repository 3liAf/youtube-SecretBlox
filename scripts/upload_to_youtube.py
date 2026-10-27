"""
scripts/upload_to_youtube.py - Multi-Channel YouTube OAuth2 Uploader
Supports per-language channel tokens (EN, DE, ES, FR).
"""

import os
import sys
import json
import argparse
import subprocess
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(ROOT_DIR, "config", "credentials")
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, "client_secret.json")

def get_token_file(lang: str = "en") -> str:
    lang_token = os.path.join(CREDENTIALS_DIR, f"youtube_token_{lang}.json")
    default_token = os.path.join(CREDENTIALS_DIR, "youtube_token.json")
    if os.path.exists(lang_token):
        return lang_token
    return default_token

def get_authenticated_service(lang: str = "en"):
    token_file = get_token_file(lang)
    
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"❌ Error: Missing Google OAuth client_secret.json at {CLIENT_SECRET_FILE}")
        sys.exit(1)

    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"Token read error ({e}). Re-authenticating...")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print(f"Refreshing expired YouTube token for [{lang.upper()}]...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Refresh failed ({e}). Re-authorizing...")
                creds = None

        if not creds:
            print(f"\n🔑 Initiating Google OAuth2 authorization for [{lang.upper()}] channel...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
            
            print(f"\nOpening browser for Google sign-in...")
            try:
                subprocess.run(["open", auth_url], check=False)
            except Exception:
                pass
                
            print("\nIf the browser did NOT open, please copy & paste this link:")
            print("-" * 65)
            print(auth_url)
            print("-" * 65 + "\n")
            
            creds = flow.run_local_server(port=8089, prompt="consent", open_browser=False)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
        print(f"Saved authenticated token to: {token_file}")

    return build("youtube", "v3", credentials=creds)

def upload_video(video_path: str, title: str, description: str, tags: list, lang: str = "en", privacy: str = "public"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    youtube = get_authenticated_service(lang)

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags[:30],
            "categoryId": "20"  # Gaming
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=1024*1024*4, resumable=True, mimetype="video/mp4")
    print(f"Uploading to YouTube [{lang.upper()}] channel ({privacy})...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    video_id = response.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"✅ Video published successfully! URL: {video_url}")
    return video_id, video_url

def main():
    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument("video_path", help="Path to video MP4")
    parser.add_argument("--meta", help="Path to metadata JSON")
    parser.add_argument("--lang", default="en", help="Language channel (en, de, es, fr)")
    parser.add_argument("--privacy", default="public", choices=["public", "unlisted", "private"])
    args = parser.parse_args()

    meta_data = {}
    meta_path = args.meta or os.path.splitext(args.video_path)[0] + "_meta.json"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta_data = json.load(f)

    title = meta_data.get("title", os.path.splitext(os.path.basename(args.video_path))[0])
    description = meta_data.get("description", "SecretBlox Roblox Short")
    tags = meta_data.get("tags", ["roblox", "secretblox", "shorts"])
    lang = meta_data.get("lang", args.lang)

    upload_video(args.video_path, title, description, tags, lang=lang, privacy=args.privacy)

if __name__ == "__main__":
    main()
