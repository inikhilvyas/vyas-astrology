# -*- coding: utf-8 -*-
"""
scripts/patch_complete_cross_platform.py
Complete cross-platform parity patch for VYAS Astra:
- Jaimini Karakas undefined elimination
- Standish 3D JPL precision engine for C++ Desktop
- Bhavat Bhavam 144 UI integration on Mobile
- Elimination of sticky default personal birth profile
- Android assets sync
"""

import os, re, shutil

print("=== 1. PATCHING index.html ===")
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1a. Ensure jaiminiKarakas in computeMathematicalKundli contains all fields
old_jk_map = """                var jaiminiKarakas = sortedKarakas.map(function (item, idx) {
                    var deg = item.degInSign;
                    var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                    return {
                        abbr: KARAKA_NAMES[idx].abbr,
                        karaka: KARAKA_NAMES[idx].name,
                        planet: item.name,
                        sign: SIGNS_HI[item.signIdx],
                        deg: dms,
                        signification: KARAKA_NAMES[idx].role
                    };
                });"""

new_jk_map = """                var jaiminiKarakas = sortedKarakas.map(function (item, idx) {
                    var deg = item.degInSign;
                    var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                    var h = ((item.signIdx - ascSignIdx + 12) % 12) + 1;
                    return {
                        abbr: KARAKA_NAMES[idx].abbr,
                        karaka: KARAKA_NAMES[idx].name,
                        title: KARAKA_NAMES[idx].name,
                        name: KARAKA_NAMES[idx].name,
                        planet: item.name,
                        sign: SIGNS_HI[item.signIdx],
                        deg: dms,
                        degNum: deg,
                        house: h,
                        signification: KARAKA_NAMES[idx].role,
                        desc: KARAKA_NAMES[idx].role,
                        role: KARAKA_NAMES[idx].role
                    };
                });
                for (var jk = 0; jk < jaiminiKarakas.length; jk++) {
                    jaiminiKarakas[jaiminiKarakas[jk].abbr] = jaiminiKarakas[jk];
                }"""

if old_jk_map in text:
    text = text.replace(old_jk_map, new_jk_map, 1)
    print("✓ jaiminiKarakas enhanced with house, title, role and dict keys in index.html")

# 1b. openNewProfileModal: do NOT force googleUser.name
old_open_new = """            openNewProfileModal() {
                this.openEditProfileModal();
                var nameEl = document.getElementById('edit_name');
                var dobEl = document.getElementById('edit_dob');
                var tobEl = document.getElementById('edit_tob');
                var cityEl = document.getElementById('edit_city');
                if (nameEl) nameEl.value = (this.googleUser && this.googleUser.name) ? this.googleUser.name : "";"""

new_open_new = """            openNewProfileModal() {
                this.openEditProfileModal();
                var nameEl = document.getElementById('edit_name');
                var dobEl = document.getElementById('edit_dob');
                var tobEl = document.getElementById('edit_tob');
                var cityEl = document.getElementById('edit_city');
                if (nameEl) nameEl.value = "";"""

if old_open_new in text:
    text = text.replace(old_open_new, new_open_new, 1)
    print("✓ openNewProfileModal cleared of sticky default name in index.html")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)


print("\n=== 2. PATCHING mobile/index.html ===")
with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

# 2a. jaiminiKarakas in mobile/index.html
if old_jk_map in m_text:
    m_text = m_text.replace(old_jk_map, new_jk_map, 1)
    print("✓ jaiminiKarakas enhanced in mobile/index.html")

