with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("Soul's", "Soul\\'s")
text = text.replace("Jaimini's", "Jaimini\\'s")
text = text.replace("Planets represent the source", 'Planets represent the source')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✓ Fixed single quote escapes.")

