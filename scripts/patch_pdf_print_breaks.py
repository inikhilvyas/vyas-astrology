with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Replace hard page breaks in PDF print with smart container breaks
code = code.replace("chartsHtml +\n                    '<div style=\"page-break-before:always;\"></div>' +", "chartsHtml +")
code = code.replace("'<div style=\"page-break-before:always;\"></div>' +\n                                    '<div class=\"section-title\"", "'<div class=\"section-title\"")
code = code.replace("'<div style=\"page-break-before:always;\"></div>' +\n                    '<div style=\"margin-top:40px;", "'<div style=\"margin-top:40px;")

# Add smart print CSS
old_print_style = "'.sav-table td { background:#f8fafc; }' +"
new_print_style = "'.sav-table td { background:#f8fafc; }' +\n                    '.doc-section, .info-grid, .dasha-box, table, .certification-seal { break-inside: avoid; page-break-inside: avoid; margin-bottom: 20px; }' +\n                    '.section-title { break-after: avoid; page-break-after: avoid; }' +"

if old_print_style in code:
    code = code.replace(old_print_style, new_print_style)

# Sanitize founder email and name in PDF print header/footer
code = code.replace(
    '<div class="doc-founder">शोध पीठ निदेशक: <b>निखिल व्यास</b>, M.A. (Jyotish), LL.B • ईमेल: inikhilvyas@gmail.com</div>',
    '<div class="doc-founder">शोध पीठ: <b>व्यास अस्त्र वैदिक शोध संस्थान</b> • NASA JPL 0.001″ उच्च-परिशुद्धता खगोलीय वेध</div>'
)

code = code.replace(
    '<div><span style="font-size:13px; color:#64748b;">शोध निदेशक:</span><br><b style="font-size:16px; color:#1e3a8a;">निखिल व्यास</b><br><span style="font-size:12px; color:#64748b;">M.A. (Jyotish), LL.B</span></div>',
    '<div><span style="font-size:13px; color:#64748b;">प्रमाणन:</span><br><b style="font-size:16px; color:#1e3a8a;">आचार्य दैवज्ञ मण्डल</b><br><span style="font-size:12px; color:#64748b;">व्यास अस्त्र शोध पीठ</span></div>'
)

# Sanitize proUserEmailText default if present
code = code.replace(
    '<b id="proUserEmailText" style="color:#f8fafc;">निखिल व्यास (संस्थापक • Verified VIP)</b>',
    '<b id="proUserEmailText" style="color:#f8fafc;">सत्यापित प्रो सदस्य (Verified VIP)</b>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: index.html PDF print breaks & privacy sanitization updated!")

