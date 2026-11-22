with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Check modalProManager structure
target = '<div style="margin-bottom:22px;">\n                <b style="color:#d4af37; font-size:0.90rem; display:block; margin-bottom:12px;">✦ सदस्यता प्लान चुनें'
print("Found target in index.html:", target in code)

