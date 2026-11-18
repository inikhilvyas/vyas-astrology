import urllib.request
import re
import json
import time

subfolders = [
    {"id": "0B8PLpDKw1NhKZUg2OG1GOG13S0E", "name": "astrology"},
    {"id": "0B8PLpDKw1NhKcW12bFdDM3RrVDQ", "name": "B L Thakur Vedic Jyotish Books (Vedic Astrology)"},
    {"id": "0B8PLpDKw1NhKVzVEY3FmTUJSYms", "name": "Future Samachar-(मासिक पत्रिका )"},
    {"id": "0B8PLpDKw1NhKR2RPdkVVb0dmMkE", "name": "Hindi Vedic Astrology Books"},
    {"id": "0B8PLpDKw1NhKem5rb2Q1MTBLSEU", "name": "Prachin Hindi Jyotish Granth (Ancient Vedic Astrology Books)"}
]

def fetch_folder_items(folder_id):
    url = f"https://drive.google.com/drive/folders/{folder_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        matches = re.findall(r'_DRIVE_ivd\s*=\s*\'(.*?)\';', html)
        if not matches:
            matches = re.findall(r'window\[\'_DRIVE_ivd\'\]\s*=\s*\'(.*?)\';', html)
        if not matches:
            return []
        txt = matches[0]
        decoded = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), txt)
        decoded = decoded.replace('\/', '/')
        data = json.loads(decoded)
        
        items = []
        def extract(obj):
            if isinstance(obj, list):
                if len(obj) >= 4 and isinstance(obj[0], str) and isinstance(obj[2], str) and isinstance(obj[3], str):
                    if 'pdf' in obj[3] or obj[2].lower().endswith('.pdf') or 'google-apps.folder' in obj[3]:
                        items.append({
                            'id': obj[0],
                            'name': obj[2],
                            'mimeType': obj[3],
                            'size': obj[4] if len(obj) > 4 else 0
                        })
                for child in obj:
                    extract(child)
        extract(data)
        # Deduplicate
        seen = {}
        unique = []
        for it in items:
            if it['id'] not in seen:
                seen[it['id']] = True
                unique.append(it)
        return unique
    except Exception as e:
        print(f"Error fetching {folder_id}: {e}")
        return []

all_items = {}
# Load root files from earlier
with open('scripts/gdrive_books_catalog.json', 'r', encoding='utf-8') as f:
    root_data = json.load(f)
    for f_item in root_data['files']:
        f_item['folder'] = 'Root'
        all_items[f_item['id']] = f_item

for sf in subfolders:
    print(f"Fetching subfolder: {sf['name']} ({sf['id']})...")
    items = fetch_folder_items(sf['id'])
    print(f"  Found {len(items)} items in {sf['name']}")
    for it in items:
        if 'folder' not in it['mimeType']:
            it['folder'] = sf['name']
            all_items[it['id']] = it
    time.sleep(1)

master_catalog = list(all_items.values())
print(f"\n==========================================")
print(f"Total Unique Books / PDFs in Master Catalog: {len(master_catalog)}")
print(f"==========================================")

with open('scripts/gdrive_master_books_catalog.json', 'w', encoding='utf-8') as out:
    json.dump(master_catalog, out, indent=2, ensure_ascii=False)

