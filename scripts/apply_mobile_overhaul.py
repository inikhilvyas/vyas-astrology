import re

print("=== STARTING MOBILE OVERHAUL ===")

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace VIP with PRO / PREMIUM
html = html.replace('NIKHIL (VIP)', 'NIKHIL (PRO)')
html = html.replace('NIKHIL (PRO VIP)', 'NIKHIL (PRO)')
html = html.replace('(PRO VIP)', '(PRO)')
html = html.replace('VIP क्लब', 'PRO क्लब')
html = html.replace('VIP एक्सेस', 'PRO एक्सेस')
html = html.replace('VIP PDF', 'PRO शोध डॉसियर')
html = html.replace('VIP सदस्य', 'PRO सदस्य')
html = html.replace('VIP जातक', 'PRO जातक')
html = html.replace('vyas_vip_member_', 'vyas_pro_member_')

# 2. Replace emojis with clean SVGs
svg_gem = '<svg class="v-icon v-gem" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><path d="M6 3h12l4 6-10 12L2 9z"/></svg>'
svg_spark = '<svg class="v-icon v-spark" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg>'
svg_time = '<svg class="v-icon v-time" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
svg_chart = '<svg class="v-icon v-chart" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
svg_book = '<svg class="v-icon v-book" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15z"/></svg>'
svg_warn = '<svg class="v-icon v-warn" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:3px;"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

m_replacements = [
    ('💎 ', svg_gem),
    ('💎', svg_gem),
    ('✨ ', svg_spark),
    ('✨', svg_spark),
    ('⏳ ', svg_time),
    ('⏳', svg_time),
    ('📊 ', svg_chart),
    ('📊', svg_chart),
    ('📖 ', svg_book),
    ('📖', svg_book),
    ('📜 ', svg_book),
    ('📜', svg_book),
    ('📕 ', svg_book),
    ('📕', svg_book),
    ('⚠️ ', svg_warn),
    ('⚠️', svg_warn),
    ('⛔ ', svg_warn),
    ('⛔', svg_warn),
    ('🚩 ', svg_spark),
    ('🚩', svg_spark),
    ('🪐 ', svg_spark),
    ('🪐', svg_spark),
    ('🔮 ', svg_spark),
    ('🔮', svg_spark),
]
for old, new in m_replacements:
    html = html.replace(old, new)

# 3. Add Safe Data Vault and Quick Founder Access to VyasMobile
m_vault_code = """
        // Safe Data Vault
        saveToUserVault: function(profileData) {
            if (!profileData) return;
            try {
                localStorage.setItem('vyas_active_profile', JSON.stringify(profileData));
                var email = (this.googleUser && this.googleUser.email) ? this.googleUser.email.trim().toLowerCase() : 'nikhilvyas007@gmail.com';
                localStorage.setItem('vyas_user_vault_' + email, JSON.stringify(profileData));
                localStorage.setItem('vyas_user_has_vault', 'true');
            } catch(e) {}
        },

        quickLoginFounder: function() {
            var founderUser = {
                name: "NIKHIL VYAS",
                email: "nikhilvyas007@gmail.com",
                sub: "109876543210987654321",
                picture: "logo_icon.png",
                isVerified: true
            };
            this.googleUser = founderUser;
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(founderUser));
                localStorage.setItem('vyas_pro_active', 'true');
                localStorage.setItem('vyas_vip_member_nikhilvyas007@gmail.com', 'true');
            } catch(e) {}
            this.updateGoogleAuthUI();
            this.loadStoredProfile();
            this.renderChart(this.currentVarga || 'd1');
            this.closeModals();
            alert("✓ स्वागतम् निखिल व्यास जी! Pro एक्सेस सक्रिय है।");
        },
"""

if 'saveToUserVault:' not in html:
    html = html.replace('loadStoredProfile() {', m_vault_code + '\n        loadStoredProfile() {')

# 4. Add 1-Click Founder Button in mobile modal if exists
if 'quickLoginFounder' not in html and 'modalGoogleAuth' in html:
    btn_markup = """<button type="button" onclick="VyasMobile.quickLoginFounder()" style="width:100%; margin-top:10px; display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(135deg, rgba(212,175,55,0.18), rgba(15,23,42,0.9)); border:1.5px solid #d4af37; border-radius:20px; padding:10px 14px; color:#d4af37; font-weight:700; font-size:0.82rem; cursor:pointer;">
        <span>💎</span><span>निखिल व्यास (Pro जातक) 1-क्लिक प्रवेश</span>
    </button>"""
    html = html.replace('id="dGoogleUnauth">', 'id="dGoogleUnauth">\n' + btn_markup)

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: mobile/index.html overhauled!")
