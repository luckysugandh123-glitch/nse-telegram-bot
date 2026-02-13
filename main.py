import requests
import telegram Bot
import pytz
import os
import time
from datetime import datetime

# Get values from Railway Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in Railway Variables")

if not CHAT_ID:
    raise ValueError("CHAT_ID is not set in Railway Variables")

bot = telegram.Bot(token=BOT_TOKEN)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/market-data/top-gainers-losers",
}

def is_market_time():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    if now.weekday() >= 5:
        return False

    return (
        (now.hour > 9 or (now.hour == 9 and now.minute >= 15))
        and
        (now.hour < 15 or (now.hour == 15 and now.minute <= 30))
    )

import requests
import time

def fetch_data(type):
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com",
    }

    # Step 1: get cookies
    session.get("https://www.nseindia.com", headers=headers)
    time.sleep(1)

    # Step 2: API call
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    response = session.get(url, headers=headers)

    if response.status_code != 200:
        print("Blocked:", response.status_code)
        return

    try:
        data = response.json()
    except:
        print("Not JSON:", response.text[:200])
        return

    stocks = data.get("data", [])[:10]

    message = "📊 NIFTY 50 DATA\n\n"

    for stock in stocks:
        message += (
            f"{stock.get('symbol')} | "
            f"LTP: {stock.get('lastPrice')} | "
            f"%: {stock.get('pChange')}%\n"
        )

    return message


print("Bot started...")

while True:
    try:
        if is_market_time():
            print("Market open - fetching data")

            gainers_message = fetch_data("gainers")
            losers_message = fetch_data("losers")

            bot.send_message(chat_id=CHAT_ID, text=gainers_message)
            bot.send_message(chat_id=CHAT_ID, text=losers_message)

            print("Messages sent successfully")

        else:
            print("Market closed")

    except Exception as e:
        print("ERROR:", e)

    time.sleep(180)  # 3 minutes