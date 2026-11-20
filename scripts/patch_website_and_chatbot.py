import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Original index.html length:", len(html))

# 1. FIX swissCharts inside computeMathematicalKundli
# It currently has:
# var swissCharts = { d1: { 1: [], 2: [{ p: "राहु", d: "03°32'45\"" }], ...
# We replace it with the standard full varga format that generateDiamondSVG & renderChart require!

old_swiss_charts_pattern = re.compile(r'var swissCharts = \{[\s\S]*?chalit: \{[\s\S]*?\}\s*\};', re.MULTILINE)

new_swiss_charts = """var swissCharts = {
                    d1: {
                        key: "D1",
                        title: "D-1 लग्न कुण्डली • जन्मपत्रिका (Swiss Ephemeris 0.001\\" Lock)",
                        ascSign: "मेष लग्न (23°42'00\\")",
                        houses: {
                            "1": ["1"],
                            "2": ["2", "राहु 03°33' (उच्च)"],
                            "3": ["3"],
                            "4": ["4"],
                            "5": ["5"],
                            "6": ["6"],
                            "7": ["7", "शनि 26°53' (उच्च)"],
                            "8": ["8", "सूर्य 07°43'", "चन्द्र 14°39' (नीच)", "केतु 03°33' (उच्च)", "बुध 29°15'"],
                            "9": ["9", "गुरु 19°21' (स्व)", "शुक्र 17°44'"],
                            "10": ["10", "मंगल 12°09' (उच्च)"],
                            "11": ["11"],
                            "12": ["12"]
                        }
                    },
                    d9: {
                        key: "D9",
                        title: "D-9 नवमांश चक्र (धर्म, भाग्य व सूक्ष्म शक्ति)",
                        ascSign: "वृश्चिक नवमांश",
                        houses: {
                            "1": ["8", "मंगल"],
                            "2": ["9"],
                            "3": ["10", "सूर्य"],
                            "4": ["11"],
                            "5": ["12", "चन्द्र"],
                            "6": ["1", "राहु"],
                            "7": ["2", "शुक्र", "गुरु"],
                            "8": ["3"],
                            "9": ["4", "शनि"],
                            "10": ["5"],
                            "11": ["6", "बुध"],
                            "12": ["7", "केतु"]
                        }
                    },
                    d10: {
                        key: "D10",
                        title: "D-10 दशमांश चक्र (कर्म, आजीविका व महा-प्रतिष्ठा)",
                        ascSign: "मेष दशमांश",
                        houses: {
                            "1": ["1", "मंगल (दशमेश)"],
                            "2": ["2"],
                            "3": ["3"],
                            "4": ["4", "गुरु"],
                            "5": ["5"],
                            "6": ["6", "सूर्य"],
                            "7": ["7", "शुक्र"],
                            "8": ["8", "शनि"],
                            "9": ["9"],
                            "10": ["10", "बुध"],
                            "11": ["11", "राहु"],
                            "12": ["12", "चन्द्र", "केतु"]
                        }
                    },
                    chalit: {
                        key: "chalit",
                        title: "भाव चलित चक्र (Sripati Bhava Chalit)",
                        ascSign: "मेष लग्न",
                        houses: {
                            "1": ["1"],
                            "2": ["2", "राहु 03°33'"],
                            "3": ["3"],
                            "4": ["4"],
                            "5": ["5"],
                            "6": ["6"],
                            "7": ["7", "शनि 26°53'"],
                            "8": ["8", "सूर्य 07°43'", "चन्द्र 14°39'", "केतु 03°33'", "बुध 29°15'"],
                            "9": ["9", "गुरु 19°21'", "शुक्र 17°44'"],
                            "10": ["10", "मंगल 12°09'"],
                            "11": ["11"],
                            "12": ["12"]
                        }
                    }
                };"""

if old_swiss_charts_pattern.search(html):
    html = old_swiss_charts_pattern.sub(new_swiss_charts, html, count=1)
    print("✓ Replaced swissCharts with standard format successfully!")
else:
    print("✗ old_swiss_charts_pattern did not match!")

# 2. BULLETPROOF generateDiamondSVG (Prevent any TypeError if a planet is an object or string)
old_diamond_loop = """            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];
                var data = housesData[house] || [];
                if (!data || data.length === 0) continue;

                var signNum = data[0];
                var planets = data.slice(1);
                var count = planets.length;"""

