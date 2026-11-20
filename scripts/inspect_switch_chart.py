with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('switchChart(')
if idx != -1:
    print(content[idx-100:idx+1500])

