import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Check SHODASHAVARGA_DATA in index.html
matches = re.findall(r'\"key\":\s*\"(D\d+)\"[\s\S]*?\"ascSign\":\s*\"([^\"]+)\"', text[200000:350000])
print("Static SHODASHAVARGA_DATA ascSigns:")
for m in matches:
    print(f"  {m[0]}: {m[1]}")

# 2. Check why user said: 'D charts bhi galat hai. sab me mesh lagna aane lag gaya.'
# Let's check how activeChartData.charts is constructed for Nikhil Vyas
idx = text.find('computeMathematicalKundli')
idx2 = text.find('var isNikhilVyas', idx)
print("\nisNikhilVyas block starts at", idx2)
print(text[idx2:idx2+600])
