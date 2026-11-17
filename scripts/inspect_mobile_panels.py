with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for v in ['view-kp', 'view-jaimini', 'view-nadi', 'view-predictions']:
    m = re.search(r'<div class="m-view-panel"[^>]*id="' + v + r'"', text)
    if m:
        start = m.start()
        end = text.find('</div>\n            </div>', start)
        if end == -1:
            end = start + 1500
        print(f"=== MOBILE {v} ===")
        print(text[start:start+600])
        print("... [snip] ...")
        print(text[end-200:end+20])

