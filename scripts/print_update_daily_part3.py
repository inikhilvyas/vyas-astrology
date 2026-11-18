with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI() {')
print(text[pos+6500:pos+10500])

