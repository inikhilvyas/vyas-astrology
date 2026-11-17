with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
views = ['view-predictions', 'view-kp', 'view-jaimini', 'view-nadi']
for v in views:
    m = re.search(r'<div class="view-panel" id="' + v + r'">', text)
    if m:
        start = m.start()
        # Find next view panel or end
        m_next = re.search(r'<div class="view-panel"', text[start+30:])
        if m_next:
            end = start + 30 + m_next.start()
        else:
            end = start + 2000
        print(f"=== {v} ===")
        print(text[start:start+400])
        print("... [snip] ...")
        print(text[end-300:end])

