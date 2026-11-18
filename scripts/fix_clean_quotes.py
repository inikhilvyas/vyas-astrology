import re

for filepath in ['index.html', 'mobile/index.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Match 'X°Y'Z"' or 'X°Y'Z\"'
    # Replace with "X°Y'Z\""
    def repl(m):
        deg = m.group(1)
        minute = m.group(2)
        sec = m.group(3)
        return f'"{deg}°{minute}\'{sec}\\""'

    text = re.sub(r'[\'"](\d+)°(\d+)[\'’](\d+)[\\\'"]*[\'"]', repl, text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Updated with properly escaped double quotes!")

