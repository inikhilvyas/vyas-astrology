import os, glob

md_files = glob.glob('books/*.md')
print(f"Total markdown books in books/: {len(md_files)}")
total_bytes = sum(os.path.getsize(f) for f in md_files)
print(f"Total size of books: {total_bytes / (1024*1024):.2f} MB")

# Check if vyas_sutras_bank.js is loaded in index.html
with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    h = f.read()

print("index.html loads vyas_sutras_bank.js:", 'vyas_sutras_bank.js' in h)
import re
print("Script tags matching sutra:", re.findall(r'<script[^>]*sutra[^>]*>.*?</script>|<script[^>]*src=[\'"][^\'"]*sutra[^\'"]*[\'"]', h))

# Check vyas_sutras_bank.js content
with open('js/vyas_sutras_bank.js', 'r', encoding='utf-8', errors='ignore') as f:
    header = f.read(500)
print("vyas_sutras_bank.js header snippet:\n", header[:300])

