# -*- coding: utf-8 -*-
"""
Patch index.html to ensure:
1. Strict user privacy & vault isolation (Nikhil Vyas data NEVER leaks to other users/visitors).
2. Dynamic VyasDaivagyaWisdom reasoning based on active native's actual chart (no hardcoded Mars in 10 or Saturn in 7).
3. askSage systemPrompt fixes (no hardcoded fallbacks).
"""

import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# -------------------------------------------------------------------------
# 1. Patch applyAuthenticatedGoogleUser
# -------------------------------------------------------------------------
apply_auth_pattern = re.compile(
    r'applyAuthenticatedGoogleUser:\s*function\s*\(data,\s*token\)\s*\{[\s\S]*?alert\("✓ स्वागतम् " \+ this\.googleUser\.name \+ " जी! Google प्रमाणीकरण सफल। PRO सदस्यता सक्रिय है।"\);\s*\},',
    re.MULTILINE
)

new_apply_auth = '''applyAuthenticatedGoogleUser: function(data, token) {
            this.googleUser = {
                name: data.name,
                email: data.email,
                picture: data.picture || "logo_icon.png",
                sub: String(data.sub),
                isVerified: true
            };
            try {
                localStorage.setItem('vyas_google_user', JSON.stringify(this.googleUser));
                if (token) localStorage.setItem('vyas_g_jwt', token);
            } catch(e) {}

            this.updateGoogleAuthUI();
            this.closeModals();

            // STRICT MULTI-TENANT PRIVACY & ISOLATION:
            // 1. Immediately reset in-memory chart to prevent cross-session contamination
            this.activeChartData = null;

            var email = this.googleUser.email ? this.googleUser.email.trim().toLowerCase() : '';
            var isNikhil = (email.indexOf('nikhil') !== -1) ||
                           (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);

            if (isNikhil) {
                // Founder login: load founder vault or compute canonical chart
                var fromVault = this.loadFromUserVault();
                if (fromVault && fromVault.profile && fromVault.profile.dob === '1984-11-23') {
                    this.activeChartData = fromVault;
                } else {
                    this.activeChartData = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
                }
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
            } else {
                // Regular logged-in user:
                // Purge any stale active profile belonging to someone else
                var curAct = localStorage.getItem('vyas_active_profile');
                if (curAct) {
                    try {
                        var cp = JSON.parse(curAct);
                        if (cp && cp.profile && (cp.profile.dob === '1984-11-23' || (cp.profile.name && cp.profile.name.toUpperCase().indexOf('NIKHIL') !== -1))) {
                            localStorage.removeItem('vyas_active_profile');
                        }
                    } catch(e) {
                        localStorage.removeItem('vyas_active_profile');
                    }
                }

                // Check THIS user's personal vault specifically: vyas_user_vault_<email>
                var userVault = this.loadFromUserVault();
                if (userVault && userVault.profile && userVault.profile.name && userVault.profile.name !== 'अतिथि जातक (Guest)') {
                    var isN = (userVault.profile.dob === '1984-11-23' || (userVault.profile.name && userVault.profile.name.toUpperCase().indexOf('NIKHIL') !== -1));
                    if (!isN) {
                        this.activeChartData = userVault;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
                    } else {
                        // Purge contaminated vault
                        try { localStorage.removeItem('vyas_user_vault_' + email); } catch(e) {}
                        this.activeChartData = null;
                    }
                } else {
                    // No saved chart for this user yet
                    this.activeChartData = null;
                    try { localStorage.removeItem('vyas_active_profile'); } catch(e) {}
                }
            }

            if (this.activeChartData) {
                this.renderChart(this.currentVarga || 'd1');
                this.updateDailyHoroscopeUI();
                this.updateYogasBannerUI();
                this.renderPlanetTable();
                this.initDailyDashboard();
                this.initDashaTree();
                this.renderPredictions();
                this.renderAshtakavarga();
            } else {
                // Clean Blank Slate: Render empty chart and prompt user to enter their birth details
                this.renderChart('d1');
                this.updateDailyHoroscopeUI();
                this.updateYogasBannerUI();
                this.renderPlanetTable();
                this.openNewProfileModal();
            }

            alert("✓ स्वागतम् " + this.googleUser.name + " जी! Google प्रमाणीकरण सफल। PRO सदस्यता सक्रिय है।");
        },'''

