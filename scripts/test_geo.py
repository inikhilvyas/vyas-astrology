import urllib.request
import json
import urllib.parse

def test_nominatim(query="Osian, Rajasthan"):
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'VYAS-Astra-Astrology/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print("Nominatim result:", data[0]['display_name'], data[0]['lat'], data[0]['lon'])
    except Exception as e:
        print("Nominatim error:", e)

def test_ip_api():
    try:
        with urllib.request.urlopen("http://ip-api.com/json", timeout=5) as resp:
            data = json.loads(resp.read().decode())
            print("IP-API result:", data.get('city'), data.get('lat'), data.get('lon'), data.get('timezone'))
    except Exception as e:
        print("IP-API error:", e)

if __name__ == '__main__':
    test_nominatim()
    test_ip_api()

