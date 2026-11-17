with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

views = ['view-kp', 'view-jaimini', 'view-nadi', 'view-predictions']
for v in views:
    idx = text.find(f'id="{v}"')
    if idx != -1:
        print(f"=== {v} found at char {idx} ===")
        print(text[idx:idx+1500])
    else:
        print(f"=== {v} NOT found ===")