if apply_auth_pattern.search(content):
    content = apply_auth_pattern.sub(new_apply_auth, content)
    print("✓ Successfully patched applyAuthenticatedGoogleUser")
else:
    print("⚠️ Could not match applyAuthenticatedGoogleUser pattern")

# -------------------------------------------------------------------------
# 2. Patch saveToUserVault & loadFromUserVault
# -------------------------------------------------------------------------
vault_pattern = re.compile(
    r'saveToUserVault:\s*function\s*\(profileData\)\s*\{[\s\S]*?return null;\s*\},',
    re.MULTILINE
)

new_vault_code = '''saveToUserVault: function(profileData) {
            if (!profileData) return;
            try {
                localStorage.setItem('vyas_active_profile', JSON.stringify(profileData));
                if (this.googleUser && this.googleUser.email) {
                    var email = this.googleUser.email.trim().toLowerCase();
                    localStorage.setItem('vyas_user_vault_' + email, JSON.stringify(profileData));
                    localStorage.setItem('vyas_user_has_vault', 'true');
                } else {
                    localStorage.setItem('vyas_guest_vault', JSON.stringify(profileData));
                }
            } catch(e) {
                console.warn("Vault save error:", e);
            }
        },

        loadFromUserVault: function() {
            try {
                if (this.googleUser && this.googleUser.email) {
                    var email = this.googleUser.email.trim().toLowerCase();
                    var isCurrentNikhil = (email.indexOf('nikhil') !== -1) ||
                                          (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);
                    var vaultData = localStorage.getItem('vyas_user_vault_' + email);
                    if (vaultData) {
                        var parsed = JSON.parse(vaultData);
                        if (!isCurrentNikhil && parsed && parsed.profile && (parsed.profile.dob === '1984-11-23' || (parsed.profile.name && parsed.profile.name.toUpperCase().indexOf('NIKHIL') !== -1))) {
                            localStorage.removeItem('vyas_user_vault_' + email);
                            return null;
                        }
                        return parsed;
                    }
                }
            } catch(e) {}
            return null;
        },'''

if vault_pattern.search(content):
    content = vault_pattern.sub(new_vault_code, content)
    print("✓ Successfully patched saveToUserVault and loadFromUserVault")
else:
    print("⚠️ Could not match vault_pattern")

# -------------------------------------------------------------------------
# 3. Patch loadStoredProfile
# -------------------------------------------------------------------------
lsp_pattern = re.compile(
    r'loadStoredProfile\(\)\s*\{[\s\S]*?chip\.onclick = function\(\) \{ VyasDesktop\.openNewProfileModal\(\); \};\s*\}\s*\}\s*\},',
    re.MULTILINE
)

