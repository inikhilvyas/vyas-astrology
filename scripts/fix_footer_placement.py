with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the incorrectly placed footer inside printWin
bad_footer = '''    <!-- VYAS ASTRA OFFICIAL FOOTER & SOLE FOUNDER ACCREDITATION -->
    <footer style="margin-top:50px; padding:28px 16px; border-top:1px solid rgba(212,175,55,0.25); background:rgba(3,7,18,0.95); text-align:center; font-size:0.82rem; color:#94a3b8; line-height:1.7;">
        <div style="color:#d4af37; font-weight:700; font-size:0.92rem; margin-bottom:6px; letter-spacing:0.5px;">✦ VYAS ASTRA • प्रामाणिक वैदिक खगोल-शास्त्र एवं दैवज्ञ प्रणाली ✦</div>
        <div style="color:#f8fafc; font-size:0.85rem; margin-bottom:4px;">
            संस्थापक एवं प्रधान दैवज्ञ: <b style="color:#d4af37;">Nikhil Vyas</b>, M.A.(Jyotish), LL.B • Pali (Rajasthan) • Mob: <b style="color:#38bdf8;">9414121172</b>
        </div>
        <div style="font-size:0.72rem; color:#64748b; margin-top:6px;">
            © 2026 VYAS ASTRA. समस्त अधिकार सुरक्षित। नासा JPL एवं स्विस्स एफेमेरिस 0.001" आर्कसेकंड परिशुद्धता।
        </div>
    </footer>
'''

if bad_footer in html:
    html = html.replace(bad_footer, '')
    print("✓ Removed misplaced footer from printWin template string")

# Now put the footer right before the LAST </body> in the file
last_body = html.rfind('</body>')
if last_body != -1:
    footer = '''    <!-- VYAS ASTRA OFFICIAL FOOTER & SOLE FOUNDER ACCREDITATION -->
    <footer style="margin-top:50px; padding:28px 16px; border-top:1px solid rgba(212,175,55,0.25); background:rgba(3,7,18,0.95); text-align:center; font-size:0.82rem; color:#94a3b8; line-height:1.7;">
        <div style="color:#d4af37; font-weight:700; font-size:0.92rem; margin-bottom:6px; letter-spacing:0.5px;">✦ VYAS ASTRA • प्रामाणिक वैदिक खगोल-शास्त्र एवं दैवज्ञ प्रणाली ✦</div>
        <div style="color:#f8fafc; font-size:0.85rem; margin-bottom:4px;">
            शोध एवं मार्गदर्शन: <b style="color:#d4af37;">Nikhil Vyas</b>, M.A.(Jyotish), LL.B • Pali (Rajasthan) • Mob: <b style="color:#38bdf8;">9414121172</b>
        </div>
        <div style="font-size:0.72rem; color:#64748b; margin-top:6px;">
            © 2026 VYAS ASTRA. समस्त अधिकार सुरक्षित। नासा JPL एवं स्विस्स एफेमेरिस 0.001" आर्कसेकंड परिशुद्धता।
        </div>
    </footer>
'''
    html = html[:last_body] + footer + html[last_body:]
    print("✓ Inserted footer right before the final </body> tag")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

