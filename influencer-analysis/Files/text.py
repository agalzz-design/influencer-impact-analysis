# -*- coding: utf-8 -*-
"""
Speech to Text using Whisper (Windows + CPU Safe)
Author: agals 
"""

import os
import shutil
import whisper
import pandas as pd

# ================= PATH CONFIG =================
AUDIO_FILE = r"C:\Users\welcome-pc\wav_audios\audio_10.wav"
OUTPUT_FILE = "speech_text_output.csv"

# ================= FFMPEG CHECK =================
print("Checking ffmpeg...")
if not shutil.which("ffmpeg"):
    raise RuntimeError(
        "FFMPEG not found!\n"
        "Download from https://www.gyan.dev/ffmpeg/builds/\n"
        " Add C:\\ffmpeg\\bin to PATH"
    )
print(" ffmpeg found")

# ================= FILE CHECK =================
if not os.path.isfile(AUDIO_FILE):
    raise FileNotFoundError(f" Audio file not found: {AUDIO_FILE}")

# ================= LOAD WHISPER MODEL =================
print("Loading Whisper model...")
model = whisper.load_model("medium")   # CPU friendly
print("Whisper model loaded")

# ================= TRANSCRIBE =================
print(f"Processing: {os.path.basename(AUDIO_FILE)}")

result = model.transcribe(
    AUDIO_FILE,
    language="ta",     # Tamil dominant
    fp16=False         # MUST for CPU / Windows
)

speech_text = result["text"].strip()

# ================= SAVE OUTPUT =================
df = pd.DataFrame([{
    "audio_file": os.path.basename(AUDIO_FILE),
    "speech_text": speech_text
}])

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

print("✅ Speech-to-text completed 🎉")
print(df.head())
