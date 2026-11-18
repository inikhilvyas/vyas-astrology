with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

pos = m_text.find('computeMathematicalKundli')
print("computeMathematicalKundli in mobile at", pos)

