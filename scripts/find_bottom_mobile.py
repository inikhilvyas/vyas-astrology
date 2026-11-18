with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'class="[^"]*bottom[^"]*"', text)
if m:
    print('Bottom class match:', m.group(0))
    pos = m.start()
    print(text[pos-100:pos+500])
else:
    print('No bottom class found.')

