# scripts/fix_syntax_in_ask_sage.py
for path in ['index.html', 'mobile/index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    old_snippet = '].join("\\n");\n\n            // 1. Try PHP Backend Proxy First'
    new_snippet = '].join("\\n");\n            }\n\n            // 1. Try PHP Backend Proxy First'

    if old_snippet in text:
        text = text.replace(old_snippet, new_snippet, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✓ Successfully closed else block in {path}")
    else:
        print(f"! Snippet not found in {path}")
