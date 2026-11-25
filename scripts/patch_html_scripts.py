# -*- coding: utf-8 -*-

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<script src="js/vyas_treatise_engine.js"></script>'
replacement = '''<script src="js/vyas_treatise_sutras.js"></script>
    <script src="js/vyas_treatise_engine.js"></script>'''

if target in text and 'js/vyas_treatise_sutras.js' not in text:
    text = text.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added vyas_treatise_sutras.js to index.html")
else:
    print("index.html already has vyas_treatise_sutras.js or target not found")

# 2. Update mobile/index.html
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

m_target = """    <script src="../js/vyas_kp_horary_solver.js"
        onerror="this.onerror=null;this.src='/js/vyas_kp_horary_solver.js';"></script>"""

m_replacement = """    <script src="../js/vyas_bhavat_bhavam.js"
        onerror="this.onerror=null;this.src='/js/vyas_bhavat_bhavam.js';"></script>
    <script src="../js/vyas_treatise_sutras.js"
        onerror="this.onerror=null;this.src='/js/vyas_treatise_sutras.js';"></script>
    <script src="../js/vyas_kp_horary_solver.js"
        onerror="this.onerror=null;this.src='/js/vyas_kp_horary_solver.js';"></script>"""

if m_target in m_text and 'vyas_bhavat_bhavam.js' not in m_text:
    m_text = m_text.replace(m_target, m_replacement, 1)
    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_text)
    print("Added scripts to mobile/index.html")
else:
    print("mobile/index.html already has scripts or target not found")
