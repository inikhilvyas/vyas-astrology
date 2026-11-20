with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('desktopSageChatCol')
print(content[idx-600:idx])

