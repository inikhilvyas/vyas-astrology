with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    for i, line in enumerate(f):
        if 'id="view-' in line:
            print(str(i+1) + ': ' + line.strip()[:100])
