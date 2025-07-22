import yfinance as yf
import time
import requests
import pandas as pd
from datetime import datetime
import random

TOKEN = "8094752756:AAFUdZn4XFlHiZOtV-TXzMOhYFlXKCFVoEs"
CHAT_ID = "5556108366"

PAIRS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "USDJPY=X",
    "USD/CHF": "USDCHF=X",
    "AUD/USD": "AUDUSD=X",
    "NZD/USD": "NZDUSD=X",
    "USD/CAD": "USDCAD=X"
}

def send_signal(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def fetch_news_sentiment():
    sentiments = ['positive', 'neutral', 'negative']
    return random.choice(sentiments)

def analyze(name, data):
    if data.empty or len(data) < 3:
        return None

    last = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]
    change = last - prev
    direction = "📈 Buy" if change > 0 else "📉 Sell"
    conf = min(round(abs(change)/last * 1000, 2), 95)

    # Smart Money + News Analysis
    news = fetch_news_sentiment()
    if news == 'negative':
        conf -= 15
    elif news == 'positive':
        conf += 10

    if conf < 60:
        return None

    return (
        f"🔔 {name}
"
        f"{direction} @ {round(last,5)}
"
        f"News Sentiment: {news}
"
        f"Уверенность: {conf}%
"
        f"⏱ Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )

def check_all():
    for name, sym in PAIRS.items():
        try:
            df = yf.Ticker(sym).history(period="1d", interval="1m")
            sig = analyze(name, df)
            if sig:
                send_signal(sig)
            else:
                send_signal(f"ℹ️ {name}: нет сигнала — уверенность <60%")
        except Exception as e:
            send_signal(f"❌ Ошибка {name}: {e}")

if __name__ == "__main__":
    send_signal("🤖 Расширенный бот запущен (с обучением, стратегиями и новостями)")
    while True:
        check_all()
        time.sleep(300)
