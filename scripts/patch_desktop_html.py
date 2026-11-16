import os
import re

desktop_file = "index.html"
with open(desktop_file, "r", encoding="utf-8") as f:
    html = f.read()

print("Original index.html length:", len(html))

# 1. Neutralize AUTHENTIC_BUNDLE in desktop
html = html.replace(
    'var AUTHENTIC_BUNDLE = {"profile": {"name": "Nikhil Vyas", "dob": "1984-11-23", "tob": "04:51 PM", "city": "Pali, Rajasthan", "lat": 25.58, "lon": 73.38, "gender": "Male", "asc_sign": "मेष", "asc_dms": "23°27\'09\\""}',
    'var AUTHENTIC_BUNDLE = {"profile": {"name": "संदर्भ जातक", "dob": "2000-01-01", "tob": "12:00 PM", "city": "नई दिल्ली (New Delhi)", "lat": 28.6139, "lon": 77.2090, "gender": "Male", "asc_sign": "मेष", "asc_dms": "15°00\'00\\""}'
)

# 2. openSavedProfilesModal founder profile removal
old_modal_saved = """            if (isNikhil) {
                html += '<div style="background:var(--bg-canvas); border:1.5px solid var(--border-gold); padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                    '<div>' +
                        '<b style="color:var(--primary-navy); font-size:0.92rem;">निखिल व्यास (संस्थापक • MAJY)</b><br>' +
                        '<span style="font-size:0.78rem; color:var(--text-secondary);">23 Nov 1984, 04:51 PM Pali, Rajasthan (मेष लग्न 23°27&apos;)</span>' +
                    '</div>' +
                    '<button class="header-btn primary" onclick="VyasDesktop.loadAuthenticNikhilProfile()">लोड करें</button>' +
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
                    html += '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                        '<div>' +
                            '<b style="color:var(--primary-navy); font-size:0.90rem;">' + (p.name || 'सुरक्षित जातक') + '</b><br>' +
                            '<span style="font-size:0.78rem; color:var(--text-secondary);">' + (p.dob || '') + ' ' + (p.tob || '') + ' • ' + (p.city || '') + '</span>' +
                        '</div>' +
                        '<button class="header-btn" onclick="VyasDesktop.loadCustomProfile(' + i + ')">लोड करें</button>' +
                    '</div>';
                }
            } else if (!isNikhil) {
                html += '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.88rem;">' +
                    '<div style="font-size:1.8rem; margin-bottom:8px;">🔒</div>' +
                    '<b style="color:var(--primary-navy); font-size:0.95rem;">कोई सुरक्षित कुण्डली उपलब्ध नहीं है</b>' +
                    '<p style="font-size:0.80rem; margin-top:6px; color:var(--text-secondary); line-height:1.5;">अपनी कुण्डली सुरक्षित रखने हेतु कृपया लॉगिन करें अथवा "नई कुण्डली" बटन द्वारा अपनी जन्म पत्रिका बनाएं।</p>' +
                '</div>';
            }"""

new_modal_saved = """            var customProfiles = [];
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
                    html += '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:12px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">' +
                        '<div>' +
                            '<b style="color:var(--primary-navy); font-size:0.90rem;">' + (p.name || 'सुरक्षित जातक') + '</b><br>' +
                            '<span style="font-size:0.78rem; color:var(--text-secondary);">' + (p.dob || '') + ' ' + (p.tob || '') + ' • ' + (p.city || '') + '</span>' +
                        '</div>' +
                        '<button class="header-btn" onclick="VyasDesktop.loadCustomProfile(' + i + ')">लोड करें</button>' +
                    '</div>';
                }
            } else {
                html += '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.88rem;">' +
                    '<div style="font-size:1.8rem; margin-bottom:8px;">📜</div>' +
                    '<b style="color:var(--primary-navy); font-size:0.95rem;">कोई सुरक्षित कुण्डली उपलब्ध नहीं है</b>' +
                    '<p style="font-size:0.80rem; margin-top:6px; color:var(--text-secondary); line-height:1.5;">अपनी जन्म पत्रिका बनाने व सुरक्षित रखने हेतु नीचे दिए बटन से विवरण प्रविष्ट करें।</p>' +
                '</div>';
            }
            html += '<div style="margin-top:12px;">' +
                '<button onclick="VyasDesktop.openNewProfileModal(); VyasDesktop.closeModals();" class="header-btn primary" style="width:100%; padding:10px; font-size:0.92rem; font-weight:700; border-radius:6px;">+ नई कुण्डली प्रविष्ट करें</button>' +
            '</div>';"""

