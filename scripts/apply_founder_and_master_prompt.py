import os
import json
import re

with open('skills/vyas-jyotisha/SKILL.md', 'r', encoding='utf-8') as f:
    skill_content = f.read()

from save_prompt_text import prompt_text

print("Prompt length:", len(prompt_text))

# 1. Write js/vyas_master_system_prompt.js
js_code = f"""/**
 * VYAS 34.0 AGENTIC JYOTISHA INTELLIGENCE SYSTEM — MASTER SYSTEM PROMPT
 * Founder & Principal Researcher: Nikhil Vyas (Pali, Rajasthan)
 * Email: inikhilvyas@gmail.com | Phone/WhatsApp: +91 9414121172
 * Institutional Foundation: VYAS Research Foundation
 */
(function(global) {{
    global.VYAS_MASTER_SYSTEM_PROMPT = {json.dumps(prompt_text, ensure_ascii=False)};
    if (typeof module !== 'undefined' && module.exports) {{
        module.exports = global.VYAS_MASTER_SYSTEM_PROMPT;
    }}
}})(typeof window !== 'undefined' ? window : global);
"""

with open('js/vyas_master_system_prompt.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("Wrote js/vyas_master_system_prompt.js")

# Copy to android assets js
android_js_dir = 'android_app/app/src/main/assets/js'
if os.path.exists(android_js_dir):
    with open(os.path.join(android_js_dir, 'vyas_master_system_prompt.js'), 'w', encoding='utf-8') as f:
        f.write(js_code)
    print("Wrote android_app/app/src/main/assets/js/vyas_master_system_prompt.js")

# 2. Update api/ai_chat.php
with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    php = f.read()

prompt_json_php = json.dumps(prompt_text, ensure_ascii=False)
php_prompt_logic = f'''$vyas34MasterPrompt = {prompt_json_php};
$incomingPrompt = isset($input['systemPrompt']) ? trim($input['systemPrompt']) : '';
$systemPrompt = !empty($incomingPrompt) ? ($vyas34MasterPrompt . "\\n\\n" . $incomingPrompt) : $vyas34MasterPrompt;'''

pattern_php = r'(\$vyas34MasterPrompt\s*=[\s\S]*?\$systemPrompt\s*=[\s\S]*?;|\$systemPrompt\s*=\s*isset\(\$input\[\'systemPrompt\'\]\)[\s\S]*?;)'
if re.search(pattern_php, php):
    php = re.sub(pattern_php, lambda m: php_prompt_logic, php, count=1)
    with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
        f.write(php)
    print("Updated api/ai_chat.php successfully")
else:
    print("Could not match prompt logic in api/ai_chat.php")

# Founder HTML Footer template
founder_footer_html = '''    <!-- VYAS ASTRA OFFICIAL FOOTER & FOUNDER ACCREDITATION -->
    <footer style="margin-top:50px; padding:32px 16px; border-top:1px solid rgba(212,175,55,0.3); background:rgba(7,11,25,0.95); text-align:center; font-size:0.88rem; color:#94A3B8; line-height:1.7;">
        <div style="color:var(--accent-gold); font-weight:700; font-size:0.96rem; margin-bottom:8px; letter-spacing:0.5px;">
            ✦ VYAS ASTRA • प्रामाणिक वैदिक खगोल-शास्त्र एवं दैवज्ञ प्रणाली ✦
        </div>
        <div style="color:#E2E8F0; font-size:0.94rem; margin-bottom:6px;">
            संस्थापक एवं मुख्य शोधकर्ता: <b style="color:var(--accent-gold); font-size:1.02rem;">निखिल व्यास (Nikhil Vyas)</b> • <span style="color:#cbd5e1;">पाली, राजस्थान (Pali, Rajasthan)</span>
        </div>
        <div style="color:#CBD5E1; font-size:0.86rem; margin-bottom:6px;">
            वैदिक शोध संस्थान: <b>व्यास अस्त्र वैदिक शोध संस्थान (VYAS Research Foundation)</b> • आचार्य दैवज्ञ मण्डल
        </div>
        <div style="margin-bottom:8px; font-size:0.86rem; color:#CBD5E1;">
            📞 सम्पर्क / WhatsApp: <a href="https://wa.me/919414121172?text=नमस्ते%20निखिल%20जी,%20मुझे%20VYAS%20ASTRA%20हेतु%20जानकारी%20चाहिए।" target="_blank" style="color:#38BDF8; font-weight:700; text-decoration:none;">+91 9414121172</a> • ✉️ ईमेल: <a href="mailto:inikhilvyas@gmail.com" style="color:#38BDF8; font-weight:700; text-decoration:none;">inikhilvyas@gmail.com</a>
        </div>
        <div style="font-size:0.75rem; color:#64748B; margin-top:6px;">
            © 2026 VYAS ASTRA • सर्वाधिकार सुरक्षित • NASA JPL Swiss Ephemeris 0.001" विशुद्ध खगोलीय परिशुद्धता।
        </div>
    </footer>'''

mobile_footer_html = '''    <!-- VYAS ASTRA MOBILE FOOTER & FOUNDER ACCREDITATION -->
    <footer style="margin-top:30px; margin-bottom:80px; padding:24px 16px; border-top:1px solid rgba(212,175,55,0.25); background:rgba(7,11,25,0.95); text-align:center; font-size:0.84rem; color:#94A3B8; line-height:1.7;">
        <div style="color:var(--primary); font-weight:700; font-size:0.90rem; margin-bottom:6px;">✦ VYAS ASTRA • वैदिक खगोलीय संस्थान ✦</div>
        <div style="color:#E2E8F0; font-size:0.88rem; margin-bottom:6px;">
            संस्थापक एवं मुख्य शोधकर्ता: <b style="color:var(--primary);">निखिल व्यास (Nikhil Vyas)</b> • <span style="color:#cbd5e1;">पाली, राजस्थान (Pali, Rajasthan)</span>
        </div>
        <div style="margin-bottom:6px; font-size:0.82rem; color:#CBD5E1;">
            📞 <a href="https://wa.me/919414121172?text=नमस्ते%20निखिल%20जी" target="_blank" style="color:#38BDF8; font-weight:700; text-decoration:none;">+91 9414121172</a> • ✉️ <a href="mailto:inikhilvyas@gmail.com" style="color:#38BDF8; font-weight:700; text-decoration:none;">inikhilvyas@gmail.com</a>
        </div>
        <div style="font-size:0.72rem; color:#64748B;">
            © 2026 VYAS ASTRA • Swiss Ephemeris 0.001" परिशुद्धता
        </div>
    </footer>'''

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Make sure script tag exists
if '/js/vyas_master_system_prompt.js' not in idx:
    idx = idx.replace('<script src="/js/vyas_daivagya_engine.js"></script>', '<script src="/js/vyas_master_system_prompt.js"></script>\n    <script src="/js/vyas_daivagya_engine.js"></script>')

# Update MASTER_SYSTEM_PROMPT in index.html
idx = re.sub(
    r'MASTER_SYSTEM_PROMPT:\s*(["\'][\s\S]*?["\']|\(window\.VYAS_MASTER_SYSTEM_PROMPT\s*\|\|[\s\S]*?\)),',
    lambda m: 'MASTER_SYSTEM_PROMPT: (typeof window !== "undefined" && window.VYAS_MASTER_SYSTEM_PROMPT) ? window.VYAS_MASTER_SYSTEM_PROMPT : ' + json.dumps(prompt_text, ensure_ascii=False) + ',',
    idx,
    count=1
)

# Update footer
idx = re.sub(r'<footer[\s\S]*?</footer>', lambda m: founder_footer_html.strip(), idx, count=1)

# Update Pro Modal support box
new_support_card = '''<!-- Support / Direct Contact & UPI -->
            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(212,175,55,0.25); border-radius:10px; padding:12px 16px; margin-bottom:18px; font-size:0.78rem; color:#cbd5e1; line-height:1.6;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                    <div>
                        <b style="color:#d4af37;">📞 संस्थापक एवं सदस्यता सहायता (Founder Support):</b><br>
                        <b>निखिल व्यास (पाली, राजस्थान)</b> • WhatsApp: <a href="https://wa.me/919414121172?text=नमस्ते%20निखिल%20जी,%20मुझे%20VYAS%20ASTRA%20PRO%20सदस्यता%20सक्रिय%20करनी%20है।" target="_blank" style="color:#f1d797; text-decoration:none; font-weight:700;">+91 9414121172</a> • ईमेल: <a href="mailto:inikhilvyas@gmail.com" style="color:#f1d797; text-decoration:none; font-weight:700;">inikhilvyas@gmail.com</a>
                    </div>
                    <a href="https://wa.me/919414121172?text=नमस्ते%20निखिल%20जी,%20मुझे%20VYAS%20ASTRA%20PRO%20सदस्यता%20सक्रिय%20करनी%20है।" target="_blank" style="background:#25D366; color:#fff; padding:6px 14px; border-radius:20px; font-weight:800; text-decoration:none; display:inline-flex; align-items:center; gap:6px; font-size:0.76rem;">
                        💬 WhatsApp पर संपर्क करें
                    </a>
                </div>
            </div>'''
idx = re.sub(r'<!-- Support / Direct Contact & UPI -->[\s\S]*?<!-- License Key Activation -->', lambda m: new_support_card + '\n\n            <!-- License Key Activation -->', idx, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx)
print("Updated index.html successfully")

# 4. Update mobile files
for mf in ['mobile/index.html', 'static/mobile/index.html', 'android_app/app/src/main/assets/mobile/index.html']:
    if not os.path.exists(mf): continue
    with open(mf, 'r', encoding='utf-8') as f:
        m_txt = f.read()

    if '/js/vyas_master_system_prompt.js' not in m_txt:
        m_txt = m_txt.replace('<script src="/js/vyas_astronomical_engine.js"></script>', '<script src="/js/vyas_master_system_prompt.js"></script>\n    <script src="/js/vyas_astronomical_engine.js"></script>')

    if 'MASTER_SYSTEM_PROMPT' in m_txt:
        m_txt = re.sub(
            r'MASTER_SYSTEM_PROMPT:\s*(["\'][\s\S]*?["\']|\(window\.VYAS_MASTER_SYSTEM_PROMPT[\s\S]*?\)),',
            lambda m: 'MASTER_SYSTEM_PROMPT: (typeof window !== "undefined" && window.VYAS_MASTER_SYSTEM_PROMPT) ? window.VYAS_MASTER_SYSTEM_PROMPT : ' + json.dumps(prompt_text, ensure_ascii=False) + ',',
            m_txt,
            count=1
        )

    m_txt = re.sub(r'<footer[\s\S]*?</footer>', lambda m: mobile_footer_html.strip(), m_txt, count=1)

    with open(mf, 'w', encoding='utf-8') as f:
        f.write(m_txt)
    print(f"Updated {mf} successfully")

# 5. Update subpages
subpages = [
    'kundli-matching/index.html',
    'varshphal/index.html',
    'ashtakavarga/index.html',
    'prashna/index.html',
    'dasha/index.html',
    'kp-system/index.html',
    'panchang/index.html',
    'nadi-astrology/index.html',
    'admin.html'
]

for sp in subpages:
    if not os.path.exists(sp): continue
    with open(sp, 'r', encoding='utf-8') as f:
        sp_txt = f.read()

    if '<footer' in sp_txt:
        sp_txt = re.sub(r'<footer[\s\S]*?</footer>', lambda m: founder_footer_html.strip(), sp_txt, count=1)
        with open(sp, 'w', encoding='utf-8') as f:
            f.write(sp_txt)
        print(f"Updated footer in {sp}")

print("ALL UPDATES COMPLETE!")
