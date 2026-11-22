with open('android_app/app/build.gradle.kts', 'r', encoding='utf-8') as f:
    print("=== build.gradle.kts ===\n", f.read())
with open('android_app/app/src/main/AndroidManifest.xml', 'r', encoding='utf-8') as f:
    print("=== AndroidManifest.xml ===\n", f.read())

