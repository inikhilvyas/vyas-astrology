import urllib.request
import re

client_id = '341351445313-ddlkfiqsndnvbl290bubh1u3s827c3b2.apps.googleusercontent.com'
redirect_uri = 'https://vyasastro.in/'
auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=token&scope=openid%20email%20profile'

req = urllib.request.Request(auth_url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8', errors='ignore')

# Find all text inside div or span or heading
strings = re.findall(r'>([^<]{4,150})<', html)
for s in strings:
    s = s.strip()
    if any(k in s.lower() for k in ['error', 'mismatch', 'redirect', 'origin', 'access_denied', 'developer', 'client', 'app', 'sign in']):
        print('->', s)

