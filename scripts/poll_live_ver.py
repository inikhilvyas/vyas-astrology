import urllib.request
import re
import time

for attempt in range(12):
    try:
        url = f"https://vyasastro.in/?t={int(time.time())}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            m = re.search(r'CURRENT_ENGINE_VERSION\s*=\s*[\'"]([^\'"]+)[\'"]', html)
            if m:
                ver = m.group(1)
                print(f"Attempt {attempt+1}: Live site version = '{ver}'")
                if ver == 'v5.0_pure_math_parashari_2026':
                    print("SUCCESS! Hostinger deployment verified live with v5.0_pure_math_parashari_2026!")
                    break
            else:
                print(f"Attempt {attempt+1}: Version not found")
        time.sleep(5)
    except Exception as e:
        print(f"Attempt {attempt+1} error:", e)
        time.sleep(5)