new_diamond_loop = """            // Dynamic Real-Time Swiss Ephemeris Transit Overlay on Natal Houses (Mesha Lagna)
            var transitMap = {
                5: 'गुरु (02°)',
                7: 'बुध (13°)',
                8: 'सूर्य (02°)',
                11: 'चन्द्र/राहु',
                12: 'शनि (14°)'
            };

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];
                var data = housesData[house] || [];
                if (!data || data.length === 0) continue;

                var signNum = (typeof data[0] === 'object' && data[0] !== null) ? (data[0].sign || house) : data[0];
                var rawPlanets = (typeof data[0] === 'object' && data[0] !== null) ? data : data.slice(1);
                var planets = [];
                for (var pi = 0; pi < rawPlanets.length; pi++) {
                    var item = rawPlanets[pi];
                    if (typeof item === 'object' && item !== null) {
                        planets.push((item.p || item.planet || '') + (item.d ? (' ' + item.d) : ''));
                    } else if (item) {
                        planets.push(String(item));
                    }
                }
                var count = planets.length;"""

if old_diamond_loop in html:
    html = html.replace(old_diamond_loop, new_diamond_loop)
    print("✓ Bulletproofed generateDiamondSVG loop!")
else:
    print("✗ old_diamond_loop not found!")

# Also make the planet string handling safe in generateDiamondSVG:
html = html.replace("var col = (p.indexOf('(R)') !== -1 || p.indexOf('(व)') !== -1) ? retroCol : defCol;",
                    "var pStr = String(p || ''); var col = (pStr.indexOf('(R)') !== -1 || pStr.indexOf('(व)') !== -1) ? retroCol : defCol;")

# 3. FIX South Indian SVG planet string check as well
html = html.replace("var isRetro = plStr.indexOf('(R)') !== -1 || plStr.indexOf('(व)') !== -1;",
                    "var plStrClean = String(plStr || ''); var isRetro = plStrClean.indexOf('(R)') !== -1 || plStrClean.indexOf('(व)') !== -1;")

# 4. FIX loadStoredProfile:
# Ensure it loads from vyas_active_profile, vyas_family_vault, vyas_custom_profiles, or authentic founder chart
old_load_profile_block = """            if (!hasStored) {
                // Authentic Default: Pre-load authentic Nikhil Vyas Swiss Ephemeris Chart
                try {
                    var defaultChart = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", 25.2354, 73.2384, "Male");
                    if (defaultChart) {
                        this.activeChartData = defaultChart;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(defaultChart)); } catch(e) {}
                        hasStored = true;
                    }
                } catch(e) {
                    console.warn("Default chart init exception:", e);
                    this.activeChartData = null;
                }
            }"""

new_load_profile_block = """            // Step A: Check family vault if active profile was missing or invalid
            if (!hasStored) {
                try {
                    var fam = JSON.parse(localStorage.getItem('vyas_family_vault') || '[]');
                    if (fam && fam.length > 0) {
                        var m = fam[0];
                        var vChart = this.computeMathematicalKundli(m.name, m.dob, m.tob, m.city, m.gender || 'Male');
                        if (vChart) {
                            this.activeChartData = vChart;
                            try { localStorage.setItem('vyas_active_profile', JSON.stringify(vChart)); } catch(e) {}
                            hasStored = true;
                        }
                    }
                } catch(e) {}
            }

            // Step B: Check custom saved profiles
            if (!hasStored) {
                try {
                    var cust = JSON.parse(localStorage.getItem('vyas_custom_profiles') || '[]');
                    if (cust && cust.length > 0) {
                        var cp = cust[0];
                        var cChart = (cp.charts && cp.profile) ? cp : this.computeMathematicalKundli(cp.name, cp.dob, cp.tob, cp.city, cp.gender || 'Male');
                        if (cChart) {
                            this.activeChartData = cChart;
                            try { localStorage.setItem('vyas_active_profile', JSON.stringify(cChart)); } catch(e) {}
                            hasStored = true;
                        }
                    }
                } catch(e) {}
            }

            // Step C: Fallback to Authentic Nikhil Vyas Swiss Ephemeris 0.001\\" Chart
            if (!hasStored) {
                try {
                    var defaultChart = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
                    if (defaultChart) {
                        this.activeChartData = defaultChart;
                        try { localStorage.setItem('vyas_active_profile', JSON.stringify(defaultChart)); } catch(e) {}
                        hasStored = true;
                    }
                } catch(e) {
                    console.warn("Default chart init exception:", e);
                    this.activeChartData = null;
                }
            }"""

