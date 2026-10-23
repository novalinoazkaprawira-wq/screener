import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

def list_recordings():
    files = []
    if os.path.exists(RECORDINGS_DIR):
        for name in os.listdir(RECORDINGS_DIR):
            if name.lower().endswith((".mp4", ".webm", ".mkv")):
                path = os.path.join(RECORDINGS_DIR, name)
                stat = os.stat(path)
                files.append({
                    "name": name,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "mtime_str": "Recently added",
                })
    return files

@app.route("/")
def index():
    return render_template("index.html", recordings=list_recordings())

@app.route("/video/<path:filename>")
def video(filename):
    return send_from_directory(RECORDINGS_DIR, filename, conditional=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
