import requests
import time
from keep_alive import keep_alive

# === KEEP ALIVE SERVER ===
keep_alive()

# === CONFIGURATION ===
TELEGRAM_TOKEN = "8023747614:AAGerV6fBYMTiIu2jPMI4xL6W450mm2DxgU"  # 🔁 Replace with your Telegram Bot Token
CHAT_ID = "1290853860"
CRYPTOPANIC_TOKEN = "a3248d4b49886a49eddaeb898174a3aa210e7305"

# === PRICE ALERTS SETUP ===
WATCHLIST = {"bitcoin": 2, "ethereum": 2, "ronin": 3, "pepe": 5, "dogecoin": 3}

# === STATE TRACKING ===
last_alerted = {}
last_news_id = None


# === SEND MESSAGE ===
def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Failed to send message: {e}")


# === CHECK PRICE MOVES ===
def check_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    ids = ",".join(WATCHLIST.keys())
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    try:
        res = requests.get(url, params=params).json()
        for coin, data in res.items():
            change = data.get("usd_24h_change", 0)
            price = data.get("usd", 0)
            threshold = WATCHLIST[coin]
            rounded_change = round(change, 1)
            last = last_alerted.get(coin)

            if abs(change) > threshold and last != rounded_change:
                arrow = "📈" if change > 0 else "📉"
                msg = f"{arrow} <b>{coin.upper()}</b>\nPrice: ${price:.4f}\n24h Change: {change:.2f}%"
                send_message(msg)
                last_alerted[coin] = rounded_change

    except Exception as e:
        print(f"❌ Price check failed: {e}")


# === GET ALPHA NEWS ===
def get_alpha_news():
    global last_news_id
    try:
        url = "https://cryptopanic.com/api/developer/v2/posts/"
        params = {
            "auth_token": CRYPTOPANIC_TOKEN,
            "filter": "important",
            "public": "true"
        }
        response = requests.get(url, params=params)
        posts = response.json().get("results", [])

        for post in posts:
            post_id = post.get("id")
            title = post.get("title")
            link = post.get("url")

            if post_id != last_news_id:
                send_message(f"🧠 <b>{title}</b>\n🔗 {link}")
                last_news_id = post_id
                break  # send only one new item per cycle

    except Exception as e:
        print(f"❌ Alpha news fetch failed: {e}")


# === MAIN LOOP ===
while True:
    print("⏳ Checking market + alpha...")
    check_prices()
    get_alpha_news()
    time.sleep(600)  # Check every 10 minutes
