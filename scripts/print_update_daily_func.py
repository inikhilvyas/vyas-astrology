with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI() {')
if pos == -1:
    pos = text.find('updateDailyHoroscopeUI')
print(f"Pos {pos}")
print(text[pos:pos+3000])

