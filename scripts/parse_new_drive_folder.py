import urllib.request
import re
import json

url = 'https://drive.google.com/drive/folders/1lU6wQNPm6cK403OgbOvoizDlElVknkmV'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

print("Fetching new folder page...")
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

matches = re.findall(r'_DRIVE_ivd\s*=\s*\'(.*?)\';', html)
if not matches:
    matches = re.findall(r'window\[\'_DRIVE_ivd\'\]\s*=\s*\'(.*?)\';', html)

if not matches:
    print("No data blob found!")
    exit(1)

txt = matches[0]
decoded = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), txt)
decoded = decoded.replace('\/', '/')

data = json.loads(decoded)
print("Parsed JSON data successfully! Top level len:", len(data))

items = []
def extract(obj):
    if isinstance(obj, list):
        if len(obj) >= 4 and isinstance(obj[0], str) and isinstance(obj[2], str) and isinstance(obj[3], str):
            if 'pdf' in obj[3] or obj[2].lower().endswith('.pdf') or 'google-apps.folder' in obj[3] or 'document' in obj[3] or 'text' in obj[3]:
                items.append({
                    'id': obj[0],
                    'name': obj[2],
                    'mimeType': obj[3],
                    'size': obj[4] if len(obj) > 4 else 0
                })
        for child in obj:
            extract(child)

extract(data)

seen = {}
unique = []
for it in items:
    if it['id'] not in seen:
        seen[it['id']] = True
        unique.append(it)

folders = [it for it in unique if 'folder' in it['mimeType']]
files = [it for it in unique if 'folder' not in it['mimeType']]

print(f"\n==========================================")
print(f"Total Unique Items Found in 'books' Folder: {len(unique)}")
print(f"Folders count: {len(folders)}")
print(f"Files / Books count: {len(files)}")
print(f"==========================================\n")

print("--- FOLDERS ---")
for fo in folders:
    print(f"📁 {fo['id']} | {fo['name']}")

print("\n--- SAMPLE FILES ---")
for fi in files[:25]:
    print(f"📄 {fi['id']} | {fi['name']} | size: {fi['size']}")

with open('scripts/new_drive_catalog.json', 'w', encoding='utf-8') as out:
    json.dump({
        'folder_id': '1lU6wQNPm6cK403OgbOvoizDlElVknkmV',
        'title': 'books',
        'folders': folders,
        'files': files
    }, out, indent=2, ensure_ascii=False)

