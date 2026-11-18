with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Search for where dates are formatted: e.g. toLocaleDateString, getDate, getFullYear, dayNames, etc.
lines = text.split('\n')
for i, line in enumerate(lines):
    if any(k in line for k in ['toLocaleDateString', 'dPanDate', 'dailyDate', 'todayDate', 'curDate', 'currentDate']):
        print(f"Line {i+1}: {line.strip()[:140]}")

