with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('switchChart:')
if idx == -1:
    idx = content.find('switchChart(')
    idx = content.find('switchChart', idx+1)
print('switchChart at:', idx)
print(content[idx:idx+1500])

