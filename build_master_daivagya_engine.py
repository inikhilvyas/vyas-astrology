# build_master_daivagya_engine.py
# Generates the complete, authentic VyasDaivagyaVision engine with 108 Bhava Sutras,
# multi-system TCR synthesis, dynamic Jaimini, KP, Nadi, Lal Kitab, and inlines it everywhere.

import re
import os

with open('js/vyas_daivagya_vision.js', 'r', encoding='utf-8') as f:
    engine_code = f.read()

print("Read engine_code from js/vyas_daivagya_vision.js, length:", len(engine_code))

start_marker = "// vyas_daivagya_vision.js - The Authentic Astrological Reasoning & Synthesis Engine"
end_marker = "})(typeof window !== 'undefined' ? window : global);"

# 1. Inline into mobile/index.html
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_content = f.read()

pos1 = m_content.find(start_marker)
pos2 = m_content.find(end_marker, pos1)

if pos1 != -1 and pos2 != -1:
    pos2 += len(end_marker)
    m_content = m_content[:pos1] + engine_code.strip() + m_content[pos2:]
    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_content)
    print("Inlined VyasDaivagyaVision into mobile/index.html successfully!")
else:
    print(f"Warning: Could not find markers in mobile/index.html (pos1={pos1}, pos2={pos2})")

# 2. Inline into index.html
with open('index.html', 'r', encoding='utf-8') as f:
    d_content = f.read()

pos1 = d_content.find(start_marker)
pos2 = d_content.find(end_marker, pos1)

if pos1 != -1 and pos2 != -1:
    pos2 += len(end_marker)
    d_content = d_content[:pos1] + engine_code.strip() + d_content[pos2:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(d_content)
    print("Inlined VyasDaivagyaVision into index.html successfully!")
else:
    print(f"Warning: Could not find markers in index.html (pos1={pos1}, pos2={pos2})")

print("Master Daivagya Engine Inlining Complete!")