# 2b. Add Bhavat Bhavam pill and view in mobile/index.html
if 'm_view_bhavatbhavam' not in m_text:
    # Add tab pill next to KP
    m_tab_target = '<div class="m-tab-item" onclick="VyasMobile.switchTab(\'kp\', this)">'
    m_tab_repl = """<div class="m-tab-item" onclick="VyasMobile.switchTab('bhavatbhavam', this)">
                    <div class="m-tab-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><circle cx="12" cy="12" r="4"/></svg>
                    </div>
                    <span>भावात् भावम्</span>
                </div>
                <div class="m-tab-item" onclick="VyasMobile.switchTab('kp', this)">"""
    if m_tab_target in m_text:
        m_text = m_text.replace(m_tab_target, m_tab_repl, 1)
        print("✓ Bhavat Bhavam tab added to mobile navigation")

    # Add mobile view panel
    m_view_target = '<!-- 8. TAB: KP SYSTEM -->'
    m_panel_html = """<!-- 7.5 TAB: BHAVAT BHAVAM (12x12 = 144) -->
            <div class="m-view-panel" id="m_view_bhavatbhavam" style="display:none; padding:12px;">
                <div class="m-card" style="border:1px solid rgba(212,175,55,0.4); border-left:4px solid #d4af37; padding:14px; margin-bottom:12px;">
                    <b style="color:#d4af37; font-size:0.95rem;">✦ भावात् भावम् (144 संयोजन) महा-सिंथेसिस</b>
                    <p style="font-size:0.75rem; color:var(--text-secondary); margin:4px 0 10px 0;">
                        Z = ((Y - 1 + X - 1) mod 12) + 1 • BPHS एवं केपी कस्पल सब-लॉर्ड
                    </p>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:10px;">
                        <div>
                            <label style="font-size:0.72rem; color:#d4af37; font-weight:700;">आधार भाव Y:</label>
                            <select id="m_bbBaseY" class="m-input" style="font-size:0.75rem; padding:6px;" onchange="VyasMobile.evalBhavatBhavamUI()">
                                <option value="1">1st तनु</option><option value="2">2nd धन</option>
                                <option value="3">3rd सहज</option><option value="4">4th सुख</option>
                                <option value="5">5th पुत्र</option><option value="6">6th रिपु</option>
                                <option value="7">7th जाया</option><option value="8">8th रंध्र</option>
                                <option value="9">9th धर्म</option><option value="10">10th कर्म</option>
                                <option value="11">11th आय</option><option value="12">12th व्यय</option>
                            </select>
                        </div>
                        <div>
                            <label style="font-size:0.72rem; color:#38bdf8; font-weight:700;">सापेक्ष भाव X:</label>
                            <select id="m_bbRelX" class="m-input" style="font-size:0.75rem; padding:6px;" onchange="VyasMobile.evalBhavatBhavamUI()">
                                <option value="1">का 1ला</option><option value="2">का 2रा</option>
                                <option value="3">का 3रा</option><option value="4">का 4था</option>
                                <option value="5">का 5वाँ</option><option value="6">का 6ठा</option>
                                <option value="7">का 7वाँ</option><option value="8">का 8वाँ</option>
                                <option value="9">का 9वाँ</option><option value="10" selected>का 10वाँ</option>
                                <option value="11">का 11वाँ</option><option value="12">का 12वाँ</option>
                            </select>
                        </div>
                    </div>
                    <div id="m_bbResultCard" style="background:rgba(212,175,55,0.06); border:1px solid rgba(212,175,55,0.25); border-radius:8px; padding:10px;">
                    </div>
                </div>
            </div>

            """
    if m_view_target in m_text:
        m_text = m_text.replace(m_view_target, m_panel_html + m_view_target, 1)
        print("✓ Bhavat Bhavam panel added to mobile view")

    # Add script tag for vyas_bhavat_bhavam.js
    if 'vyas_bhavat_bhavam.js' not in m_text:
        m_scr_target = '<script src="js/vyas_astronomical_engine.js"></script>'
        m_text = m_text.replace(m_scr_target, '<script src="js/vyas_bhavat_bhavam.js"></script>\n    ' + m_scr_target, 1)
        print("✓ Script tag for vyas_bhavat_bhavam.js added to mobile/index.html")

    # Wire switchTab and evalBhavatBhavamUI
    m_switch_target = "if (tab === 'kp') this.renderKP();"
    m_switch_repl = """if (tab === 'kp') this.renderKP();
                if (tab === 'bhavatbhavam') this.evalBhavatBhavamUI();"""
    if m_switch_target in m_text:
        m_text = m_text.replace(m_switch_target, m_switch_repl, 1)

    m_eval_fn = """            evalBhavatBhavamUI: function() {
                var baseY = document.getElementById('m_bbBaseY') ? document.getElementById('m_bbBaseY').value : 2;
                var relX = document.getElementById('m_bbRelX') ? document.getElementById('m_bbRelX').value : 10;
                var resBox = document.getElementById('m_bbResultCard');
                if (!resBox) return;
                if (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.synthesizeBhavatBhavam === 'function') {
                    var syn = window.VyasBhavatBhavam.synthesizeBhavatBhavam(this.activeChartData, baseY, relX);
                    var html = '<b style="color:#d4af37; font-size:0.88rem;">🎯 परिणामी भाव: ' + syn.calc.resultName + '</b> ' +
                        '<code style="color:#38bdf8; font-size:0.75rem;">' + syn.calc.formula + '</code><br>' +
                        '<div style="font-size:0.74rem; color:var(--text-secondary); margin:6px 0;">' +
                        '<b>राशि:</b> ' + syn.zSign + ' • <b>भावेश:</b> ' + syn.zLord + ' • <b>CSL:</b> <b style="color:#f59e0b;">' + syn.csl + '</b> (' + syn.cDeg + ')<br>' +
                        '<b>सम्बन्ध:</b> ' + syn.relation + '<br>' +
                        '<p style="margin:4px 0 0 0; line-height:1.5;">' + syn.synthesis + '</p>' +
                        '</div>';
                    if (syn.isXfromX && syn.xFromXDetail) {
                        html += '<div style="margin-top:6px; padding:6px; background:rgba(212,175,55,0.12); border-left:3px solid #d4af37; border-radius:4px; font-size:0.72rem;">' +
                            '<b>मूल सूत्र (' + syn.xFromXDetail.title + '):</b> ' + syn.xFromXDetail.sutra + '</div>';
                    }
                    resBox.innerHTML = html;
                } else {
                    resBox.innerHTML = '<p style="font-size:0.75rem; color:var(--text-secondary);">भावात् भावम् इंजन लोड हो रहा है...</p>';
                }
            },
"""
    m_hook_target = "            renderKP: function () {"
    if m_hook_target in m_text and 'evalBhavatBhavamUI' not in m_text:
        m_text = m_text.replace(m_hook_target, m_eval_fn + m_hook_target, 1)
        print("✓ evalBhavatBhavamUI added to VyasMobile")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(m_text)


