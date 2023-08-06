import openai
import speech_recognition as sr
from jprint import jprint


def audio_data_to_wave(data, filename):
    if not filename.endswith(".wav"):
        raise ValueError("filename must be a *.wav file.")

    with open(filename, "wb") as f:
        f.write(data.get_wav_data())


def listen_to_mic(
    non_speaking_duration=0.75,
    pause_threshold=1.5,
    phrase_time_limit=8,
    recognize="whisper",
):
    print(f"listening to mic...")
    r = sr.Recognizer()
    r.non_speaking_duration = non_speaking_duration
    r.pause_threshold = pause_threshold
    with sr.Microphone() as source:
        # Added noise cancellation
        r.adjust_for_ambient_noise(source, duration=0.25)
        audio = r.listen(source, phrase_time_limit=phrase_time_limit)

        if recognize == "google":
            try:
                return r.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                print("Unable to recognize speech. Please try again.")
                return None
        elif recognize == "whisper":
            filename = "input.wav"
            audio_data_to_wave(audio, filename)
            with open(filename, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
                jprint(transcript)

            # Extract the transcribed text
            text = transcript.get("text")
            text.strip()
            if text.endswith("."):
                text = text[:-1]

            # whisper sometimes returns empty like ". . . ."
            valid_chars = [".", " "]
            if all(char in valid_chars for char in text):
                print("Invalid string returning None")
                return None
            return text
