with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('asc_dms: "23°27\'"', 'asc_dms: "00°00\'"')
text = text.replace('(prof.asc_dms || "23°27\'")', '(prof.asc_dms || "00°00\'")')
text = text.replace('मेष 23°27\'09"', 'लग्न स्पष्ट (D-1 Asc)')
text = text.replace('23°27\'09"', '00°00\'00"')
text = text.replace('23°27′', '00°00′')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m = f.read()

m = m.replace('asc_dms: "23°27\'"', 'asc_dms: "00°00\'"')
m = m.replace('(prof.asc_dms || "23°27\'")', '(prof.asc_dms || "00°00\'")')
m = m.replace('मेष 23°27\'09"', 'लग्न स्पष्ट (D-1 Asc)')
m = m.replace('23°27\'09"', '00°00\'00"')
m = m.replace('23°27′', '00°00′')

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(m)

print("✓ Cleaned remaining DMS degrees")
