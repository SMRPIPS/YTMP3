import os
import sys
import requests
import yt_dlp
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["chrome-extension://jemmamfoekigdclkfoghiabmnbmhglio", "https://ytmp3-ae81.onrender.com"])

# 🔹 FFmpeg GitHub Release URL
FFMPEG_URL = "https://github.com/SMRPIPS/YTMP3/releases/download/v1.0.0/ffmpeg.exe"
FFMPEG_PATH = "./ffmpeg.exe"

# 🔹 Manually add cookies from **EditThisCookie**
YOUTUBE_COOKIES = "PREF=f7=100; VISITOR_INFO1_LIVE=XX1234abc; YSC=abc123;"  # Replace with your real cookies

# 🔹 User-Agent (Mimics a real browser)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": YOUTUBE_COOKIES,
}

# 🔹 Step 1: Auto-Update yt-dlp
def update_yt_dlp():
    os.system("pip install --upgrade yt-dlp")

# 🔹 Step 2: Download FFmpeg if missing
def download_ffmpeg():
    if not os.path.isfile(FFMPEG_PATH):
        try:
            print("Downloading FFmpeg from GitHub Release...")
            response = requests.get(FFMPEG_URL, stream=True, allow_redirects=True)
            
            if response.status_code == 200:
                with open(FFMPEG_PATH, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                print("FFmpeg downloaded successfully!")
            else:
                raise Exception(f"Failed to download FFmpeg. HTTP Status: {response.status_code}")
        except Exception as e:
            print(f"Error downloading FFmpeg: {e}")
            sys.exit(1)

# 🔹 Run updates on startup
update_yt_dlp()
download_ffmpeg()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Server is running!"}), 200

@app.route("/download", methods=["POST"])
def handle_download():
    data = request.json
    youtube_url = data.get("url")

    if not youtube_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                "ffmpeg_location": FFMPEG_PATH,
                "noplaylist": True,
                "cookie": YOUTUBE_COOKIES,  # Pass cookies
                "http_headers": HEADERS,  # Pass headers
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            return jsonify({"status": "success", "message": "Download started"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
