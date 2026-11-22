import urllib.request
import time
import re

url = f"https://vyasastro.in/kundli-matching/?_nocache={int(time.time())}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print(f"Status: {resp.status}, Length: {len(html)}")
        
        # Check for personal details
        found_nikhil = "निखिल" in html
        found_1984 = "1984" in html
        found_suyogya = "सुयोग्य" in html
        
        print(f"Live HTML contains 'निखिल': {found_nikhil}")
        print(f"Live HTML contains '1984': {found_1984}")
        print(f"Live HTML contains 'सुयोग्य': {found_suyogya}")
        
        # Check input values
        groom_match = re.search(r'id=["\']groomName["\'][^>]*', html)
        if groom_match:
            print("groomName tag:", groom_match.group(0))
        bride_match = re.search(r'id=["\']brideName["\'][^>]*', html)
        if bride_match:
            print("brideName tag:", bride_match.group(0))
            
except Exception as e:
    print("Error fetching:", e)

