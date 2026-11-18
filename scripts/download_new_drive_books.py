import urllib.request
import json
import os
import time

with open('scripts/new_drive_catalog.json', 'r', encoding='utf-8') as f:
    cat = json.load(f)

files = cat['files']
os.makedirs('books', exist_ok=True)

print(f"Starting download of {len(files)} markdown books from Google Drive...")
downloaded = 0
failed = 0

for idx, fi in enumerate(files, 1):
    fid = fi['id']
    name = fi['name'].strip()
    # Clean filename
    clean_name = name.replace('/', '_').replace('\\', '_')
    target_path = os.path.join('books', clean_name)
    
    # Download URL
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    print(f"[{idx}/{len(files)}] Downloading: {clean_name} (ID: {fid})...")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = resp.read()
        
        # Check if received HTML error/redirect instead of text/markdown
        if data.startswith(b'<!DOCTYPE html>') and b'Google Drive - Virus scan warning' in data:
            # Need confirm token for large file
            print("  Virus scan confirm needed, retrying with confirm=t...")
            confirm_url = f"https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t"
            req2 = urllib.request.Request(confirm_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req2, timeout=30) as resp2:
                data = resp2.read()
                
        with open(target_path, 'wb') as out_f:
            out_f.write(data)
            
        sz_kb = len(data) // 1024
        print(f"  ✓ Saved to {target_path} ({sz_kb} KB)")
        downloaded += 1
    except Exception as e:
        print(f"  ✗ Failed to download {clean_name}: {e}")
        failed += 1
    
    time.sleep(0.5)

print("\n==========================================")
print(f"Download Summary: {downloaded} Succeeded, {failed} Failed out of {len(files)}")
print("==========================================")
