"""
core/tts.py - Multi-Language Neural Text-To-Speech Engine
Generates ultra-natural narration and word-level timestamps via Edge-TTS.
Supports English, German, Spanish, French, and automatic retries.
"""

import os
import asyncio
import edge_tts

async def generate_speech_async(text: str, output_audio: str, voice: str, rate: str = "+0%", max_retries: int = 3):
    """Generates audio file (.mp3) and subtitle file (.srt) with word boundaries."""
    os.makedirs(os.path.dirname(os.path.abspath(output_audio)), exist_ok=True)
    
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            submaker = edge_tts.SubMaker()
            
            with open(output_audio, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                        submaker.feed(chunk)
                        
            srt_path = os.path.splitext(output_audio)[0] + ".srt"
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(submaker.get_srt())
                
            return output_audio, srt_path
        except Exception as e:
            last_err = e
            print(f"[TTS] Attempt {attempt} failed ({e}), retrying in 1s...")
            await asyncio.sleep(1.0)
            
    raise RuntimeError(f"TTS generation failed after {max_retries} attempts: {last_err}")

def generate_speech(text: str, output_audio: str, voice: str, rate: str = "+0%"):
    """Synchronous entry point."""
    return asyncio.run(generate_speech_async(text, output_audio, voice, rate=rate))
