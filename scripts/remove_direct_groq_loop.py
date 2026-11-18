for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()

    start_marker = "// Tier 2: Direct client-side attempt with key rotation"
    end_marker = "// 3. High-precision dynamic local astrological reasoning fallback"

    p1 = text.find(start_marker)
    p2 = text.find(end_marker, p1)

    if p1 != -1 and p2 != -1:
        text = text[:p1] + text[p2:]
        print(f"✓ Removed direct Groq loop from {fp}")
    else:
        print(f"! Marker not found in {fp}, p1={p1}, p2={p2}")

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(text)

# verify
for fp in ['index.html', 'mobile/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        t = f.read()
    print(f"{fp}: 'api.groq.com' count = {t.count('api.groq.com')}, 'gsk_' count = {t.count('gsk_')}")

