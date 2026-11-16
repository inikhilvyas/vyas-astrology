import os
import re

mobile_file = "mobile/index.html"
with open(mobile_file, "r", encoding="utf-8") as f:
    html = f.read()

print("Original length:", len(html))

# 1. Neutralize AUTHENTIC_BUNDLE
html = html.replace(
    'window.AUTHENTIC_BUNDLE = {"profile": {"name": "Nikhil Vyas", "dob": "1984-11-23", "tob": "04:51 PM", "city": "Pali, Rajasthan", "lat": 25.58, "lon": 73.38, "gender": "Male", "asc_sign": "मेष", "asc_dms": "23°27\'09\\""}',
    'window.AUTHENTIC_BUNDLE = {"profile": {"name": "संदर्भ जातक", "dob": "2000-01-01", "tob": "12:00 PM", "city": "नई दिल्ली (New Delhi)", "lat": 28.6139, "lon": 77.2090, "gender": "Male", "asc_sign": "मेष", "asc_dms": "15°00\'00\\""}'
)

# 2. In openSavedProfilesModal, remove founder 1-click card
old_modal_saved = """            var gUser = null;
            try {
                var gStored = localStorage.getItem('vyas_google_user');
                if (gStored) gUser = JSON.parse(gStored);
            } catch(e) {}

            var isNikhil = (gUser && gUser.name && gUser.name.toLowerCase().indexOf('nikhil') !== -1) ||
                           (gUser && gUser.email && gUser.email.toLowerCase().indexOf('nikhil') !== -1);

            var html = '';

            // ONLY show founder profile if verified Nikhil Vyas
            if (isNikhil) {
                html += '<div style="background:var(--bg-card); border:1.5px solid var(--border-gold); padding:10px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                    '<div>' +
                        '<b style="color:var(--primary); font-size:0.86rem;">निखिल व्यास (संस्थापक • MAJY)</b><br>' +
                        '<span style="font-size:0.74rem; color:var(--text-muted);">23 Nov 1984, 04:51 PM Pali (मेष 23°27&apos;)</span>' +
                    '</div>' +
                    '<button onclick="VyasMobile.loadAuthenticProfile(); VyasMobile.closeModals();" class="gold-btn" style="padding:5px 12px; font-size:0.76rem;">लोड करें</button>' +
                '</div>';
            }

            var customProfiles = [];
            try {
                var custom = localStorage.getItem('vyas_custom_profiles');
                if (custom) customProfiles = JSON.parse(custom);
            } catch(e) {}

            var familyProfiles = [];
            try {
                var fam = localStorage.getItem('vyas_family_vault');
                if (fam) familyProfiles = JSON.parse(fam);
            } catch(e) {}

            var allProfiles = customProfiles.concat(familyProfiles);

            if (allProfiles.length > 0) {
                for (var i = 0; i < allProfiles.length; i++) {
                    var p = allProfiles[i];
                    html += '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                        '<div>' +
                            '<b style="color:var(--primary); font-size:0.84rem;">' + (p.name || 'सुरक्षित जातक') + '</b><br>' +
                            '<span style="font-size:0.72rem; color:var(--text-muted);">' + (p.dob || '') + ' ' + (p.tob || '') + ' • ' + (p.city || '') + '</span>' +
                        '</div>' +
                        '<button onclick="VyasMobile.loadFamilyMember(' + i + '); VyasMobile.closeModals();" class="gold-btn" style="padding:5px 12px; font-size:0.76rem;">लोड करें</button>' +
                    '</div>';
                }
            } else if (!isNikhil) {
                html += '<div style="padding:24px 16px; text-align:center; color:var(--text-muted); font-size:0.84rem;">' +
                    '<div style="font-size:1.8rem; margin-bottom:8px;">🔒</div>' +
                    '<b style="color:var(--primary); font-size:0.90rem;">कोई सुरक्षित कुण्डली उपलब्ध नहीं है</b>' +
                    '<p style="font-size:0.76rem; margin-top:6px; color:var(--text-secondary); line-height:1.5;">अपनी जन्म कुण्डली सुरक्षित रखने हेतु कृपया लॉगिन करें अथवा "नई कुण्डली" बटन द्वारा अपनी जन्म पत्रिका बनाएं।</p>' +
                '</div>';
            }"""

