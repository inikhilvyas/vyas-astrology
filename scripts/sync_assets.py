# -*- coding: utf-8 -*-
import shutil, os

# 1. Sync mobile/index.html
shutil.copy2('mobile/index.html', 'static/mobile/index.html')
print("Synced mobile/index.html -> static/mobile/index.html")

os.makedirs('android_app/app/src/main/assets/mobile', exist_ok=True)
shutil.copy2('mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html')
print("Synced mobile/index.html -> android_app/app/src/main/assets/mobile/index.html")

# 2. Sync JS files to android_app
os.makedirs('android_app/app/src/main/assets/js', exist_ok=True)
js_files = [
    'vyas_bhavat_bhavam.js',
    'vyas_treatise_sutras.js',
    'vyas_treatise_engine.js',
    'vyas_astronomical_engine.js',
    'vyas_daivagya_engine.js',
    'vyas_kp_horary_solver.js',
    'vyas_chart_renderers.js',
    'vyas_sutras_bank.js',
    'vyas_swipe_navigation.js'
]

for jf in js_files:
    src = os.path.join('js', jf)
    if os.path.exists(src):
        dst = os.path.join('android_app/app/src/main/assets/js', jf)
        shutil.copy2(src, dst)
        print(f"Synced {src} -> {dst}")

print("Sync completed successfully!")
