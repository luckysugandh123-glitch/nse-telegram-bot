import requests
import telegram
import pytz
import os
import time
from datetime import datetime

BOT_TOKEN = os.environ.get("8492113943:AAGfAo14XXmEdN78W8qed7GwVsZml-jliX8")
CHAT_ID = os.environ.get("8099868217")

bot = telegram.Bot(token= 8492113943:AAGfAo14XXmEdN78W8qed7GwVsZml-jliX8)

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

def is_market_time():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    if now.weekday() >= 5:
        return False

    return (now.hour > 9 or (now.hour == 9 and now.minute >= 15)) and \
           (now.hour < 15 or (now.hour == 15 and now.minute <= 30))

def fetch_data(index_type):
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)

    url = f"https://www.nseindia.com/api/live-analysis-variations?index={index_type}"
    response = session.get(url, headers=headers)
    data = response.json()

    message = f"📊 TOP {index_type.upper()}\n\n"

    for stock in data['data']:
        message += (
            f"{stock.get('symbol')}\n"
            f"Open: {stock.get('openPrice')}\n"
            f"High: {stock.get('dayHigh')}\n"
            f"Low: {stock.get('dayLow')}\n"
            f"Volume: {stock.get('totalTradedVolume')}\n\n"
        )

    return message

print("Bot Started...")

while True:
    if is_market_time():
        try:
            gainers = fetch_data("gainers")
            losers = fetch_data("losers")

            bot.send_message(chat_id=CHAT_ID, text=gainers)
            bot.send_message(chat_id=CHAT_ID, text=losers)

            print("Sent Successfully")

        except Exception as e:
            print("Error:", e)
    else:
        print("Market Closed")

    time.sleep(180)
