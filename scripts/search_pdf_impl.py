with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['generatePDF', 'window.print', 'downloadPdf', 'printReport', 'pdf-container', 'html2pdf']):
        print(f"{i+1}: {l.strip()[:100]}")

