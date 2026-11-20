with open('index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'modal-overlay' in line and 'id=' in line:
            print(f'{i+1}: {line.strip()[:80]}')

