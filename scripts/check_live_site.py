import urllib.request, re

req = urllib.request.Request('https://vyasastro.in/', headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
resp = urllib.request.urlopen(req).read().decode('utf-8')
print("Length:", len(resp))
for m in re.finditer(r'vyas[-_a-zA-Z0-9]+v[0-9]+[^\s"\'<>]*', resp):
    print("Match:", m.group(0))
    break
print("Contains pavDailyKakshyaCard:", 'pavDailyKakshyaCard' in resp)
print("Contains savSum === 337:", 'savSum === 337' in resp)

