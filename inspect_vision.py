with open('js/vyas_daivagya_vision.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(120, 240):
    print(f"{i+1}: {lines[i].rstrip()}")