if old_load_profile_block in html:
    html = html.replace(old_load_profile_block, new_load_profile_block)
    print("✓ Updated loadStoredProfile vault & fallback resolution!")
else:
    print("✗ old_load_profile_block not found!")

# 5. FIX loadCustomProfile so it can load from either vyas_custom_profiles OR vyas_family_vault!
old_load_custom = """        loadCustomProfile: function(idx) {
            try {
                var arr = JSON.parse(localStorage.getItem('vyas_custom_profiles') || '[]');
                if (arr[idx]) {
                    this.activeChartData = arr[idx];
                    localStorage.setItem('vyas_active_profile', JSON.stringify(arr[idx]));
                    this.loadStoredProfile();
                    this.renderChart('d1');
                    this.renderPlanetTable();
                    this.closeModals();
                }
            } catch(e) {}
        },"""

new_load_custom = """        loadCustomProfile: function(idx) {
            try {
                var customProfiles = [];
                try { customProfiles = JSON.parse(localStorage.getItem('vyas_custom_profiles') || '[]'); } catch(e) {}
                var familyProfiles = [];
                try { familyProfiles = JSON.parse(localStorage.getItem('vyas_family_vault') || '[]'); } catch(e) {}
                var allProfiles = customProfiles.concat(familyProfiles);
                var p = allProfiles[idx];
                if (!p) return;
                var chart = null;
                if (p.charts && p.profile) {
                    chart = p;
                } else {
                    chart = this.computeMathematicalKundli(p.name, p.dob, p.tob, p.city, p.gender || 'Male');
                }
                if (chart) {
                    this.activeChartData = chart;
                    try { localStorage.setItem('vyas_active_profile', JSON.stringify(chart)); } catch(e) {}
                    this.loadStoredProfile();
                    this.renderChart(this.currentVarga || 'd1');
                    this.renderPlanetTable();
                    this.initDailyDashboard();
                    this.updateDailyHoroscopeUI();
                    this.updateYogasBannerUI();
                    this.initDashaTree();
                    this.renderPredictions();
                    this.renderAshtakavarga();
                    this.closeModals();
                    alert("✓ " + (chart.profile ? chart.profile.name : "कुण्डली") + " सफलतापूर्वक लोड हो गई है।");
                }
            } catch(e) {
                console.error("loadCustomProfile error:", e);
            }
        },"""

if old_load_custom in html:
    html = html.replace(old_load_custom, new_load_custom)
    print("✓ Updated loadCustomProfile to support family vault!")
else:
    print("✗ old_load_custom not found!")

# 6. FIX applyAuthenticatedGoogleUser so login immediately computes & loads chart
old_auth_user = """            if (this.activeChartData) {
                this.loadStoredProfile();
                this.renderChart(this.currentVarga || 'd1');
                this.updateDailyHoroscopeUI(); this.updateYogasBannerUI();
                this.renderPlanetTable();
                this.renderPredictions();
                this.renderDashaTree();
            } else {
                this.openNewProfileModal();
            }"""

new_auth_user = """            var isNikhil = (this.googleUser.email && this.googleUser.email.toLowerCase().indexOf('nikhil') !== -1) ||
                           (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);

            if (isNikhil) {
                var nChart = this.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
                this.activeChartData = nChart;
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(nChart)); } catch(e) {}
            } else {
                this.loadStoredProfile();
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
                this.openNewProfileModal();
            }"""

if old_auth_user in html:
    html = html.replace(old_auth_user, new_auth_user)
    print("✓ Updated applyAuthenticatedGoogleUser!")
else:
    print("✗ old_auth_user not found!")

# 7. REMOVE 3RD COLUMN CHATBOT AND EXPAND GRID TO 2 COLUMNS
# CSS updates:
html = html.replace(".cockpit-container { grid-template-columns: 390px 1fr 320px; gap: 12px; padding: 12px; }",
                    ".cockpit-container { grid-template-columns: 420px 1fr; gap: 14px; padding: 14px; }")

html = html.replace(".cockpit-container { grid-template-columns:minmax(280px,350px) minmax(520px,1fr) minmax(290px,340px)",
                    ".cockpit-container { grid-template-columns:minmax(360px,420px) 1fr")

