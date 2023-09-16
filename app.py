import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/',methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join("Data", "video.mp4"))
        import main
        main.extractAudio()
        return redirect(url_for('download'))
    return render_template('index.html')

@app.route('/download')
def download():
    folder_path = 'static/segments'
    images = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
    srtFilename = os.path.join(f"static/transcript/transcript.srt")
    with open(srtFilename, 'r') as f:
        subtitle_text = f.read()
    return render_template('download.html', images=images,subtitle_text=subtitle_text)

if __name__ == '__main__':
    app.run()
