import urllib.request
import re

url = "https://vyasastro.in/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    m = re.search(r'CURRENT_ENGINE_VERSION\s*=\s*[\'"][^\'"]+[\'"]', html)
    if m:
        print("Live version found:", m.group())
    else:
        print("Version not found in live HTML")

