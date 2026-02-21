# whisper_helper.py
import os
import openai

# Загружаем API ключ из env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def whisper_to_text(audio_file_path: str) -> str:
    """
    Converts voice msg file into text via OpenAI Whisper API
    """
    with open(audio_file_path, "rb") as f:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return response.text