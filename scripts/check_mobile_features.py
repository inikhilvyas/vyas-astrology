with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

print("Length of mobile/index.html:", len(m_text))
for q in ['Abhijit', 'abhijit', 'panchang', 'VyasDayIndex', 'vIndex', 'Sampat', 'Mitra', 'quickLogin']:
    print(f"'{q}': {m_text.count(q)}")

