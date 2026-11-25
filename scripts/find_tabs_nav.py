with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'view-kp' in line or 'switchView' in line or 'tab-btn' in line:
            print(str(i+1) + ': ' + line.strip()[:100])
