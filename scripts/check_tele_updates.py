import requests

BOT_TOKEN = "9076187059:AAGsuSCU-aQiGWIVajtdk3T-vUGgVHy1FAo"
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

try:
    resp = requests.get(url, timeout=10)
    print("getUpdates status:", resp.status_code)
    updates = resp.json().get('result', [])
    print(f"Total updates pending: {len(updates)}")
    for u in updates[-5:]:
        msg = u.get('message', {})
        sender = msg.get('from', {})
        txt = msg.get('text', '')
        print(f"Update {u.get('update_id')}: from {sender.get('first_name')} (@{sender.get('username')}): {txt}")
except Exception as e:
    print("Error:", e)

