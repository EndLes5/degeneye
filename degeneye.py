import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time

# =========================
# CONFIG
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable not set!")

# Optional: caching last price to avoid too many API requests
latest_price = None
last_update_time = 0
UPDATE_INTERVAL = 10  # seconds between API calls

# =========================
# FETCH BTC PRICE FUNCTION
# =========================
def fetch_btc_price():
    global latest_price, last_update_time
    current_time = time.time()
    if current_time - last_update_time > UPDATE_INTERVAL:
        try:
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            )
            data = response.json()
            latest_price = data["bitcoin"]["usd"]
            last_update_time = current_time
        except Exception as e:
            print("❌ Error fetching BTC price:", e)
    return latest_price

# =========================
# TELEGRAM COMMANDS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👁️ DegenEye is online.\nUse /price to get the latest BTC price."
    )

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = fetch_btc_price()
    if price:
        await update.message.reply_text(f"📈 BTC/USD: ${price}")
    else:
        await update.message.reply_text("⏳ Unable to fetch price. Try again in a few seconds.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! Bot is alive.")

# =========================
# MAIN FUNCTION
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("ping", ping))

    print("🤖 DegenEye bot running with CoinGecko REST polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