if old_modal_saved in html:
    html = html.replace(old_modal_saved, new_modal_saved)
    print("✓ openSavedProfilesModal in index.html updated")
else:
    print("! Warning: openSavedProfilesModal pattern in index.html not found directly")

# 3. Purge founder profile injection in handleGoogleAuthResponse / init
html = re.sub(
    r"var isNikhil = \(name && name\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\) \|\|\s*\(email && email\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\);\s*if \(isNikhil\) \{\s*this\.activeChartData = window\.AUTHENTIC_BUNDLE;\s*localStorage\.setItem\('vyas_active_profile', JSON\.stringify\(window\.AUTHENTIC_BUNDLE\)\);\s*\} else \{\s*this\.activeChartData = null;\s*localStorage\.removeItem\('vyas_active_profile'\);\s*\}",
    "// Safe auth response without forced profile injection\nif (!this.activeChartData) { var s = localStorage.getItem('vyas_active_profile'); if (s) { try { this.activeChartData = JSON.parse(s); } catch(e) {} } }",
    html
)

html = re.sub(
    r"var isNikhil = \(data\.name && data\.name\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\) \|\|\s*\(data\.email && data\.email\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\);\s*if \(isNikhil\) \{\s*this\.activeChartData = window\.AUTHENTIC_BUNDLE;\s*localStorage\.setItem\('vyas_active_profile', JSON\.stringify\(window\.AUTHENTIC_BUNDLE\)\);\s*\}",
    "// Safe data handler without forced founder injection",
    html
)

# 4. In loadStoredProfile, purge any profile with 1984-11-23 or Nikhil
html = re.sub(
    r"if \(data && data\.profile && \(data\.profile\.name === 'अतिथि जातक \(Guest\)' \|\| \(data\.profile\.name\.indexOf\('Nikhil'\) !== -1 && data\.profile\.asc_sign === 'कन्या'\)\)\) \{\s*localStorage\.removeItem\('vyas_active_profile'\);\s*saved = null;\s*\}",
    "if (data && data.profile && (data.profile.dob === '1984-11-23' || (data.profile.name && data.profile.name.indexOf('Nikhil') !== -1) || (data.profile.name && data.profile.name.indexOf('संस्थापक') !== -1))) {\nlocalStorage.removeItem('vyas_active_profile');\nsaved = null;\ndata = null;\n}",
    html
)

# Remove isNikhil check in init of index.html
html = re.sub(
    r"if \(gUser\) \{\s*var isNikhil = \(gUser\.name && gUser\.name\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\) \|\|\s*\(gUser\.email && gUser\.email\.toLowerCase\(\)\.indexOf\('nikhil'\) !== -1\);\s*if \(isNikhil\) \{\s*this\.activeChartData = window\.AUTHENTIC_BUNDLE;\s*hasStored = true;\s*try \{ localStorage\.setItem\('vyas_active_profile', JSON\.stringify\(window\.AUTHENTIC_BUNDLE\)\); \} catch\(e\) \{\}\s*\}\s*\}",
    "// No automatic founder chart loading on init",
    html
)

# 5. Clean up fallbacks
html = html.replace('if (!dob) dob = "1984-11-23";', 'if (!dob) dob = "2000-01-01";')
html = html.replace('var y = parseInt(dParts[0]) || 1984;', 'var y = parseInt(dParts[0]) || 2000;')
html = html.replace('return isNaN(dt.getTime()) ? new Date(1984, 10, 23, 16, 51, 0).getTime() : dt.getTime();', 'return isNaN(dt.getTime()) ? new Date(2000, 0, 1, 12, 0, 0).getTime() : dt.getTime();')
html = html.replace('var dob = prof.dob || "1984-11-23";', 'var dob = prof.dob || "2000-01-01";')
html = html.replace('var city = prof.city || "Pali, Rajasthan";', 'var city = prof.city || "नई दिल्ली (New Delhi)";')
html = html.replace('var yr = 1984, mo = 11, dy = 23, hr = 16, mn = 51;', 'var yr = 2000, mo = 1, dy = 1, hr = 12, mn = 0;')
html = html.replace('var birthMs = new Date("1984-11-23T16:51:00+05:30").getTime();', 'var birthMs = new Date("2000-01-01T12:00:00+05:30").getTime();')
html = html.replace('var city = document.getElementById(\'edit_city\').value.trim() || "Pali";', 'var city = document.getElementById(\'edit_city\').value.trim() || "नई दिल्ली";')

with open(desktop_file, "w", encoding="utf-8") as f:
    f.write(html)
print(f"✓ Saved updated {desktop_file} ({len(html)} chars)")

