import os
import glob

def remove_data():
    files = glob.glob('Data/subclips/*')
    try:
        for f in files:
            os.remove(f)
        os.remove('Data/video-audio.wav')
        os.remove(f'Data/input.txt')
        os.remove(f'Data/subtitles.srt')
    except:
        print("file doesnt exists")

def renew_summary():
    files = glob.glob('static/segments/*')
    try:
        for f in files:
            os.remove(f)
        os.remove(f'static/transcript/transcript.srt')
    except:
        print("file doesnt exists")
