with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 602769
# find next function in VyasDesktop
import re
for m in re.finditer(r'\n\s*([a-zA-Z0-9_]+)\s*\([^)]*\)\s*\{', text[pos+50:pos+3000]):
    print("Next fn:", m.group(1), "at", pos+50+m.start())
