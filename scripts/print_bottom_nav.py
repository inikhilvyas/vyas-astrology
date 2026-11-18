with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<nav class="bottom-nav-bar">.*?</nav>', text, re.DOTALL)
if m:
    print(m.group(0))

