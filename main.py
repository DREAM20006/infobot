import requests
import time
from keep_alive import keep_alive
import os

# ✅ Telegram bot config
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
CRYPTOPANIC_TOKEN = os.environ.get("CRYPTOPANIC_TOKEN")

# ✅ Memory to avoid duplicate news
sent_titles = set()

# ✅ Send message to Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# ✅ Fetch & send unique alpha news
def fetch_alpha_news():
    url = f'https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_TOKEN}&public=true'
    try:
        res = requests.get(url).json()
        for post in res.get("results", []):
            title = post.get("title")
            link = post.get("url") or "None"
            if title and title not in sent_titles:
                sent_titles.add(title)
                send_telegram_message(f"🧠 <b>{title}</b>\n🔗 {link}")
        if len(sent_titles) > 100:
            sent_titles.clear()
    except Exception as e:
        print("Alpha News Error:", e)

# ✅ Dummy price pump checker (custom logic can be added)
def check_price_alerts():
    try:
        # Example check for ETH
        res = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd").json()
        eth_price = res["ethereum"]["usd"]
        print(f"ETH Price: ${eth_price}")
        if eth_price > 4000:  # Change this threshold as needed
            send_telegram_message(f"🚀 Ethereum is pumping!\nPrice: ${eth_price}")
    except Exception as e:
        print("Price Alert Error:", e)

# ✅ Start keep_alive Flask server
keep_alive()

# ✅ Main loop
while True:
    print("⏳ Checking market + alpha...")
    fetch_alpha_news()
    check_price_alerts()
    time.sleep(180)  # check every 3 minutes

elif text.startswith("/addwallet"):
    try:
        parts = text.split(" ", 2)
        address = parts[1]
        label = parts[2] if len(parts) > 2 else "Unnamed"

        with open("wallets.json", "r") as f:
            wallets = json.load(f)

        if address in wallets:
            send_telegram_message("⚠️ This wallet is already being tracked.")
        else:
            wallets[address] = label
            with open("wallets.json", "w") as f:
                json.dump(wallets, f, indent=2)
            send_telegram_message(f"✅ Added wallet:\n{address}\n📛 Label: {label}")
    except:
        send_telegram_message("❌ Usage: /addwallet ronin:addr Label")