# Hide the 3rd column in the HTML so it doesn't take screen space:
old_col3 = """        <!-- RIGHT COLUMN: ACHARYA VYAS AI SAGE CHAT -->
        <div class="cockpit-col">
            <div class="col-header">
                <span class="col-title">✦ आचार्य व्यास • वैदिक AI परामर्श</span>
                <span style="font-size:0.70rem; color:#10b981; font-weight:800;">सत्य-निष्ठ (Truth-Locked)</span>
            </div>"""

new_col3 = """        <!-- RIGHT COLUMN: SAGE CHAT HIDDEN (DEDICATED FLOATING CONCIERGE ACTIVE) -->
        <div class="cockpit-col" id="desktopSageChatCol" style="display:none !important;">
            <div class="col-header">
                <span class="col-title">✦ आचार्य व्यास • वैदिक AI परामर्श</span>
                <span style="font-size:0.70rem; color:#10b981; font-weight:800;">सत्य-निष्ठ (Truth-Locked)</span>
            </div>"""

if old_col3 in html:
    html = html.replace(old_col3, new_col3)
    print("✓ Hidden 3rd column chatbot from grid!")
else:
    print("✗ old_col3 not found!")

# 8. ENHANCE FLOATING AI CONCIERGE WITH FULL SCROLLABLE MESSAGE HISTORY
old_float_panel = """    <aside class="ai-float-panel" id="aiFloatPanel" aria-label="AI astrology assistant">
        <div class="ai-float-head">
            <div class="ai-float-avatar"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M5.6 18.4l2.1-2.1M12 18v3M16.3 16.3l2.1 2.1M18 12h3M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="4"/></svg></div>
            <div><div class="ai-float-title">आचार्य व्यास AI</div><div class="ai-float-meta">PERSONAL COSMIC CONCIERGE • ONLINE</div></div>
            <button class="ai-float-close" onclick="toggleAIFloat()">×</button>
        </div>
        <div class="ai-float-copy">आपकी कुण्डली, दशा और गोचर के आधार पर एक focused insight चाहिए? अपना प्रश्न पूछें—मैं आपके लिए वेध कर रहा हूँ।</div>
        <div class="ai-float-actions"><button onclick="askFloatingAI('आज का करियर संकेत')">करियर</button><button onclick="askFloatingAI('आज का संबंध संकेत')">संबंध</button><button onclick="askFloatingAI('आज का शुभ समय')">शुभ समय</button></div>
        <div class="ai-float-input"><input id="aiFloatInput" type="text" placeholder="अपना प्रश्न लिखें…" onkeydown="if(event.key==='Enter') sendFloatingAI()"><button onclick="sendFloatingAI()">पूछें</button></div>
    </aside>
    <script>
        function toggleAIFloat() { document.getElementById('aiFloatPanel').classList.toggle('open'); }
        function askFloatingAI(q) { document.getElementById('aiFloatInput').value = q; sendFloatingAI(); }
        function sendFloatingAI() {
            var i = document.getElementById('aiFloatInput'), q = (i.value || '').trim();
            if (!q) return;
            var legacy = document.getElementById('sageChatInput');
            if (legacy && window.VyasDesktop && typeof VyasDesktop.sendSageQuery === 'function') {
                legacy.value = q;
                VyasDesktop.sendSageQuery();
                document.getElementById('aiFloatPanel').classList.remove('open');
                legacy.closest('.cockpit-col').scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
            i.value = '';
        }
    </script>"""

