with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderChart(vargaKey) {')
if pos == -1:
    pos = text.find('renderChart:')
if pos == -1:
    pos = text.find('renderChart')
    pos = text.find('renderChart', pos + 20)

print(pos)
print(text[pos:pos+1500])