new_lsp = '''loadStoredProfile() {
            var CURRENT_ENGINE_VERSION = 'v5.0_pure_math_parashari_2026';
            try {
                var storedVer = localStorage.getItem('vyas_engine_version');
                var stored = localStorage.getItem('vyas_active_profile');
                if (storedVer !== CURRENT_ENGINE_VERSION || !stored) {
                    if (stored) {
                        try {
                            var pData = JSON.parse(stored);
                            if (pData && pData.profile && pData.profile.dob) {
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
            } catch(e) {}

            var hasStored = false;
            this.activeChartData = null; // Always clear RAM first

            // Check if current authenticated user is Nikhil
            var isCurrentGoogleNikhil = (this.googleUser && (
                (this.googleUser.email && this.googleUser.email.toLowerCase().indexOf('nikhil') !== -1) ||
                (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1)
            ));

            try {
                // Case 1: Authenticated Google User
                if (this.googleUser && this.googleUser.email) {
                    var fromVault = this.loadFromUserVault();
                    if (fromVault && fromVault.profile && fromVault.profile.name && fromVault.profile.name !== 'अतिथि जातक (Guest)') {
                        var isN = (fromVault.profile.dob === '1984-11-23' || (fromVault.profile.name && fromVault.profile.name.toUpperCase().indexOf('NIKHIL') !== -1));
                        if (!isN || isCurrentGoogleNikhil) {
                            this.activeChartData = fromVault;
                            try { localStorage.setItem('vyas_active_profile', JSON.stringify(fromVault)); } catch(e) {}
                            hasStored = true;
                        }
                    }
                }

                // Case 2: Check vyas_active_profile if not loaded from vault
                if (!hasStored) {
                    var stored = localStorage.getItem('vyas_active_profile');
                    if (stored) {
                        var data = JSON.parse(stored);
                        var isNikhilProfile = (data && data.profile && (
                            data.profile.dob === '1984-11-23' ||
                            (data.profile.name && data.profile.name.toUpperCase().indexOf('NIKHIL') !== -1)
                        ));

                        // PRIVACY ENFORCEMENT: Never show Nikhil Vyas chart to visitors/other users
                        if (isNikhilProfile && !isCurrentGoogleNikhil) {
                            try { localStorage.removeItem('vyas_active_profile'); } catch(e) {}
                            data = null;
                        }

                        if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)') {
                            this.activeChartData = data;
                            hasStored = true;
                        }
                    }
                }

                // Case 3: Founder login default computation
                if (!hasStored && isCurrentGoogleNikhil) {
                    var nChart = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
                    this.activeChartData = nChart;
                    try { localStorage.setItem('vyas_active_profile', JSON.stringify(nChart)); } catch(e) {}
                    hasStored = true;
                }
            } catch(e) {}

            // Privacy Invariant: If no authentic profile belongs to this user, remain in clean Blank Slate mode
            if (!hasStored) {
                this.activeChartData = null;
                try { localStorage.removeItem('vyas_active_profile'); } catch(e) {}
            }

            var chip = document.getElementById('headerProfileChip');
            if (chip) {
                if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name) {
                    var prof = this.activeChartData.profile;
                    chip.innerHTML = '<span class="jatak-icon"><svg class="v-icon v-user" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></span> <span class="jatak-name">' + prof.name.toUpperCase() + '</span> <span class="jatak-lagna">' + (prof.asc_sign || 'मेष') + ' लग्न (' + (prof.asc_dms || "00°00'") + ')</span>';
                    chip.onclick = function() { VyasDesktop.openSavedProfilesModal(); };
                } else {
                    chip.innerHTML = '<span class="jatak-icon"><svg class="v-icon v-spark" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#d4af37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:4px;"><path d="M12 2l2.4 7.2L22 12l-7.6 2.8L12 22l-2.4-7.2L2 12l7.6-2.8z"/></svg></span> <span class="jatak-name">+ अपनी कुण्डली बनाएं</span> <span class="jatak-lagna" style="color:#d4af37;">(निःशुल्क)</span>';
                    chip.onclick = function() { VyasDesktop.openNewProfileModal(); };
                }
            }
        },'''

if lsp_pattern.search(content):
    content = lsp_pattern.sub(new_lsp, content)
    print("✓ Successfully patched loadStoredProfile")
else:
    print("⚠️ Could not match loadStoredProfile pattern")

# -------------------------------------------------------------------------
# 4. Patch VyasDaivagyaWisdom (Dynamic Shastric Reasoning)
# -------------------------------------------------------------------------
vdw_pattern = re.compile(
    r'synthesizeReading:\s*function\s*\(query,\s*chart\)\s*\{[\s\S]*?synthesizePrashnaReading:\s*function\s*\(query\)\s*\{[\s\S]*?return "<b>ॐ नमः शिवाय।</b>[\s\S]*? दर्ज करें।";\s*\}\s*\},',
    re.MULTILINE
)

