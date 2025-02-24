import os
import sys
import urllib.request
import yt_dlp
import tempfile
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for your extension
CORS(app, origins=["chrome-extension://jemmamfoekigdclkfoghiabmnbmhglio", "https://ytmp3-ae81.onrender.com"])

# FFmpeg GitHub Release URL
FFMPEG_URL = "https://github.com/SMRPIPS/YTMP3/releases/download/v1.0.0/ffmpeg.exe"
FFMPEG_PATH = "./ffmpeg.exe"  # Save FFmpeg in the current directory

# Download FFmpeg if it's not already present
if not os.path.isfile(FFMPEG_PATH):
    print("Downloading FFmpeg from GitHub Release...")
    urllib.request.urlretrieve(FFMPEG_URL, FFMPEG_PATH)
    print("FFmpeg downloaded!")

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
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
                
                # Manually added cookies for authentication
                "cookie": {
                    '__Secure-1PAPISID': 'fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh',
                    '__Secure-1PSID': 'g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltyUnh-4c0zq0LhBYMoUCNUwACgYKAUoSARESFQHGX2Mi76v_v08Rkjch2DZzoF9yghoVAUF8yKpUASxVGYHAjdjhez1wNdSN0076',
                    '__Secure-1PSIDCC': 'AKEyXzXxZVDkxaOOKz5_Ze4FndN6vOWZJGtVac5ogRVTHPjnjoisd3DlUUtKbARFkGOXKd98-r0q',
                    '__Secure-1PSIDTS': 'sidts-CjEBEJ3XV5Y-LgjGjn0wnrRKnF3MIrdjRFHmeRbVFjYKAB4F28wINS1AD9Us0Zrhl9v8EAA',
                    '__Secure-3PAPISID': 'fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh',
                    '__Secure-3PSID': 'g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltiGIcZNfcGvSET1Uk3zN8hgACgYKAXQSARESFQHGX2MiD5Fd-CnEmlvy3VdufQGaRBoVAUF8yKqXoXMm7iD5rFLYrcsmMbsv0076',
                    '__Secure-3PSIDCC': 'AKEyXzUo13f1ow3lsQuY8HdY5iXFnu1Kfog_lGzPBoYWYjj781EG-TU4KfhVwwmPhkkmPNdL9tE',
                    '__Secure-3PSIDTS': 'sidts-CjEBEJ3XV5Y-LgjGjn0wnrRKnF3MIrdjRFHmeRbVFjYKAB4F28wINS1AD9Us0Zrhl9v8EAA',
                    '__Secure-YEC': 'CgtUNzBiN1FPRzFGWSjA77C4BjIKCgJHQhIEGgAgPA%3D%3D',
                    '_ga': 'GA1.1.20236561.1730022507',
                    '_ga_VCGEPY40VB': 'GS1.1.1730022507.1.1.1730022913.54.0.0',
                    'APISID': 'wx4sfcRll3RIEsXN/AmZ2-HOMT2nl63w1J',
                    'HSID': 'A_BbHeUv8bzRVQ_N2',
                    'LOGIN_INFO': 'AFmmF2swRQIhAK4UXJsQYSrbYRDfAaz6sLC6T-dtNfWKb9Dy34A9FYF1AiADUQT0ewab4c4u6l-uVKjV3M1bOwqgc7xIuUQn9RIxpw',
                    'NID': '518=hQ2stLJUIfNut696EYHwfKITa4Xk5eSqHJtLZIziNcR7rqbOC1Vi7mtjxLrY8mHNbZF1NNmOYd0aH7BqcMIsMkyPRH8bao20jLoUg4PSfyDxfRORguhiL4nzJnmNZvwQr4W1_MKET2okh46mA7axmI-7-6inTHlaVs13TwSpHy-T2Cr1Y1dke5lun1oStTu7LtKvqg2KqMy2Jl-m6-TLuRaM8HguI76KmfS3kAMwcnwjH5h3iA9Kblhvc8q7sUInDhwr9wg',
                    'PREF': 'f7=4100&tz=Europe.London&f6=400&f5=20000&repeat=NONE',
                    'SAPISID': 'fPmedbRnTKEzqx0V/AxQeiGrvqP2VJ-OTh',
                    'SID': 'g.a000uAgZs6_P8881lIKNFF0pOvr3INMTvbmKhYzEPw_L03b2_TltUbh_0Ip2jhsPJ6uNuBa-7AACgYKATQSARESFQHGX2MiPwYr7RJe-_fze2r5UT2tqRoVAUF8yKr2mLriZ379a66pxqQaz0iF0076',
                    'SIDCC': 'AKEyXzVS7F0wJCEXdojlOU6eeUk3ftdXPw7k4Ey434rN2xc3eoQHfCXENy-aS9Ym9nXZN9eraHRU',
                    'SSID': 'AwNWzvqTxI9qi-nSn'
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])

            return jsonify({"status": "success", "message": "Download started"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
