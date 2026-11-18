with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"app.py has {len(lines)} lines")
for i, line in enumerate(lines[:100]):
    if any(k in line for k in ['import', 'calculate', 'ephemeris', 'kundli', 'ayanamsa']):
        print(f"Line {i+1}: {line.strip()}")

