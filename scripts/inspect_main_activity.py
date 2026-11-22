with open('android_app/app/src/main/java/in/vyasastro/app/MainActivity.java', 'r', encoding='utf-8') as f:
    code = f.read()

print("Contains WebAppInterface:", 'WebAppInterface' in code)
print("Contains @JavascriptInterface:", '@JavascriptInterface' in code)
import re
print("JavascriptInterface methods:")
for m in re.finditer(r'@JavascriptInterface\s+public\s+([^\(]+)\(([^\)]*)\)', code):
    print(" ", m.group(1).strip(), "(", m.group(2).strip(), ")")

