with open('drive_page.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'([A-Za-z0-9_\-\.\u0900-\u097F\s]{4,80}\.(?:pdf|docx?|xlsx?|txt|md|zip))', html)
print(f"Direct extension matches: {len(matches)}")
for m in list(set(matches))[:30]:
    print(" -", m.strip())

# Search for any hindi title or book name
hindi_titles = re.findall(r'[\u0900-\u097F]{4,}', html)
print(f"Hindi tokens: {len(hindi_titles)}")
for h in list(set(hindi_titles))[:20]:
    print(" H:", h)

# Search for JSON data structures
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total scripts: {len(scripts)}")
for idx, s in enumerate(scripts):
    if '1zQjXfq2DqHipfr-sfwTHmox7kaIdQz-t' in s:
        print(f"Script {idx} contains folder ID! Length: {len(s)}")
        # Search for file names inside this script
        fnames = re.findall(r'"([^"]{4,100}\.(?:pdf|PDF|txt|docx?))"', s)
        print(" Files in script:", fnames)
