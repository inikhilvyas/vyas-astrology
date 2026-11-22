with open('ashtakavarga/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("३° ४५'</span>", "३° ४५&#39;</span>")
c = c.replace("३° ४५\'</span>", "३° ४५&#39;</span>")

with open('ashtakavarga/index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed quotes in ashtakavarga/index.html")
