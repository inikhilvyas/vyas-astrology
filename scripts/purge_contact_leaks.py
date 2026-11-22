import os
import re

files_to_clean = [
    'index.html',
    'mobile/index.html',
    'static/mobile/index.html',
    'android_app/app/src/main/assets/mobile/index.html',
    'admin.html'
]

for fp in files_to_clean:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_len = len(content)
    
    # 1. Clean vyasbilawas@gmail.com
    content = content.replace('vyasbilawas@gmail.com', 'support@vyasastro.in')
    
    # 2. Clean whatsapp 9414121172
    content = re.sub(r'https://wa\.me/919414121172\?text=[^\s"\'<>]*', 'mailto:support@vyasastro.in', content)
    content = content.replace('https://wa.me/919414121172', 'mailto:support@vyasastro.in')
    content = content.replace('9414121172', 'support@vyasastro.in')
    content = content.replace('+91 9414121172', 'support@vyasastro.in')
    content = content.replace('+919414121172', 'support@vyasastro.in')
    content = content.replace('+919251021800', '')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Cleaned {fp}: {orig_len} -> {len(content)}")