new_modal_saved = """            var html = '';
            var customProfiles = [];
            try {
                var custom = localStorage.getItem('vyas_custom_profiles');
                if (custom) customProfiles = JSON.parse(custom);
            } catch(e) {}

            var familyProfiles = [];
            try {
                var fam = localStorage.getItem('vyas_family_vault');
                if (fam) familyProfiles = JSON.parse(fam);
            } catch(e) {}

            var allProfiles = customProfiles.concat(familyProfiles);

            if (allProfiles.length > 0) {
                for (var i = 0; i < allProfiles.length; i++) {
                    var p = allProfiles[i];
                    html += '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:12px 14px; border-radius:10px; display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                        '<div>' +
                            '<b style="color:var(--primary); font-size:0.95rem;">' + (p.name || 'सुरक्षित जातक') + '</b><br>' +
                            '<span style="font-size:0.82rem; color:var(--text-muted);">' + (p.dob || '') + ' ' + (p.tob || '') + ' • ' + (p.city || '') + '</span>' +
                        '</div>' +
                        '<button onclick="VyasMobile.loadFamilyMember(' + i + '); VyasMobile.closeModals();" class="gold-btn" style="padding:6px 14px; font-size:0.84rem; font-weight:700; border-radius:8px;">लोड करें</button>' +
                    '</div>';
                }
            } else {
                html += '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.92rem;">' +
                    '<div style="font-size:2.2rem; margin-bottom:10px;">📜</div>' +
                    '<b style="color:var(--primary); font-size:1.05rem;">कोई सुरक्षित कुण्डली उपलब्ध नहीं है</b>' +
                    '<p style="font-size:0.86rem; margin-top:8px; color:var(--text-secondary); line-height:1.5;">अपनी व्यक्तिगत जन्म कुण्डली बनाने व देखने हेतु नीचे दिए बटन पर क्लिक करें।</p>' +
                '</div>';
            }
            html += '<div style="margin-top:14px;">' +
                '<button onclick="VyasMobile.openNewProfileModal(); VyasMobile.closeModals();" class="gold-btn" style="width:100%; padding:12px; font-size:0.95rem; font-weight:700; border-radius:10px; display:flex; align-items:center; justify-content:center; gap:8px;">' +
                    '<span>+</span> नई कुण्डली प्रविष्ट करें' +
                '</button>' +
            '</div>';"""

if old_modal_saved in html:
    html = html.replace(old_modal_saved, new_modal_saved)
    print("✓ openSavedProfilesModal founder profile removed")
else:
    print("! Warning: openSavedProfilesModal exact pattern not found, trying regex")

# 3. In handleGoogleAuthResponse, remove auto-load of founder profile
old_auth_resp = """            var isNikhil = (name && name.toLowerCase().indexOf('nikhil') !== -1) ||
                           (email && email.toLowerCase().indexOf('nikhil') !== -1);
            if (isNikhil) {
                this.activeChartData = window.AUTHENTIC_BUNDLE;
                this.activeChart = window.AUTHENTIC_BUNDLE;
                localStorage.setItem('vyas_active_profile', JSON.stringify(window.AUTHENTIC_BUNDLE));
            } else {
                this.activeChartData = null;
                this.activeChart = null;
                localStorage.removeItem('vyas_active_profile');
            }"""

new_auth_resp = """            // Keep user session clean without injecting personal details
            if (!this.activeChartData) {
                var saved = localStorage.getItem('vyas_active_profile');
                if (saved) {
                    try { this.activeChartData = JSON.parse(saved); this.activeChart = this.activeChartData; } catch(e) {}
                }
            }"""

