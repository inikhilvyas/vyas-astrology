with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

d_idx = d_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')
m_idx = m_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')

print("=== DESKTOP computeMathematicalKundli (first 4000 chars) ===")
print(d_text[d_idx:d_idx+3500])
print("\n" + "="*70 + "\n")
print("=== MOBILE computeMathematicalKundli (first 4000 chars) ===")
print(m_text[m_idx:m_idx+3500])

