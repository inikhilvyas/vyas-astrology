import os, re, glob

def check_broken_links_and_assets():
    html_files = [
        'index.html',
        'mobile/index.html',
        'panchang/index.html',
        'ashtakavarga/index.html',
        'varshphal/index.html',
        'nadi-astrology/index.html',
        'kundli-matching/index.html',
        'saved-kundli/index.html'
    ]
    
    missing_assets = []
    broken_hrefs = []
    
    for hf in html_files:
        if not os.path.exists(hf):
            print(f"File missing: {hf}")
            continue
        with open(hf, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check script src
        scripts = re.findall(r'<script[^>]+src=[\'"]([^\'"]+)[\'"]', content)
        for s in scripts:
            if s.startswith('http') or s.startswith('//'): continue
            s_clean = s.lstrip('/')
            if not os.path.exists(s_clean):
                missing_assets.append((hf, 'script', s))
                
        # Check link href
        links = re.findall(r'<link[^>]+href=[\'"]([^\'"]+)[\'"]', content)
        for l in links:
            if l.startswith('http') or l.startswith('//'): continue
            l_clean = l.lstrip('/')
            if not os.path.exists(l_clean):
                missing_assets.append((hf, 'stylesheet/icon', l))

    print(f"Missing internal assets count: {len(missing_assets)}")
    for ma in missing_assets:
        print("  Missing:", ma)

check_broken_links_and_assets()

