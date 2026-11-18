with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderChart(vargaKey)')
if pos == -1:
    pos = text.find('renderChart')
print(text[pos:pos+1500])

