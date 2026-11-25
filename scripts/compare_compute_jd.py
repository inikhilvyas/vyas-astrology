with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

d_start = d_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')
m_start = m_text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr')

d_jd = d_text.find('jd0 =', d_start)
m_jd = m_text.find('jd0 =', m_start)

print("=== DESKTOP computeMathematicalKundli Time & JD calculation ===")
print(d_text[d_jd-1200:d_jd+600])
print("\n" + "="*70 + "\n")
print("=== MOBILE computeMathematicalKundli Time & JD calculation ===")
print(m_text[m_jd-1200:m_jd+600])

