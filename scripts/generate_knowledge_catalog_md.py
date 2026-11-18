import json
import os

with open('scripts/gdrive_master_books_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

# Sort by folder and name
catalog.sort(key=lambda x: (x.get('folder', 'Root'), x['name']))

md_lines = [
    "# VYAS DAIVAGYA KNOWLEDGE BANK — VEDIC ASTROLOGY TREATISES CATALOG",
    "",
    "> **स्रोत (Source)**: Google Drive Public Rare Jyotish Collection (`0B8PLpDKw1NhKVFUyVzB3QXdTMEE`)",
    "> **संरचना (Format)**: Markdown (`.md`) व JSON (`.json`) नॉलेज बेस (99% साइज़ कम्प्रेशन, AI-रेडी, RAG-सर्च)",
    "",
    "---",
    "",
    "## 📚 वर्गीकृत ग्रंथ सूची (Categorized Master Index)",
    ""
]

current_folder = None
for item in catalog:
    folder = item.get('folder', 'Root')
    if folder != current_folder:
        current_folder = folder
        md_lines.append(f"\n### 🏛️ {current_folder}")
        md_lines.append("")
        md_lines.append("| क्र. | ग्रन्थ / पुस्तक का नाम | Google Drive ID | लक्षित फॉर्मेट | स्थिति |")
        md_lines.append("|:---|:---|:---|:---|:---|")
        idx = 1
    
    name = item['name']
    fid = item['id']
    clean_name = name.replace('.pdf', '')
    md_lines.append(f"| {idx} | **{clean_name}** | `{fid}` | `.md` / `.json` | Ready for Ingestion |")
    idx += 1

md_lines.append("\n---\n")
md_lines.append("## 🚀 कन्वर्ज़न व नॉलेज बैंक एकीकरण योजना (Ingestion Architecture)")
md_lines.append("1. **साइज कम्प्रेशन (99% Reduction)**: भारी 30-100MB की PDF फाइल्स टेक्स्ट-एक्सट्रैक्शन के बाद 200KB - 800KB के लाइटवेट `.md` व `.json` में सुरक्षित होती हैं।")
md_lines.append("2. **श्लोक व फलित इंडेक्सिंग (Sutra & Phalit Index)**: प्रत्येक श्लोक का भाव (1-12 भाव), ग्रह (सूर्य-केतु), दशा व गोचर से सीधा टैगिंग।")
md_lines.append("3. **व्यासास्त्र AI इंजन लिंकेज**: `data/vyas_phalit_vault.db` में सीधे इन्सर्ट होकर आचार्य व्यास चैट, दैनिक राशिफल व कुंडली विश्लेषण में प्रमाण-सहित उद्धृत होगा।")

os.makedirs('books', exist_ok=True)
with open('books/KNOWLEDGE_BANK_CATALOG.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(md_lines))

print("Created books/KNOWLEDGE_BANK_CATALOG.md successfully!")

