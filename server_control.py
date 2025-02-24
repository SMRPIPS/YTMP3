import os
import sys
import requests
import yt_dlp
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for Chrome Extension
CORS(app, origins=["chrome-extension://jemmamfoekigdclkfoghiabmnbmhglio", "https://ytmp3-ae81.onrender.com"])

# FFmpeg GitHub Release URL
FFMPEG_URL = "https://github.com/SMRPIPS/YTMP3/releases/download/v1.0.0/ffmpeg.exe"
FFMPEG_PATH = "./ffmpeg.exe"  # Path where FFmpeg should be saved

# Function to download FFmpeg if missing
def download_ffmpeg():
    if not os.path.isfile(FFMPEG_PATH):
        try:
            print("Downloading FFmpeg from GitHub Release...")
            
            # Use requests to handle redirects
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
            print("Ensure the URL is correct and the file exists in the GitHub Release.")
            sys.exit(1)  # Stop the server if FFmpeg download fails

# Check and download FFmpeg
download_ffmpeg()

@app.route("/download", methods=["POST"])
def handle_download():
    """ Download and convert YouTube video to MP3. """
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
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            return jsonify({"status": "success", "message": "Download started"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