if old_auth_resp in html:
    html = html.replace(old_auth_resp, new_auth_resp)
    print("✓ handleGoogleAuthResponse founder injection removed")
else:
    print("! Warning: handleGoogleAuthResponse exact pattern not found")

# 4. In loadProfile, purge any stored profile with 1984-11-23 or Nikhil
old_load_prof = """                    if (data && data.profile && (data.profile.name === 'अतिथि जातक (Guest)' || (data.profile.name.indexOf('Nikhil') !== -1 && data.profile.asc_sign === 'कन्या'))) {
                        localStorage.removeItem('vyas_active_profile');
                        saved = null;
                    } else if (data && data.profile && data.profile.name) {
                        this.activeChartData = data;
                        this.activeChart = data;
                        hasStored = true;
                    }
                }
            } catch(e) {}

            if (!hasStored) {
                var gUser = null;
                try {
                    var gStored = localStorage.getItem('vyas_google_user');
                    if (gStored) gUser = JSON.parse(gStored);
                } catch(e) {}
                var isNikhil = (gUser && gUser.name && gUser.name.toLowerCase().indexOf('nikhil') !== -1) ||
                               (gUser && gUser.email && gUser.email.toLowerCase().indexOf('nikhil') !== -1);
                if (isNikhil) {
                    this.activeChartData = window.AUTHENTIC_BUNDLE;
                    this.activeChart = window.AUTHENTIC_BUNDLE;
                    hasStored = true;
                    try { localStorage.setItem('vyas_active_profile', JSON.stringify(window.AUTHENTIC_BUNDLE)); } catch(e) {}
                }
            }

            if (!hasStored) {
                // USER INVARIANT: Blank slate by default when not logged in.
                this.activeChartData = null;
                this.activeChart = null;
            }"""

new_load_prof = """                    // Auto-purge any stale cached founder profile with 1984-11-23 or Nikhil
                    if (data && data.profile && (data.profile.dob === '1984-11-23' || (data.profile.name && data.profile.name.indexOf('Nikhil') !== -1) || (data.profile.name && data.profile.name.indexOf('संस्थापक') !== -1))) {
                        localStorage.removeItem('vyas_active_profile');
                        saved = null;
                        data = null;
                    } else if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)') {
                        this.activeChartData = data;
                        this.activeChart = data;
                        hasStored = true;
                    }
                }
            } catch(e) {}

            if (!hasStored) {
                // USER INVARIANT: Clean blank slate by default
                this.activeChartData = null;
                this.activeChart = null;
            }"""

if old_load_prof in html:
    html = html.replace(old_load_prof, new_load_prof)
    print("✓ loadProfile founder injection removed and auto-purge added")
else:
    print("! Warning: loadProfile exact pattern not found")

# 5. Remove leftover install button in home tab
orphan_btn = """                    <button onclick="VyasMobile.triggerPwaInstall()" class="hdr-pill-btn gold">इंस्टॉल ⬇</button>
                </div>"""
if orphan_btn in html:
    html = html.replace(orphan_btn, "")
    print("✓ Orphaned install button removed")

# 6. Streamline Header: Remove redundant Vault and BTR buttons from top row
old_hdr_btns = """                <button class="hdr-pill-btn" onclick="VyasMobile.openFamilyVaultModal()" title="परिवार वॉल्ट">
                    <span>वॉल्ट</span>
                </button>
                <button class="hdr-pill-btn" onclick="VyasMobile.openBTRModal()" title="BTR सुधार">
                    <span>BTR</span>
                </button>"""
if old_hdr_btns in html:
    html = html.replace(old_hdr_btns, "")
    print("✓ Top header streamlined: removed cramped Vault & BTR pills from header row")

