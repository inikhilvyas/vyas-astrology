for path in ['index.html', 'mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('alert("📍 GPS स्थान प्राप्त:\n"', 'alert("📍 GPS स्थान प्राप्त:\\n"')
    c = c.replace('alert("📍 GPS स्थान प्राप्त:\r\n"', 'alert("📍 GPS स्थान प्राप्त:\\n"')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
print('Fixed unescaped alert newlines successfully!')
