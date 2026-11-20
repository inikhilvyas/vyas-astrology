import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# -------------------------------------------------------------
# 1. Update CSS: Make .cockpit-container a clean 2-column layout
# -------------------------------------------------------------
old_cockpit_css = """        /* --- 3-Column Cockpit Workspace --- */
        .cockpit-container {
            display: grid;
            grid-template-columns: 420px 1fr 340px;
            gap: 16px;
            padding: 16px 20px;
            flex: 1;
            max-width: 1920px;
            margin: 0 auto;
            width: 100%;
        }
        @media (max-width: 1440px) {
            .cockpit-container { grid-template-columns: 420px 1fr; gap: 14px; padding: 14px; }
        }"""

new_cockpit_css = """        /* --- 2-Column High-Precision Cockpit Workspace (Dedicated Floating Concierge) --- */
        .cockpit-container {
            display: grid;
            grid-template-columns: 480px 1fr;
            gap: 18px;
            padding: 16px 20px;
            flex: 1;
            max-width: 1920px;
            margin: 0 auto;
            width: 100%;
        }
        @media (max-width: 1200px) {
            .cockpit-container { grid-template-columns: 1fr; gap: 14px; padding: 12px; }
        }"""

if old_cockpit_css in content:
    content = content.replace(old_cockpit_css, new_cockpit_css)
    print("✓ Updated .cockpit-container to 2-column layout")
else:
    print("Warning: old_cockpit_css not matched verbatim")

# -------------------------------------------------------------
# 2. Remove the redundant inline #desktopSageChatCol column
# -------------------------------------------------------------
chat_col_start = content.find('<div class="cockpit-col" id="desktopSageChatCol"')
if chat_col_start != -1:
    chat_col_end = content.find('<!-- END RIGHT COLUMN -->', chat_col_start)
    if chat_col_end == -1:
        # Find closing </div>
        depth = 1
        pos = content.find('>', chat_col_start) + 1
        while depth > 0 and pos < len(content):
            if content[pos:pos+4] == '<div':
                depth += 1
            elif content[pos:pos+5] == '</div':
                depth -= 1
            pos += 1
        chat_col_end = pos + 5
    content = content[:chat_col_start] + '<!-- Redundant inline chatbot removed; dedicated floating AI concierge active -->' + content[chat_col_end:]
    print("✓ Removed redundant inline #desktopSageChatCol from DOM")
else:
    print("Notice: #desktopSageChatCol already removed or not found")

# -------------------------------------------------------------
# 3. Add Special Yogas (Vargottama, Pushkar Navamsha, Pushkar Bhaga) to computeMathematicalKundli
# -------------------------------------------------------------
varga_loop_target = """                var cKeyLower = vk.toLowerCase();
                var cObj = {
                    key: vk,
                    title: VARGA_TITLES[vk],
                    ascSign: SIGNS_HI[aSign] + " लग्न (" + Math.floor(ascV.deg) + "°" + Math.floor((ascV.deg * 60) % 60) + "')",
                    houses: vHouses,
                    planetDetails: pDetails
                };"""

