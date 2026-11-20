import requests

BOT_TOKEN = "9076187059:AAGsuSCU-aQiGWIVajtdk3T-vUGgVHy1FAo"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"

try:
    resp = requests.get(url, timeout=10)
    print("getMe status:", resp.status_code)
    print("getMe response:", resp.json())
except Exception as e:
    print("Error connecting to Telegram:", e)

