# -*- coding: utf-8 -*-
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("--- TABS & VIEWS IN MOBILE ---")
for idx, line in enumerate(lines):
    if 'switchTab' in line or 'id="view-' in line or 'VyasMobile.switchTab' in line or 'class="view-panel' in line:
        print(f'{idx+1}: {line.strip()[:100]}')

