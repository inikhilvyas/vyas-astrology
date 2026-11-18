with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('4 24" width="15"')
print("--- Pos around 78578 ---")
print(text[pos-100:pos+300])

print("\n--- toggleLanguage occurrences ---")
idx = 0
while True:
    idx = text.find('toggleLanguage', idx)
    if idx == -1:
        break
    print(f"Index {idx}:")
    print(text[idx-50:idx+400])
    idx += len('toggleLanguage')

print("\n--- langSwitch occurrences ---")
idx = 0
while True:
    idx = text.find('langSwitch', idx)
    if idx == -1:
        break
    print(f"Index {idx}:")
    print(text[idx-50:idx+300])
    idx += len('langSwitch')
