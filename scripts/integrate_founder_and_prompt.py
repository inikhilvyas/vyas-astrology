import os
import json
import re
from save_prompt_text import prompt_text

print("Prompt length:", len(prompt_text))

# 1. Create js/vyas_master_system_prompt.js
js_code = f"""/**
 * VYAS 34.0 AGENTIC JYOTISHA INTELLIGENCE SYSTEM — MASTER SYSTEM PROMPT
 * Founder & Research Direction: Nikhil Vyas (Pali, Rajasthan)
 * Institutional Core: VYAS Research Foundation
 */
(function(global) {{
    global.VYAS_MASTER_SYSTEM_PROMPT = {json.dumps(prompt_text)};
    if (typeof module !== 'undefined' && module.exports) {{
        module.exports = global.VYAS_MASTER_SYSTEM_PROMPT;
    }}
}})(typeof window !== 'undefined' ? window : global);
"""

with open('js/vyas_master_system_prompt.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("Created js/vyas_master_system_prompt.js")

# 2. Update api/ai_chat.php default system prompt
with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    php_content = f.read()

php_default_prompt_code = f'''
$vyas34MasterPrompt = {json.dumps(prompt_text)};
$systemPrompt = (isset($input['systemPrompt']) && !empty(trim($input['systemPrompt']))) 
    ? $vyas34MasterPrompt . "\\n\\n" . trim($input['systemPrompt'])
    : $vyas34MasterPrompt;
'''

old_prompt_line = "$systemPrompt = isset($input['systemPrompt']) ? trim($input['systemPrompt']) : '';"
if old_prompt_line in php_content:
    php_content = php_content.replace(old_prompt_line, php_default_prompt_code.strip())
    print("Updated api/ai_chat.php with VYAS 34.0 Master Prompt")
    with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
        f.write(php_content)
else:
    print("old_prompt_line not found in api/ai_chat.php")

# 3. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

# Replace MASTER_SYSTEM_PROMPT in index.html
idx_content = re.sub(
    r'MASTER_SYSTEM_PROMPT:\s*"You are ACHARYA VYAS \(v10\.0\)[\s\S]*?",',
    f'MASTER_SYSTEM_PROMPT: {json.dumps(prompt_text)},',
    idx_content
)

# Founder footer & contact in index.html
# Footer replacement
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

idx_content = re.sub(r'<!-- VYAS ASTRA OFFICIAL FOOTER & SOLE FOUNDER ACCREDITATION -->[\s\S]*?</footer>', founder_footer_html, idx_content)
idx_content = re.sub(r'<!-- VYAS ASTRA OFFICIAL FOOTER & FOUNDER ACCREDITATION -->[\s\S]*?</footer>', founder_footer_html, idx_content)

# Update the support card in index.html pro modal
old_support_box = re.search(r'<!-- Support / Direct Contact & UPI -->[\s\S]*?<!-- License Key Activation -->', idx_content)
if old_support_box:
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
            </div>

            <!-- License Key Activation -->'''
    idx_content = idx_content.replace(old_support_box.group(0), new_support_card)
    print("Updated support card in index.html pro modal")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(idx_content)
print("Updated index.html")

# 4. Update mobile/index.html, static/mobile/index.html, and android_app
mobile_footer_html = '''    <!-- VYAS ASTRA MOBILE FOOTER & FOUNDER ACCREDITATION -->
    <footer style="margin-top:30px; margin-bottom:80px; padding:24px 16px; border-top:1px solid rgba(212,175,55,0.25); background:rgba(7,11,25,0.95); text-align:center; font-size:0.84rem; color:#94A3B8; line-height:1.7;">
        <div style="color:var(--primary); font-weight:700; font-size:0.90rem; margin-bottom:6px;">✦ VYAS ASTRA • वैदिक खगोलीय संस्थान ✦</div>
        <div style="color:#E2E8F0; font-size:0.88rem; margin-bottom:6px;">
            संस्थापक एवं मुख्य शोधकर्ता: <b style="color:var(--primary);">निखिल व्यास (Nikhil Vyas)</b> • पाली, राजस्थान
        </div>
        <div style="margin-bottom:6px; font-size:0.82rem; color:#CBD5E1;">
            📞 <a href="https://wa.me/919414121172?text=नमस्ते%20निखिल%20जी" target="_blank" style="color:#38BDF8; font-weight:700; text-decoration:none;">+91 9414121172</a> • ✉️ <a href="mailto:inikhilvyas@gmail.com" style="color:#38BDF8; font-weight:700; text-decoration:none;">inikhilvyas@gmail.com</a>
        </div>
        <div style="font-size:0.72rem; color:#64748B;">
            © 2026 VYAS ASTRA • Swiss Ephemeris 0.001" परिशुद्धता
        </div>
    </footer>'''

target_mobile_files = [
    'mobile/index.html',
    'static/mobile/index.html',
    'android_app/app/src/main/assets/mobile/index.html'
]

for m_file in target_mobile_files:
    if not os.path.exists(m_file): continue
    with open(m_file, 'r', encoding='utf-8') as f:
        m_content = f.read()

    # Update MASTER_SYSTEM_PROMPT in mobile files
    if 'MASTER_SYSTEM_PROMPT' in m_content:
        m_content = re.sub(
            r'MASTER_SYSTEM_PROMPT:\s*"You are ACHARYA VYAS[\s\S]*?",',
            f'MASTER_SYSTEM_PROMPT: {json.dumps(prompt_text)},',
            m_content
        )

    # Update footer
    m_content = re.sub(r'<!-- VYAS ASTRA MOBILE FOOTER & FOUNDER ACCREDITATION -->[\s\S]*?</footer>', mobile_footer_html, m_content)

    with open(m_file, 'w', encoding='utf-8') as f:
        f.write(m_content)
    print(f"Updated {m_file}")

# 5. Update subpages footers (kundli-matching, varshphal, ashtakavarga, etc.)
subpages = [
    'kundli-matching/index.html',
    'varshphal/index.html',
    'ashtakavarga/index.html',
    'prashna/index.html',
    'dasha/index.html',
    'kp-system/index.html',
    'panchang/index.html',
    'nadi-astrology/index.html'
]

for sp in subpages:
    if not os.path.exists(sp): continue
    with open(sp, 'r', encoding='utf-8') as f:
        sp_content = f.read()

    # Check for footer in subpage
    if '<footer' in sp_content:
        sp_content = re.sub(
            r'<footer[\s\S]*?</footer>',
            founder_footer_html,
            sp_content
        )
        with open(sp, 'w', encoding='utf-8') as f:
            f.write(sp_content)
        print(f"Updated footer in {sp}")