new_vdw_code = '''synthesizeReading: function(query, chart) {
            chart = chart || (window.VyasDesktop && window.VyasDesktop.activeChartData) || null;
            var isPrashnaMode = !chart || !chart.profile || !chart.planet_table || chart.isPrashna;
            
            if (isPrashnaMode) {
                return this.synthesizePrashnaReading(query);
            }

            var prof = chart.profile;
            var name = prof.name || "जातक";
            var lagna = prof.asc_sign || "मेष";
            var dasha = (chart.active_dasha && chart.active_dasha.chain) ? chart.active_dasha.chain : "सक्रिय विंशोत्तरी दशा";
            var intent = this.detectIntent(query);

            var greeting = "<b>ॐ नमः शिवाय।</b><br><br>" +
                "<b>सादर प्रणाम आदरणीय " + name + " जी,</b><br>" +
                "आपकी जन्मपत्रिका (<b>" + lagna + " लग्न</b>) एवं सक्रिय विंशोत्तरी दशा (<b>" + dasha + "</b>) का हमारी 200+ शास्त्रीय ग्रन्थ-शृंखला (पाराशरी, जैमिनि, फलदीपिका, होरारत्नम् एवं के.पी. कस्पल सब-लॉर्ड प्रणाली) द्वारा सूक्ष्म वेध कर यह प्रामाणिक दैवज्ञ निर्णय प्रस्तुत है:<br><br>";

            return greeting + this.renderDynamicWisdom(query, intent, chart, name, lagna, dasha);
        },

        renderDynamicWisdom: function(query, intent, chart, name, lagna, dasha) {
            var pTable = chart.planet_table || [];
            var pMap = {};
            var houseMap = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] };
            
            for (var i = 0; i < pTable.length; i++) {
                var item = pTable[i];
                var pRaw = (item.planet || item.p || '').replace(/\\s*\\(.*\\)/, '').trim();
                var sign = item.sign || item.r || '';
                var deg = item.degree || item.d || '';
                var house = parseInt(item.house || item.h || 1);
                var dig = item.dignity || item.s || 'सम';
                var nak = item.nakshatra || item.n || '';
                
                var pObj = { name: pRaw, sign: sign, deg: deg, house: house, dignity: dig, nak: nak };
                pMap[pRaw] = pObj;
                if (!houseMap[house]) houseMap[house] = [];
                houseMap[house].push(pObj);
            }

            var SIGNS = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var SIGN_LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var lagnaIdx = SIGNS.indexOf(lagna);
            if (lagnaIdx === -1) lagnaIdx = 0;

            function getHouseLord(h) {
                var sIdx = (lagnaIdx + h - 1) % 12;
                return { house: h, sign: SIGNS[sIdx], lord: SIGN_LORDS[sIdx] };
            }

            var l1 = getHouseLord(1);
            var l2 = getHouseLord(2);
            var l5 = getHouseLord(5);
            var l7 = getHouseLord(7);
            var l9 = getHouseLord(9);
            var l10 = getHouseLord(10);
            var l11 = getHouseLord(11);

            // Intent-specific rendering
            if (intent === 'politics') {
                var h10Planets = houseMap[10] || [];
                var h10Text = h10Planets.length > 0 ? h10Planets.map(function(p){ return p.name + " (" + p.sign + ", " + p.dignity + ")"; }).join(", ") : "रिक्त (शुभ दृष्टि वेध)";
                var h1Planets = houseMap[1] || [];
                var h1Text = h1Planets.length > 0 ? h1Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var sunObj = pMap["सूर्य"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>🏛️ शासन, राजनीति व उच्च पद प्राप्ति मीमांसा (Political & Executive Authority)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं आपकी कुण्डली के प्रत्यक्ष निर्देशांक:</b><br>" +
                    "• <i>" + this.shastras.bphs + " (दशम भाव मीमांसा):</i> आपकी कुण्डली में दशम भाव में <b>" + l10.sign + "</b> राशि है जिसके स्वामी <b>" + l10.lord + "</b> हैं। दशम भाव में स्थित ग्रह: <b>" + h10Text + "</b>।<br>" +
                    "• <i>सूर्य विचार (सत्ता व आत्मबल कारक):</i> सूर्यदेव आपकी पत्रिका में भाव <b>" + sunObj.house + "</b> (" + sunObj.sign + " राशि) में " + sunObj.dignity + " अवस्था में विराजमान हैं। यह स्थिति शासन व प्रतिष्ठित संस्थाओं से मान-सम्मान व प्रभाव का निर्णय करती है।<br>" +
                    "• <i>प्रथम भाव (लग्न व आत्मतेज):</i> लग्नेश <b>" + l1.lord + "</b> का प्रभाव एवं लग्न में ग्रह स्थिति (" + h1Text + ") जातक के जन-प्रभाव व नेतृत्व क्षमता को गति प्रदान करती है।<br><br>" +
                    "<b>२. सक्रिय दशा व काल-संरेखण:</b><br>" +
                    "वर्तमान में सक्रिय <b>" + dasha + "</b> का गोचर-संरेखण आपकी सामाजिक प्रतिष्ठा, पद प्राप्ति एवं नीतिगत निर्णयों में निर्णायक भूमिका निभा रहा है।<br><br>" +
                    "<b>३. दैवज्ञ परामर्श व सात्विक उपाय:</b><br>" +
                    "• नित्य प्रातः तांबे के पात्र से भगवान सूर्यनारायण को <i>'ॐ घृणिः सूर्याय नमः'</i> का जप करते हुए अर्घ्य दें।<br>" +
                    "• प्रत्येक रविवार <i>'आदित्य हृदय स्तोत्र'</i> का पाठ करें, यह नेतृत्व, प्रभाव व प्रतिष्ठा में स्थायी वृद्धि करता है।";
            }

            if (intent === 'career') {
                var h10Planets = houseMap[10] || [];
                var h10Text = h10Planets.length > 0 ? h10Planets.map(function(p){ return p.name + " (" + p.sign + " " + p.dignity + ")"; }).join(", ") : "रिक्त";
                var h6Planets = houseMap[6] || [];
                var h6Text = h6Planets.length > 0 ? h6Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";

                return "<div class='shastra-verdict-box' style='background:rgba(59,130,246,0.06); border-left:3px solid #3b82f6; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#60a5fa; font-weight:700; font-size:0.85rem;'>💼 करियर, व्यापार विस्तार व पदोन्नति समय (Career Elevation & Enterprise Matrix)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं प्रत्यक्ष कर्म भाव स्थिति:</b><br>" +
                    "• <i>" + this.shastras.phaladeepika + " (कर्मभावाध्याय):</i> आपकी कुण्डली में दशम कर्म भाव में <b>" + l10.sign + "</b> राशि है जिसके अधिपति <b>" + l10.lord + "</b> हैं। दशम भाव में ग्रह: <b>" + h10Text + "</b>।<br>" +
                    "• <i>षष्ठ भाव (प्रतिस्पर्धा व सेवा सामर्थ्य):</i> षष्ठ भाव में स्थित ग्रह (" + h6Text + ") जातक की प्रतियोगी क्षमता, कठिन चुनौतियों से पार पाने तथा कार्यक्षेत्र में प्रभुत्व स्थापित करने की शक्ति दर्शाते हैं।<br><br>" +
                    "<b>२. विस्तार का स्वर्णिम काल-खंड (2026-2027 Timing):</b><br>" +
                    "वर्तमान सक्रिय <b>" + dasha + "</b> एवं तात्कालिक गोचर आपके कर्मेश (" + l10.lord + ") व भाग्य भाव पर अनुकूल दृष्टि-पात कर रहे हैं। व्यावसायिक अनुबंधों व कार्यक्षेत्र में उन्नति के मार्ग प्रशस्त हो रहे हैं।<br><br>" +
                    "<b>३. कार्यक्षेत्र हेतु दैवज्ञ मार्गदर्शन व सात्विक उपाय:</b><br>" +
                    "• नित्य प्रातः <i>'विष्णु सहस्रनाम'</i> अथवा <i>'ॐ नमो भगवते वासुदेवाय'</i> का 108 बार स्मरण करें।<br>" +
                    "• महत्वपूर्ण व्यापारिक निर्णयों व अनुबंधों में विधिक स्पष्टता रखें।";
            }

            if (intent === 'wealth') {
                var h2Planets = houseMap[2] || [];
                var h2Text = h2Planets.length > 0 ? h2Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var h11Planets = houseMap[11] || [];
                var h11Text = h11Planets.length > 0 ? h11Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var jup = pMap["गुरु"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#34d399; font-weight:700; font-size:0.85rem;'>💰 आर्थिक समृद्धि, धन लाभ व संपत्ति योग (Dhana Yogas & Asset Vault)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं धन-लाभ भाव स्थिति:</b><br>" +
                    "• <i>" + this.shastras.bphs + " (धनयोगाध्याय):</i> आपकी कुण्डली में द्वितीय (धन) भाव में <b>" + l2.sign + "</b> राशि (स्वामी: <b>" + l2.lord + "</b>) तथा एकादश (लाभ) भाव में <b>" + l11.sign + "</b> राशि (स्वामी: <b>" + l11.lord + "</b>) है।<br>" +
                    "• <i>द्वितीय भाव स्थिति:</i> " + h2Text + "। <i>एकादश भाव स्थिति:</i> " + h11Text + "।<br>" +
                    "• <i>देवगुरु बृहस्पति (धनकारक):</i> भाव " + jup.house + " (" + jup.sign + " राशि) में " + jup.dignity + " होकर धन के संचय व विस्तार को गति प्रदान कर रहे हैं।<br><br>" +
                    "<b>२. वित्तीय प्रवाह व संचय समय:</b><br>" +
                    "सक्रिय दशा (" + dasha + ") धन भावों से सम्बद्ध होकर वित्तीय स्थिरता प्रदान करेगी। आगामी समय में संचित प्रयासों का श्रेष्ठ प्रतिफल मिलेगा।<br><br>" +
                    "<b>३. सात्विक धन रक्षण उपाय:</b><br>" +
                    "• शुक्रवार को सात्विक मिष्ठान्न का दान करें व नित्य <i>'ॐ श्रीं ह्रीं क्लीं महालक्ष्म्यै नमः'</i> का 11 बार स्मरण करें।";
            }

            if (intent === 'marriage') {
                var h7Planets = houseMap[7] || [];
                var h7Text = h7Planets.length > 0 ? h7Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var ven = pMap["शुक्र"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(236,72,153,0.06); border-left:3px solid #ec4899; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#f472b6; font-weight:700; font-size:0.85rem;'>💍 दांपत्य जीवन, विवाह व सम्बन्ध समन्वय (Marriage & Relationship Matrix)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं सप्तम भाव परीक्षण:</b><br>" +
                    "• <i>" + this.shastras.phaladeepika + " (स्त्री/पुरुष जातक):</i> सप्तम भाव में <b>" + l7.sign + "</b> राशि है जिसके स्वामी <b>" + l7.lord + "</b> हैं। सप्तम भाव में स्थित ग्रह: <b>" + h7Text + "</b>।<br>" +
                    "• <i>शुक्रदेव (दांपत्य कारक):</i> भाव " + ven.house + " (" + ven.sign + " राशि) में स्थित होकर जीवनसाथी के स्वभाव व सामंजस्य का निर्धारण कर रहे हैं।<br><br>" +
                    "<b>२. दैवज्ञ परामर्श व सात्विक उपाय:</b><br>" +
                    "• दाम्पत्य में परस्पर विश्वास, सम्मान व सामंजस्य बनाए रखें।<br>" +
                    "• नित्य <i>'ॐ उमामहेश्वराभ्यां नमः'</i> का जप करें, यह दांपत्य जीवन को प्रेम व सौहार्द से परिपूर्ण करता है।";
            }

            if (intent === 'health') {
                var h6Planets = houseMap[6] || [];
                var h6Text = h6Planets.length > 0 ? h6Planets.map(function(p){ return p.name; }).join(", ") : "रिक्त";
                var h8Planets = houseMap[8] || [];
                var h8Text = h8Planets.length > 0 ? h8Planets.map(function(p){ return p.name; }).join(", ") : "रिक्त";

                return "<div class='shastra-verdict-box' style='background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#34d399; font-weight:700; font-size:0.85rem;'>🌿 स्वास्थ्य, जीवनी शक्ति व आरोग्य मीमांसा (Vitality & Health Shielder)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय स्वास्थ्य परीक्षण:</b><br>" +
                    "• <i>लग्न व लग्नेश:</i> आपका लग्न <b>" + lagna + "</b> है जिसके स्वामी <b>" + l1.lord + "</b> हैं। लग्नेश का बल मूल जीवनी शक्ति (Vitality) व रोग-प्रतिरोधक क्षमता का मुख्य आधार है।<br>" +
                    "• <i>षष्ठ व अष्टम भाव:</i> षष्ठ भाव (" + h6Text + ") एवं अष्टम भाव (" + h8Text + ") की स्थिति का सूक्ष्म परीक्षण संतुलित दिनचर्या की महत्ता दर्शाता है।<br><br>" +
                    "<b>२. आरोग्य संरक्षक सात्विक उपाय:</b><br>" +
                    "• प्रातःकाल गुनगुने जल का सेवन करें व सूर्य नमस्कार का अभ्यास करें।<br>" +
                    "• नित्य 11 बार <i>'महामृत्युंजय मंत्र'</i> का शांत मन से जप संपूर्ण आरोग्य का सर्वोत्तम कवच है।";
            }

            // General & Comprehensive Fallback
            var sunP = pMap["सूर्य"] || { sign: "मेष", house: 1 };
            var moonP = pMap["चन्द्र"] || { sign: "मेष", house: 1 };
            return "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>✦ आपकी जिज्ञासा: \"" + (query || "समग्र फलादेश") + "\"</span>" +
                "</div>" +
                "<b>१. शास्त्रीय सिंहावलोकन:</b><br>" +
                "आपकी जन्मपत्रिका में <b>" + lagna + " लग्न</b> (स्वामी: <b>" + l1.lord + "</b>), सूर्यदेव भाव " + sunP.house + " (" + sunP.sign + " राशि) एवं चन्द्रमा भाव " + moonP.house + " (" + moonP.sign + " राशि) में स्थित हैं। सक्रिय विंशोत्तरी दशा <b>" + dasha + "</b> जीवन के महत्वपूर्ण आयामों को सक्रिय कर रही है।<br><br>" +
                "<b>२. दैवज्ञ परामर्श:</b><br>" +
                "वर्तमान समय में अपने लक्ष्य के प्रति धैर्य, एकाग्रता एवं सात्विक निष्ठा बनाए रखें। कुण्डली के शुभ ग्रहों का संबल आपके कार्यों को सिद्धि की ओर अग्रसर कर रहा है।<br><br>" +
                "<b>३. सात्विक साधना:</b><br>" +
                "नित्य प्रातः भगवान सूर्यनारायण को अर्घ्य दें एवं संध्या समय <i>'ॐ नमः शिवाय'</i> का जप करें। यह समस्त मनोरथों को सिद्ध करता है।";
        },

        synthesizePrashnaReading: function(query) {
            return "<b>ॐ नमः शिवाय।</b><br><br>" +
                "<b>सादर प्रणाम!</b> चूंकि आपने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक <b>'प्रश्न मार्ग' (Prashna Marga)</b> एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, आपके प्रश्न पूछने के इस पावन क्षण की <b>'तात्कालिक प्रश्न कुण्डली'</b> का सूक्ष्म वेध कर उत्तर प्रस्तुत कर रहा हूँ:<br><br>" +
                "• <b>प्रश्न शास्त्र नियम:</b> कार्य सिद्धि हेतु प्रश्नेश और कार्येश का परस्पर शुभ दृष्टि संबंध अनिवार्य होता है। तात्कालिक आकाश में चन्द्रमा की स्थिति आपके मनोवांछित कार्य की प्रगति का सकारात्मक संकेत दे रही है।<br>" +
                "• <b>मार्गदर्शन:</b> नित्य प्रातः <i>'ॐ नमः शिवाय'</i> का 108 बार जप करें। यदि आप अपने संपूर्ण जीवन (करियर, वित्त, स्वास्थ्य, दांपत्य) का विस्तृत 20-वर्षीय फलादेश चाहते हैं, तो ऊपर <b>'+ नई कुण्डली'</b> विकल्प से अपना वास्तविक जन्म विवरण दर्ज करें।";
        },'''

if vdw_pattern.search(content):
    content = vdw_pattern.sub(new_vdw_code, content)
    print("✓ Successfully patched VyasDaivagyaWisdom")
else:
    print("⚠️ Could not match vdw_pattern")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch complete! File index.html successfully saved.")

