import os
import glob

books = glob.glob('books/*')
print(f"Total items in books: {len(books)}")
txt_and_md = [b for b in books if b.endswith(('.md', '.txt', '.json', '.pdf'))]
print(f"Markdown/Text/PDF books: {len(txt_and_md)}")
for b in sorted(txt_and_md)[:30]:
    sz = os.path.getsize(b)
    print(f"  {b} ({sz/1024:.1f} KB)")

