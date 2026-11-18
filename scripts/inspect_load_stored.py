with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('loadStoredProfile:')
if idx == -1:
    idx = text.find('loadStoredProfile()')
print(f"loadStoredProfile found at {idx}")
print(text[idx:idx+2500])

