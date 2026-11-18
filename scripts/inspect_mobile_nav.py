with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
bottom_bar = re.search(r'<div class="m-bottom-nav".*?</div>', text, re.DOTALL)
if bottom_bar:
    print('Found m-bottom-nav:')
    print(bottom_bar.group(0)[:400])
else:
    print('m-bottom-nav not found directly, searching nav elements:')
    navs = re.findall(r'<nav\b[^>]*>.*?</nav>|<div class="[^"]*nav[^"]*">', text)
    print(navs[:5])

