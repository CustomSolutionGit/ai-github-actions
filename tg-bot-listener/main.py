import tempfile
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests
import os
from whisper_helper import whisper_to_text

BOT_TOKEN = os.environ["BOT_TOKEN"]
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
CHAT_ID = os.getenv("CHAT_ID")
REPO = os.getenv("GITHUB_REPO")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    
    # создаём временный файл
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
        await file.download_to_drive(tmp_file.name)
        print("Voice message file is saved:", tmp_file.name)
        # тут можно конвертировать в wav, отправить на STT и т.д.

    # 1. Преобразуем голос в текст (Whisper/OpenAI API)
    # text_command = whisper_to_text(tmp_file.name)  # TODO through the whisper API
    text_command = "Create a basic angular 20 app with no standalone components, with a single page that has a button. When the button is clicked, it should display an alert with the message 'Hello, World!'"
    # 2. Создаем GitHub Issue
    create_github_issue(text_command)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text_command = update.message.text
        create_github_issue(text_command)

def create_github_issue(text):
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {"title": f"AI task", "body": text, "labels": ["to-code"]}
    requests.post(url, json=data, headers=headers)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.VOICE, voice_handler))
app.add_handler(MessageHandler(filters.TEXT, text_handler))
app.run_polling()
