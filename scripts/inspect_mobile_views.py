with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for v in ['view-kp', 'view-jaimini', 'view-nadi', 'view-predictions']:
    idx = text.find(f'id="{v}"')
    print(f'mobile {v}: {idx}')
    if idx != -1:
        print(text[idx:idx+400])
        print("...")
