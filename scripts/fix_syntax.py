# -*- coding: utf-8 -*-
import os

files = ['index.html', 'mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html', 'js/vyas_daivagya_vision.js']

for path in files:
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    old_bad = '"<i>कल्याणमस्तु सादर प्रणाम " + name + " जी + "! आपकी जिज्ञासा'
    new_good = '"<i>सादर प्रणाम " + name + " जी! आपकी जिज्ञासा'

    if old_bad in c:
        c = c.replace(old_bad, new_good)
        print("Fixed old_bad in:", path)

    # Also check if any other bad pattern
    c = c.replace('" जी + "!', '" जी! ')
    c = c.replace('" जी + "।', '" जी। ')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print("Syntax fix script completed.")

