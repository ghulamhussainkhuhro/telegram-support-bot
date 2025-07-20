import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I'm your AI assistant. Ask me anything!")

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_KEY
    }

    body = {
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            f"{AZURE_ENDPOINT}openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version=2024-03-01-preview",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = f"❌ Error: {e}"

    await update.message.reply_text(bot_reply)

# Build the Telegram bot app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
if __name__ == "__main__":
    app.run_polling()
# Ensure the bot runs continuously
# This will keep the bot running and listening for messages