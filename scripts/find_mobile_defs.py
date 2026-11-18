with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

pos = m_text.find('computeMathematicalKundli(')
pos = m_text.find('computeMathematicalKundli(', pos+30)
while pos != -1:
    print(f"Pos {pos}:", m_text[pos-40:pos+120])
    pos = m_text.find('computeMathematicalKundli(', pos+30)

