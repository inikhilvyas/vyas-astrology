import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect generateDiamondSVG around house sign calculation
idx = content.find('generateDiamondSVG(housesData, size, title)')
print("generateDiamondSVG found at:", idx)
sub = content[idx:idx+4000]
m = re.search(r'for\s*\(\s*var\s+house\s*=\s*1\s*;\s*house\s*<=\s*12\s*;\s*house\+\+\s*\)\s*\{', sub)
if m:
    print("Found house loop at relative pos:", m.start())
    print(sub[m.start():m.start()+1000])

