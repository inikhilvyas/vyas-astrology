import re, sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Original size:", len(html))

# 1. Remove quickLoginFounder function
pos_qlf = html.find('quickLoginFounder: function() {')
if pos_qlf != -1:
    pos_end_qlf = html.find('launchGoogleOAuth: function() {', pos_qlf)
    if pos_end_qlf != -1:
        html = html[:pos_qlf] + html[pos_end_qlf:]
        print("✓ Removed quickLoginFounder function completely")
    else:
        print("WARNING: launchGoogleOAuth not found after quickLoginFounder")
else:
    print("WARNING: quickLoginFounder not found")

# 2. Remove authenticSwissPlanets array holding Nikhil's planets
pos_asp = html.find('authenticSwissPlanets: [')
if pos_asp != -1:
    pos_end_asp = html.find('],', pos_asp)
    if pos_end_asp != -1:
        html = html[:pos_asp] + 'authenticSwissPlanets: []' + html[pos_end_asp+1:]
        print("✓ Cleared authenticSwissPlanets array")
    else:
        print("WARNING: end of authenticSwissPlanets not found")

# 3. Remove hardcoded isFounderPrecise check and anchor in computeMathematicalKundli
target_fp_def = '''var isFounderPrecise = isNikhilVyas && (
                !tobStr || 
                (parsedHr === 16 && parsedMn >= 48 && parsedMn <= 54) ||
                tobStr.indexOf("16:51") !== -1 || 
                tobStr.indexOf("04:51") !== -1 || 
                tobStr.indexOf("4:51") !== -1 ||
                tobStr.indexOf("16:52") !== -1 || 
                tobStr.indexOf("16:50") !== -1
            );'''
if target_fp_def in html:
    html = html.replace(target_fp_def, 'var isFounderPrecise = false;')
    print("✓ Disabled isFounderPrecise flag")

# Remove the block that overrode sids with hardcoded values:
pos_anchor = html.find('// NASA JPL / Swiss Ephemeris 0.001" Exact Precision Anchor for Founder')
if pos_anchor != -1:
    pos_anchor_end = html.find('// 8. Planet Table & Bhavas Placement', pos_anchor)
    if pos_anchor_end != -1:
        html = html[:pos_anchor] + html[pos_anchor_end:]
        print("✓ Removed hardcoded planetary anchor block from computeMathematicalKundli")

# 4. Remove fallback Anuradha Moon longitude (224.639)
html = html.replace("var moonLon = 224.639; // Default: Anuradha 14°38' Scorpio (Nikhil Vyas)",
                    "var moonLon = 0.0; // Default: Ashwini 0° Mesha")
html = html.replace("(typeof mp.lon === 'number' ? mp.lon : (mp.full_degree || 224.639))",
                    "(typeof mp.lon === 'number' ? mp.lon : (mp.full_degree || 0.0))")
print("✓ Replaced fallback Moon longitude 224.639 with neutral 0.0")

# 5. Remove hardcoded computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", ...) from onGoogleAuthSuccess and loadStoredProfile
html = html.replace('this.activeChartData = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);',
                    'this.activeChartData = null;')

pos_case3 = html.find('// Case 3: Founder login default computation')
if pos_case3 != -1:
    pos_case3_end = html.find('// Privacy Invariant: If no authentic profile belongs to this user, remain in clean Blank Slate mode', pos_case3)
    if pos_case3_end != -1:
        html = html[:pos_case3] + html[pos_case3_end:]
        print("✓ Removed Case 3 Founder default computation from loadStoredProfile")

# 6. Change default edit_tob in HTML
html = html.replace('id="edit_tob" value="16:51"', 'id="edit_tob" value="12:00"')
html = html.replace('placeholder="16:51 या 04:51 PM"', 'placeholder="12:00 या 10:30 AM"')
print("✓ Set default edit_tob to neutral 12:00")

# 7. Add user login audit logging call in onGoogleAuthSuccess
login_audit_call = '''            // Send lightweight privacy-respecting login record to server (Zero Kundli Data transmitted)
            try {
                fetch('/api/log_user_login.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: this.googleUser.name,
                        email: this.googleUser.email,
                        picture: this.googleUser.picture,
                        sub: this.googleUser.sub,
                        time: new Date().toISOString()
                    })
                }).catch(function(e) {});
            } catch(e) {}
'''

pos_succ = html.find('this.updateGoogleAuthUI();\n            this.closeModals();')
if pos_succ != -1:
    html = html[:pos_succ] + 'this.updateGoogleAuthUI();\n            this.closeModals();\n' + login_audit_call + html[pos_succ + len('this.updateGoogleAuthUI();\n            this.closeModals();'):]
    print("✓ Added login audit call in onGoogleAuthSuccess")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html size:", len(html))

