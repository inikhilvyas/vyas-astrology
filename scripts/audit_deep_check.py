import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. PDF and dossier links
pdf_links = re.findall(r'href=[\'\"]([^\'\"]*\.pdf[^\'\"]*)[\'\"]', c, re.IGNORECASE)
dossier_links = re.findall(r'href=[\'\"]([^\'\"]*dossier[^\'\"]*)[\'\"]', c, re.IGNORECASE)
print('PDF links in index.html:', set(pdf_links))
print('Dossier links in index.html:', set(dossier_links))

for pl in set(pdf_links):
    clean_p = pl.split('?')[0].split('#')[0]
    if clean_p.startswith('/'): clean_p = clean_p[1:]
    exists = os.path.exists(clean_p)
    print(f'Link {clean_p}: exists on disk? {exists}')

# 2. Check how dobStr is parsed
dob_matches = [m.start() for m in re.finditer(r'dobStr\.split', c)]
print('dobStr.split matches:', len(dob_matches))

# 3. Check timezone and DST handling
tz_matches = [m.start() for m in re.finditer(r'5\.5|5:30|timezone|dst', c, re.IGNORECASE)]
print('Timezone / DST mentions:', len(tz_matches))

