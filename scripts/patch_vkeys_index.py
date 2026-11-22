# scripts/patch_vkeys_index.py
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'var vKeys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"];'
repl = 'var vKeys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60", "D150"];'

if target in c:
    c = c.replace(target, repl)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Added D150 to vKeys in index.html!")
else:
    print("Target not found or already patched.")

