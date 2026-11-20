# Comprehensive patch script for VYAS platform
# 1. Bump CURRENT_ENGINE_VERSION to v5.0_pure_math_parashari_2026
# 2. Add full client-side auto-heal in loadStoredProfile()
# 3. Enhance computeMathematicalKundli with Vargottama, Pushkar Navamsha, and Pushkar Bhaga
# 4. Bulletproof generateDiamondSVG so House 1 always shows true Varga Ascendant sign
# 5. Fix renderAshtakavarga to strictly use authentic mathematical BPHS SAV and dynamic sutra text
# 6. Complete 7-Day Day & Night Chaughadiya engine with live active highlight & Wednesday Abhijit lock
# 7. Remove duplicate inline chatbot column and optimize cockpit layout to 2-column

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original index.html length:", len(content))

# 1. Update CURRENT_ENGINE_VERSION
old_ver = "var CURRENT_ENGINE_VERSION = 'v4.2_swiss_precision_2026';"
new_ver = "var CURRENT_ENGINE_VERSION = 'v5.0_pure_math_parashari_2026';"
if old_ver in content:
    content = content.replace(old_ver, new_ver)
    print("Updated CURRENT_ENGINE_VERSION to v5.0_pure_math_parashari_2026")
else:
    print("Warning: old_ver string not found verbatim, searching regex")
    content = re.sub(r"var\s+CURRENT_ENGINE_VERSION\s*=\s*['\"][^'\"]+['\"];", new_ver, content)
    print("Regex replaced CURRENT_ENGINE_VERSION")

# 2. Enhance loadStoredProfile with universal auto-heal
load_stored_old = '''        loadStoredProfile() {
            var CURRENT_ENGINE_VERSION = 'v5.0_pure_math_parashari_2026';
            try {
                if (localStorage.getItem('vyas_engine_version') !== CURRENT_ENGINE_VERSION) {
                    var stored = localStorage.getItem('vyas_active_profile');
                    if (stored) {
                        var parsed = JSON.parse(stored);
                        if (parsed && parsed.profile && (parsed.profile.name.indexOf('NIKHIL') !== -1 || parsed.profile.dob === '1984-11-23')) {
                            // Purge stale cached profile to reload fresh Swiss Ephemeris 23°27'09" & accurate SAV 337
                            localStorage.removeItem('vyas_active_profile');
                        }
                    }
                    localStorage.setItem('vyas_engine_version', CURRENT_ENGINE_VERSION);
                }
            } catch(e) {}'''

load_stored_new = '''        loadStoredProfile() {
            var CURRENT_ENGINE_VERSION = 'v5.0_pure_math_parashari_2026';
            try {
                var storedVer = localStorage.getItem('vyas_engine_version');
                var stored = localStorage.getItem('vyas_active_profile');
                if (storedVer !== CURRENT_ENGINE_VERSION || !stored) {
                    // Universal Auto-Heal: Stale engine version or corrupted D-charts/SAV detected
                    if (stored) {
                        try {
                            var pData = JSON.parse(stored);
                            if (pData && pData.profile && pData.profile.dob) {
                                // Dynamically recompute pure mathematical kundli for ANY user
                                var fresh = this.computeMathematicalKundli(
                                    pData.profile.name,
                                    pData.profile.dob,
                                    pData.profile.tob || '12:00',
                                    pData.profile.city || '',
                                    pData.profile.gender || 'Male',
                                    pData.profile.lat || 25.0,
                                    pData.profile.lon || 73.0
                                );
                                if (fresh) {
                                    localStorage.setItem('vyas_active_profile', JSON.stringify(fresh));
                                }
                            } else {
                                localStorage.removeItem('vyas_active_profile');
                            }
                        } catch(err) {
                            localStorage.removeItem('vyas_active_profile');
                        }
                    }
                    localStorage.setItem('vyas_engine_version', CURRENT_ENGINE_VERSION);
                }
            } catch(e) {}'''

if load_stored_old in content:
    content = content.replace(load_stored_old, load_stored_new)
    print("Replaced loadStoredProfile with universal auto-heal")
else:
    print("Warning: load_stored_old not found verbatim!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved intermediate index.html")

