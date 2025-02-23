from flask import Flask, request, jsonify, send_file
import os
import yt_dlp
import tempfile

app = Flask(__name__)

@app.route("/")
def home():
    return "YouTube MP3 Downloader Server is Running!"

@app.route("/download", methods=["POST"])
def handle_download():
    """ Download and send the MP3 file directly to the user. """
    data = request.json
    youtube_url = data.get("url")

    if not youtube_url:
        return jsonify({"status": "error", "message": "No URL provided"}), 400

    try:
        # Create a temporary directory for the download
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

            # Send the MP3 file to the user
            return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
