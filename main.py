import os, requests, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
BALL_KEY = os.environ.get("BALLDONTLIE_KEY")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot SavNbaProno en ligne"

async def start(update: Update, context):
    await update.message.reply_text("Bienvenue sur SavNbaProno ! Envoie /matchs pour voir les matchs")

async def matchs(update: Update, context):
    headers = {"Authorization": BALL_KEY}
    try:
        r = requests.get("https://api.balldontlie.io/nba/games?dates[]=2026-11-13", headers=headers)
        data = r.json().get("data", [])
        if not data:
            await update.message.reply_text("Pas de matchs aujourd'hui")
            return
        msg = ""
        for g in data[:5]:
            msg += f"{g['home_team']['abbreviation']} vs {g['visitor_team']['abbreviation']}\n"
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Erreur: {e}")

def run_bot():
    print("Bot lance...", flush=True)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("matchs", matchs))
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
