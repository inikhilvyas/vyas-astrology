with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

print('mobile/index.html length:', len(m_text))

import re
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', m_text)
print('Script src tags in mobile/index.html:')
for s in scripts:
    print('  -', s)

print('\nCheck keywords in mobile/index.html:')
for kw in ['calculateLagna', 'ascendant', 'computeKundli', 'getActiveKundli', 'VyasAstronomicalEngine', 'ayanamsha', 'lahiri', 'google', 'oauth', 'ashtakavarga', 'sav-table', 'ashtakvarga']:
    matches = list(re.finditer(kw, m_text, re.IGNORECASE))
    print(f'  {kw}: {len(matches)} occurrences')
    if matches and len(matches) <= 3:
        for m in matches:
            idx = m.start()
            print(f'    [{idx}]: {m_text[max(0, idx-50):min(len(m_text), idx+100)].strip()}')

