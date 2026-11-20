import urllib.request
import time

url = f"https://vyasastro.in/?t={int(time.time())}"
print("Checking live deployment with cachebuster at:", url)

for attempt in range(6):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            if 'v5.0_pure_math_parashari_2026' in html:
                print(f"SUCCESS on attempt {attempt+1}! Live site has v5.0_pure_math_parashari_2026.")
                break
            else:
                print(f"Attempt {attempt+1}: Deploying... waiting 10s...")
                time.sleep(10)
    except Exception as e:
        print(f"Attempt {attempt+1} error:", e)
        time.sleep(10)

