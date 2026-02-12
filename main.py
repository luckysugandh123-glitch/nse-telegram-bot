
import requests
import telegram
import pytz
import os
import time
from datetime import datetime

BOT_TOKEN = os.environ.get("8492113943:AAGfAo14XXmEdN78W8qed7GwVsZml-jliX8")
CHAT_ID = os.environ.get("8099868217")

bot = telegram.Bot(token=8492113943:AAGfAo14XXmEdN78W8qed7GwVsZml-jliX8)

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

    return (now.hour > 9 or (now.hour == 9 and now.minute >= 15)) and (now.hour < 15 or (now.hour == 15 and now.minute <= 30))

def get_page_data():
    session = requests.Session()
    # Visit the real page first (to get cookies)
    session.get("https://www.nseindia.com/market-data/top-gainers-losers", headers=headers)

    # Then call the actual API endpoints
    gainers_url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"
    losers_url = "https://www.nseindia.com/api/live-analysis-variations?index=losers"

    gainers_resp = session.get(gainers_url, headers=headers).json()
    losers_resp = session.get(losers_url, headers=headers).json()

    return gainers_resp, losers_resp

while True:
    print("Checking market...")

    try:
        if is_market_time():
            gainers_data, losers_data = get_page_data()

            # Build messages
            gainers_msg = "📈 TOP GAINERS\n\n"
            for stock in gainers_data.get("data", []):
                gainers_msg += (
                    f"{stock.get('symbol')} | O:{stock.get('openPrice')} | H:{stock.get('dayHigh')} | L:{stock.get('dayLow')} | V:{stock.get('totalTradedVolume')}\n"
                )

            losers_msg = "📉 TOP LOSERS\n\n"
            for stock in losers_data.get("data", []):
                losers_msg += (
                    f"{stock.get('symbol')} | O:{stock.get('openPrice')} | H:{stock.get('dayHigh')} | L:{stock.get('dayLow')} | V:{stock.get('totalTradedVolume')}\n"
                )

            bot.send_message(chat_id=CHAT_ID, text=gainers_msg)
            bot.send_message(chat_id=CHAT_ID, text=losers_msg)

            print("Sent messages")

        else:
            print("Market Closed")

    except Exception as e:
        print("Error:", e)

    time.sleep(180)  # 3 minutes
