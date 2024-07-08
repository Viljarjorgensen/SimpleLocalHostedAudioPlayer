from flask import Flask, render_template, request, redirect, url_for, flash
from pygame import mixer
import time
import threading
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
mixer.init()

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('hello'))
    file = request.files['file']
    if file.filename == "":
        flash('No selected file')
        return redirect(url_for('hello'))

    # Check file extension
    if not (file.filename.endswith('.mp3') or file.filename.endswith('.wav')):
        flash('Invalid file type. Please upload an MP3 or WAV file.')
        return redirect(url_for('hello'))

    file.save("uploaded_audio" + os.path.splitext(file.filename)[1])
    threading.Thread(target=play_audio).start()
    return redirect(url_for('playing'))

def play_audio():
    mixer.music.load("uploaded_audio.mp3" if os.path.exists("uploaded_audio.mp3") else "uploaded_audio.wav")
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)

@app.route('/playing')
def playing():
    return render_template("playing.html")

@app.route('/pause', methods=['POST'])
def pause():
    mixer.music.pause()
    return 'paused'

@app.route('/unpause', methods=['POST'])
def unpause():
    mixer.music.unpause()
    return 'unpaused'

@app.route('/stop', methods=['POST'])
def stop():
    mixer.music.stop()
    return 'stopped'

if __name__ == "__main__":
    app.run(debug=True)
