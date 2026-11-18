with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateDailyHoroscopeUI:')
if pos != -1:
    print("Found updateDailyHoroscopeUI: at pos", pos)
    print(text[pos:pos+2500])
else:
    print("Not found exact 'updateDailyHoroscopeUI:'")
    # let's search for updateDailyHoroscopeUI
    import re
    for m in re.finditer(r'updateDailyHoroscopeUI\s*\(', text):
        print(text[m.start():m.start()+1500])

