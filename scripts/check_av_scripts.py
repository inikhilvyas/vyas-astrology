with open('ashtakavarga/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("Contains VyasAshtakavargaEngine:", 'VyasAshtakavargaEngine' in c)
import re
print("Script sources in ashtakavarga:")
for s in re.findall(r'<script[^>]*src=[\'"][^\'"]*[\'"]', c):
    print(" ", s)

