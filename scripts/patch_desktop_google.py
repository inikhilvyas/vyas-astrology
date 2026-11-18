import re

def update_desktop():
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Add global callback and g_id_onload if not present
    if "handleGlobalGoogleCredential" not in html:
        global_cb = """    <script>
        function handleGlobalGoogleCredential(response) {
            if (window.VyasDesktop && typeof VyasDesktop.handleGoogleCredentialResponse === 'function') {
                VyasDesktop.handleGoogleCredentialResponse(response);
            }
        }
    </script>
    <div id="g_id_onload"
         data-client_id="341351445313-ddlkfiqsndnvbl290bubh1u3s827c3b2.apps.googleusercontent.com"
         data-context="signin"
         data-ux_mode="popup"
         data-callback="handleGlobalGoogleCredential"
         data-auto_prompt="false"
         data-cancel_on_tap_outside="true">
    </div>
"""
        html = html.replace('<div class="modal-overlay" id="modalGoogleAuth"', global_cb + '    <div class="modal-overlay" id="modalGoogleAuth"')

    # 2. Update modal dialog dGoogleUnauth
    old_unauth = """            <div id="dGoogleUnauth">
                <div style="width:52px; height:52px; border-radius:50%; background:rgba(212,175,55,0.12); border:1.5px solid #d4af37; margin:0 auto 12px auto; display:flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#d4af37" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <h4 style="margin:0 0 6px 0; color:#f1f5f9; font-size:1.02rem; font-weight:700;">VYAS ASTRA VIP क्लब</h4>
                <p style="font-size:0.78rem; color:#94a3b8; margin:0 0 16px 0; line-height:1.5;">
                    पारिवारिक कुण्डलियाँ सुरक्षित रखने, असीमित AI परामर्श एवं VIP PDF एक्सेस हेतु साइन-इन करें।
                </p>



                <div style="display:flex; flex-direction:column; gap:10px; text-align:left; margin-bottom:14px;">
                    <div>
                        <label style="font-size:0.75rem; color:#94a3b8; display:block; margin-bottom:4px;">जातक / आपका नाम:</label>
                        <input type="text" id="customGoogleName" placeholder="उदा. राहुल शर्मा" style="width:100%; box-sizing:border-box; background:#0f172a; border:1px solid rgba(212,175,55,0.3); border-radius:6px; padding:9px 12px; color:#f8fafc; font-size:0.85rem;">
                    </div>
                    <div>
                        <label style="font-size:0.75rem; color:#94a3b8; display:block; margin-bottom:4px;">Google Email ID:</label>
                        <input type="email" id="customGoogleEmail" placeholder="उदा. rahul@gmail.com" style="width:100%; box-sizing:border-box; background:#0f172a; border:1px solid rgba(212,175,55,0.3); border-radius:6px; padding:9px 12px; color:#f8fafc; font-size:0.85rem;">
                    </div>
                </div>

                <button onclick="VyasDesktop.signInCustomProfile()" style="width:100%; background:linear-gradient(135deg, #d4af37, #b8860b); border:none; border-radius:8px; padding:11px; color:#0b1324; font-weight:800; font-size:0.86rem; cursor:pointer; box-shadow:0 4px 14px rgba(212,175,55,0.3);">
                    Google खाते से सुरक्षित लॉगिन करें
                </button>
            </div>"""

    new_unauth = """            <div id="dGoogleUnauth">
                <div style="width:52px; height:52px; border-radius:50%; background:rgba(212,175,55,0.12); border:1.5px solid #d4af37; margin:0 auto 12px auto; display:flex; align-items:center; justify-content:center;">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="#d4af37" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <h4 style="margin:0 0 6px 0; color:#f1f5f9; font-size:1.02rem; font-weight:700;">VYAS ASTRA VIP क्लब</h4>
                <p style="font-size:0.78rem; color:#94a3b8; margin:0 0 16px 0; line-height:1.5;">
                    पारिवारिक कुण्डलियाँ सुरक्षित रखने, असीमित AI परामर्श एवं VIP PDF एक्सेस हेतु आधिकारिक Google खाते से साइन-इन करें।
                </p>

                <!-- Official Google Identity Services Sign-In Button Container -->
                <div style="display:flex; justify-content:center; align-items:center; margin:16px 0 12px 0; min-height:44px;">
                    <div id="g_id_signin_desktop" class="g_id_signin"
                         data-type="standard"
                         data-shape="pill"
                         data-theme="filled_blue"
                         data-text="continue_with"
                         data-size="large"
                         data-logo_alignment="left"
                         data-width="280">
                    </div>
                </div>

                <div style="font-size:0.75rem; color:#94a3b8; margin:8px 0 14px 0;">
                    🔒 Google Identity Services द्वारा 256-बिट सुरक्षित प्रमाणीकरण
                </div>

                <!-- Secondary Manual Fallback (Collapsed by default, only for offline/testing) -->
                <div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:10px; margin-top:10px;">
                    <a href="javascript:void(0)" onclick="var s = document.getElementById('dManualLoginSection'); if(s) s.style.display = (s.style.display==='none'?'block':'none');" style="color:#d4af37; font-size:0.74rem; text-decoration:none;">
                        ⚙️ वैकल्पिक: बिना Google मैन्युअल नाम से जारी रखें ▾
                    </a>
                    <div id="dManualLoginSection" style="display:none; margin-top:10px; text-align:left;">
                        <div style="margin-bottom:8px;">
                            <label style="font-size:0.72rem; color:#94a3b8; display:block; margin-bottom:3px;">जातक / आपका नाम:</label>
                            <input type="text" id="customGoogleName" placeholder="उदा. राहुल शर्मा" style="width:100%; box-sizing:border-box; background:#0f172a; border:1px solid rgba(212,175,55,0.3); border-radius:6px; padding:7px 10px; color:#f8fafc; font-size:0.82rem;">
                        </div>
                        <div style="margin-bottom:8px;">
                            <label style="font-size:0.72rem; color:#94a3b8; display:block; margin-bottom:3px;">Email ID:</label>
                            <input type="email" id="customGoogleEmail" placeholder="उदा. rahul@gmail.com" style="width:100%; box-sizing:border-box; background:#0f172a; border:1px solid rgba(212,175,55,0.3); border-radius:6px; padding:7px 10px; color:#f8fafc; font-size:0.82rem;">
                        </div>
                        <button onclick="VyasDesktop.signInCustomProfile()" style="width:100%; background:rgba(212,175,55,0.2); border:1px solid #d4af37; border-radius:6px; padding:8px; color:#d4af37; font-weight:700; font-size:0.80rem; cursor:pointer;">
                            नाम दर्ज कर जारी रखें
                        </button>
                    </div>
                </div>
            </div>"""

    if old_unauth in html:
        html = html.replace(old_unauth, new_unauth)
        print("✓ dGoogleUnauth in index.html replaced successfully")
    else:
        print("! Warning: dGoogleUnauth pattern not found directly, checking regex")

    # 3. Update initGoogleAuth, setupGoogleIdentity, promptGoogleSignIn in VyasDesktop
    old_methods = """        initGoogleAuth: function() {
            try {
                var saved = localStorage.getItem('vyas_google_user');
                if (saved) {
                    var parsed = JSON.parse(saved);
                    // PURGE FAKE/DUMMY ACCOUNTS (e.g. "वैदिक जातक", "user@gmail.com", etc.)
                    if (!parsed || !parsed.email || parsed.name.indexOf('वैदिक') !== -1 || parsed.email.indexOf('user@') !== -1 || parsed.email === 'nikhilvyas@vyasastro.in') {
                        localStorage.removeItem('vyas_google_user');
                        this.googleUser = null;
                    } else {
                        this.googleUser = parsed;
                    }
                    this.updateGoogleAuthUI();
                } else {
                    this.googleUser = null;
                    this.updateGoogleAuthUI();
                }
            } catch (e) {
                console.warn('Google Auth Load Exception:', e);
                this.googleUser = null;
                this.updateGoogleAuthUI();
            }
        },

                promptGoogleSignIn: function() {
            var modal = document.getElementById('modalGoogleAuth');
            if (!modal) return;
            var unauth = document.getElementById('dGoogleUnauth');
            var auth = document.getElementById('dGoogleAuth');
            if (this.googleUser) {
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
        },"""

    new_methods = """        initGoogleAuth: function() {
            try {
                var saved = localStorage.getItem('vyas_google_user');
                if (saved) {
                    var parsed = JSON.parse(saved);
                    // PURGE FAKE/DUMMY ACCOUNTS (e.g. "वैदिक जातक", "user@gmail.com", etc.)
                    if (!parsed || !parsed.email || (parsed.name && parsed.name.indexOf('वैदिक') !== -1) || parsed.email.indexOf('user@') !== -1 || parsed.email === 'nikhilvyas@vyasastro.in') {
                        localStorage.removeItem('vyas_google_user');
                        this.googleUser = null;
                    } else {
                        this.googleUser = parsed;
                    }
                    this.updateGoogleAuthUI();
                } else {
                    this.googleUser = null;
                    this.updateGoogleAuthUI();
                }
            } catch (e) {
                console.warn('Google Auth Load Exception:', e);
                this.googleUser = null;
                this.updateGoogleAuthUI();
            }
            this.setupGoogleIdentity();
        },

        setupGoogleIdentity: function() {
            var self = this;
            if (window.google && window.google.accounts && window.google.accounts.id) {
                try {
                    google.accounts.id.initialize({
                        client_id: "341351445313-ddlkfiqsndnvbl290bubh1u3s827c3b2.apps.googleusercontent.com",
                        callback: function(resp) { self.handleGoogleCredentialResponse(resp); },
                        auto_select: false,
                        cancel_on_tap_outside: true
                    });
                    var gDiv = document.getElementById("g_id_signin_desktop");
                    if (gDiv) {
                        google.accounts.id.renderButton(gDiv, {
                            theme: "filled_blue",
                            size: "large",
                            shape: "pill",
                            text: "continue_with",
                            logo_alignment: "left",
                            width: 280
                        });
                    }
                } catch(e) {
                    console.warn("GIS setup error:", e);
                }
            } else {
                setTimeout(function() { self.setupGoogleIdentity(); }, 350);
            }
        },

        promptGoogleSignIn: function() {
            if (this.googleUser) {
                var pop = document.getElementById('userProfilePopover');
                if (pop) {
                    pop.style.display = (pop.style.display === 'none' || !pop.style.display) ? 'block' : 'none';
                    return;
                }
            }

            // Trigger Google Identity One-Tap prompt
            if (window.google && window.google.accounts && window.google.accounts.id) {
                try {
                    google.accounts.id.prompt();
                } catch(e) {
                    console.warn("One-tap prompt error:", e);
                }
            }

            // Open auth modal containing the official Google Sign-In button
            var modal = document.getElementById('modalGoogleAuth');
            if (modal) {
                var unauth = document.getElementById('dGoogleUnauth');
                var auth = document.getElementById('dGoogleAuth');
                if (this.googleUser) {
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
            }

            // Render Google Button in modal if not yet rendered
            if (window.google && window.google.accounts && window.google.accounts.id) {
                var gDiv = document.getElementById("g_id_signin_desktop");
                if (gDiv) {
                    try {
                        google.accounts.id.renderButton(gDiv, {
                            theme: "filled_blue",
                            size: "large",
                            shape: "pill",
                            text: "continue_with",
                            logo_alignment: "left",
                            width: 280
                        });
                    } catch(e) {}
                }
            }
        },"""

    if old_methods in html:
        html = html.replace(old_methods, new_methods)
        print("✓ Google auth methods in index.html replaced successfully")
    else:
        print("! Warning: Google auth methods pattern in index.html not found directly")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html written")

update_desktop()

