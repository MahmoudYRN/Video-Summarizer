# Video-Summarizer
A video summarizer using openai's whisper and subtitles method
#imports 

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
