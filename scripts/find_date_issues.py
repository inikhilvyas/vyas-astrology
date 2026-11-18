with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in index.html: {len(lines)}")

for i, l in enumerate(lines):
    if any(k in l for k in ['toISOString', 'getTimezoneOffset', 'new Date', 'renderPanchang', 'renderDailyHoroscope', 'headerPanchangTicker', '17 Nov', '18 Nov', '2026-11-']):
        if any(term in l for term in ['Panchang', 'DailyHoroscope', 'Ticker', 'toISOString', 'dateStr', 'currentDate']):
            print(f"L{i+1}: {l.strip()[:140]}")

