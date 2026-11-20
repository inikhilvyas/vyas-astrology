import urllib.request, re

url = 'https://vyasastro.in/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

print("Live HTML size:", len(html))
# search for git commit or version strings
matches = re.findall(r'v\d+\.\d+[^"\']+|commit[^"\']+|deploy[^"\']+', html[:10000], re.I)
print("Versions in header:", matches)

# Check last modified header or dates
# Also check sw.js
try:
    with urllib.request.urlopen('https://vyasastro.in/sw.js') as r2:
        print("sw.js:\n", r2.read().decode('utf-8', errors='ignore')[:300])
except Exception as e:
    print("sw.js error:", e)

