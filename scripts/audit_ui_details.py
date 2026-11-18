import re

def audit_emojis_and_tabs(filepath, label):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find emojis (Unicode ranges)
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]')
    emojis_found = {}
    
    for i, line in enumerate(content.split('\n')):
        matches = emoji_pattern.findall(line)
        if matches:
            for em in matches:
                if em not in emojis_found:
                    emojis_found[em] = []
                if len(emojis_found[em]) < 5:
                    clean_line = line.strip()[:100]
                    emojis_found[em].append((i+1, clean_line))

    # Find tabs
    tab_matches = re.findall(r'<button\b[^>]*class=["\'][^"\']*(?:tab-nav-btn|nav-tab|tab-btn|m-nav-item|bottom-nav-item)[^"\']*["\'][^>]*>(.*?)</button>', content, re.DOTALL | re.IGNORECASE)
    clean_tabs = []
    for t in tab_matches:
        txt = re.sub(r'<[^>]+>', '', t).strip()
        if txt and txt not in clean_tabs:
            clean_tabs.append(txt)

    # View panels
    panels = re.findall(r'id=["\'](?:view-|tab-|panel-)([a-zA-Z0-9_\-]+)["\']', content)

    print(f"=== {label} AUDIT ===")
    print(f"Total Unique Emojis: {len(emojis_found)}")
    for em, locs in sorted(emojis_found.items()):
        print(f"Emoji '{em}' ({len(locs)} occurrences sampled):")
        for line_num, snippet in locs[:2]:
            print(f"   L{line_num}: {snippet}")

    print(f"\nUnique Tabs Found ({len(clean_tabs)}):")
    for t in clean_tabs:
        print(f"   - {t}")

    print(f"\nView Panels Found ({len(panels)}):")
    print(f"   {set(panels)}")
    print("\n" + "="*50 + "\n")

audit_emojis_and_tabs('index.html', 'PC DESKTOP (index.html)')
audit_emojis_and_tabs('mobile/index.html', 'MOBILE (mobile/index.html)')

