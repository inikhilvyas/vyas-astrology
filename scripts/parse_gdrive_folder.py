import urllib.request
import re
import json

url = 'https://drive.google.com/drive/folders/0B8PLpDKw1NhKVFUyVzB3QXdTMEE?resourcekey=0-lKwnCujdFzbYZ29YNR0zMQ'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

print("Fetching folder page...")
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

matches = re.findall(r'_DRIVE_ivd\s*=\s*\'(.*?)\';', html)
if not matches:
    matches = re.findall(r'window\[\'_DRIVE_ivd\'\]\s*=\s*\'(.*?)\';', html)

if matches:
    raw_str = matches[0]
    # Replace JS escaped characters
    raw_str = raw_str.replace('\\x22', '"').replace('\\x27', "'").replace('\\\\', '\\')
    
    with open('scripts/drive_blob.txt', 'w', encoding='utf-8') as f:
        f.write(raw_str)
    print("Saved blob to scripts/drive_blob.txt, length:", len(raw_str))
    
    try:
        data = json.loads(raw_str)
        print("Successfully parsed json array! Length:", len(data))
        with open('scripts/drive_items.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("JSON parse error:", e)

# Also let's extract all item structures by regex
# Pattern: ["item-id", "filename.pdf", ...]
items = []
pattern = re.compile(r'\["([a-zA-Z0-9_-]{25,})",\s*\[?"([^"]+\.pdf)"', re.I)
for match in pattern.finditer(html):
    items.append({"id": match.group(1), "name": match.group(2)})

print(f"Found {len(items)} PDF items directly via regex pattern.")
if items:
    print("First 5 items:", items[:5])
    with open('scripts/gdrive_pdf_list.json', 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

