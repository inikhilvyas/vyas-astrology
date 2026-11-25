with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

import re

def get_fn(text, label):
    idx = text.find('computeMathematicalKundli(')
    if idx == -1:
        idx = text.find('computeMathematicalKundli')
    print(f"=== {label} at {idx} ===")
    end = text.find('return {', idx)
    print(text[idx:min(len(text), idx+2000)])
    print("-" * 50)

get_fn(d_text, "DESKTOP")
get_fn(m_text, "MOBILE")

