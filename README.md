# Ollama Talk

Ollama Talk is a resource-efficient Python application that allows you to have a voice conversation with an AI model using Ollama. It uses speech recognition to convert your voice input into text, sends it to Ollama for processing, and then uses text-to-speech to vocalize Ollama's response.

## Features

- Voice input using Vosk for offline speech recognition
- Text-to-speech output for Ollama's responses
- Streaming support for Ollama's API
- Low-latency, resource-efficient operation
- Ability to select a system voice for text-to-speech
- Logging of chat conversations to a styled HTML file

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- Ollama installed and running on your local machine
- A working microphone for voice input
- Speakers or headphones for audio output

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/DrewPear309/ollama-talk.git
   cd ollama-talk
   create a virtual environment if you wish.
   ```

2. Install the required Python libraries:
   ```
   pip install requests pyttsx3 pyaudio vosk
   ```

3. Download a Vosk model:
   - Visit [Vosk Models](https://alphacephei.com/vosk/models)
   - Download a model appropriate for your language (e.g., "vosk-model-small-en-us-0.15" for English)
   - Extract the model files into a directory named `vosk-model-small-en-us-0.15` in the project folder

## Configuration

1. Ensure Ollama is running on your local machine and your chosen model is installed.
2. Enter your chosen Ollama model on line 14 in ollama-talk.py.
3. frames_per_buffer on line 54 can be adjusted upwards if your machine can handle it. Try 8000.
4. If Ollama is not running on the default port (11434), update the `OLLAMA_API_BASE` variable in the script.
5. If you're using a different Vosk model, update the `model_path` in the `chat_with_voice()` function.

## Usage

1. Start Ollama on your local machine if it's not already running.

2. Run the Python script:
   ```
   python ollama-talk.py
   ```

3. Choose your desired voice.

4. The application will process your speech, send it to Ollama, and then speak the response.

5. To exit the application, press Ctrl+C in the console.

6. After the conversation, an HTML file containing the chat log will be generated in the history directory which will be created in the app folder.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://github.com/jmorganca/ollama) for the AI language model
- [Vosk](https://github.com/alphacep/vosk-api) for the speech recognition technology
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for text-to-speech functionality
