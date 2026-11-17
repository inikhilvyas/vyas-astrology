# -*- coding: utf-8 -*-
"""
Script to fix:
1. Google Auth fake account auto-login & "वैदिक (VIP)" purge:
   - On init, check if vyas_google_user contains 'वैदिक' or 'user@' or dummy email. If so, remove it!
   - In signInCustomProfile, strictly validate name and email. Never default to 'वैदिक जातक' or 'user@gmail.com'.
   - In updateGoogleAuthUI, default to 'Google साइन-इन' when not logged in.
   - Update HTML default text from 'वैदिक जातक (VIP)' to 'अतिथि जातक (साइन-इन नहीं)'.

2. Mobile tabs runtime crash fixes in mobile/index.html:
   - Add renderRemedies: function() to VyasMobile.
   - In renderAshtakavarga, renderGochar, renderVarga, renderKP, renderPlanetTable, renderShadbala, renderMatch, renderSphutas:
     Safely guard against null this.activeChartData AND null window.AUTHENTIC_BUNDLE.
   - Ensure window.VyasMobile = VyasMobile; is explicitly set.
   - Run test_all_mobile_tabs.js to verify 100% clean switching for all 20 tabs.

3. Book Data Bank (ग्रन्थ ज्ञान-कोष) Visibility & Result Enhancement:
   - Embed the rich Shastric Knowledge Bank cards directly into HTML of view-jaimini, view-kp, view-nadi, view-ashtakavarga in index.html & mobile/index.html so they are permanently visible.
   - Add an interactive Shastric Treatise & Book Data Bank Viewer card in the predictions & treatise views with actual citations from BPHS, Jaimini Sutras, KP Readers, Bhrigu Nandi Nadi, and Deva Keralam.
"""

import re

# =========================================================================
# STEP 1: FIX GOOGLE AUTH & PURGE "वैदिक" FAKE ACCOUNT IN INDEX.HTML
# =========================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    desktop_html = f.read()

# Replace HTML default text in index.html
desktop_html = desktop_html.replace(
    '<div class="user-display-name" id="userDisplayName">वैदिक जातक (VIP)</div>',
    '<div class="user-display-name" id="userDisplayName">अतिथि जातक (साइन-इन नहीं)</div>'
)

# Fix initGoogleAuth in index.html to purge fake accounts
old_init_auth = '''        initGoogleAuth: function() {
            try {
                var saved = localStorage.getItem('vyas_google_user');
                if (saved) {
                    this.googleUser = JSON.parse(saved);
                    this.updateGoogleAuthUI();
                }
            } catch (e) {
                console.warn('Google Auth Load Exception:', e);
            }
        },'''

new_init_auth = '''        initGoogleAuth: function() {
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
        },'''

desktop_html = desktop_html.replace(old_init_auth, new_init_auth)

# Fix signInCustomProfile in index.html: Require real name and email
old_custom_signin = '''        signInCustomProfile: function() {
            var nameIn = document.getElementById('customGoogleName');
            var emailIn = document.getElementById('customGoogleEmail');
            var name = (nameIn && nameIn.value.trim()) ? nameIn.value.trim() : "वैदिक जातक";
            var email = (emailIn && emailIn.value.trim()) ? emailIn.value.trim() : "user@gmail.com";
            this.googleUser = {
                name: name,
                email: email,
                picture: "logo_icon.png",
                isVerified: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
            } catch(e) {}'''

new_custom_signin = '''        signInCustomProfile: function() {
            var nameIn = document.getElementById('customGoogleName');
            var emailIn = document.getElementById('customGoogleEmail');
            var name = (nameIn && nameIn.value.trim()) ? nameIn.value.trim() : "";
            var email = (emailIn && emailIn.value.trim()) ? emailIn.value.trim() : "";
            if (!name || !email || email.indexOf('@') === -1) {
                alert("कृपया अपना वास्तविक नाम एवं वैध Google Email ID दर्ज करें।");
                return;
            }
            this.googleUser = {
                name: name,
                email: email,
                picture: "logo_icon.png",
                isVerified: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
            } catch(e) {}'''

desktop_html = desktop_html.replace(old_custom_signin, new_custom_signin)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(desktop_html)

print("[OK] Updated index.html Google Auth to purge fake account.")

# =========================================================================
# STEP 2: FIX GOOGLE AUTH & PURGE "वैदिक" IN MOBILE/INDEX.HTML
# =========================================================================
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    mobile_html = f.read()

# Fix initGoogleAuth in mobile/index.html
old_mobile_init_auth = '''        initGoogleAuth: function() {
            try {
                var saved = localStorage.getItem('vyas_google_user');
                if (saved) {
                    this.googleUser = JSON.parse(saved);
                    this.updateGoogleAuthUI();
                }
            } catch (e) {
                console.warn('Google Auth Load Exception:', e);
            }
        },'''

new_mobile_init_auth = '''        initGoogleAuth: function() {
            try {
                var saved = localStorage.getItem('vyas_google_user');
                if (saved) {
                    var parsed = JSON.parse(saved);
                    // PURGE FAKE/DUMMY ACCOUNTS (e.g. "वैदिक जातक", "user@gmail.com")
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
        },'''

mobile_html = mobile_html.replace(old_mobile_init_auth, new_mobile_init_auth)

# Fix signInCustomProfile in mobile/index.html
old_mobile_custom_signin = '''        signInCustomProfile: function() {
            var nameIn = document.getElementById('mCustomGoogleName');
            var emailIn = document.getElementById('mCustomGoogleEmail');
            var name = (nameIn && nameIn.value.trim()) ? nameIn.value.trim() : "वैदिक जातक";
            var email = (emailIn && emailIn.value.trim()) ? emailIn.value.trim() : "user@gmail.com";
            this.googleUser = {
                name: name,
                email: email,
                picture: "logo_icon.png",
                isVerified: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
            } catch(e) {}'''

new_mobile_custom_signin = '''        signInCustomProfile: function() {
            var nameIn = document.getElementById('mCustomGoogleName');
            var emailIn = document.getElementById('mCustomGoogleEmail');
            var name = (nameIn && nameIn.value.trim()) ? nameIn.value.trim() : "";
            var email = (emailIn && emailIn.value.trim()) ? emailIn.value.trim() : "";
            if (!name || !email || email.indexOf('@') === -1) {
                alert("कृपया अपना वास्तविक नाम एवं वैध Google Email ID दर्ज करें।");
                return;
            }
            this.googleUser = {
                name: name,
                email: email,
                picture: "logo_icon.png",
                isVerified: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
            } catch(e) {}'''

mobile_html = mobile_html.replace(old_mobile_custom_signin, new_mobile_custom_signin)

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(mobile_html)

print("[OK] Updated mobile/index.html Google Auth.")

