import re
import subprocess
import sys

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Total script tags in mobile: {len(scripts)}")

has_error = False
for idx, s in enumerate(scripts):
    if not s.strip():
        continue
    if 'schema.org' in s or '"@context"' in s:
        continue
    res = subprocess.run(['node', '--check', '-'], input=s, text=True, capture_output=True)
    if res.returncode != 0:
        has_error = True
        print(f"Mobile Script #{idx} HAS SYNTAX ERROR:")
        print(res.stderr)
    else:
        print(f"Mobile Script #{idx} syntax OK!")

if not has_error:
    print("ALL JAVASCRIPT BLOCKS IN MOBILE/INDEX.HTML HAVE ZERO SYNTAX ERRORS!")

