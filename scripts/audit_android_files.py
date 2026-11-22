import os

def check_android_app():
    root = 'android_app'
    files_to_check = [
        'app/build.gradle.kts',
        'app/src/main/AndroidManifest.xml',
        'app/src/main/java/in/vyasastro/app/MainActivity.java',
        'app/src/main/java/in/vyasastro/app/WebAppInterface.java',
        'app/src/main/res/values/strings.xml',
        'app/src/main/res/values/colors.xml',
        'app/src/main/assets/mobile/index.html',
        'app/proguard-rules.pro',
        'settings.gradle.kts',
        'build.gradle.kts',
        'generate_keystore.bat',
        'build_release_aab.bat'
    ]
    for rel in files_to_check:
        full = os.path.join(root, rel)
        exists = os.path.exists(full)
        size = os.path.getsize(full) if exists else 0
        print(f"{rel}: {'EXISTS' if exists else 'MISSING'} ({size} bytes)")

check_android_app()

