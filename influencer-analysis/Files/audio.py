# -*- coding: utf-8 -*-
"""
Created on Sun Jan  4 12:03:02 2026

@author: welcome-pc
"""

import yt_dlp
import os

# 🔹 Folder name
output_folder = "wav_audios"
os.makedirs(output_folder, exist_ok=True)

video_links = [
"https://youtube.com/shorts/brMLaEj9cEE",
"https://youtube.com/shorts/vjJ_nJ5b_RE",
"https://youtube.com/shorts/rbvObFG8AOo",
"https://youtube.com/shorts/hYZK0Cp1x4g",
"https://youtube.com/shorts/fWws53YY1uY",

"https://youtube.com/shorts/CsB0UrEKWYM",
"https://youtube.com/shorts/a6m0TahEPiY",
"https://youtube.com/shorts/cj4s8d3MaME",
"https://youtube.com/shorts/QqDLutjCLEI",
"https://youtube.com/shorts/oQW2cIl1cIY",

"https://youtube.com/shorts/nl5i1N44rZo",
"https://youtube.com/shorts/5jp05FnMo6c",
"https://youtube.com/shorts/i4hTCEEVQRQ",
"https://youtube.com/shorts/XPX6_xxamxA",
"https://youtube.com/shorts/9fhH8d-WZiE",

"https://youtube.com/shorts/MevIat4gh6I",
"https://youtube.com/shorts/ySS9gTzmXo4",
"https://youtube.com/shorts/eqSvPb6t4ig",
"https://youtube.com/shorts/qkY2tV0YmXk",
"https://youtube.com/shorts/NH7HN6flgZU",

"https://youtube.com/shorts/Y-wleOchRF4",
"https://youtube.com/shorts/klQSloSHCVU",
"https://youtube.com/shorts/8tCqAzTVkCg",
"https://youtube.com/shorts/v8EoWdgS0ME",
"https://youtube.com/shorts/jQh4OpDCgJ4",

"https://youtube.com/shorts/_tVc_95cSpQ",
"https://youtube.com/shorts/GGaWGFObOsg",
"https://youtube.com/shorts/WFOfEEv9LuE",
"https://youtube.com/shorts/UxRK5TjniE8",
"https://youtube.com/shorts/uQyOrGaOgm8",

"https://youtube.com/shorts/uEJoRyv72rM",
"https://youtube.com/shorts/zf1uAeqly5Y",
"https://youtube.com/shorts/96CusrSnA50",
"https://youtube.com/shorts/MvVznRSTIZo",
"https://youtube.com/shorts/kg1otbKteyU",

"https://youtube.com/shorts/TVIJoi09wcg",
"https://youtube.com/shorts/lb4_Ruxbze8",
"https://youtube.com/shorts/AFpd0-K2KEg",
"https://youtube.com/shorts/YC73rD2Ts64",
"https://youtube.com/shorts/1d-sMwgifb8",

"https://youtube.com/shorts/rm5kgrfuaLw",
"https://youtube.com/shorts/1H7cRW4RQsQ",
"https://youtube.com/shorts/1AOOx9Isr2Y",
"https://youtube.com/shorts/yRNZI7OXdQM",
"https://youtube.com/shorts/D-riz8tPtb8",

"https://youtube.com/shorts/uTf9VRGqOeM",
"https://youtube.com/shorts/fR9GBsfn4lQ",
"https://youtube.com/shorts/3huBh1eqBF8",
"https://youtube.com/shorts/wehefkkHtJk",
"https://youtube.com/shorts/HpwFUgPMgkc"
]

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(output_folder, 'temp_%(id)s.%(ext)s'),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav'
    }],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download(video_links)

# 🔁 Rename files as audio_1.wav, audio_2.wav...
wav_files = sorted([f for f in os.listdir(output_folder) if f.endswith(".wav")])

for i, filename in enumerate(wav_files, start=1):
    old_path = os.path.join(output_folder, filename)
    new_path = os.path.join(output_folder, f"audio_{i}.wav")
    os.rename(old_path, new_path)

print("🔥 All WAV files saved in one folder as audio_1.wav, audio_2.wav ...")
