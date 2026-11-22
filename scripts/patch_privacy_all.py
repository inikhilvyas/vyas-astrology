# scripts/patch_privacy_all.py
import os, re

def patch_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (not found)")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for pattern, repl in replacements:
        if isinstance(pattern, str):
            content = content.replace(pattern, repl)
        else:
            content = pattern.sub(repl, content)
    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath} successfully.")
    else:
        print(f"No changes needed in {filepath}.")

# 1. index.html replacements
index_replacements = [
    (
        '"निखिल व्यास (सत्यापित आजीवन VIP)"',
        '"सत्यापित आजीवन PRO VIP सदस्य"'
    ),
    (
        re.compile(r'शोध, सूत्र एवं निर्देशन:\s*<b[^>]*>निखिल व्यास[^<]*</b>[^•]*•\s*पाली\s*\([^)]*\)', re.I | re.DOTALL),
        'शोध, सूत्र एवं निर्देशन: <b style="color:var(--accent-gold); font-size:0.98rem;">व्यास अस्त्र वैदिक शोध संस्थान (VYAS Research Foundation)</b> • आचार्य दैवज्ञ मण्डल'
    ),
    (
        'inikhilvyas@gmail.com',
        'support@vyasastro.in'
    ),
    (
        'nikhilvyas007@gmail.com',
        'admin@vyasastro.in'
    )
]

patch_file('index.html', index_replacements)

# 2. js/vyas_daivagya_engine.js
engine_replacements = [
    (
        'निखिल व्यास (शोध निदेशक)',
        'व्यास अस्त्र वैदिक शोध संस्थान'
    )
]
patch_file('js/vyas_daivagya_engine.js', engine_replacements)

# 3. Mobile index files
mobile_replacements = [
    (
        re.compile(r'शोध एवं निर्देशन:\s*<b[^>]*>निखिल व्यास[^<]*</b>[^•]*•\s*पाली\s*\([^)]*\)', re.I | re.DOTALL),
        'शोध एवं निर्देशन: <b style="color:var(--primary);">व्यास अस्त्र वैदिक शोध संस्थान (VYAS Research Foundation)</b> • आचार्य दैवज्ञ मण्डल'
    ),
    (
        'inikhilvyas@gmail.com',
        'support@vyasastro.in'
    ),
    (
        'nikhilvyas007@gmail.com',
        'admin@vyasastro.in'
    )
]

for p in ['static/mobile/index.html', 'mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html']:
    patch_file(p, mobile_replacements)

print("All privacy patches completed.")

