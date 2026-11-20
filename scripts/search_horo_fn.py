with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI')
while pos != -1:
    print("Match at", pos, text[pos-30:pos+100].replace('\n', ' '))
    pos = text.find('updateDailyHoroscopeUI', pos+20)

