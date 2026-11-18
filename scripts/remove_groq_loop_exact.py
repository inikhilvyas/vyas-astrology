for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    pos_for = text.find('for (var attempt = 0; attempt < this.keyPool.length')
    pos_end_for = text.find('this.currentKeyIndex = (this.currentKeyIndex + 1) % this.keyPool.length;\n            }')

    if pos_for != -1 and pos_end_for != -1:
        end_idx = pos_end_for + len('this.currentKeyIndex = (this.currentKeyIndex + 1) % this.keyPool.length;\n            }')
        text = text[:pos_for] + text[end_idx:]
        print(f"✓ Removed for-attempt-groq-loop from {fp}")
    else:
        print(f"! Not found in {fp}: pos_for={pos_for}, pos_end_for={pos_end_for}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)

# verify
for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()
    print(f"{fp}: 'api.groq.com' count = {t.count('api.groq.com')}, 'gsk_' count = {t.count('gsk_')}")

