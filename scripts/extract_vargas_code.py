with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract calcVargasDetailed function
idx = text.find('function calcVargasDetailed(lon) {')
idx2 = text.find('var ascVargas = calcVargasDetailed(ascSid);', idx)
print(text[idx:idx2])

