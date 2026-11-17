with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for vid in ['view-kp', 'view-jaimini', 'view-nadi', 'view-predictions']:
    pos = text.find('id="' + vid + '"')
    print(f"=== {vid} at {pos} ===")
    if pos != -1:
        print(text[pos:pos+1200])
        print("\n" + "="*50 + "\n")

