with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI: function')
if pos == -1:
    pos = text.find('updateDailyHoroscopeUI()')
print(text[pos:pos+1000])