# 7. Replace remaining fallback strings of 1984-11-23 and Pali
html = html.replace('if (!dob) dob = "1984-11-23";', 'if (!dob) dob = "2000-01-01";')
html = html.replace('var y = parseInt(dParts[0]) || 1984;', 'var y = parseInt(dParts[0]) || 2000;')
html = html.replace('return isNaN(dt.getTime()) ? new Date(1984, 10, 23, 16, 51, 0).getTime() : dt.getTime();', 'return isNaN(dt.getTime()) ? new Date(2000, 0, 1, 12, 0, 0).getTime() : dt.getTime();')
html = html.replace('var dob = prof.dob || "1984-11-23";', 'var dob = prof.dob || "2000-01-01";')
html = html.replace('var city = prof.city || "Pali, Rajasthan";', 'var city = prof.city || "नई दिल्ली (New Delhi)";')
html = html.replace('var dobStr = prof.dob || "1984-11-23";', 'var dobStr = prof.dob || "2000-01-01";')
html = html.replace('var yr = 1984, mo = 11, dy = 23, hr = 16, mn = 51;', 'var yr = 2000, mo = 1, dy = 1, hr = 12, mn = 0;')
html = html.replace('var city = document.getElementById(\'m_inp_city\').value.trim() || "Pali";', 'var city = document.getElementById(\'m_inp_city\').value.trim() || "नई दिल्ली";')

# 8. Modern Luxury CSS Upgrade: Fonts, Spacing, Contrast
# Base font-size to 15.5px
html = html.replace('font-size: 14px;', 'font-size: 15.5px;')

# Upgrade .hdr-pill-btn CSS
old_pill_css = """.hdr-pill-btn {
            background: var(--bg-card);
            border: 1px solid var(--border-gold-soft);
            color: var(--text-primary);
            padding: 5px 8px;
            border-radius: 16px;
            font-size: 0.72rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
            white-space: nowrap;
        }"""

new_pill_css = """.hdr-pill-btn {
            background: var(--bg-card);
            border: 1.5px solid var(--border-gold-soft);
            color: var(--text-primary);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.84rem;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
        }"""

if old_pill_css in html:
    html = html.replace(old_pill_css, new_pill_css)
    print("✓ Upgraded .hdr-pill-btn CSS")

# Upgrade .profile-strip CSS
old_strip_css = """.profile-strip {
            background: var(--bg-card-alt);
            border-bottom: 1px solid var(--border-subtle);
            padding: 6px 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.75rem;
        }"""

new_strip_css = """.profile-strip {
            background: linear-gradient(90deg, #0e172a 0%, #152238 100%);
            border-bottom: 1.5px solid rgba(212, 175, 55, 0.3);
            padding: 9px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.88rem;
        }"""

if old_strip_css in html:
    html = html.replace(old_strip_css, new_strip_css)
    print("✓ Upgraded .profile-strip CSS")

# Upgrade .tab-btn CSS
old_tab_css = """.tab-btn {
            flex: 0 0 auto;
            padding: 7px 12px;
            border-radius: 20px;
            border: 1px solid var(--border-subtle);
            background: var(--bg-card);
            color: var(--text-secondary);
            font-size: 0.76rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            white-space: nowrap;
            transition: all 0.2s;
        }"""

new_tab_css = """.tab-btn {
            flex: 0 0 auto;
            padding: 8px 15px;
            border-radius: 22px;
            border: 1px solid rgba(212, 175, 55, 0.25);
            background: #111b30;
            color: #cbd5e1;
            font-size: 0.88rem;
            font-weight: 700;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            transition: all 0.2s;
        }"""

if old_tab_css in html:
    html = html.replace(old_tab_css, new_tab_css)
    print("✓ Upgraded .tab-btn CSS")

# Save updated mobile/index.html
with open(mobile_file, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✓ Saved updated {mobile_file} ({len(html)} chars)")

# Also copy to Android assets so APK matches exactly
android_asset = r"android_app\app\src\main\assets\mobile\index.html"
with open(android_asset, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✓ Synchronized to Android APK asset: {android_asset}")
