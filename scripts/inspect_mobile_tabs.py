with open('cpp/desktop/main_gui.cpp', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('DrawKPAndJaiminiTable')
print(text[pos+2500:pos+5500])