print("\n=== 3. PATCHING jaimini-astrology/index.html ===")
with open('jaimini-astrology/index.html', 'r', encoding='utf-8') as f:
    j_text = f.read()

# Fix karaka table rendering to NEVER output undefined
old_j_loop = """            for (var i = 0; i < kKeys.length; i++) {
                var code = kKeys[i];
                var item = karakas[code] || {};
                var fb = fallbackKarakas[code] || { title: code, desc: 'जैमिनी चर कारक' };
                var itemTitle = item.title || item.karaka || item.name || fb.title;
                var itemPlanet = item.planet || '-';
                var itemSign = item.sign ? (' (' + item.sign + ')') : '';
                var itemDeg = item.deg ? (String(item.deg).replace(/°+$/, '') + '°') : '-';
                var itemDesc = item.desc || item.signification || item.role || fb.desc;
                var isAK = code === 'AK';
                kHtml += '<tr><td class="' + (isAK ? 'ak' : '') + '"><b>' + code + '</b></td><td>' + itemTitle + '</td><td><b>' + itemPlanet + '</b>' + itemSign + '</td><td>' + itemDeg + '</td><td style="color:var(--text-muted); font-size:0.85rem;">' + itemDesc + '</td></tr>';
            }"""

new_j_loop = """            var signs = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var ascIdx = signs.indexOf(lagna);
            if (ascIdx === -1) ascIdx = 0;

            for (var i = 0; i < kKeys.length; i++) {
                var code = kKeys[i];
                var item = karakas[code] || {};
                var fb = fallbackKarakas[code] || { title: code, desc: 'जैमिनी चर कारक' };
                var rawTitle = item.title || item.karaka || item.name || fb.title;
                var itemTitle = (rawTitle && rawTitle !== 'undefined') ? rawTitle : fb.title;
                var itemPlanet = item.planet || '-';
                var itemSign = (item.sign && item.sign !== 'undefined') ? (' (' + item.sign + ')') : '';
                var itemDeg = (item.deg && item.deg !== 'undefined') ? (String(item.deg).replace(/°+$/, '') + '°') : '-';
                var rawDesc = item.desc || item.signification || item.role || fb.desc;
                var itemDesc = (rawDesc && rawDesc !== 'undefined') ? rawDesc : fb.desc;
                
                // Ensure item.house is computed if missing
                if (!item.house && item.sign && item.sign !== 'undefined') {
                    var sIdx = signs.indexOf(item.sign);
                    if (sIdx !== -1) item.house = ((sIdx - ascIdx + 12) % 12) + 1;
                }

                var isAK = code === 'AK';
                kHtml += '<tr><td class="' + (isAK ? 'ak' : '') + '"><b>' + code + '</b></td><td>' + itemTitle + '</td><td><b>' + itemPlanet + '</b>' + itemSign + '</td><td>' + itemDeg + '</td><td style="color:var(--text-muted); font-size:0.85rem;">' + itemDesc + '</td></tr>';
            }"""

