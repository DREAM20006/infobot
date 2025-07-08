import requests
import time
import os
import json
from ronin_tracker import check_ronin_wallets

BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ✅ Send message to Telegram
def send_telegram_message(text):
    requests.post(f"{URL}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    })

# ✅ Handle Telegram commands
def handle_commands(message):
    text = message.get("text", "")
    if text.startswith("/addwallet"):
        try:
            _, addr, label = text.split(" ", 2)
            with open("wallets.json", "r") as f:
                wallets = json.load(f)

            if addr in wallets:
                send_telegram_message("⚠️ Already tracking this wallet.")
            else:
                wallets[addr] = label
                with open("wallets.json", "w") as f:
                    json.dump(wallets, f, indent=2)
                send_telegram_message(f"✅ Wallet added:\n<code>{addr}</code>\nLabel: {label}")
        except:
            send_telegram_message("❌ Usage: /addwallet ronin:addr Label")

# ✅ Poll Telegram API
def get_updates(offset=None):
    params = {"timeout": 30, "offset": offset}
    resp = requests.get(f"{URL}/getUpdates", params=params)
    return resp.json()

# ✅ Main loop
def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for item in updates["result"]:
                offset = item["update_id"] + 1
                if "message" in item:
                    handle_commands(item["message"])

        check_ronin_wallets(send_telegram_message)
        time.sleep(60)

from keep_alive import keep_alive

if __name__ == "__main__":
    keep_alive()
    main()

