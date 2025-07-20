import os
import json
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

# Load data files once at startup
with open("data/faqs.json", "r", encoding="utf-8") as f:
    FAQs = json.load(f)

with open("data/products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

with open("data/support_rules.json", "r", encoding="utf-8") as f:
    SUPPORT_RULES = json.load(f)

CONTACT_LINK = SUPPORT_RULES.get("contact_link", "https://smartstore.io/live-support")
SEVERE_KEYWORDS = SUPPORT_RULES.get("keywords", [])

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 Welcome to SmartStore Support! "
        "Ask me about your orders, returns, products, or type 'talk to support' to reach a human."
    )
    await update.message.reply_text(welcome_msg)

def find_faq_answer(user_text: str) -> str:
    user_text_lower = user_text.lower()
    for faq in FAQs:
        if faq["question"].lower() in user_text_lower:
            return faq["answer"]
    return None

def find_product_suggestion(user_text: str) -> str:
    user_text_lower = user_text.lower()
    for product in PRODUCTS:
        if product["name"].lower() in user_text_lower or product["category"].lower() in user_text_lower:
            return (
                f"Check out our {product['name']} here: {product['link']} "
                f"Price: Rs. {product['price']}"
            )
    return None

def check_severe_issue(user_text: str) -> bool:
    user_text_lower = user_text.lower()
    for keyword in SEVERE_KEYWORDS:
        if keyword in user_text_lower:
            return True
    return False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    # Escalate if user requests human support or severe issue detected
    if "talk to support" in user_input.lower() or check_severe_issue(user_input):
        reply = (
            "⚠️ It looks like you need assistance from our human support team. "
            f"Please contact us here: {CONTACT_LINK}"
        )
        await update.message.reply_text(reply)
        return

    # Check FAQs
    faq_answer = find_faq_answer(user_input)
    if faq_answer:
        await update.message.reply_text(faq_answer)
        return

    # Check product suggestions
    product_suggestion = find_product_suggestion(user_input)
    if product_suggestion:
        await update.message.reply_text(product_suggestion)
        return

    # Otherwise, fallback to GPT-4 AI answer
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_KEY
    }

    system_prompt = {
        "role": "system",
        "content": (
            "You are a helpful customer support assistant for SmartStore, an online shop in Pakistan. "
            "Answer politely and clearly based on the context."
        )
    }

    body = {
        "messages": [
            system_prompt,
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(
            f"{AZURE_ENDPOINT}openai/deployments/{AZURE_DEPLOYMENT}/chat/completions?api-version=2024-03-01-preview",
            headers=headers,
            json=body,
            timeout=10
        )
        response.raise_for_status()
        bot_reply = response.json()['choices'][0]['message']['content']
    except Exception as e:
        bot_reply = "❌ Sorry, I couldn't process your request at the moment. Please try again later."

    await update.message.reply_text(bot_reply)

# Build the Telegram bot app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
if __name__ == "__main__":
    print("SmartStore Support Bot is running...")
    app.run_polling()
