with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderPanchang: function()')
import re
match = re.search(r'\n\s*([a-zA-Z0-9_]+)\s*[:(]', text[pos+200:])
if match:
    print("Match:", match.group(0), "at", pos + 200 + match.start())
    p2 = pos + 200 + match.start()
    print(text[p2-200:p2+300])