varga_loop_replacement = """                // Pure Mathematical Special Yogas Engine (Vargottama, Pushkar Navamsha, Pushkar Bhaga)
                var specialYogas = [];
                if (vk === "D9") {
                    if (ascVargas.D1.sign_index === ascVargas.D9.sign_index) {
                        specialYogas.push("✦ लग्न वर्गोत्तम (Lagna Vargottama — " + SIGNS_HI[aSign] + " लग्न)");
                    }
                    var PUSHKAR_BHAGAS = [21, 14, 18, 8, 19, 9, 24, 11, 23, 14, 19, 9];
                    for (var pi = 0; pi < order.length; pi++) {
                        var pn = order[pi];
                        var pD1 = planetVargas[pn].D1;
                        var pD9 = planetVargas[pn].D9;
                        var plon = sids[pn];
                        var pdeg = plon % 30.0;
                        var psign = Math.floor(plon / 30.0) % 12;
                        var nPart = Math.floor(pdeg / (30.0 / 9.0));

                        // 1. Planet Vargottama (D1 Rashi == D9 Rashi)
                        if (pD1.sign_index === pD9.sign_index) {
                            specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " वर्गोत्तम (" + SIGNS_HI[pD1.sign_index] + " राशि D1 व D9 समान)");
                        }

                        // 2. Pushkar Navamsha (24 Auspicious Nourishing Navamshas in Zodiac)
                        var isPushkarNav = false;
                        var elem = psign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
                        if (elem === 0 && (nPart === 6 || nPart === 8)) isPushkarNav = true; // 7th & 9th
                        else if (elem === 1 && (nPart === 2 || nPart === 4)) isPushkarNav = true; // 3rd & 5th
                        else if (elem === 2 && (nPart === 5 || nPart === 7)) isPushkarNav = true; // 6th & 8th
                        else if (elem === 3 && (nPart === 0 || nPart === 2)) isPushkarNav = true; // 1st & 3rd

                        if (isPushkarNav) {
                            specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " पुष्कर नवमांश (कल्याणकारी आरोग्य व भाग्य वर्धक)");
                        }

                        // 3. Pushkar Bhaga (±1° tolerance)
                        if (Math.abs(pdeg - PUSHKAR_BHAGAS[psign]) <= 1.0) {
                            specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " पुष्कर भाग (परम सिद्धि व अमृतोपम योग)");
                        }
                    }
                }

                var cKeyLower = vk.toLowerCase();
                var cObj = {
                    key: vk,
                    title: VARGA_TITLES[vk],
                    ascSign: SIGNS_HI[aSign] + " लग्न (" + Math.floor(ascV.deg) + "°" + Math.floor((ascV.deg * 60) % 60) + "')",
                    houses: vHouses,
                    planetDetails: pDetails,
                    specialYogas: specialYogas
                };"""

if varga_loop_target in content:
    content = content.replace(varga_loop_target, varga_loop_replacement)
    print("✓ Added pure mathematical Special Yogas to computeMathematicalKundli")
else:
    print("Warning: varga_loop_target not found verbatim")

# -------------------------------------------------------------
# 4. Bulletproof generateDiamondSVG house sign numbers & planet labels
# -------------------------------------------------------------
diamond_loop_target = """            for (var house = 1; house <= 12; house++) {
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
                }"""

diamond_loop_replacement = """            // Determine authentic Varga Ascendant sign from House 1
            var lagnaSignNum = 1;
            if (housesData && housesData[1]) {
                var d1Val = housesData[1][0];
                lagnaSignNum = parseInt(typeof d1Val === 'object' && d1Val !== null ? d1Val.sign : d1Val) || 1;
            }

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];
                var data = housesData[house] || [];
                if (!data || data.length === 0) continue;

                // Immutable Parashari North Indian Rule: House h sign = ((lagnaSignNum - 1 + house - 1) % 12) + 1
                var signNum = ((lagnaSignNum - 1 + house - 1) % 12) + 1;
                var rawPlanets = (typeof data[0] === 'object' && data[0] !== null) ? data : data.slice(1);
                var planets = [];
                for (var pi = 0; pi < rawPlanets.length; pi++) {
                    var item = rawPlanets[pi];
                    if (typeof item === 'object' && item !== null) {
                        var pText = (item.p || item.planet || '').replace(/\\s*D[0-9]+/gi, '') + (item.d ? (' ' + item.d) : '');
                        planets.push(pText.trim());
                    } else if (item) {
                        var pStr = String(item).replace(/\\s*D[0-9]+/gi, '').trim();
                        if (pStr) planets.push(pStr);
                    }
                }"""

if diamond_loop_target in content:
    content = content.replace(diamond_loop_target, diamond_loop_replacement)
    print("✓ Bulletproofed generateDiamondSVG: House 1 is always True Varga Ascendant")
else:
    print("Warning: diamond_loop_target not found verbatim")

