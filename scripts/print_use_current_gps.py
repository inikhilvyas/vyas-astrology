with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('useCurrentGPS')
print(text[idx:idx+1500])
