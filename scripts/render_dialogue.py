"""
scripts/render_dialogue.py - Test Runner for Character Dialogue Short
Renders a complete 2-character drama Short with Bacon vs Preppy.
"""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.dialogue_engine import create_character_dialogue_video

DEMO_STORY = [
    {
        "speaker": "preppy",
        "text": "Ew! Look at that poor Bacon Hair! You can not even afford ten Robux!"
    },
    {
        "speaker": "bacon",
        "text": "I might be broke, but at least I know the secret passcode to your Brookhaven mansion..."
    },
    {
        "speaker": "preppy",
        "text": "Wait... what?! You are lying! How could a noob like you ever know that?!"
    },
    {
        "speaker": "bacon",
        "text": "Go check your mansion safe right now. It is completely empty."
    },
    {
        "speaker": "preppy",
        "text": "NO WAY! WHAT DID YOU DO WITH MY ROBUX?!"
    },
    {
        "speaker": "bacon",
        "text": "Subscribe to SecretBlox to see where I hid them!"
    }
]

if __name__ == "__main__":
    out_file = os.path.join(ROOT_DIR, "output", "dialogue_shorts", "bacon_vs_preppy_ep1.mp4")
    create_character_dialogue_video(DEMO_STORY, out_file)
