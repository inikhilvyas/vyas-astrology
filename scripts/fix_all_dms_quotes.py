import re

print("Fixing unescaped double quotes in index.html and mobile/index.html...")

for filepath in ['index.html', 'mobile/index.html']:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Pattern: "X°Y'Z"" -> replace with 'X°Y\'Z"'
    # e.g., "7°42'50"" -> '7°42\'50"'
    def fix_dms_quote(match):
        val = match.group(1) # e.g. 7°42'50"
        return "'" + val.replace("'", "\\'") + "'"

    # Match: "(\d+°\d+['’]\d+)" followed by "
    # or dms: "..."
    # Let's do a targeted regex:
    # "(\d+°\d+['’]\d+)""
    new_text = re.sub(r'"(\d+°\d+[\'’]\d+)""', r"'\1\"'", text)
    new_text = re.sub(r'd:\s*"(\d+°\d+[\'’]\d+)""', r"d: '\1\"'", new_text)
    new_text = re.sub(r'dms:\s*"(\d+°\d+[\'’]\d+)""', r"dms: '\1\"'", new_text)
    new_text = re.sub(r'asc_dms:\s*"(\d+°\d+[\'’]\d+)""', r"asc_dms: '\1\"'", new_text)

    # Also handle if already had \"
    # Check if any remaining "(\d+°\d+'\d+)"" exist
    remaining = re.findall(r'.{0,20}\d+°\d+[\'’]\d+"".{0,20}', new_text)
    print(f"Remaining in {filepath}: {len(remaining)}")
    if remaining:
        print("Examples:", remaining[:3])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)

print("Replacement complete. Verifying syntax now...")