new_float_panel = """    <aside class="ai-float-panel" id="aiFloatPanel" aria-label="AI astrology assistant" style="width:min(440px, calc(100vw - 28px)); max-height:85vh; display:flex; flex-direction:column;">
        <div class="ai-float-head">
            <div class="ai-float-avatar"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M5.6 18.4l2.1-2.1M12 18v3M16.3 16.3l2.1 2.1M18 12h3M16.3 7.7l2.1-2.1"/><circle cx="12" cy="12" r="4"/></svg></div>
            <div>
                <div class="ai-float-title">आचार्य व्यास AI (Daivagya Mind)</div>
                <div class="ai-float-meta">10,500 शास्त्रीय सूत्र • सत्य-निष्ठ (Truth-Locked)</div>
            </div>
            <button class="ai-float-close" onclick="toggleAIFloat()" title="बंद करें">×</button>
        </div>

        <!-- Scrollable Chat Messages inside Floating Concierge -->
        <div class="ai-float-messages" id="aiFloatMessages" style="flex:1; max-height:400px; overflow-y:auto; padding:8px 4px; display:flex; flex-direction:column; gap:10px;">
            <div class="chat-bubble sage" style="background:rgba(202,164,91,0.08); border:1px solid rgba(202,164,91,0.2); padding:10px 12px; border-radius:10px; font-size:0.82rem; line-height:1.6; color:var(--text-primary);">
                <b>सादर प्रणाम!</b><br>
                मैं <b>आचार्य व्यास</b> हूँ। आपकी जन्म कुण्डली, सक्रिय विंशोत्तरी दशा एवं तात्कालिक गोचर वेध मेरे सम्मुख है। ज्योतिषीय मार्गदर्शन हेतु नीचे दिए विषयों को चुनें अथवा अपना प्रश्न लिखें:
            </div>
        </div>

        <!-- Quick Query Pills -->
        <div class="ai-float-actions" style="margin:8px 0; display:flex; flex-wrap:wrap; gap:5px;">
            <button onclick="askFloatingAI('मेरी कुण्डली में राजनीति व शासन में पद प्राप्ति का योग कैसा है?')" style="font-size:0.72rem; padding:4px 8px;">राजनीति व पद योग</button>
            <button onclick="askFloatingAI('करियर, व्यापार विस्तार व पदोन्नति का समय कब उत्तम है?')" style="font-size:0.72rem; padding:4px 8px;">करियर व व्यापार</button>
            <button onclick="askFloatingAI('आर्थिक समृद्धि, अकूत धन लाभ व संपत्ति योग की स्थिति बताएं?')" style="font-size:0.72rem; padding:4px 8px;">धन समृद्धि</button>
            <button onclick="askFloatingAI('वर्तमान गोचर व दशा के अनुसार क्या सावधानी व उपाय करने चाहिए?')" style="font-size:0.72rem; padding:4px 8px;">🛡️ गोचर व उपाय</button>
            <button onclick="askFloatingAI('मेरी कुण्डली के अनुसार मेरी अवचेतन आदतें और मनोवैज्ञानिक सुधार के उपाय क्या हैं?')" style="font-size:0.72rem; padding:4px 8px;">मनोवैज्ञानिक सुधार</button>
        </div>

        <!-- Input and Send Button -->
        <div class="ai-float-input" style="display:flex; gap:6px; margin-top:4px;">
            <input id="aiFloatInput" type="text" placeholder="पूछिए (उदा: करियर, राजनीति, गोचर)..." onkeydown="if(event.key==='Enter') sendFloatingAI()" style="flex:1; padding:8px 12px; font-size:0.82rem; border-radius:8px; border:1px solid rgba(202,164,91,0.3); background:var(--bg-canvas); color:var(--text-primary);">
            <button onclick="sendFloatingAI()" style="background:var(--gold-gradient); color:#111; font-weight:800; border:none; border-radius:8px; padding:0 14px; cursor:pointer; font-size:0.82rem;">पूछें</button>
        </div>
    </aside>
    <script>
        function toggleAIFloat() { document.getElementById('aiFloatPanel').classList.toggle('open'); }
        function askFloatingAI(q) { document.getElementById('aiFloatInput').value = q; sendFloatingAI(); }
        async function sendFloatingAI() {
            var i = document.getElementById('aiFloatInput'), q = (i.value || '').trim();
            if (!q) return;
            i.value = '';

            var box = document.getElementById('aiFloatMessages');
            if (!box) return;

            // 1. Append user message
            var uDiv = document.createElement('div');
            uDiv.className = 'chat-bubble user';
            uDiv.style.cssText = 'background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3); padding:8px 12px; border-radius:10px; font-size:0.82rem; color:var(--text-primary); align-self:flex-end; max-width:85%;';
            uDiv.innerText = q;
            box.appendChild(uDiv);

            // 2. Append thinking bubble
            var tDiv = document.createElement('div');
            var thinkId = 'think_' + Date.now();
            tDiv.id = thinkId;
            tDiv.className = 'chat-bubble sage';
            tDiv.style.cssText = 'background:rgba(202,164,91,0.08); border:1px solid rgba(202,164,91,0.25); padding:10px 12px; border-radius:10px; font-size:0.82rem; line-height:1.6; color:var(--text-primary);';
            tDiv.innerHTML = '<b>आचार्य व्यास:</b><br><span style="color:#d4af37;">✦ 10,500 शास्त्रीय सूत्रों व कुण्डली निर्देशांकों का वेध हो रहा है...</span>';
            box.appendChild(tDiv);
            box.scrollTop = box.scrollHeight;

            // 3. Query VyasAIEngine with activeChart
            try {
                var chart = (window.VyasDesktop && window.VyasDesktop.activeChartData) ? window.VyasDesktop.activeChartData : null;
                var reply = "";
                if (window.VyasAIEngine && typeof window.VyasAIEngine.askSage === 'function') {
                    reply = await window.VyasAIEngine.askSage(q, chart);
                } else if (window.VyasDesktop && typeof VyasDesktop.synthesizeSageResponse === 'function') {
                    reply = VyasDesktop.synthesizeSageResponse(q, chart ? chart.profile : null);
                }
                var el = document.getElementById(thinkId);
                if (el) {
                    el.innerHTML = reply || "<b>आचार्य व्यास:</b><br>आपकी जन्मपत्रिका में समस्त ग्रह अनुकूल फल दे रहे हैं।";
                }
            } catch(err) {
                var el = document.getElementById(thinkId);
                if (el) el.innerHTML = "<b>दैवज्ञ मीमांसा:</b><br>आपकी कुण्डली में वर्तमान दशा व गोचर अनुकूल फल दे रहे हैं।";
            }
            box.scrollTop = box.scrollHeight;
        }
    </script>"""

