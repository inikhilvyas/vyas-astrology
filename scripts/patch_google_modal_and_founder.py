with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update promptGoogleSignIn to open modal
old_prompt = """        promptGoogleSignIn: function() {
            // If already verified and logged in, toggle profile popover/modal
            if (this.googleUser) {
                var pop = document.getElementById('userProfilePopover');
                if (pop) {
                    pop.style.display = (pop.style.display === 'none' || !pop.style.display) ? 'block' : 'none';
                    return;
                }
                var modal = document.getElementById('modalGoogleAuth');
                if (modal) {
                    var unauth = document.getElementById('dGoogleUnauth');
                    var auth = document.getElementById('dGoogleAuth');
                    if (unauth) unauth.style.display = 'none';
                    if (auth) auth.style.display = 'block';
                    var nameEl = document.getElementById('dAuthName');
                    var emailEl = document.getElementById('dAuthEmail');
                    if (nameEl) nameEl.textContent = this.googleUser.name || 'सत्यापित VIP जातक';
                    if (emailEl) emailEl.textContent = this.googleUser.email || '';
                    modal.classList.add('active');
                    modal.style.setProperty('display', 'flex', 'important');
                }
                return;
            }

            // If not logged in: IMMEDIATELY launch real Google OAuth!
            this.launchGoogleOAuth();
        },"""

new_prompt = """        promptGoogleSignIn: function() {
            var modal = document.getElementById('modalGoogleAuth');
            if (!modal) return;
            var unauth = document.getElementById('dGoogleUnauth');
            var auth = document.getElementById('dGoogleAuth');

            if (this.googleUser) {
                var pop = document.getElementById('userProfilePopover');
                if (pop) {
                    pop.style.display = (pop.style.display === 'none' || !pop.style.display) ? 'block' : 'none';
                    return;
                }
                if (unauth) unauth.style.display = 'none';
                if (auth) auth.style.display = 'block';
                var nameEl = document.getElementById('dAuthName');
                var emailEl = document.getElementById('dAuthEmail');
                if (nameEl) nameEl.textContent = this.googleUser.name || 'सत्यापित VIP जातक';
                if (emailEl) emailEl.textContent = this.googleUser.email || '';
            } else {
                if (unauth) unauth.style.display = 'block';
                if (auth) auth.style.display = 'none';
            }
            modal.classList.add('active');
            modal.style.setProperty('display', 'flex', 'important');
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
                localStorage.setItem('vyas_vip_member_inikhilvyas@gmail.com', 'true');
            } catch(e) {}
            this.updateGoogleAuthUI();
            this.loadStoredProfile();
            this.renderChart(this.currentVarga || 'd1');
            this.updateDailyHoroscopeUI();
            this.updateYogasBannerUI();
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderDashaTree();
            this.closeModals();
            alert("✓ स्वागतम् निखिल व्यास जी! Pro VIP एक्सेस सफलतापूर्वक सक्रिय हो गया है।");
        },"""

if old_prompt in content:
    content = content.replace(old_prompt, new_prompt)
    print("SUCCESS: Updated promptGoogleSignIn to open modal smoothly!")
else:
    print("WARNING: old_prompt not found directly, checking regex...")
    import re
    pat = re.compile(r'promptGoogleSignIn:\s*function\(\)\s*\{.*?this\.launchGoogleOAuth\(\);\s*\},', re.DOTALL)
    if pat.search(content):
        content = pat.sub(new_prompt, content)
        print("SUCCESS: Updated promptGoogleSignIn via regex!")
    else:
        print("Regex failed.")

# 2. Add quickLoginFounder button to modalGoogleAuth
modal_target = '<!-- GIS Container (for auto One-Tap & standard button fallback) -->'
modal_button = """<!-- Quick Founder VIP Access Button -->
                <button type="button" onclick="VyasDesktop.quickLoginFounder()" style="width:100%; margin-top:12px; display:flex; align-items:center; justify-content:center; gap:10px; background:linear-gradient(135deg, rgba(212,175,55,0.18), rgba(15,23,42,0.9)); border:1.5px solid #d4af37; border-radius:24px; padding:11px 16px; color:#d4af37; font-weight:700; font-size:0.86rem; cursor:pointer; box-shadow:0 0 12px rgba(212,175,55,0.25); transition:all 0.2s ease;">
                    <span>💎</span>
                    <span>निखिल व्यास (Pro VIP जातक) के रूप में तुरंत लॉगिन करें</span>
                </button>

                <div style="font-size:0.72rem; color:#94a3b8; margin-top:6px; line-height:1.4;">
                    (Google Redirect URI सेटिंग पेंडिंग होने पर भी निर्बाध VIP एक्सेस हेतु)
                </div>

                <!-- GIS Container (for auto One-Tap & standard button fallback) -->"""

if modal_target in content and 'quickLoginFounder' not in content:
    content = content.replace(modal_target, modal_button)
    print("SUCCESS: Injected quickLoginFounder button into modalGoogleAuth!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

