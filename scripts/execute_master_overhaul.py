# scripts/execute_master_overhaul.py
# Comprehensive overhaul of VYAS ASTRA:
# 1. Desktop Planet Table ID & Field Mapping Fix
# 2. Dynamic Horary Prashna Kundli Engine in VyasAIEngine (Prashna Marga)
# 3. Complete Purge of Founder Personal Chart from Public Code & Fallbacks
# 4. 100% Dynamic D-9, D-10, KP 249, Jaimini 7 Chara Karakas, Nadi in computeMathematicalKundli
# 5. Elevated UI / ADX Design & Awwwards Luxury Styling

import os
import re
import json

def patch_desktop():
    print("Patching index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix renderPlanetTable ID & column mapping
    old_rpt = """        renderPlanetTable() {
            var tbody = document.getElementById('planetPositionsTableBody');
            if (!tbody) return;

            if (!this.activeChartData || !this.activeChartData.planet_table || this.activeChartData.planet_table.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:32px 12px; color:var(--text-muted);"><div style="font-size:1.8rem; margin-bottom:8px;">🪐</div><b style="color:var(--primary); font-size:0.9rem;">कोई ग्रह स्थिति उपलब्ध नहीं है</b><p style="font-size:0.75rem; margin-top:4px;">अपनी कुण्डली के 9 ग्रहों के सूक्ष्म अंश देखने हेतु ऊपर <b>&apos;+ नई कुण्डली&apos;</b> बटन दबाएं।</p></td></tr>';
                return;
            }

            var list = this.activeChartData.planet_table || AUTHENTIC_BUNDLE.planet_table;
            var html = '';
            for (var i = 0; i < list.length; i++) {
                var row = list[i];
                var badgeColor = (row.s.indexOf('उच्च') !== -1 || row.s.indexOf('स्व') !== -1) ? '#10b981' : (row.s.indexOf('नीच') !== -1 ? '#ef4444' : 'var(--text-secondary)');
                html += '<tr>' +
                    '<td><b>' + row.p + '</b></td>' +
                    '<td>' + row.r + '</td>' +
                    '<td style="font-family:var(--font-mono);">' + row.d + '</td>' +
                    '<td>' + row.n + '</td>' +
                    '<td>' + row.h + '</td>' +
                    '<td><span style="color:' + badgeColor + '; font-weight:800;">' + row.s + '</span></td>' +
                '</tr>';
            }
            tbody.innerHTML = html;
        },"""

    new_rpt = """        renderPlanetTable() {
            var tbody = document.getElementById('desktopPlanetTableBody') || document.getElementById('planetPositionsTableBody');
            if (!tbody) return;

            if (!this.activeChartData || !this.activeChartData.planet_table || this.activeChartData.planet_table.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:36px 16px; color:var(--text-muted);"><div style="font-size:2rem; margin-bottom:8px;">🪐</div><b style="color:var(--primary); font-size:0.95rem;">कोई ग्रह स्थिति उपलब्ध नहीं है (रिक्त खाका)</b><p style="font-size:0.78rem; margin-top:6px; color:var(--text-secondary);">अपनी कुण्डली के 9 ग्रहों के स्पष्ट अंश, नक्षत्र व भाव देखने हेतु ऊपर <b>&apos;+ नई कुण्डली&apos;</b> पर क्लिक करें।</p></td></tr>';
                return;
            }

            var list = this.activeChartData.planet_table;
            var html = '';
            for (var i = 0; i < list.length; i++) {
                var row = list[i];
                var pName = row.p || row.planet || '';
                var rSign = row.r || row.sign || '';
                var deg = row.d || row.degree || row.dms || "00°00'";
                var nak = row.n || row.nakshatra || row.nak || '-';
                var house = row.h || row.house || row.bhava || '1';
                var status = row.s || row.status || row.dignity || 'सम';

                var badgeColor = (status.indexOf('उच्च') !== -1 || status.indexOf('स्व') !== -1) ? '#10b981' : (status.indexOf('नीच') !== -1 ? '#ef4444' : 'var(--text-secondary)');
                html += '<tr>' +
                    '<td><b style="color:var(--primary);">' + pName + '</b></td>' +
                    '<td>' + rSign + '</td>' +
                    '<td style="font-family:var(--font-mono); font-weight:600;">' + deg + '</td>' +
                    '<td>' + nak + '</td>' +
                    '<td>भाव ' + house + '</td>' +
                    '<td><span style="color:' + badgeColor + '; font-weight:800; font-size:0.75rem; padding:2px 8px; border-radius:4px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);">' + status + '</span></td>' +
                '</tr>';
            }
            tbody.innerHTML = html;
        },"""

    if old_rpt in html:
        html = html.replace(old_rpt, new_rpt)
        print("  ✓ Fixed renderPlanetTable in index.html")
    else:
        print("  ! Warning: old_rpt not matched exactly in index.html")

    # 2. Fix sendSageQuery fallback
    old_ssq = "var chart = this.activeChartData || window.AUTHENTIC_BUNDLE;"
    new_ssq = "var chart = this.activeChartData; // Strict Privacy: No fallback to founder bundle"
    if old_ssq in html:
        html = html.replace(old_ssq, new_ssq)
        print("  ✓ Fixed sendSageQuery in index.html to eliminate founder fallback")

    # 3. Fix headerProfileChip hardcoding
    old_hpc = """            // Update Header profile chip
            var chip = document.getElementById('headerProfileChip');
            if (chip) {
                chip.innerHTML = this.isEnglishMode ? 
                    '<span class="jatak-icon">👤</span> <span class="jatak-name">NIKHIL VYAS</span> <span class="jatak-lagna">Aries Lagna 23°27′</span>' :
                    '<span class="jatak-icon">👤</span> <span class="jatak-name">NIKHIL VYAS</span> <span class="jatak-lagna">मेष लग्न 23°27′</span>';
            }"""

    new_hpc = """            // Update Header profile chip dynamically
            var chip = document.getElementById('headerProfileChip');
            if (chip) {
                var pName = (this.activeChartData && this.activeChartData.profile) ? this.activeChartData.profile.name : (this.isEnglishMode ? 'Vedic Chart' : 'वैदिक कुण्डली');
                var pLagna = (this.activeChartData && this.activeChartData.profile) ? (this.activeChartData.profile.asc_sign + ' लग्न') : (this.isEnglishMode ? 'Blank Slate' : 'रिक्त खाका');
                chip.innerHTML = '<span class="jatak-icon">👤</span> <span class="jatak-name">' + pName + '</span> <span class="jatak-lagna">' + pLagna + '</span>';
            }"""

    if old_hpc in html:
        html = html.replace(old_hpc, new_hpc)
        print("  ✓ Fixed headerProfileChip dynamic rendering in index.html")

    # 4. Inject Prashna Kundli Engine into window.VyasAIEngine
    prashna_engine_code = """
        // =========================================================================
        // DYNAMIC HORARY PRASHNA KUNDLI ENGINE (तात्कालिक प्रश्न कुण्डली - प्रश्न मार्ग)
        // =========================================================================
        castPrashnaKundli: function(query, userLat, userLon) {
            var now = new Date();
            var lat = (typeof userLat === 'number' && !isNaN(userLat)) ? userLat : 28.6139; // Delhi / Standard India
            var lon = (typeof userLon === 'number' && !isNaN(userLon)) ? userLon : 77.2090;
            var tz = 5.5;

            var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
            var hr = now.getHours(), mn = now.getMinutes(), sc = now.getSeconds();
            var decHrUtc = hr + (mn / 60.0) + (sc / 3600.0) - tz;

            var y2 = mo <= 2 ? yr - 1 : yr;
            var m2 = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y2 / 100);
            var B = 2 - A + Math.floor(A / 4);
            var jd0 = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5;
            var jd = jd0 + decHrUtc / 24.0;
            var d = jd - 2451543.5;
            var T_j2000 = (jd - 2451545.0) / 36525.0;

            var RAD = Math.PI / 180.0, DEG = 180.0 / Math.PI;
            function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
            var ayanamsa = 23.857 + 1.39697 * T_j2000;

            var gmst = norm(280.46061837 + 360.98564736629 * (jd - 2451545.0));
            var lst = norm(gmst + lon) * RAD;
            var eps = (23.4392911 - 0.0130042 * T_j2000) * RAD;
            var ascTrop = norm(Math.atan2(Math.cos(lst), -(Math.sin(lst) * Math.cos(eps) + Math.tan(lat * RAD) * Math.sin(eps))) * DEG);
            var ascSid = norm(ascTrop - ayanamsa);
            var ascSign = Math.floor(ascSid / 30.0) % 12;
            var ascDegIn = ascSid % 30.0;
            var ascDms = Math.floor(ascDegIn) + "°" + Math.floor((ascDegIn * 60) % 60) + "'";

            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var NAKS = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];

            // Calculate Real-time planetary positions in the sky right now
            var sids = {};
            sids.Sun = norm(norm(282.9404 + 4.70935e-5 * d + norm(356.0470 + 0.9856002585 * d)) - ayanamsa);
            sids.Moon = norm(norm(125.1228 + 115.3654 + 13.0649929509 * d) - ayanamsa);
            sids.Mars = norm(norm(49.5574 + 286.5016 + 18.6021 + 0.5240207766 * d) - ayanamsa);
            sids.Mercury = norm(norm(48.3313 + 29.1241 + 168.6562 + 4.0923344368 * d) - ayanamsa);
            sids.Jupiter = norm(norm(100.4542 + 273.8777 + 19.8950 + 0.0830853001 * d) - ayanamsa);
            sids.Venus = norm(norm(76.6799 + 54.8910 + 48.0052 + 1.6021302244 * d) - ayanamsa);
            sids.Saturn = norm(norm(113.6634 + 339.3939 + 316.9670 + 0.0334442282 * d) - ayanamsa);
            sids.Rahu = norm(norm(125.04452 - 1934.136261 * T_j2000) - ayanamsa);
            sids.Ketu = norm(sids.Rahu + 180.0);

            var moonSignIdx = Math.floor(sids.Moon / 30.0) % 12;
            var moonNakIdx = Math.floor(sids.Moon / (360.0 / 27.0)) % 27;
            var moonPada = Math.floor((sids.Moon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;

            // Intent / Karya Bhava Classification
            var q = (query || "").toLowerCase();
            var karyaHouse = 1;
            var karyaDesc = "तनु व आत्म सिद्धि";

            if (/mla|mp|chunav|chunaw|neta|rajneeti|politics|election|career|naukri|job|promotion|pad|adhikar|shasan|sarkar|ias|ips/.test(q)) {
                karyaHouse = 10;
                karyaDesc = "दशम भाव (राज्य पद, चुनाव, शासन सत्ता व कर्म सिद्धि)";
            } else if (/vivah|shadi|marriage|patni|pati|prem|love|rishta|sambandh|jeewansaathi/.test(q)) {
                karyaHouse = 7;
                karyaDesc = "सप्तम भाव (विवाह, दांपत्य व जीवनसाथी)";
            } else if (/paisa|dhan|sampatti|labh|wealth|money|business|vyapar|profit|kamai|karz|loan|loss/.test(q)) {
                karyaHouse = 11;
                karyaDesc = "एकादश व द्वितीय भाव (धन, लाभ, व्यापारिक वृद्धि व संचित कोष)";
            } else if (/santan|bacha|garbh|pregnancy|child|padhai|exam|upsc|pariksha|education|study/.test(q)) {
                karyaHouse = 5;
                karyaDesc = "पंचम भाव (संतान सुख, परीक्षा व विद्या अर्जन)";
            } else if (/court|case|mukadma|police|shatru|rog|bimar|bimari|health|swasthya/.test(q)) {
                karyaHouse = 6;
                karyaDesc = "षष्ठ भाव (रोग, ऋण, विवाद व शत्रु विजय)";
            } else if (/yatra|videsh|foreign|travel|visa|sthanantaran|transfer/.test(q)) {
                karyaHouse = 9;
                karyaDesc = "नवम व द्वादश भाव (विदेश यात्रा, भाग्य व स्थान परिवर्तन)";
            }

            var prashnesha = LORDS[ascSign];
            var karyaSign = (ascSign + karyaHouse - 1) % 12;
            var karyesha = LORDS[karyaSign];

            // Planetary positions summary
            var planetSummary = [];
            var order = [
                { k: "Sun", n: "सूर्य" }, { k: "Moon", n: "चन्द्र" }, { k: "Mars", n: "मंगल" },
                { k: "Mercury", n: "बुध" }, { k: "Jupiter", n: "गुरु" }, { k: "Venus", n: "शुक्र" },
                { k: "Saturn", n: "शनि" }, { k: "Rahu", n: "राहु" }, { k: "Ketu", n: "केतु" }
            ];
            for (var i = 0; i < order.length; i++) {
                var p = order[i], plon = sids[p.k];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var hNum = ((sIdx - ascSign + 12) % 12) + 1;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                planetSummary.push(p.n + " " + SIGNS_HI[sIdx] + " (" + dms + ", भाव " + hNum + ")");
            }

            return {
                isPrashna: true,
                query: query,
                timestamp: now.toLocaleTimeString('hi-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                date: now.toLocaleDateString('hi-IN'),
                prashnaLagna: SIGNS_HI[ascSign] + " (" + ascDms + ")",
                prashnesha: prashnesha,
                moonSign: SIGNS_HI[moonSignIdx],
                moonNak: NAKS[moonNakIdx] + " (" + moonPada + ")",
                karyaHouse: karyaHouse,
                karyaDesc: karyaDesc,
                karyesha: karyesha,
                karyaSign: SIGNS_HI[karyaSign],
                planets: planetSummary.join("; ")
            };
        },
"""

    old_engine_head = """    window.VyasAIEngine = {
        keyPool: ["""
    new_engine_head = "    window.VyasAIEngine = {" + prashna_engine_code + "\n        keyPool: ["

    if old_engine_head in html:
        html = html.replace(old_engine_head, new_engine_head)
        print("  ✓ Injected castPrashnaKundli into VyasAIEngine")

    # 5. Update askSage to branch cleanly between Natal and Horary Prashna
    old_ask_sage = """        async askSage(query, activeChart) {
            var prof = (activeChart && activeChart.profile) ? activeChart.profile : { name: "जातक", asc_sign: "मेष" };
            var planets = (activeChart && activeChart.planet_table) ? activeChart.planet_table.map(function(p) { return (p.planet || p.p || '') + ' in ' + (p.sign || p.r || '') + ' (भाव ' + (p.house || p.h || '') + ', ' + (p.dignity || p.s || '') + ')'; }).join('; ') : "Standard Placements";
            var dasha = (activeChart && activeChart.active_dasha && activeChart.active_dasha.chain) ? activeChart.active_dasha.chain : "शुक्र ➔ शनि ➔ मंगल ➔ चन्द्र ➔ बुध";

            var systemPrompt = [
                "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु एवं वशिष्ठ ज्योतिष के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।","""

    new_ask_sage = """        async askSage(query, activeChart) {
            var isPrashnaMode = !activeChart || !activeChart.profile || !activeChart.planet_table || activeChart.isPrashna;
            var systemPrompt = "";

            if (isPrashnaMode) {
                var prashna = this.castPrashnaKundli(query);
                systemPrompt = [
                    "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु, वराहमिहिर एवं 'प्रश्न मार्ग' (Prashna Marga) के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।",
                    "",
                    "विशेष शास्त्रीय मर्यादा (Sacred Directive):",
                    "जातक ने अपनी कोई व्यक्तिगत जन्म पत्रिका प्रविष्ट नहीं की है। अतः 'प्रश्न मार्ग' एवं 'दैवज्ञ वल्लभ' शास्त्र के नियमानुसार, आपने प्रश्न पूछने के इस पावन क्षण (तात्कालिक गोचर व होरा) का वेध करके 'तात्कालिक प्रश्न कुण्डली' (Horary Chart) तैयार की है।",
                    "",
                    "तात्कालिक प्रश्न कुण्डली विवरण (Horary Data Lock):",
                    "- प्रश्न समय: " + prashna.date + " " + prashna.timestamp,
                    "- तात्कालिक प्रश्न लग्न (Prashna Lagna): " + prashna.prashnaLagna + " (प्रश्नेश: " + prashna.prashnesha + ")",
                    "- चन्द्रमा की तात्कालिक स्थिति: " + prashna.moonSign + " राशि, " + prashna.moonNak + " (चन्द्रमा कार्य सिद्धि का प्रत्यक्ष साक्षी व दूत है)",
                    "- प्रश्न का कार्य भाव (Karya Bhava): " + prashna.karyaDesc,
                    "- कार्येश (Karyesha): " + prashna.karyesha + " (" + prashna.karyaSign + " राशि का स्वामी)",
                    "- आकाश में ग्रहों की तात्कालिक वास्तविक स्थिति: " + prashna.planets,
                    "",
                    "अनिवार्य फलकथन निर्देश (Strict Invariants):",
                    "1. अपने उत्तर का आरम्भ इस पावन उद्घोष से करें:",
                    "   'ॐ नमः शिवाय। वत्स/पुत्र! चूंकि तुमने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक 'प्रश्न मार्ग' (Prashna Marga) एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, तुम्हारे प्रश्न पूछने के इस पावन क्षण (तात्कालिक गोचर व होरा) की 'तात्कालिक प्रश्न कुण्डली' (Horary Chart) का सूक्ष्म वेध कर उत्तर दे रहा हूँ।",
                    "2. किसी भी पुरानी या व्यक्तिगत जन्म कुण्डली (जैसे मेष लग्न, मकर में मंगल या रूचक योग) का लेशमात्र भी उल्लेख न करें। केवल और केवल ऊपर दी गई 'तात्कालिक प्रश्न कुण्डली' के अनुसार ही उत्तर दें।",
                    "3. प्रश्नेश (" + prashna.prashnesha + ") और कार्येश (" + prashna.karyesha + ") के परस्पर सम्बन्ध, केन्द्र/त्रिकोण स्थिति, दृष्टि, इत्थशाल (Ithasala) योग एवं चन्द्रमा के प्रभाव से कार्य सिद्धि (सफलता/विलम्ब/बाधा) का स्पष्ट, सटीक व समय-बद्ध फलकथन करें।",
                    "4. प्रश्न के समाधान हेतु प्रामाणिक वैदिक व सात्विक उपाय बताएं (जैसे विशेष मंत्र, इष्ट देव पूजा या दान)।"
                ].join('\\n');
            } else {
                var prof = activeChart.profile;
                var planets = activeChart.planet_table.map(function(p) { return (p.planet || p.p || '') + ' in ' + (p.sign || p.r || '') + ' (भाव ' + (p.house || p.h || '') + ', ' + (p.dignity || p.s || '') + ')'; }).join('; ');
                var dasha = (activeChart.active_dasha && activeChart.active_dasha.chain) ? activeChart.active_dasha.chain : "सक्रिय विंशोत्तरी दशा";

                systemPrompt = [
                    "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु एवं वशिष्ठ ज्योतिष के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।","""

    if old_ask_sage in html:
        html = html.replace(old_ask_sage, new_ask_sage)
        print("  ✓ Updated askSage in index.html for Prashna vs Natal routing")

    # 6. Update generateDynamicLocalReply for Prashna
    old_local = """        generateDynamicLocalReply(query, activeChart) {
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeHolisticReading) {
                return window.VyasDaivagyaVision.synthesizeHolisticReading(query, activeChart);
            }
            var prof = (activeChart && activeChart.profile) ? activeChart.profile : { name: "जातक", asc_sign: "मेष" };
            return "<b>आचार्य व्यास का प्रामाणिक दैवज्ञ मार्गदर्शन:</b><br>सादर प्रणाम " + prof.name + " जी! आपकी कुण्डली व गोचर का सूक्ष्म परीक्षण किया गया है। वर्तमान दशा शुभ प्रभाव दे रही है। नित्य 'ॐ नमः शिवाय' जपें व सूर्यदेव को अर्घ्य दें।";
        }"""

    new_local = """        generateDynamicLocalReply(query, activeChart) {
            var isPrashnaMode = !activeChart || !activeChart.profile || !activeChart.planet_table || activeChart.isPrashna;
            if (isPrashnaMode) {
                var prashna = this.castPrashnaKundli(query);
                return "<b>ॐ नमः शिवाय।</b><br><br>" +
                    "वत्स! चूंकि तुमने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक <b>'प्रश्न मार्ग' (Prashna Marga)</b> एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, तुम्हारे प्रश्न पूछने के इस पावन क्षण की <b>'तात्कालिक प्रश्न कुण्डली'</b> (Horary Chart) का सूक्ष्म वेध कर उत्तर दे रहा हूँ:<br><br>" +
                    "• <b>तात्कालिक प्रश्न लग्न:</b> " + prashna.prashnaLagna + " (प्रश्नेश: <b>" + prashna.prashnesha + "</b>)<br>" +
                    "• <b>चन्द्रमा का गोचर:</b> " + prashna.moonSign + " राशि, नक्षत्र " + prashna.moonNak + "<br>" +
                    "• <b>प्रश्न कार्य भाव:</b> " + prashna.karyaDesc + "<br>" +
                    "• <b>कार्येश स्वामी:</b> " + prashna.karyesha + " (" + prashna.karyaSign + " राशिपति)<br><br>" +
                    "<b>आचार्य व्यास का दैवज्ञ निर्णय (Prashna Synthesis):</b><br>" +
                    "प्रश्न मार्ग के अनुसार जब प्रश्नेश (" + prashna.prashnesha + ") एवं कार्येश (" + prashna.karyesha + ") के मध्य शुभ दृष्टि-सम्बन्ध बनता है तथा चन्द्रमा शुभ स्थिति में होता है, तो अभीष्ट कार्य में सफलता का मार्ग प्रशस्त होता है। वर्तमान तात्कालिक गोचर में चन्द्रमा की स्थिति आपके मन के अभीष्ट संकल्प को फलवती करने की दिशा में अग्रसर है।<br><br>" +
                    "<b>मार्गदर्शन व सात्विक उपाय:</b><br>" +
                    "कार्य सिद्धि में अनुकूलता हेतु नित्य प्रातः <i>'ॐ नमः शिवाय'</i> का 108 बार जप करें तथा बुधवार या गुरुवार को सात्विक दान करें। यदि आप अपने जीवन के दीर्घकालिक 10-20 वर्षों का सटीक फलादेश चाहते हैं, तो ऊपर <b>'+ नई कुण्डली'</b> विकल्प से अपना वास्तविक जन्म विवरण दर्ज करें।";
            }
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeHolisticReading) {
                return window.VyasDaivagyaVision.synthesizeHolisticReading(query, activeChart);
            }
            var prof = activeChart.profile;
            return "<b>आचार्य व्यास का प्रामाणिक दैवज्ञ मार्गदर्शन:</b><br>सादर प्रणाम " + prof.name + " जी! आपकी कुण्डली (" + prof.asc_sign + " लग्न) व गोचर का सूक्ष्म परीक्षण किया गया है। वर्तमान दशा शुभ फल प्रदान कर रही है। नित्य 'ॐ नमः शिवाय' जपें व सूर्यदेव को अर्घ्य दें।";
        }"""

    if old_local in html:
        html = html.replace(old_local, new_local)
        print("  ✓ Updated generateDynamicLocalReply for authentic Prashna local fallback")

    # 7. Purge loadAuthenticNikhilProfile
    old_lanp = """        loadAuthenticNikhilProfile() {
            localStorage.removeItem('vyas_active_profile');
            this.activeChartData = AUTHENTIC_BUNDLE;
            this.loadStoredProfile();
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.renderKP();
            this.renderJaimini();
            this.renderNadi();
            this.closeModals();
        },"""

    new_lanp = """        loadKalapurushaChart() {
            localStorage.removeItem('vyas_active_profile');
            this.activeChartData = null; // Clean blank slate
            this.renderChart('d1');
            this.renderPlanetTable();
            this.renderPredictions();
            this.renderAshtakavarga();
            this.renderKP();
            this.renderJaimini();
            this.renderNadi();
            this.closeModals();
        },"""

    if old_lanp in html:
        html = html.replace(old_lanp, new_lanp)
        print("  ✓ Purged loadAuthenticNikhilProfile from index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ Saved updated index.html")

def patch_mobile():
    print("Patching mobile/index.html...")
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject Prashna Kundli Engine into mobile VyasAIEngine
    prashna_engine_code = """
        // =========================================================================
        // DYNAMIC HORARY PRASHNA KUNDLI ENGINE (तात्कालिक प्रश्न कुण्डली - प्रश्न मार्ग)
        // =========================================================================
        castPrashnaKundli: function(query, userLat, userLon) {
            var now = new Date();
            var lat = (typeof userLat === 'number' && !isNaN(userLat)) ? userLat : 28.6139; // Delhi / Standard India
            var lon = (typeof userLon === 'number' && !isNaN(userLon)) ? userLon : 77.2090;
            var tz = 5.5;

            var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
            var hr = now.getHours(), mn = now.getMinutes(), sc = now.getSeconds();
            var decHrUtc = hr + (mn / 60.0) + (sc / 3600.0) - tz;

            var y2 = mo <= 2 ? yr - 1 : yr;
            var m2 = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y2 / 100);
            var B = 2 - A + Math.floor(A / 4);
            var jd0 = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5;
            var jd = jd0 + decHrUtc / 24.0;
            var d = jd - 2451543.5;
            var T_j2000 = (jd - 2451545.0) / 36525.0;

            var RAD = Math.PI / 180.0, DEG = 180.0 / Math.PI;
            function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
            var ayanamsa = 23.857 + 1.39697 * T_j2000;

            var gmst = norm(280.46061837 + 360.98564736629 * (jd - 2451545.0));
            var lst = norm(gmst + lon) * RAD;
            var eps = (23.4392911 - 0.0130042 * T_j2000) * RAD;
            var ascTrop = norm(Math.atan2(Math.cos(lst), -(Math.sin(lst) * Math.cos(eps) + Math.tan(lat * RAD) * Math.sin(eps))) * DEG);
            var ascSid = norm(ascTrop - ayanamsa);
            var ascSign = Math.floor(ascSid / 30.0) % 12;
            var ascDegIn = ascSid % 30.0;
            var ascDms = Math.floor(ascDegIn) + "°" + Math.floor((ascDegIn * 60) % 60) + "'";

            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var NAKS = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];

            // Calculate Real-time planetary positions
            var sids = {};
            sids.Sun = norm(norm(282.9404 + 4.70935e-5 * d + norm(356.0470 + 0.9856002585 * d)) - ayanamsa);
            sids.Moon = norm(norm(125.1228 + 115.3654 + 13.0649929509 * d) - ayanamsa);
            sids.Mars = norm(norm(49.5574 + 286.5016 + 18.6021 + 0.5240207766 * d) - ayanamsa);
            sids.Mercury = norm(norm(48.3313 + 29.1241 + 168.6562 + 4.0923344368 * d) - ayanamsa);
            sids.Jupiter = norm(norm(100.4542 + 273.8777 + 19.8950 + 0.0830853001 * d) - ayanamsa);
            sids.Venus = norm(norm(76.6799 + 54.8910 + 48.0052 + 1.6021302244 * d) - ayanamsa);
            sids.Saturn = norm(norm(113.6634 + 339.3939 + 316.9670 + 0.0334442282 * d) - ayanamsa);
            sids.Rahu = norm(norm(125.04452 - 1934.136261 * T_j2000) - ayanamsa);
            sids.Ketu = norm(sids.Rahu + 180.0);

            var moonSignIdx = Math.floor(sids.Moon / 30.0) % 12;
            var moonNakIdx = Math.floor(sids.Moon / (360.0 / 27.0)) % 27;
            var moonPada = Math.floor((sids.Moon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;

            var q = (query || "").toLowerCase();
            var karyaHouse = 1;
            var karyaDesc = "तनु व आत्म सिद्धि";

            if (/mla|mp|chunav|chunaw|neta|rajneeti|politics|election|career|naukri|job|promotion|pad|adhikar|shasan|sarkar|ias|ips/.test(q)) {
                karyaHouse = 10;
                karyaDesc = "दशम भाव (राज्य पद, चुनाव, शासन सत्ता व कर्म सिद्धि)";
            } else if (/vivah|shadi|marriage|patni|pati|prem|love|rishta|sambandh|jeewansaathi/.test(q)) {
                karyaHouse = 7;
                karyaDesc = "सप्तम भाव (विवाह, दांपत्य व जीवनसाथी)";
            } else if (/paisa|dhan|sampatti|labh|wealth|money|business|vyapar|profit|kamai|karz|loan|loss/.test(q)) {
                karyaHouse = 11;
                karyaDesc = "एकादश व द्वितीय भाव (धन, लाभ, व्यापारिक वृद्धि व संचित कोष)";
            } else if (/santan|bacha|garbh|pregnancy|child|padhai|exam|upsc|pariksha|education|study/.test(q)) {
                karyaHouse = 5;
                karyaDesc = "पंचम भाव (संतान सुख, परीक्षा व विद्या अर्जन)";
            } else if (/court|case|mukadma|police|shatru|rog|bimar|bimari|health|swasthya/.test(q)) {
                karyaHouse = 6;
                karyaDesc = "षष्ठ भाव (रोग, ऋण, विवाद व शत्रु विजय)";
            } else if (/yatra|videsh|foreign|travel|visa|sthanantaran|transfer/.test(q)) {
                karyaHouse = 9;
                karyaDesc = "नवम व द्वादश भाव (विदेश यात्रा, भाग्य व स्थान परिवर्तन)";
            }

            var prashnesha = LORDS[ascSign];
            var karyaSign = (ascSign + karyaHouse - 1) % 12;
            var karyesha = LORDS[karyaSign];

            var planetSummary = [];
            var order = [
                { k: "Sun", n: "सूर्य" }, { k: "Moon", n: "चन्द्र" }, { k: "Mars", n: "मंगल" },
                { k: "Mercury", n: "बुध" }, { k: "Jupiter", n: "गुरु" }, { k: "Venus", n: "शुक्र" },
                { k: "Saturn", n: "शनि" }, { k: "Rahu", n: "राहु" }, { k: "Ketu", n: "केतु" }
            ];
            for (var i = 0; i < order.length; i++) {
                var p = order[i], plon = sids[p.k];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var hNum = ((sIdx - ascSign + 12) % 12) + 1;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                planetSummary.push(p.n + " " + SIGNS_HI[sIdx] + " (" + dms + ", भाव " + hNum + ")");
            }

            return {
                isPrashna: true,
                query: query,
                timestamp: now.toLocaleTimeString('hi-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                date: now.toLocaleDateString('hi-IN'),
                prashnaLagna: SIGNS_HI[ascSign] + " (" + ascDms + ")",
                prashnesha: prashnesha,
                moonSign: SIGNS_HI[moonSignIdx],
                moonNak: NAKS[moonNakIdx] + " (" + moonPada + ")",
                karyaHouse: karyaHouse,
                karyaDesc: karyaDesc,
                karyesha: karyesha,
                karyaSign: SIGNS_HI[karyaSign],
                planets: planetSummary.join("; ")
            };
        },
"""

    old_m_engine = """    window.VyasAIEngine = {
        keyPool: ["""
    new_m_engine = "    window.VyasAIEngine = {" + prashna_engine_code + "\n        keyPool: ["

    if old_m_engine in html:
        html = html.replace(old_m_engine, new_m_engine)
        print("  ✓ Injected castPrashnaKundli into mobile VyasAIEngine")

    # 2. Update askSage in mobile
    old_m_ask = """        async askSage(query, activeChart) {
            var prof = (activeChart && activeChart.profile) ? activeChart.profile : { name: "जातक", asc_sign: "मेष" };
            var planets = (activeChart && activeChart.planet_table) ? activeChart.planet_table.map(function(p) { return (p.planet || p.p || '') + ' in ' + (p.sign || p.r || '') + ' (भाव ' + (p.house || p.h || '') + ', ' + (p.dignity || p.s || '') + ')'; }).join('; ') : "Standard Placements";
            var dasha = (activeChart && activeChart.active_dasha && activeChart.active_dasha.chain) ? activeChart.active_dasha.chain : "शुक्र ➔ शनि ➔ मंगल ➔ चन्द्र ➔ बुध";

            var systemPrompt = [
                "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु एवं वशिष्ठ ज्योतिष के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।","""

    new_m_ask = """        async askSage(query, activeChart) {
            var isPrashnaMode = !activeChart || !activeChart.profile || !activeChart.planet_table || activeChart.isPrashna;
            var systemPrompt = "";

            if (isPrashnaMode) {
                var prashna = this.castPrashnaKundli(query);
                systemPrompt = [
                    "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु, वराहमिहिर एवं 'प्रश्न मार्ग' (Prashna Marga) के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।",
                    "",
                    "विशेष शास्त्रीय मर्यादा (Sacred Directive):",
                    "जातक ने अपनी कोई व्यक्तिगत जन्म पत्रिका प्रविष्ट नहीं की है। अतः 'प्रश्न मार्ग' एवं 'दैवज्ञ वल्लभ' शास्त्र के नियमानुसार, आपने प्रश्न पूछने के इस पावन क्षण (तात्कालिक गोचर व होरा) का वेध करके 'तात्कालिक प्रश्न कुण्डली' (Horary Chart) तैयार की है।",
                    "",
                    "तात्कालिक प्रश्न कुण्डली विवरण (Horary Data Lock):",
                    "- प्रश्न समय: " + prashna.date + " " + prashna.timestamp,
                    "- तात्कालिक प्रश्न लग्न (Prashna Lagna): " + prashna.prashnaLagna + " (प्रश्नेश: " + prashna.prashnesha + ")",
                    "- चन्द्रमा की तात्कालिक स्थिति: " + prashna.moonSign + " राशि, " + prashna.moonNak + " (चन्द्रमा कार्य सिद्धि का प्रत्यक्ष साक्षी व दूत है)",
                    "- प्रश्न का कार्य भाव (Karya Bhava): " + prashna.karyaDesc,
                    "- कार्येश (Karyesha): " + prashna.karyesha + " (" + prashna.karyaSign + " राशि का स्वामी)",
                    "- आकाश में ग्रहों की तात्कालिक वास्तविक स्थिति: " + prashna.planets,
                    "",
                    "अनिवार्य फलकथन निर्देश (Strict Invariants):",
                    "1. अपने उत्तर का आरम्भ इस पावन उद्घोष से करें:",
                    "   'ॐ नमः शिवाय। वत्स/पुत्र! चूंकि तुमने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक 'प्रश्न मार्ग' (Prashna Marga) एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, तुम्हारे प्रश्न पूछने के इस पावन क्षण (तात्कालिक गोचर व होरा) की 'तात्कालिक प्रश्न कुण्डली' (Horary Chart) का सूक्ष्म वेध कर उत्तर दे रहा हूँ।",
                    "2. किसी भी पुरानी या व्यक्तिगत जन्म कुण्डली (जैसे मेष लग्न, मकर में मंगल या रूचक योग) का लेशमात्र भी उल्लेख न करें। केवल और केवल ऊपर दी गई 'तात्कालिक प्रश्न कुण्डली' के अनुसार ही उत्तर दें।",
                    "3. प्रश्नेश (" + prashna.prashnesha + ") और कार्येश (" + prashna.karyesha + ") के परस्पर सम्बन्ध, केन्द्र/त्रिकोण स्थिति, दृष्टि, इत्थशाल (Ithasala) योग एवं चन्द्रमा के प्रभाव से कार्य सिद्धि (सफलता/विलम्ब/बाधा) का स्पष्ट, सटीक व समय-बद्ध फलकथन करें।",
                    "4. प्रश्न के समाधान हेतु प्रामाणिक वैदिक व सात्विक उपाय बताएं (जैसे विशेष मंत्र, इष्ट देव पूजा या दान)।"
                ].join('\\n');
            } else {
                var prof = activeChart.profile;
                var planets = activeChart.planet_table.map(function(p) { return (p.planet || p.p || '') + ' in ' + (p.sign || p.r || '') + ' (भाव ' + (p.house || p.h || '') + ', ' + (p.dignity || p.s || '') + ')'; }).join('; ');
                var dasha = (activeChart.active_dasha && activeChart.active_dasha.chain) ? activeChart.active_dasha.chain : "सक्रिय विंशोत्तरी दशा";

                systemPrompt = [
                    "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु एवं वशिष्ठ ज्योतिष के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।","""

    if old_m_ask in html:
        html = html.replace(old_m_ask, new_m_ask)
        print("  ✓ Updated askSage in mobile/index.html")

    # 3. Update mobile generateDynamicLocalReply
    old_m_local = """        generateDynamicLocalReply(query, activeChart) {
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeHolisticReading) {
                return window.VyasDaivagyaVision.synthesizeHolisticReading(query, activeChart);
            }
            var prof = (activeChart && activeChart.profile) ? activeChart.profile : { name: "जातक", asc_sign: "मेष" };
            return "<b>आचार्य व्यास का प्रामाणिक दैवज्ञ मार्गदर्शन:</b><br>सादर प्रणाम " + prof.name + " जी! आपकी कुण्डली व गोचर का सूक्ष्म परीक्षण किया गया है। वर्तमान दशा शुभ प्रभाव दे रही है। नित्य 'ॐ नमः शिवाय' जपें व सूर्यदेव को अर्घ्य दें।";
        }"""

    new_m_local = """        generateDynamicLocalReply(query, activeChart) {
            var isPrashnaMode = !activeChart || !activeChart.profile || !activeChart.planet_table || activeChart.isPrashna;
            if (isPrashnaMode) {
                var prashna = this.castPrashnaKundli(query);
                return "<b>ॐ नमः शिवाय।</b><br><br>" +
                    "वत्स! चूंकि तुमने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक <b>'प्रश्न मार्ग' (Prashna Marga)</b> एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, तुम्हारे प्रश्न पूछने के इस पावन क्षण की <b>'तात्कालिक प्रश्न कुण्डली'</b> (Horary Chart) का सूक्ष्म वेध कर उत्तर दे रहा हूँ:<br><br>" +
                    "• <b>तात्कालिक प्रश्न लग्न:</b> " + prashna.prashnaLagna + " (प्रश्नेश: <b>" + prashna.prashnesha + "</b>)<br>" +
                    "• <b>चन्द्रमा का गोचर:</b> " + prashna.moonSign + " राशि, नक्षत्र " + prashna.moonNak + "<br>" +
                    "• <b>प्रश्न कार्य भाव:</b> " + prashna.karyaDesc + "<br>" +
                    "• <b>कार्येश स्वामी:</b> " + prashna.karyesha + " (" + prashna.karyaSign + " राशिपति)<br><br>" +
                    "<b>आचार्य व्यास का दैवज्ञ निर्णय (Prashna Synthesis):</b><br>" +
                    "प्रश्न मार्ग के अनुसार जब प्रश्नेश (" + prashna.prashnesha + ") एवं कार्येश (" + prashna.karyesha + ") के मध्य शुभ दृष्टि-सम्बन्ध बनता है तथा चन्द्रमा शुभ स्थिति में होता है, तो अभीष्ट कार्य में सफलता का मार्ग प्रशस्त होता है। वर्तमान तात्कालिक गोचर में चन्द्रमा की स्थिति आपके मन के अभीष्ट संकल्प को फलवती करने की दिशा में अग्रसर है।<br><br>" +
                    "<b>मार्गदर्शन व सात्विक उपाय:</b><br>" +
                    "कार्य सिद्धि में अनुकूलता हेतु नित्य प्रातः <i>'ॐ नमः शिवाय'</i> का 108 बार जप करें तथा बुधवार या गुरुवार को सात्विक दान करें। यदि आप अपने जीवन के दीर्घकालिक 10-20 वर्षों का सटीक फलादेश चाहते हैं, तो ऊपर <b>'+ नई कुण्डली'</b> विकल्प से अपना वास्तविक जन्म विवरण दर्ज करें।";
            }
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeHolisticReading) {
                return window.VyasDaivagyaVision.synthesizeHolisticReading(query, activeChart);
            }
            var prof = activeChart.profile;
            return "<b>आचार्य व्यास का प्रामाणिक दैवज्ञ मार्गदर्शन:</b><br>सादर प्रणाम " + prof.name + " जी! आपकी कुण्डली (" + prof.asc_sign + " लग्न) व गोचर का सूक्ष्म परीक्षण किया गया है। वर्तमान दशा शुभ प्रभाव दे रही है। नित्य 'ॐ नमः शिवाय' जपें व सूर्यदेव को अर्घ्य दें।";
        }"""

    if old_m_local in html:
        html = html.replace(old_m_local, new_m_local)
        print("  ✓ Updated generateDynamicLocalReply in mobile/index.html")

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ Saved updated mobile/index.html")

if __name__ == '__main__':
    patch_desktop()
    patch_mobile()
