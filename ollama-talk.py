import requests
import json
import pyttsx3
import pyaudio
from vosk import Model, KaldiRecognizer
import os
from datetime import datetime

OLLAMA_API_BASE = "http://localhost:11434/api"

def chat_with_ollama(prompt):
    url = f"{OLLAMA_API_BASE}/generate"
    data = {
        "model": "tinydolphin:latest",
        "prompt": prompt,
        "stream": True
    }
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    json_response = json.loads(decoded_line)
                    if 'response' in json_response:
                        full_response += json_response['response']
                    if json_response.get('done', False):
                        break
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON: {decoded_line}")

        return full_response.strip()
    except requests.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I couldn't get a response from Ollama."

def chat_with_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Available voices:")
    for i, voice in enumerate(voices):
        print(f"{i+1}. ID: {voice.id}, Name: {voice.name}")
    voice_choice = int(input("Enter the number of the voice you want to use: "))
    engine.setProperty('voice', voices[voice_choice-1].id)

    model = Model(model_path="vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)

    if not os.path.exists("history"):
        os.makedirs("history")

    chat_log_file = None
    current_datetime = None

    while True:
        try:
            data = stream.read(4000)
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                user_input = result['text']

                if user_input:
                    if not chat_log_file:
                        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        chat_log_file = open(f"history/chat_log_{current_datetime}.html", "w")
                        chat_log_file.write("""
                        <html>
                        <head>
                            <title>Chat Log</title>
                            <style>
                                body {
                                    font-family: Arial, sans-serif;
                                    background-color: #f0f0f0;
                                }
                                .user-input {
                                    color: #007bff;
                                }
                                .ai-response {
                                    color: #28a745;
                                }
                                .timestamp {
                                    font-size: 0.8em;
                                    color: #666;
                                }
                            </style>
                        </head>
                        <body>
                        """)

                    print(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} You said: {user_input}")
                    chat_log_file.write(f"<p class='timestamp'>{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}</p><p class='user-input'>You said: {user_input}</p>\n")
                    chat_log_file.flush()

                    if user_input.lower() == 'quit':
                        print("Exiting...")
                        break

                    ai_response = chat_with_ollama(user_input)
                    print(f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')} AI: {ai_response}")
                    chat_log_file.write(f"<p class='timestamp'>{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}</p><p class='ai-response'>AI: {ai_response}</p>\n")
                    chat_log_file.flush()

                    engine.say(ai_response)
                    engine.runAndWait()

        except OSError as e:
            print(f"Error: {e}")
            continue

    chat_log_file.write("</body></html>")
    chat_log_file.close()

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    chat_with_voice()

