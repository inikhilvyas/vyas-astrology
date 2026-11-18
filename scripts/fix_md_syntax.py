with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad_str = "onclick=\"VyasDesktop.toggleDashaChildren('md', ' + m + ')\""
good_str = "onclick=\"VyasDesktop.toggleDashaChildren(\\'md\\', ' + m + ')\""

if bad_str in content:
    content = content.replace(bad_str, good_str)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("FIXED: Successfully escaped 'md' in index.html!")
else:
    print("NOT FOUND: bad_str was not found directly, checking regex...")
    import re
    pat = re.compile(r"VyasDesktop\.toggleDashaChildren\('md',\s*'\s*\+\s*m")
    if pat.search(content):
        content = pat.sub(r"VyasDesktop.toggleDashaChildren(\\'md\\', ' + m", content)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("FIXED via regex!")
    else:
        print("Regex also did not match.")