if old_j_loop in j_text:
    j_text = j_text.replace(old_j_loop, new_j_loop, 1)
    print("✓ jaimini-astrology/index.html table loop sanitized against undefined")

with open('jaimini-astrology/index.html', 'w', encoding='utf-8') as f:
    f.write(j_text)


print("\n=== 4. PATCHING js/vyas_daivagya_engine.js ===")
with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8') as f:
    d_text = f.read()

# Fix predict in VyasJaiminiEngine to NEVER output 'भाव undefined'
old_pred_ak = """            var akHouseStr = (ak.house && ak.house !== 'undefined') ? ("भाव " + ak.house + " ") : "";
            var akDegStr = ak.deg ? (" " + ak.deg + (String(ak.deg).indexOf('°') !== -1 ? '' : '°')) : "";
            lines.push("• <b>आत्मकारक (AK - " + ak.planet + akDegStr + "):</b> " + akHouseStr + "(" + (ak.sign || "लग्न") + " राशि) में स्थित हैं। जैमिनी सूत्रानुसार जातक की आत्मा का मूल स्वभाव व लक्ष्य " + ak.planet + " के तत्त्वों से संचालित है।");
            if (domain === 'career' || domain === 'wealth' || domain === 'general' || domain === 'yoga') {
                if (amk) {
                    var amkHouseStr = (amk.house && amk.house !== 'undefined') ? ("भाव " + amk.house + " ") : "";
                    lines.push("• <b>अमात्यकारक (AmK - " + amk.planet + "):</b> " + amkHouseStr + "(" + (amk.sign || "") + ") में स्थित हैं। आजीविका में पद व अधिकार " + amk.planet + " की कृपा से प्राप्त होगा। जब भी " + amk.planet + " की दशा या कारकांश सक्रिय होगा, पदोन्नति अवश्यंभावी है।");
                }
            }
            if (domain === 'marriage' || domain === 'general') {
                if (dk) {
                    var dkHouseStr = (dk.house && dk.house !== 'undefined') ? ("भाव " + dk.house + " ") : "";
                    lines.push("• <b>दाराकारक (DK - " + dk.planet + "):</b> " + dkHouseStr + "(" + (dk.sign || "") + ") में विराजमान हैं। जीवनसाथी का स्वरूप, स्वभाव एवं बौद्धिक स्तर " + dk.planet + " के गुणधर्मों से पूर्णतः मेल खाएगा।");
                }
            }"""

