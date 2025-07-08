import requests
import json

seen_ronin_txs = set()

def load_wallets():
    with open("wallets.json", "r") as f:
        return json.load(f)

def ronin_to_eth(address):
    return address.replace("ronin:", "0x")

def check_ronin_wallets():
    wallets = load_wallets()
    for ronin_address, label in wallets.items():
        try:
            eth_address = ronin_to_eth(ronin_address)
            url = f"https://explorer.roninchain.com/api/addresses/{eth_address}/transactions"
            res = requests.get(url, timeout=10)
            txs = res.json()

            for tx in txs:
                tx_hash = tx.get("hash")
                if tx_hash and tx_hash not in seen_ronin_txs:
                    seen_ronin_txs.add(tx_hash)

                    from_addr = tx.get("from")
                    to_addr = tx.get("to")
                    value = tx.get("value", "N/A")
                    symbol = tx.get("token_symbol", "RON")

                    send_telegram_message(f"""🦊 <b>Ronin Wallet Activity</b>
📛 <b>{label}</b>
🔹 From: <code>{from_addr}</code>
🔸 To: <code>{to_addr}</code>
💰 Token: {symbol}
💸 Value: {value}
🔗 <a href="https://explorer.roninchain.com/tx/{tx_hash}">View Tx</a>""")

            if len(seen_ronin_txs) > 100:
                seen_ronin_txs.clear()

        except Exception as e:
            print(f"[{label}] Ronin Error:", e)


