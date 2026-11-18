with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

pos = 295346
print(m_text[pos:pos+1500])

