# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "आपकी जिज्ञासा:" in line:
        print(f"Found at line {i+1}: {line}")
        lines[i] = '                "<span style=\'color:var(--accent-gold); font-weight:700; font-size:0.85rem;\'>✦ आपकी जिज्ञासा: &quot;" + (query || "समग्र फलादेश") + "&quot;</span>" +\n'
        print(f"Replaced with: {lines[i]}")
        break

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")

