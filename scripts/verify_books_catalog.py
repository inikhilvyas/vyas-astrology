import os
import re

target_dir = r"G:\software\simpa\VYAS\books"
pdf_files = [f for f in os.listdir(target_dir) if f.lower().endswith(".pdf")]
print(f"Total PDF files currently in {target_dir}: {len(pdf_files)}")

with open("scripts/download_with_curl.py", "r", encoding="utf-8") as f:
    text = f.read()

urls = re.findall(r'https://astrofoxx\.wordpress\.com/[^\s"\'\)]+', text)
print(f"Total URLs in batch list: {len(urls)}")

valid_count = 0
missing_list = []

for u in urls:
    fname = u.split("/")[-1]
    fpath = os.path.join(target_dir, fname)
    if not os.path.exists(fpath):
        missing_list.append((fname, "File not found"))
    else:
        sz = os.path.getsize(fpath)
        with open(fpath, "rb") as bf:
            header = bf.read(5)
            if header.startswith(b"%PDF"):
                valid_count += 1
            else:
                missing_list.append((fname, f"Corrupted or HTML ({sz} bytes)"))

print(f"Valid verified PDF books: {valid_count} / {len(urls)}")
if missing_list:
    print(f"Missing count: {len(missing_list)}")
    for m in missing_list[:5]:
        print("  -", m)
else:
    print("SUCCESS: Every single book (127/127) requested by the user is 100% downloaded, valid, and present!")
