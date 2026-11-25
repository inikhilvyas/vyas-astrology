with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

d_idx = d_text.find('// 1. Exact Julian Date & Ephemeris Time')
m_idx = m_text.find('// 1. Exact Julian Date & Ephemeris Time')

print("=== DESKTOP TIME PARSING ===")
print(d_text[d_idx-300:d_idx+600])
print("\n" + "="*70 + "\n")
print("=== MOBILE TIME PARSING ===")
print(m_text[m_idx-300:m_idx+600])

