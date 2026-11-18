import urllib.request
import fitz
import json

with open('scripts/gdrive_master_books_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

targets = [c for c in cat if any(k in c['name'] for k in ['Brihat', 'Jaimini', 'Lal', 'Samhita'])]

for t in targets[:4]:
    fid = t['id']
    name = t['name']
    print(f"\nTesting: {name} (ID: {fid})")
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        print(f"  Downloaded size: {len(data) // 1024} KB")
        doc = fitz.open(stream=data, filetype='pdf')
        print(f"  Total Pages: {len(doc)}")
        for pno in [0, 1, 2]:
            if pno < len(doc):
                txt = doc[pno].get_text().strip()
                print(f"  Page {pno+1} ({len(txt)} chars): {txt[:150]!r}")
    except Exception as e:
        print(f"  Error: {e}")

