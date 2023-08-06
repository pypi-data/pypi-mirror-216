#!/usr/bin/env python

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

dir_name = "audio_files/"
files = os.listdir(dir_name)

files = sorted(files, key=lambda x: int(x.split("-")[1].split(".")[0]))
# print(files)
# input()
for file in files:
    audio_file = open(f"{dir_name}{file}", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript.get("text"))
