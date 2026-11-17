import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    'https://api.github.com/repos/ayushman1024/ASTROLOGY-BOOKS-DATABASE/contents',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        print('Repo items count:', len(data))
        for item in data:
            print(f"- {item['name']} ({item['type']})")
except Exception as e:
    print('Error:', e)

