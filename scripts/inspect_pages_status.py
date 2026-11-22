import re, json

def inspect_ashtakavarga():
    with open('ashtakavarga/index.html', 'r', encoding='utf-8') as f:
        c = f.read()
    print("=== ASHTAKAVARGA ===")
    for m in re.finditer(r'card-title[^>]*>(.*?)</div>', c):
        print("  Card title:", re.sub('<[^<]+?>', '', m.group(1)).strip())
    # Check if there is 12 house analysis or kakshya analysis
    print("  Has 12 bhavas SAV:", 'द्वादश भाव सर्वाष्टकवर्ग' in c or 'SAV फलित' in c)
    print("  Has Prastara Kakshya details:", 'प्रस्ताराष्टकवर्ग' in c)

def inspect_varshphal():
    with open('varshphal/index.html', 'r', encoding='utf-8') as f:
        c = f.read()
    print("\n=== VARSHPHAL ===")
    for m in re.finditer(r'card-title[^>]*>(.*?)</div>', c):
        print("  Card title:", re.sub('<[^<]+?>', '', m.group(1)).strip())

def inspect_nadi():
    with open('nadi-astrology/index.html', 'r', encoding='utf-8') as f:
        c = f.read()
    print("\n=== NADI ===")
    for m in re.finditer(r'card-title[^>]*>(.*?)</div>', c):
        print("  Card title:", re.sub('<[^<]+?>', '', m.group(1)).strip())

if __name__ == '__main__':
    inspect_ashtakavarga()
    inspect_varshphal()
    inspect_nadi()
