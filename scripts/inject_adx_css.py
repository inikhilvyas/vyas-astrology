with open('styles/adx_elevation.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'ADX DESIGN ENGINEER X' not in html:
    pos = html.find('</style>')
    if pos != -1:
        html = html[:pos] + "\n\n" + css + "\n" + html[pos:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Successfully injected ADX elevation CSS into index.html")
    else:
        print("! Could not find </style> in index.html")
else:
    print("ADX CSS already injected in index.html")

