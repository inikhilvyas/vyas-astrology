with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace any range: '0°00' - 3°45'' with double quotes: range: "0°00' - 3°45'"
import re
c = re.sub(r"range:\s*'([^']*)'([^']*)''", r'range: "\1\'\2\'"', c)
c = c.replace("range: '0°00' - 3°45''", 'range: "0°00\' - 3°45\'"')
c = c.replace("range: '3°45' - 7°30''", 'range: "3°45\' - 7°30\'"')
c = c.replace("range: '7°30' - 11°15''", 'range: "7°30\' - 11°15\'"')
c = c.replace("range: '11°15' - 15°00''", 'range: "11°15\' - 15°00\'"')
c = c.replace("range: '15°00' - 18°45''", 'range: "15°00\' - 18°45\'"')
c = c.replace("range: '18°45' - 22°30''", 'range: "18°45\' - 22°30\'"')
c = c.replace("range: '22°30' - 26°15''", 'range: "22°30\' - 26°15\'"')
c = c.replace("range: '26°15' - 30°00''", 'range: "26°15\' - 30°00\'"')

# Also check for any 3°45' unescaped in comments/strings
c = c.replace("इस 3°45' अंतराल", "इस ३°४५' अंतराल")

with open('js/vyas_daivagya_engine.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed quotes in js/vyas_daivagya_engine.js")