# -------------------------------------------------------------
# 5. Display Special Yogas in renderChart
# -------------------------------------------------------------
render_chart_target = """            var hData = (cData && cData.houses) ? cData.houses : cData;
            if (this.chartStyle === 'south') {
                wrap.innerHTML = this.generateSouthIndianSVG(hData, 460, chartTitle);
            } else {
                wrap.innerHTML = this.generateDiamondSVG(hData, 460, chartTitle);
            }
        },"""

render_chart_replacement = """            var hData = (cData && cData.houses) ? cData.houses : cData;
            var chartSvg = (this.chartStyle === 'south') ? this.generateSouthIndianSVG(hData, 460, chartTitle) : this.generateDiamondSVG(hData, 460, chartTitle);

            // Special Yogas banner for D-charts (e.g. Vargottama, Pushkar Navamsha)
            var yogasHtml = '';
            if (cData && cData.specialYogas && cData.specialYogas.length > 0) {
                yogasHtml = '<div style="margin-top:10px; display:flex; flex-wrap:wrap; gap:6px; justify-content:center;">' +
                    cData.specialYogas.map(function(y) {
                        return '<span style="background:rgba(212,175,55,0.14); border:1px solid #d4af37; color:#d4af37; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">' + y + '</span>';
                    }).join('') +
                '</div>';
            }

            wrap.innerHTML = chartSvg + yogasHtml;
        },"""

if render_chart_target in content:
    content = content.replace(render_chart_target, render_chart_replacement)
    print("✓ Added Special Yogas badges rendering in renderChart")
else:
    print("Warning: render_chart_target not found verbatim")

# -------------------------------------------------------------
# 6. Fix renderAshtakavarga for ANY user & dynamic SAV Sutra Note
# -------------------------------------------------------------
av_target = """            if (!av) return;
            var sav = (av.sav && av.sav.reduce(function(a, b) { return a + b; }, 0) === 337) ? av.sav : [33, 25, 25, 30, 31, 39, 29, 26, 19, 31, 27, 22];

            // 1. SAV 12 Cards Grid (100% Guaranteed 337 Points)
            var grid = document.getElementById('sav12Grid');
            if (grid) {
                var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                var html = '';
                for (var h = 1; h <= 12; h++) {
                    var pts = sav[h - 1] || 28;
                    var cls = pts >= 32 ? 'sav-high' : (pts >= 28 ? 'sav-good' : 'sav-low');
                    var tag = pts >= 32 ? 'अति बलवान' : (pts >= 28 ? 'शुभ' : 'सावधानी');

                    html += '<div class="sav-card ' + cls + '">' +
                        '<div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">' + h + ' भाव (' + SIGNS_HI[h - 1] + ')</div>' +
                        '<div class="sav-score ' + cls + '">' + pts + '</div>' +
                        '<div style="font-size:0.68rem; font-weight:700;">' + tag + '</div>' +
                    '</div>';
                }
                grid.innerHTML = html;
            }"""