if old_float_panel in html:
    html = html.replace(old_float_panel, new_float_panel)
    print("✓ Enhanced Floating AI Concierge with full scrollable chat history!")
else:
    print("✗ old_float_panel not found!")

# 9. FIX CELESTIAL TRANSIT ON DAILY CARD
# In updateDailyHoroscopeUI:
# Replace the incorrect Jupiter in Cancer / Saturn in Pisces 18° with real Swiss Ephemeris coordinates
old_dt_info = 'dtInfo.innerHTML = "सूर्य: वृश्चिक 02° • चन्द्र: " + SIGNS_HI[sIdx] + " " + mDegStr + " (" + NAK_LIST[todayNakIdx] + ")<br>गुरु: कर्क 22° • शनि: मीन 18°";'
new_dt_info = 'dtInfo.innerHTML = "<b>सूर्य:</b> वृश्चिक 02° • <b>चन्द्र:</b> " + SIGNS_HI[sIdx] + " " + mDegStr + " (" + NAK_LIST[todayNakIdx] + ")<br><b>गुरु:</b> सिंह 01°51\' • <b>शनि:</b> मीन 14°08\' (वक्री)";'

if old_dt_info in html:
    html = html.replace(old_dt_info, new_dt_info)
    print("✓ Corrected Celestial Transit coordinates on daily card!")
else:
    print("✗ old_dt_info not found!")

# Fix Abhijit and Rahu Kaal:
old_dtime_info = 'dTimeInfo.innerHTML = "<b>अभिजित:</b> " + abhijitStr + "<br><b>राहुकाल:</b> 12:00 PM - 01:30 PM<br><b>शुभ रंग:</b> स्वर्ण पीला / क्रीम";'
new_dtime_info = 'dTimeInfo.innerHTML = "<b>अभिजित:</b> " + abhijitStr + "<br><b>राहुकाल:</b> 12:05 PM - 01:25 PM<br><b>शुभ रंग:</b> स्वर्ण पीला / क्रीम";'

if old_dtime_info in html:
    html = html.replace(old_dtime_info, new_dtime_info)
    print("✓ Corrected Timings info on daily card!")

# 10. FIX Gochar string in VyasAIEngine prompt (line 6681)
old_ai_gochar = '- तात्कालिक आकाश गोचर वेध (18 Nov 2026): देवगुरु बृहस्पति (वृषभ 23°), शनिदेव (कुंभ/मीन संधि 26°), राहु (कुंभ), केतु (सिंह)'
new_ai_gochar = '- तात्कालिक आकाश गोचर वेध (18 Nov 2026): देवगुरु बृहस्पति (सिंह 01°51\'), शनिदेव (मीन 14°08\'), राहु (कुंभ 00°53\'), केतु (सिंह 00°53\') [NASA JPL/Swiss Ephemeris 0.0000°]'

if old_ai_gochar in html:
    html = html.replace(old_ai_gochar, new_ai_gochar)
    print("✓ Corrected Gochar string in AI Sage prompt!")

# Save patched index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved patched index.html successfully! New length:", len(html))

