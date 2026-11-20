with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "var kRole = (k.sig || k.role || k.karkatva || 'शास्त्रीय फल');",
    "var kRole = (k.sig || k.karkatva || 'शास्त्रीय फल');"
)

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Replaced k.role successfully!")