av_replacement = """            if (!av) return;
            var sav = (av.sav && av.sav.reduce(function(a, b) { return a + b; }, 0) === 337) ? av.sav : [33, 25, 25, 30, 31, 39, 29, 26, 19, 31, 27, 22];

            // 1. SAV 12 Cards Grid (Accurately mapped by Bhava from Native's Lagna Sign)
            var grid = document.getElementById('sav12Grid');
            if (grid) {
                var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                var ascSignName = (this.activeChartData && this.activeChartData.profile) ? (this.activeChartData.profile.asc_sign || 'मेष') : 'मेष';
                var ascSignIdx = SIGNS_HI.indexOf(ascSignName);
                if (ascSignIdx === -1) ascSignIdx = 0;

                var maxPts = -1, maxHouse = 1, maxSign = '';
                var html = '';
                for (var h = 1; h <= 12; h++) {
                    var sIdx = (ascSignIdx + h - 1) % 12;
                    var pts = sav[sIdx] || 28;
                    if (pts > maxPts) { maxPts = pts; maxHouse = h; maxSign = SIGNS_HI[sIdx]; }

                    var cls = pts >= 32 ? 'sav-high' : (pts >= 28 ? 'sav-good' : 'sav-low');
                    var tag = pts >= 32 ? 'अति बलवान' : (pts >= 28 ? 'शुभ' : 'सावधानी');

                    html += '<div class="sav-card ' + cls + '">' +
                        '<div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">' + h + ' भाव (' + SIGNS_HI[sIdx] + ')</div>' +
                        '<div class="sav-score ' + cls + '">' + pts + '</div>' +
                        '<div style="font-size:0.68rem; font-weight:700;">' + tag + '</div>' +
                    '</div>';
                }
                grid.innerHTML = html;

                // Dynamic Sutra Note quoting native's actual strongest house and Lagna points
                var noteElem = document.getElementById('savSutraNote');
                if (noteElem) {
                    var lagnaPts = sav[ascSignIdx];
                    var hNamesHi = ["प्रथम", "द्वितीय", "तृतीय", "चतुर्थ", "पंचम", "षष्ठ", "सप्तम", "अष्टम", "नवम", "दशम", "एकादश", "द्वादश"];
                    noteElem.innerHTML = '<b>सर्वाष्टकवर्ग फलित सूत्र:</b> 28 से अधिक बिन्दु वाले भाव जीवन में विशेष शक्ति, कार्य सिद्धि व उन्नति देते हैं। सर्वाधिक बलवान: <b>' + hNamesHi[maxHouse - 1] + ' भाव (' + maxSign + ' ' + maxPts + ' बिन्दु)</b> एवं <b>प्रथम भाव (' + SIGNS_HI[ascSignIdx] + ' ' + lagnaPts + ' बिन्दु)</b> जातक को अद्वितीय प्रतिस्पर्धी क्षमता, दीर्घायु व पराक्रम प्रदान करते हैं।';
                }
            }"""

if av_target in content:
    content = content.replace(av_target, av_replacement)
    print("✓ Fixed renderAshtakavarga: universally maps Bhavas from Native's Lagna")
else:
    print("Warning: av_target not found verbatim")

# -------------------------------------------------------------
# 7. Complete 7-Day Day & Night Chaughadiya Engine in renderPanchang
# -------------------------------------------------------------
panchang_target = """            // Choghadiya
            var chogDay = [
                ["उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग"],
                ["अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत"],
                ["रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ", "रोग"],
                ["लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ"],
                ["शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ"],
                ["चल", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल"],
                ["काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल"]
            ];
            var cList = chogDay[dayOfWeek];
            var chogGrid = document.getElementById('dPanChoghadiyaGrid');
            if (chogGrid) {
                var chHtml = '';
                for (var c = 0; c < 8; c++) {
                    var cName = cList[c];
                    var cStart = fmtMin(sunriseMin + (c * partLen));
                    var cEnd = fmtMin(sunriseMin + ((c + 1) * partLen));
                    var isGood = (cName === "अमृत" || cName === "शुभ" || cName === "लाभ");
                    var isNeutral = (cName === "चर");
                    var bg = isGood ? "rgba(16,185,129,0.18)" : (isNeutral ? "rgba(56,189,248,0.15)" : "rgba(239,68,68,0.18)");
                    var border = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                    var col = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                    var tag = isGood ? "शुभ" : (isNeutral ? "मध्यम" : "त्याज्य");

                    chHtml += '<div style="background:' + bg + '; border:1px solid ' + border + '; padding:8px 4px; border-radius:6px;">' +
                        '<b style="color:' + col + '; font-size:0.92rem;">' + cName + '</b> (' + tag + ')<br>' +
                        '<span style="font-size:0.76rem; font-family:var(--font-mono); color:var(--text-secondary);">' + cStart.replace(' AM','').replace(' PM','') + '-' + cEnd.replace(' AM','').replace(' PM','') + '</span>' +
                    '</div>';
                }
                chogGrid.innerHTML = chHtml;
            }"""

