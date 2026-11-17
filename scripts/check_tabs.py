# scripts/check_tabs.py
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

tabs = ['daily', 'dasha', 'predictions', 'ashtakavarga', 'shadbala', 'match', 'prashna', 'remedies', 'sphutas', 'transit', 'vargas', 'kp', 'jaimini', 'nadi', 'pdf']
for t in tabs:
    target_id = f'view-{t}'
    pos = text.find(f'id="{target_id}"')
    print(f"Tab {t:15} -> {target_id:20} found: {pos != -1} (at {pos})")