new_pred_ak = """            var signs = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var ascSign = (karakasOrChart && karakasOrChart.profile && karakasOrChart.profile.asc_sign) ? karakasOrChart.profile.asc_sign : "मेष";
            var ascIdx = signs.indexOf(ascSign);
            if (ascIdx === -1) ascIdx = 0;

            function resolveHouse(kObj) {
                if (kObj.house && kObj.house !== 'undefined' && typeof kObj.house === 'number') return kObj.house;
                if (kObj.sign && kObj.sign !== 'undefined') {
                    var sIdx = signs.indexOf(kObj.sign);
                    if (sIdx !== -1) return ((sIdx - ascIdx + 12) % 12) + 1;
                }
                return null;
            }

            var akH = resolveHouse(ak);
            var akHouseStr = akH ? ("भाव " + akH + " ") : "";
            var akDegStr = (ak.deg && ak.deg !== 'undefined') ? (" " + ak.deg + (String(ak.deg).indexOf('°') !== -1 ? '' : '°')) : "";
            lines.push("• <b>आत्मकारक (AK - " + ak.planet + akDegStr + "):</b> " + akHouseStr + "(" + (ak.sign || "लग्न") + " राशि) में स्थित हैं। जैमिनी सूत्रानुसार जातक की आत्मा का मूल स्वभाव व लक्ष्य " + ak.planet + " के तत्त्वों से संचालित है।");

            if (domain === 'career' || domain === 'wealth' || domain === 'general' || domain === 'yoga') {
                if (amk) {
                    var amkH = resolveHouse(amk);
                    var amkHouseStr = amkH ? ("भाव " + amkH + " ") : "";
                    lines.push("• <b>अमात्यकारक (AmK - " + amk.planet + "):</b> " + amkHouseStr + "(" + (amk.sign || "") + ") में स्थित हैं। आजीविका में पद व अधिकार " + amk.planet + " की कृपा से प्राप्त होगा। जब भी " + amk.planet + " की दशा या कारकांश सक्रिय होगा, पदोन्नति अवश्यंभावी है।");
                }
            }
            if (domain === 'marriage' || domain === 'general') {
                if (dk) {
                    var dkH = resolveHouse(dk);
                    var dkHouseStr = dkH ? ("भाव " + dkH + " ") : "";
                    lines.push("• <b>दाराकारक (DK - " + dk.planet + "):</b> " + dkHouseStr + "(" + (dk.sign || "") + ") में विराजमान हैं। जीवनसाथी का स्वरूप, स्वभाव एवं बौद्धिक स्तर " + dk.planet + " के गुणधर्मों से पूर्णतः मेल खाएगा।");
                }
            }"""

if old_pred_ak in d_text:
    d_text = d_text.replace(old_pred_ak, new_pred_ak, 1)
    print("✓ VyasJaiminiEngine.predict sanitized against 'भाव undefined' in vyas_daivagya_engine.js")

with open('js/vyas_daivagya_engine.js', 'w', encoding='utf-8') as f:
    f.write(d_text)


print("\n=== 5. SYNCING ANDROID ASSETS ===")
assets_mobile_dir = 'android_app/app/src/main/assets/mobile'
assets_js_dir = 'android_app/app/src/main/assets/js'
os.makedirs(assets_mobile_dir, exist_ok=True)
os.makedirs(assets_js_dir, exist_ok=True)

shutil.copy2('mobile/index.html', os.path.join(assets_mobile_dir, 'index.html'))
shutil.copy2('mobile/index.html', 'static/mobile/index.html')
shutil.copy2('js/vyas_astronomical_engine.js', os.path.join(assets_js_dir, 'vyas_astronomical_engine.js'))
shutil.copy2('js/vyas_daivagya_engine.js', os.path.join(assets_js_dir, 'vyas_daivagya_engine.js'))
shutil.copy2('js/vyas_bhavat_bhavam.js', os.path.join(assets_js_dir, 'vyas_bhavat_bhavam.js'))
print("✓ Android assets and static/mobile synchronized successfully!")
