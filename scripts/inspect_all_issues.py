with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

print("=== 1. Occurrences of 'संस्थापक' ===")
for m in re.finditer(r'संस्थापक', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print("MATCH at", m.start(), ":", repr(text[start:end]))

print("\n=== 2. Occurrences of 'Nikhil' or 'निखिल' ===")
matches = list(re.finditer(r'(?:Nikhil|निखिल)', text, re.IGNORECASE))
print(f"Total occurrences: {len(matches)}")
for m in matches[:15]:
    start = max(0, m.start() - 80)
    end = min(len(text), m.end() + 80)
    print("MATCH at", m.start(), ":", repr(text[start:end]))

print("\n=== 3. Occurrences of '26°55' or '26*55' or Kanya Lagna ===")
for m in re.finditer(r'26[°\*]55', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print("MATCH at", m.start(), ":", repr(text[start:end]))

print("\n=== 4. Occurrences of 'कुल सुरक्षित चार्ट' ===")
for m in re.finditer(r'कुल सुरक्षित चार्ट', text):
    start = max(0, m.start() - 100)
    end = min(len(text), m.end() + 100)
    print("MATCH at", m.start(), ":", repr(text[start:end]))

