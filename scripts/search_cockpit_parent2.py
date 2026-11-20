with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="desktopSageChatCol"')
idx_prev_col = content.rfind('<div class="cockpit', 0, idx - 100)
idx_prev_prev = content.rfind('<div class="cockpit', 0, idx_prev_col - 100)
idx_parent = content.rfind('<div', 0, idx_prev_prev - 50)
print(content[idx_parent:idx_parent+400])

