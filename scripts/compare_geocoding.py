with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

d_start = d_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')
m_start = m_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')

print("=== DESKTOP GEOCODING (chars around lat/lon) ===")
print(d_text[d_start+1500:d_start+3500])
print("\n" + "="*70 + "\n")
print("=== MOBILE GEOCODING (chars around lat/lon) ===")
print(m_text[m_start+1500:m_start+3500])

