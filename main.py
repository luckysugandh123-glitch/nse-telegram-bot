import requests
import telegram
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

def fetch_data(index_type):
    session = requests.Session()

    # Visit real page first (important for cookies)
    session.get("https://www.nseindia.com/market-data/top-gainers-losers", headers=headers)

    api_url = f"https://www.nseindia.com/api/live-analysis-variations?index={index_type}"
    response = session.get(api_url, headers=headers)

    data = response.json()

    message = f"📊 TOP {index_type.upper()}\n\n"

    for stock in data.get("data", [])[:10]:  # limit to 10
        message += (
            f"{stock.get('symbol')} | "
            f"O:{stock.get('openPrice')} | "
            f"H:{stock.get('dayHigh')} | "
            f"L:{stock.get('dayLow')} | "
            f"V:{stock.get('totalTradedVolume')}\n"
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