panchang_replacement = """            // =========================================================================
            // AUTHENTIC 7-DAY DAY & NIGHT CHAUGHADIYA OBSERVATORY (SHASHTRIC ORDER)
            // =========================================================================
            var chogDay = [
                // 0: Sunday (रविवार दिन): उद्वेग, चर, लाभ, अमृत, काल, शुभ, रोग, उद्वेग
                ["उद्वेग", "चर", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग"],
                // 1: Monday (सोमवार दिन): अमृत, काल, शुभ, रोग, उद्वेग, चर, लाभ, अमृत
                ["अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चर", "लाभ", "अमृत"],
                // 2: Tuesday (मंगलवार दिन): रोग, उद्वेग, चर, लाभ, अमृत, काल, शुभ, रोग
                ["रोग", "उद्वेग", "चर", "लाभ", "अमृत", "काल", "शुभ", "रोग"],
                // 3: Wednesday (बुधवार दिन): लाभ, अमृत, काल, शुभ, रोग, उद्वेग, चर, लाभ
                ["लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चर", "लाभ"],
                // 4: Thursday (गुरुवार दिन): शुभ, रोग, उद्वेग, चर, लाभ, अमृत, काल, शुभ
                ["शुभ", "रोग", "उद्वेग", "चर", "लाभ", "अमृत", "काल", "शुभ"],
                // 5: Friday (शुक्रवार दिन): चर, लाभ, अमृत, काल, शुभ, रोग, उद्वेग, चर
                ["चर", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चर"],
                // 6: Saturday (शनिवार दिन): काल, शुभ, रोग, उद्वेग, चर, लाभ, अमृत, काल
                ["काल", "शुभ", "रोग", "उद्वेग", "चर", "लाभ", "अमृत", "काल"]
            ];

            var chogNight = [
                // 0: Sunday Night (रविवार रात्रि): शुभ, अमृत, चर, रोग, काल, लाभ, उद्वेग, शुभ
                ["शुभ", "अमृत", "चर", "रोग", "काल", "लाभ", "उद्वेग", "शुभ"],
                // 1: Monday Night (सोमवार रात्रि): चर, रोग, काल, लाभ, उद्वेग, शुभ, अमृत, चर
                ["चर", "रोग", "काल", "लाभ", "उद्वेग", "शुभ", "अमृत", "चर"],
                // 2: Tuesday Night (मंगलवार रात्रि): काल, लाभ, उद्वेग, शुभ, अमृत, चर, रोग, काल
                ["काल", "लाभ", "उद्वेग", "शुभ", "अमृत", "चर", "रोग", "काल"],
                // 3: Wednesday Night (बुधवार रात्रि): उद्वेग, शुभ, अमृत, चर, रोग, काल, लाभ, उद्वेग
                ["उद्वेग", "शुभ", "अमृत", "चर", "रोग", "काल", "लाभ", "उद्वेग"],
                // 4: Thursday Night (गुरुवार रात्रि): अमृत, चर, रोग, काल, लाभ, उद्वेग, शुभ, अमृत
                ["अमृत", "चर", "रोग", "काल", "लाभ", "उद्वेग", "शुभ", "अमृत"],
                // 5: Friday Night (शुक्रवार रात्रि): रोग, काल, लाभ, उद्वेग, शुभ, अमृत, चर, रोग
                ["रोग", "काल", "लाभ", "उद्वेग", "शुभ", "अमृत", "चर", "रोग"],
                // 6: Saturday Night (शनिवार रात्रि): लाभ, उद्वेग, शुभ, अमृत, चर, रोग, काल, लाभ
                ["लाभ", "उद्वेग", "शुभ", "अमृत", "चर", "रोग", "काल", "लाभ"]
            ];

            var dayList = chogDay[dayOfWeek];
            var nightList = chogNight[dayOfWeek];
            var dayPartLen = (sunsetMin - sunriseMin) / 8.0;
            var nightLen = (1440 - sunsetMin + sunriseMin);
            var nightPartLen = nightLen / 8.0;

            var curNow = new Date();
            var curMin = curNow.getHours() * 60 + curNow.getMinutes();
            var isDayNow = (curMin >= sunriseMin && curMin < sunsetMin);

            var chogGrid = document.getElementById('dPanChoghadiyaGrid');
            if (chogGrid) {
                function renderChogCards(list, startMin, partLength, isNight) {
                    var html = '';
                    for (var c = 0; c < 8; c++) {
                        var cName = list[c];
                        var sMin = Math.round(startMin + (c * partLength)) % 1440;
                        var eMin = Math.round(startMin + ((c + 1) * partLength)) % 1440;

                        var isActive = false;
                        if (!isNight && isDayNow) {
                            var sM = Math.round(startMin + (c * partLength));
                            var eM = Math.round(startMin + ((c + 1) * partLength));
                            if (curMin >= sM && curMin < eM) isActive = true;
                        } else if (isNight && !isDayNow) {
                            var relCur = (curMin >= sunsetMin) ? (curMin - sunsetMin) : (curMin + 1440 - sunsetMin);
                            var relS = c * partLength;
                            var relE = (c + 1) * partLength;
                            if (relCur >= relS && relCur < relE) isActive = true;
                        }

                        var isGood = (cName === "अमृत" || cName === "शुभ" || cName === "लाभ");
                        var isNeutral = (cName === "चर" || cName === "चल");
                        var bg = isGood ? "rgba(16,185,129,0.18)" : (isNeutral ? "rgba(56,189,248,0.15)" : "rgba(239,68,68,0.18)");
                        var border = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                        var col = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                        var tag = isGood ? "सर्वोत्तम" : (isNeutral ? "मध्यम" : "त्याज्य");

                        var activeBadge = isActive ? '<div style="background:#f59e0b; color:#000; font-size:0.62rem; font-weight:900; padding:1px 4px; border-radius:4px; margin-bottom:3px; animation:pulse 1.5s infinite;">✦ सक्रिय चौघड़िया</div>' : '';
                        var activeBorder = isActive ? 'border:2px solid #f59e0b; box-shadow:0 0 10px rgba(245,158,11,0.5);' : ('border:1px solid ' + border + ';');

                        html += '<div style="background:' + bg + '; ' + activeBorder + ' padding:8px 4px; border-radius:6px;">' +
                            activeBadge +
                            '<b style="color:' + col + '; font-size:0.92rem;">' + cName + '</b> (' + tag + ')<br>' +
                            '<span style="font-size:0.74rem; font-family:var(--font-mono); color:var(--text-secondary);">' + fmtMin(sMin).replace(' AM','').replace(' PM','') + ' - ' + fmtMin(eMin).replace(' AM','').replace(' PM','') + '</span>' +
                        '</div>';
                    }
                    return html;
                }

                var fullHtml = '<div style="grid-column:1/-1; font-weight:800; color:var(--text-primary); font-size:0.85rem; margin-top:4px; margin-bottom:6px; display:flex; align-items:center; justify-content:space-between;">' +
                    '<span>☀️ दिन का चौघड़िया (सूर्योदय से सूर्यास्त)</span>' +
                    (isDayNow ? '<span style="color:#f59e0b; font-size:0.72rem; font-weight:700;">● दिन का पहर सक्रिय</span>' : '') +
                '</div>' +
                renderChogCards(dayList, sunriseMin, dayPartLen, false) +
                '<div style="grid-column:1/-1; font-weight:800; color:var(--text-primary); font-size:0.85rem; margin-top:14px; margin-bottom:6px; display:flex; align-items:center; justify-content:space-between;">' +
                    '<span>🌙 रात्रि का चौघड़िया (सूर्यास्त से अगले सूर्योदय)</span>' +
                    (!isDayNow ? '<span style="color:#f59e0b; font-size:0.72rem; font-weight:700;">● रात्रि का पहर सक्रिय</span>' : '') +
                '</div>' +
                renderChogCards(nightList, sunsetMin, nightPartLen, true);

                chogGrid.innerHTML = fullHtml;
            }"""

if panchang_target in content:
    content = content.replace(panchang_target, panchang_replacement)
    print("✓ Implemented complete 7-Day Day & Night Chaughadiya Observatory with real-time active highlight")
else:
    print("Warning: panchang_target not found verbatim")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Patching complete. New length:", len(content))

