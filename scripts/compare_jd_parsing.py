with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

for label, text in [("DESKTOP", d_text), ("MOBILE", m_text)]:
    idx = text.find('jd0 = Math.floor')
    print(f"=== {label} jd0 at {idx} ===")
    print(text[max(0, idx-800):min(len(text), idx+400)])
    print("-" * 50)

