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

# Hardcoded Cookies (Replace with your cookies in JSON format)
COOKIES = {
    "__Secure-1PAPISID": "fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh",
    "__Secure-1PSID": "g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltyUnh-4c0zq0LhBYMoUCNUwACgYKAUoSARESFQHGX2Mi76v_v08Rkjch2DZzoF9yghoVAUF8yKpUASxVGYHAjdjhez1wNdSN0076",
    "__Secure-1PSIDCC": "AKEyXzVDWO_Bggn8KQFM61-On_PKsu3FpO38_DaJ-2Pq8HpLajt9TaO1ka0q79lFb2isireFuSmS",
    "__Secure-1PSIDTS": "sidts-CjEBEJ3XV1rVt_lEslydKTAS2bnFezMWJVJlbMkGxK8ZQB3JyI6-BQtY_GhQvz2c2gwQEAA",
    "__Secure-3PAPISID": "fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh",
    "__Secure-3PSID": "g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltiGIcZNfcGvSET1Uk3zN8hgACgYKAXQSARESFQHGX2MiD5Fd-CnEmlvy3VdufQGaRBoVAUF8yKqXoXMm7iD5rFLYrcsmMbsv0076",
    "__Secure-3PSIDCC": "AKEyXzX4Hd83-OLkT9nhqjOR9E8ra0YFozQ_P4XFAl4tODJIbZw_hKKZRn92UQzYLT44JTAh9xc",
    "__Secure-3PSIDTS": "sidts-CjEBEJ3XV1rVt_lEslydKTAS2bnFezMWJVJlbMkGxK8ZQB3JyI6-BQtY_GhQvz2c2gwQEAA",
    "__Secure-YEC": "CgtUNzBiN1FPRzFGWSjA77C4BjIKCgJHQhIEGgAgPA%3D%3D",
    "_ga": "GA1.1.20236561.1730022507",
    "_ga_VCGEPY40VB": "GS1.1.1730022507.1.1.1730022913.54.0.0",
    "APISID": "wx4sfcRll3RIEsXN/AmZ2-HOMT2nl63w1J",
    "HSID": "A_BbHeUv8bzRVQ_N2",
    "LOGIN_INFO": "AFmmF2swRQIhAK4UXJsQYSrbYRDfAaz6sLC6T-dtNfWKb9Dy34A9FYF1AiADUQT0ewab4c4u6l-uVKjV3M1bOwqgc7xIuUQn9RIxpw:QUQ3MjNmd0YxOVJESW9mR2UyWlZ3N3JxSnE3dGs4RDZ0V2xBNFBrM0Ezd3drZHEzSDRXa2xydHRFZm4xWkNTZTNxYVVOT2d5aVdVdlRSWWpKR01nY1NpUzF4RFplQ3prMi03MWpfM3FFYkVwdEhnTEY0djFncU54MFVyOFA2d1o1VUU4UjZYeDdrZFFyZlNXaTRLYTBIUG5JUmVRQmM0ejBvQzJUMkZ2Ynd2TE5LVkNHRmV5ckRIVlhGMDBBSkFLOUpQeTNXQnA0ZUphYWNmc21Sd3JEQm5UVGpCNkRFOGdvdw==",
    "NID": "518=hQ2stLJUIfNut696EYHwfKITa4Xk5eSqHJtLZIziNcR7rqbOC1Vi7mtjxLrY8mHNbZF1NNmOYd0aH7BqcMIsMkyPRH8bao20jLoUg4PSfyDxfRORguhiL4nzJnmNZvwQr4W1_MKET2okh46mA7axmI-7-6inTHlaVs13TwSpHy-T2Cr1Y1dke5lun1oStTu7LtKvqg2KqMy2Jl-m6-TLuRaM8HguI76KmfS3kAMwcnwjH5h3iA9Kblhvc8q7sUInDhwr9wg",
    "PREF": "f7=4100&tz=Europe.London&f6=400&f5=20000&repeat=NONE",
    "SAPISID": "fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh",
    "SID": "g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltUbh_0Ip2jhsPJ6uNuBa-7AACgYKATQSARESFQHGX2MiPwYr7RJe-_fze2r5UT2tqRoVAUF8yKr2mLriZ379a66pxqQaz0iF0076",
    "SIDCC": "AKEyXzX8XT_-BiQ9z_fYRRMZ2X4Wu3KYlHZJ_N1vIpBacgYw8VnnDTwBZx3tU1wfdtGHnh1REGtG",
    "SSID": "AwNWzvqTxI9qi-nSn"
}

# Function to download FFmpeg if missing
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
            sys.exit(1)  # Stop the server if FFmpeg download fails

# Check and download FFmpeg
download_ffmpeg()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "Server is running!"}), 200

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
                "ffmpeg_location": FFMPEG_PATH,  # Use the downloaded FFmpeg
                "cookies": COOKIES,  # Pass cookies directly (instead of cookies.txt)
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            return jsonify({"status": "success", "message": "Download started"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
