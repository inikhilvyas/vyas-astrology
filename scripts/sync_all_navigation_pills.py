import os
import glob
import re

bhavat_pill = '<a href="/bhavat-bhavam/" class="portal-pill"><span>⚡</span><span>भावात् भावम्</span></a>'
bhavat_pill_active = '<a href="/bhavat-bhavam/" class="portal-pill active"><span>⚡</span><span>भावात् भावम्</span></a>'

files_to_check = [
    'index.html',
    'kp-astrology/index.html',
    'jaimini-astrology/index.html',
    'dasha/index.html',
    'panchang/index.html',
    'horary/index.html',
    'mobile/index.html',
    'static/mobile/index.html'
]

for fpath in files_to_check:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if bhavat-bhavam already linked
    if 'href="/bhavat-bhavam/"' in content:
        print(f"[{fpath}] already has /bhavat-bhavam/ link.")
        continue

    # Insert after kp-astrology pill
    kp_pattern = r'(<a\s+href=["\']/kp-astrology/["\'][^>]*>.*?</a>)'
    m = re.search(kp_pattern, content, re.DOTALL)
    if m:
        matched_str = m.group(1)
        replacement = matched_str + '\n        ' + bhavat_pill
        content = content.replace(matched_str, replacement, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[{fpath}] Injected /bhavat-bhavam/ pill after /kp-astrology/.")
    else:
        print(f"[{fpath}] Could not find /kp-astrology/ pill to inject after.")

print("Finished syncing navigation pills.")
