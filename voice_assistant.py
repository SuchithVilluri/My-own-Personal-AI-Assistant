import sounddevice as sd
import json
import requests
import os
from vosk import Model, KaldiRecognizer

# ---------------- TTS (Windows native - guaranteed) ----------------
def speak(text):
    print("Jarvis:", text)
    safe_text = text.replace('"', '').replace("'", "")
    command = (
        'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\\"{safe_text}\\")"'
    )
    os.system(command)

# ---------------- STT SETUP ----------------
model = Model("vosk-model")   # folder must exist in project directory
recognizer = KaldiRecognizer(model, 16000)

def listen():
    print("Listening...")

    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype='int16'
    ) as stream:
        while True:
            data, _ = stream.read(4000)
            data_bytes = data.tobytes()

            if recognizer.AcceptWaveform(data_bytes):
                result = json.loads(recognizer.Result())
                return result.get("text", "")

# ---------------- BACKEND ----------------
def ask_backend(question):
    res = requests.post(
        "http://localhost:8000/chat",
        json={"question": question},
        timeout=60
    )
    return res.json()["answer"]

# ---------------- MAIN LOOP ----------------
if __name__ == "__main__":
    speak("Jarvis is online.")

    while True:
        text = listen()

        if text:
            print("You:", text)

            if "exit" in text.lower():
                speak("Goodbye.")
                break

            answer = ask_backend(text)
            speak(answer)
