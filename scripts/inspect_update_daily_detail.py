with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI() {')
end = text.find('// -------------------------------------------------------------', pos + 300)
print(text[pos:pos+1600])

