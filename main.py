import datetime
import time
from flask import Flask, render_template, request, redirect, url_for
import ffmpeg
import subprocess
import gensim
import whisper
import os, sys, re
from datetime import timedelta
import pysrt
from gensim.summarization.summarizer import summarize

import app
import handler

raw_video = "Data/video.mp4"
model = whisper.load_model("base")
handler.renew_summary()

def extractAudio():
    print('Extracting Audio...')
    time.sleep(1)
    inputFile = raw_video
    fileName = "video-audio"
    fileType = "wav"

    command = ['ffmpeg', '-i', inputFile, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
               f'Data/{fileName}.{fileType}']
    subprocess.call(command)
    audio = "Data/video-audio.wav"
    transcribe(audio)

def transcribe(audio):
    print("Whisper model loaded.")
    print('Transcribing Audio...')
    time.sleep(1)
    transcribe = model.transcribe(audio,fp16=False)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"

        srtFilename = os.path.join(f"Data/subtitles.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)
    return summerize_transcript()

def summerize_transcript():
    # Load the SRT file and extract the text and timings
    print("Summarizing subtitles...")
    time.sleep(1)
    srt = pysrt.open('Data/subtitles.srt')
    # extract text only
    text = '\n'.join([subtitle.text for subtitle in srt])
    # array list of timestamps
    timings = [
        (subtitle.start.to_time().strftime('%H:%M:%S.%f')[:-3], subtitle.end.to_time().strftime('%H:%M:%S.%f')[:-3]) for
        subtitle in srt]

    # Clean and preprocess the text
    text = gensim.summarization.textcleaner.clean_text_by_sentences(text)
    text = '\n'.join([str(subtitle.text) for subtitle in srt])
    # Summarize the text
    summary = gensim.summarization.summarize(text, ratio=0.1)
    return extract_timestamps(summary)

def extract_timestamps(summary):
    print('Extracting Timestamps...')
    time.sleep(1)
    srt = pysrt.open('Data/subtitles.srt')
    time_stamps = []
    transcript_file = 'static/transcript/transcript.srt'
    with open(transcript_file, 'w') as f:
        for sub in srt:
          for line in summary.splitlines():
             if line in sub.text:
                ti1 = sub.start.to_time().strftime('%H:%M:%S.%f')[:-3]
                f.write(f"{ti1} --> {sub.text}'\n")
            # myStamps = [(sub.start.to_time(), sub.end.to_time())]
                time_stamps.append((sub.start.to_time().strftime('%H:%M:%S.%f')[:-3], sub.end.to_time().strftime('%H:%M:%S.%f')[:-3]))
    trim_SubClips(time_stamps)

def trim_SubClips(time_stamps):
    #keep same framerates
    print('Extracting subclips...')
    time.sleep(1)
    input_file = 'Data/video.mp4'
    sum = 0
    sub_clip_list = []
    for stamp in time_stamps:
        sum = sum + 1
        #calculate the duration of the subclip to generate
        start_time = datetime.datetime.strptime(stamp[0], '%H:%M:%S.%f')
        end_time = datetime.datetime.strptime(stamp[1], '%H:%M:%S.%f')
        duration = (end_time - start_time).total_seconds()
        start_time_str = start_time.strftime('%H:%M:%S.%f')[:-3]

        command = ['ffmpeg', '-ss', str(start_time_str), '-t', str(duration),'-i', input_file, '-c:v', 'copy', '-c:a',
                   'copy', f'Data/subclips/subclip{sum}.mov']
        command1 = ['ffmpeg', '-ss', str(start_time_str), '-i', input_file, '-vf', f'thumbnail,scale=640:-1',
                    '-frames:v', '1',
                    f'static/segments/segments{sum}.jpg']
        sub_clip_list.append(f'subclips/subclip{sum}.mov')
        subprocess.call(command)
        subprocess.call(command1)
    summarize_video(sub_clip_list)

def summarize_video(sub_clip_list):
    print('Merging Subclips...')
    time.sleep(1)
    concat_file = 'Data/input.txt'
    with open(concat_file, 'w') as f:
        for sub_clip in sub_clip_list:
            f.write(f"file '{sub_clip}'\n")
    output_file = 'static/output/summerised_video.mp4'
    if os.path.exists(output_file):
        os.remove(output_file)
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', output_file]
    subprocess.call(command)
    handler.remove_data()