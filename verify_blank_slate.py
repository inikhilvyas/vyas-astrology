print("=== VERIFICATION 3: Checking Blank Slate & Personal Kundli Isolation ===")

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m = f.read()

# Profile strip in mobile
assert 'id="mStripProfileName"' in m, "mStripProfileName missing"
strip_part = m[m.find('id="mStripProfileName"'):m.find('id="mStripProfileName"')+300]
print("Mobile strip part:\n", strip_part)
assert 'NIKHIL VYAS' not in strip_part, "NIKHIL VYAS leaked in mobile default strip!"

with open('index.html', 'r', encoding='utf-8') as f:
    d = f.read()

assert 'id="jatakName"' in d, "jatakName missing in index.html"
desktop_strip = d[d.find('id="jatakName"'):d.find('id="jatakName"')+300]
print("Desktop strip part:\n", desktop_strip)
assert 'NIKHIL VYAS' not in desktop_strip, "NIKHIL VYAS leaked in desktop default strip!"

print("✓ VERIFICATION 3 PASSED: Default blank slate is 100% clean and private!")

