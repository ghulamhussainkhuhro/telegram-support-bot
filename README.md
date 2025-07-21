# 🤖 SmartStore Support Bot

A fully functional AI-powered **Telegram bot** that automates **Tier-1 customer support** for e-commerce and service-based businesses.

---

## 🚀 Features

- ✅ Handles **FAQs** from `faqs.json`
- ✅ Offers **product recommendations** using `products.json`
- ✅ Escalates issues using **smart support rules** from `support_rules.json`
- ✅ Uses **GPT-4 fallback** (via Azure OpenAI) for natural language queries

---

## 🗂️ Project Structure

📁 data  
├── faqs.json              # Predefined FAQ responses  
├── products.json          # Product catalog for recommendations  
└── support_rules.json     # Rules to escalate complex queries  
📄 bot.py                  # Main bot logic (Telegram + GPT-4)  
📄 .env                    # Environment variables (do not commit this)  
📄 requirements.txt        # Python dependencies  
📄 railway.json            # Railway deployment config  
📄 README.md               # Project documentation

---

## 🛠️ Tech Stack

- **Python** · Telegram Bot API  
- **Azure OpenAI (GPT-4)**  
- **Railway** (cloud deployment)  
- `.env` via `dotenv` for API key security

---

## 📽️ Demo & LinkedIn Post

🎥 A complete demo is shared in my LinkedIn post:  
👉 [Watch it here](https://www.linkedin.com/in/ghulamhussainkhuhro)

---

## ⚙️ How to Run Locally

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   cd YOUR_REPO

---

## ⚙️ How to Run Locally

1. **Create a `.env` file** with your credentials:

   ```env
   TELEGRAM_TOKEN=
   AZURE_OPENAI_ENDPOINT=
   AZURE_OPENAI_API_KEY=
   AZURE_OPENAI_DEPLOYMENT=
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot**:

   ```bash
   python bot.py
   ```

---

## 💼 Hire Me

I build custom AI bots for:

- Customer Support  
- WhatsApp / Telegram / Instagram / Slack Automation  
- Knowledge Base Assistants  

🔗 [View my Fiverr gig](https://www.fiverr.com/sellers/ghussaink/)  
🔗 [Connect on LinkedIn](https://www.linkedin.com/in/ghulamhussainkhuhro)

---

## 📜 License

**MIT** – Free to use with credit

---




