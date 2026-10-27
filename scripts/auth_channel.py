"""
scripts/auth_channel.py - Authenticate YouTube Channels
Launches OAuth2 authorization flow and opens the browser on macOS.
Saves token to config/credentials/youtube_token_<lang>.json
"""

import os
import sys
import argparse
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_DIR = os.path.join(ROOT_DIR, "config", "credentials")
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, "client_secret.json")

def authenticate(lang: str = "en"):
    if not os.path.exists(CLIENT_SECRET_FILE):
        print(f"❌ Error: Missing {CLIENT_SECRET_FILE}")
        sys.exit(1)

    token_file = os.path.join(CREDENTIALS_DIR, f"youtube_token_{lang}.json")
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    
    # Generate auth URL
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    
    print("\n" + "=" * 65)
    print(f"🔑 AUTHENTICATING YOUTUBE CHANNEL FOR: [{lang.upper()}]")
    print("=" * 65)
    print("\nOpening your default browser now...")
    
    # Force open on macOS
    try:
        subprocess.run(["open", auth_url], check=False)
    except Exception:
        pass
        
    print("\nIf the browser did NOT open automatically, copy & open this link:")
    print("-" * 65)
    print(auth_url)
    print("-" * 65 + "\n")
    print("Waiting for you to complete sign-in in your browser...")
    
    creds = flow.run_local_server(port=8089, prompt="consent", open_browser=False)
    
    with open(token_file, "w") as f:
        f.write(creds.to_json())
        
    print(f"\n✅ SUCCESS! Token saved to: {token_file}")
    return token_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Authenticate YouTube Channel")
    parser.add_argument("--lang", default="en", choices=["en", "de", "es", "fr"], help="Channel language")
    args = parser.parse_args()
    authenticate(args.lang)
