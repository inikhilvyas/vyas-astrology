import json

with open('scripts/gdrive_parsed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = []

def extract_items(obj):
    if isinstance(obj, list):
        if len(obj) >= 4 and isinstance(obj[0], str) and isinstance(obj[2], str) and isinstance(obj[3], str):
            if 'google-apps' in obj[3] or 'pdf' in obj[3] or obj[2].endswith('.pdf'):
                items.append({
                    'id': obj[0],
                    'name': obj[2],
                    'mimeType': obj[3],
                    'size': obj[4] if len(obj) > 4 else None
                })
        for item in obj:
            extract_items(item)

extract_items(data)
print(f"Total extracted items: {len(items)}")
# Remove duplicates by id
unique_items = {}
for it in items:
    unique_items[it['id']] = it

print(f"Unique items count: {len(unique_items)}")

folders = [it for it in unique_items.values() if 'folder' in it['mimeType']]
files = [it for it in unique_items.values() if 'folder' not in it['mimeType']]

print(f"Folders count: {len(folders)}")
print(f"Files count: {len(files)}")

print("\n--- SAMPLE FOLDERS ---")
for f in folders[:10]:
    print(f"{f['id']} | {f['name']}")

print("\n--- SAMPLE FILES ---")
for f in files[:20]:
    print(f"{f['id']} | {f['name']} | size: {f['size']}")

with open('scripts/gdrive_books_catalog.json', 'w', encoding='utf-8') as out:
    json.dump({
        'folders': folders,
        'files': files
    }, out, indent=2, ensure_ascii=False)

