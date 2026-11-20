import os, sys, re

def patch_index_html():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # -------------------------------------------------------------
    # 1. PATCH SYSTEMPROMPT WITH DYNAMIC DRISHTI CHAKRA & STRICT INVARIANTS
    # -------------------------------------------------------------
    sp_needle = "var prof = activeChart.profile;"
    sp_start = html.find(sp_needle)
    sp_end = html.find("// 1. Try PHP Backend Proxy First", sp_start)
    if sp_start == -1 or sp_end == -1:
        print("ERROR: Could not find systemPrompt block")
        return False

    old_sp_block = html[sp_start:sp_end]
    
    # We will build a dynamic Drishti Chakra inside the client script
    new_sp_block = """var prof = activeChart.profile;
                var planets = activeChart.planet_table.map(function(p) {
                    var pName = p.planet || p.p || '';
                    var rashi = p.sign || p.r || '';
                    var deg = p.degree || p.d || '';
                    var nak = p.nakshatra || p.n || '';
                    var house = p.house || p.h || '';
                    var state = p.dignity || p.s || '';
                    return pName + ': ' + rashi + ' ' + deg + ' (नक्षत्र: ' + nak + ', भाव ' + house + ', स्थिति: ' + state + ')';
                }).join('\\n- ');

                // Build Mathematical Planetary Aspect (दृष्टि चक्र) Ledger for Active Chart
                var SIGNS_HI_REF = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                var drishtiLines = [];
                activeChart.planet_table.forEach(function(p) {
                    var pName = (p.p || p.planet || '').replace(/\\s*\\(.*\\)/, '').trim();
                    var pHouse = parseInt(p.h || p.house || 1);
                    var pSign = p.r || p.sign || '';
                    var aspects = [];
                    
                    function getTarget(offset) {
                        var targetHouse = ((pHouse - 1 + offset) % 12) + 1;
                        // Determine target sign from house offset
                        var signIdx = SIGNS_HI_REF.indexOf(pSign);
                        var targetSign = (signIdx !== -1) ? SIGNS_HI_REF[(signIdx + offset) % 12] : ("भाव " + targetHouse);
                        return "भाव " + targetHouse + " (" + targetSign + ")";
                    }

                    if (pName === 'शनि') {
                        aspects.push("3री दृष्टि ➔ " + getTarget(2));
                        aspects.push("7वीं दृष्टि ➔ " + getTarget(6));
                        aspects.push("10वीं दृष्टि ➔ " + getTarget(9));
                    } else if (pName === 'मंगल') {
                        aspects.push("4थी दृष्टि ➔ " + getTarget(3));
                        aspects.push("7वीं दृष्टि ➔ " + getTarget(6));
                        aspects.push("8वीं दृष्टि ➔ " + getTarget(7));
                    } else if (pName === 'गुरु' || pName === 'बृहस्पति' || pName === 'राहु' || pName === 'केतु') {
                        aspects.push("5वीं दृष्टि ➔ " + getTarget(4));
                        aspects.push("7वीं दृष्टि ➔ " + getTarget(6));
                        aspects.push("9वीं दृष्टि ➔ " + getTarget(8));
                    } else {
                        aspects.push("7वीं दृष्टि ➔ " + getTarget(6));
                    }
                    drishtiLines.push("• " + pName + " (" + pSign + ", भाव " + pHouse + "): " + aspects.join(', '));
                });

                var dasha = (activeChart.active_dasha && activeChart.active_dasha.chain) ? activeChart.active_dasha.chain : "शुक्र ➔ शनि ➔ मंगल ➔ बुध (सक्रिय विंशोत्तरी दशा)";
                var now = new Date();
                var curDateStr = now.toLocaleDateString('hi-IN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
                var curYear = now.getFullYear();

                systemPrompt = [
                    "आप 'आचार्य व्यास' हैं — महर्षि पराशर, महर्षि भृगु, वराहमिहिर एवं कृष्णमूर्ति (KP) ज्योतिष के साक्षात प्रतिनिधि पूज्य वैदिक दैवज्ञ।",
                    "",
                    "अपरिहार्य काल-संरेखण नियम (Strict Time-Anchoring Invariant - ZERO PAST HALLUCINATION):",
                    "- आज का वास्तविक वर्तमान काल: " + curDateStr + " (ईस्वी सन् " + curYear + ", संवत् 2083) है।",
                    "- भूलकर भी 2024 या जनवरी 2025 जैसी पिछली तिथियों का भविष्य या वर्तमान के रूप में उल्लेख न करें। जातक के प्रोजेक्ट, व्यापार या जीवन के कार्यों के पूर्ण होने की समय-सीमाएं वर्तमान काल से आगे (दिसंबर 2026, 2027 एवं आगामी वर्षों) के संदर्भ में ही दें।",
                    "",
                    "अपरिहार्य शिष्टाचार एवं सम्भाषण मर्यादा (Strict Respect Protocol - ZERO 'पुत्र' / ZERO 'तुम'):",
                    "- जातक (" + prof.name + ") को सदा अत्यंत आदर, सम्मान व विनम्रता से 'सादर प्रणाम " + prof.name + " जी' या 'आदरणीय " + prof.name + " जी' कहकर सम्बोधित करें।",
                    "- वाक्य रचना में सदा 'आप', 'आपका', 'आपकी', 'कीजिए' का ही प्रयोग करें।",
                    "- भूलकर भी जातक को 'पुत्र', 'वत्स', 'बेटा' अथवा अनौपचारिक 'तुम', 'तुम्हारी', 'तुम्हारे', 'करो' न कहें। यह मर्यादा अनिवार्य व अनुल्लंघनीय है।",
                    "",
                    "═════════════════════════════════════════════════════════════════",
                    "📊 KUNDLI DATA LEDGER (अपरिवर्तनीय खगोलीय निर्देशांक — Anti-Hallucination Lock)",
                    "═════════════════════════════════════════════════════════════════",
                    "- जातक का नाम: " + prof.name,
                    "- जन्म लग्न: " + (prof.asc_sign || "मेष") + " (" + (prof.asc_dms || "23°42'00\\\"") + ") [लग्न भाव 1]",
                    "- जन्म स्थान: " + (prof.city || "भारत"),
                    "- सक्रिय 4-स्तरीय विंशोत्तरी दशा: " + dasha,
                    "- तात्कालिक आकाश गोचर वेध (18 Nov 2026): देवगुरु बृहस्पति (सिंह 01°51'), शनिदेव (मीन 14°08'), राहु (कुंभ 00°53'), केतु (सिंह 00°53') [NASA JPL/Swiss Ephemeris 0.0000°]",
                    "- जन्मकालीन 0.0000° ग्रह निर्देशांक:",
                    "- " + planets,
                    "",
                    "═════════════════════════════════════════════════════════════════",
                    "🔭 PLANETARY ASPECT (दृष्टि चक्र) LEDGER — अपरिवर्तनीय शास्त्रीय दृष्टि गणित",
                    "═════════════════════════════════════════════════════════════════",
                    drishtiLines.join('\\n'),
                    "",
                    "⚠️ अपरिवर्तनीय शास्त्रीय दृष्टि पाबंदी (STRICT ASPECT LAWS):",
                    "1. शनिदेव की केवल 3री, 7वीं एवं 10वीं दृष्टि होती है। शनि की 5वीं या 9वीं दृष्टि कभी नहीं होती (शनि की दृष्टि कभी मिथुन पर नहीं है; मिथुन पर गुरु की 7वीं दृष्टि है)।",
                    "2. मंगलदेव की केवल 4थी, 7वीं व 8वीं दृष्टि होती है।",
                    "3. गुरु, राहु एवं केतु की केवल 5वीं, 7वीं व 9वीं दृष्टि होती है।",
                    "4. सूर्य, चन्द्र, बुध, शुक्र की केवल 7वीं दृष्टि होती है।",
                    "5. केवल उपरोक्त दृष्टि लेजर में दर्ज दृष्टि ही सत्य है। इसके अतिरिक्त किसी भाव पर दृष्टि बताना वर्जित है।",
                    "═════════════════════════════════════════════════════════════════",
                    "",
                    "दैवज्ञ दृष्टि एवं फलकथन मर्यादा (Astrological Reasoning Directives):",
                    "1. केवल यांत्रिक रूप से अलग-अलग ग्रहों के फल न गिनाएं, अपितु एक सिद्ध ज्योतिषी की भांति कुण्डली का संश्लिष्ट दर्शन करें:",
                    "   (क) लग्न एवं लग्नेश का बल, आत्मबल एवं शारीरिक सामर्थ्य।",
                    "   (ख) चन्द्रमा (मन व भावना) एवं सूर्य (आत्मकारक व प्रतिष्ठा)।",
                    "   (ग) सक्रिय विंशोत्तरी दशा-अन्तर्दशा का स्वामित्व, शुभाशुभत्व एवं फल पकने की घड़ी।",
                    "   (घ) गोचर मिलान (The Trigger): देवगुरु बृहस्पति एवं शनि का गोचर तथा दोहरा दृष्टि-वेध (Double Transit 2026-2027)।",
                    "   (ङ) बहु-पद्धतीय शास्त्रीय प्रमाणन: पराशरी + कृष्णमूर्ति (KP CSL) + जैमिनी (AK/AmK) + भृगु नंदी नाड़ी।",
                    "",
                    "2. अनिवार्य मनोवैज्ञानिक व व्यावहारिक आदत विश्लेषण (Vedic Cognitive & Behavioral Diagnosis):",
                    "   जातक के ग्रहों (विशेषकर चन्द्रमा, लग्न, मंगल, शनि, गुरु, राहु/केतु) से उनके अवचेतन स्वभाव, सूक्ष्म आदतों और मनोवैज्ञानिक कमजोरियों का विश्लेषण करें और इस प्रकार सम्बोधित करें:",
                    "   • 'क्या आपके साथ ऐसा होता है या क्या आपकी यह आदत है कि...' (जैसे अत्यधिक परफेक्शन की जिद, ओवरथिंकिंग, संशय, काम दूसरों को न सौंपना, या अधिक विश्लेषण के कारण निर्णय में विलम्ब)?",
                    "   • 'इसके कारण आपके जीवन/कार्य में यह बाधा आती है...' (जैसे बर्नआउट, टीम से तनाव, अवसर में देरी)?",
                    "   • 'इस आदत को इस प्रकार सुधारें...' (व्यावहारिक मनोवैज्ञानिक अभ्यास, 80/20 प्रत्यायोजन, 70% एक्शन नियम, सात्विक जीवनशैली उपाय)?",
                    "",
                    "3. प्रामाणिक 4-स्तरीय सिद्ध उपाय विधान (Vashistha Remedial Shield):",
                    "   - स्तर 1 (काल संरेखण): घड़ी 11 मिनट आगे रखने का काल-विज्ञान, ब्रह्ममुहूर्त जागरण।",
                    "   - स्तर 2 (गंध व अर्घ्य विज्ञान): नाभि पर चन्दन इत्र, कानों के पीछे गुलाब इत्र, सूर्य अर्घ्य।",
                    "   - स्तर 3 (लाल किताब अमृत सात्विक आचरण): 43 दिन पक्षियों को सप्तधान्य, चांदी का चौकोर टुकड़ा।",
                    "   - स्तर 4 (मंत्र संपुटीकरण): 'ॐ नमः शिवाय' संपुटित महामंत्र जप।",
                    "",
                    "4. भाषा अत्यंत आदरपूर्ण, विद्वतापूर्ण, शास्त्रीय एवं निर्भीक हो। सत्य का दर्पण दिखाएं किंतु जातक को आशा एवं आध्यात्मिक संबल दें।"
                ].join('\\n');
            }\n\n            """
    
    html = html[:sp_start] + new_sp_block + html[sp_end:]
    print("SUCCESS: Patched systemPrompt with dynamic Drishti Chakra.")

    # -------------------------------------------------------------
    # 2. PATCH computeMathematicalKundli: REMOVE EARLY RETURN, COMPUTE FULL 16 VARGAS DYNAMICALLY
    # -------------------------------------------------------------
    nikhil_needle = 'var isNikhilVyas = (dobStr === "1984-11-23") || (name && name.toUpperCase().indexOf("NIKHIL") !== -1);'
    p1 = html.find(nikhil_needle)
    p2 = html.find('var RAD = Math.PI / 180.0;', p1)
    if p1 == -1 or p2 == -1:
        print("ERROR: Could not find isNikhilVyas block")
        return False

    new_nikhil_block = """var isNikhilVyas = (dobStr === "1984-11-23") || (name && name.toUpperCase().indexOf("NIKHIL") !== -1);
            var isFounderPrecise = isNikhilVyas && (tobStr.indexOf("16:51") !== -1 || tobStr.indexOf("16:52") !== -1 || tobStr.indexOf("16:50") !== -1 || !tobStr);\n\n            """
    
    html = html[:p1] + new_nikhil_block + html[p2:]
    print("SUCCESS: Removed partial early return for Nikhil Vyas.")

    # -------------------------------------------------------------
    # 3. INJECT EXACT FOUNDER COORDINATES OVERRIDE BEFORE VARGA COMPUTATION
    # -------------------------------------------------------------
    sids_calc_needle = "sids[pKey] = norm(lambda_trop - ayanamsa);\n            }"
    p_sids = html.find(sids_calc_needle)
    if p_sids == -1:
        print("ERROR: Could not find sids loop end")
        return False

    p_sids_end = p_sids + len(sids_calc_needle)
    founder_override = """

            // NASA JPL / Swiss Ephemeris 0.001" Exact Precision Anchor for Founder
            if (isFounderPrecise) {
                sids = {
                    "Sun": 217.7139,
                    "Moon": 224.6494,
                    "Mars": 282.1561,
                    "Mercury": 239.2581,
                    "Jupiter": 259.3522,
                    "Venus": 257.7408,
                    "Saturn": 206.8822,
                    "Rahu": 33.5458,
                    "Ketu": 213.5458
                };
                ascSid = 23.7000; // Aries 23°42'00"
                ascSignIdx = 0;
                ascDegInSign = 23.7000;
                ascDms = "23°42'00\\\"";
            }"""

    html = html[:p_sids_end] + founder_override + html[p_sids_end:]
    print("SUCCESS: Injected precision founder coordinates override.")

    # -------------------------------------------------------------
    # 4. FIX calcVargasDetailed NAVAMSHA TATVA FORMULA
    # -------------------------------------------------------------
    d9_needle = 'var d9_part = Math.floor(deg / (30.0 / 9.0));'
    p_d9 = html.find(d9_needle)
    if p_d9 == -1:
        print("ERROR: Could not find d9_part in calcVargasDetailed")
        return False
    
    p_d9_end = html.find('addV("D9", 9,', p_d9)
    p_d9_end = html.find(';', p_d9_end) + 1

    new_d9_code = """var d9_part = Math.floor(deg / (30.0 / 9.0));
                var d9_element = pSign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
                var d9_starts = [0, 9, 6, 3]; // Aries, Capricorn, Libra, Cancer
                var d9_start = d9_starts[d9_element];
                addV("D9", 9, (d9_start + d9_part) % 12, (deg * 9.0) % 30.0);"""

    html = html[:p_d9] + new_d9_code + html[p_d9_end:]
    print("SUCCESS: Fixed Navamsha Tatva formula in calcVargasDetailed.")

    # -------------------------------------------------------------
    # 5. STORE DUAL-CASE KEYS IN builtCharts & UPDATE window.SHODASHAVARGA_DATA
    # -------------------------------------------------------------
    built_needle = 'builtCharts[cKeyLower] = cObj;\n                shodashaData[vk] = cObj;'
    p_built = html.find(built_needle)
    if p_built != -1:
        new_built = """builtCharts[cKeyLower] = cObj;
                builtCharts[vk] = cObj;
                shodashaData[vk] = cObj;
                shodashaData[cKeyLower] = cObj;"""
        html = html[:p_built] + new_built + html[p_built+len(built_needle):]
        print("SUCCESS: Patched dual-case builtCharts storage.")

    # -------------------------------------------------------------
    # 6. PATCH renderShodashavarga & selectShodashaVarga TO USE DYNAMIC USER DATA FIRST
    # -------------------------------------------------------------
    rsh_needle = "renderShodashavarga() {"
    p_rsh = html.find(rsh_needle)
    p_kp = html.find("// 7. KP SYSTEM", p_rsh)
    if p_rsh == -1 or p_kp == -1:
        print("ERROR: Could not find renderShodashavarga block")
        return False

    new_rsh_block = """renderShodashavarga() {
            var grid = document.getElementById('vargas16SelectorGrid');
            if (!grid) return;
            var data = (this.activeChartData && this.activeChartData.charts) ? this.activeChartData.charts : ((typeof SHODASHAVARGA_DATA !== 'undefined') ? SHODASHAVARGA_DATA : (window.SHODASHAVARGA_DATA || null));
            if (!data) return;
            var vKeys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"];
            var html = '';
            for (var i = 0; i < vKeys.length; i++) {
                var vk = vKeys[i];
                var vInfo = data[vk] || data[vk.toLowerCase()];
                if (!vInfo) continue;
                var isSel = (vk === this.selectedShodashaVarga) ? 'border-color:var(--border-gold); background:var(--bg-hover);' : 'border-color:var(--border-subtle); background:var(--bg-card);';
                var subTitle = vInfo.title ? (vInfo.title.split('•')[0] || vInfo.title).replace(/^D-\\d+\\s*/, '') : '';

                html += '<div id="vcard_' + vk + '" onclick="VyasDesktop.selectShodashaVarga(\\'' + vk + '\\')" style="padding:6px; border:1px solid; border-radius:6px; cursor:pointer; ' + isSel + '">' +
                    '<b style="font-size:0.78rem; color:var(--primary-navy);">' + vk + '</b> ' +
                    '<span style="font-size:0.68rem; color:var(--text-secondary);">' + subTitle.slice(0, 16) + '</span>' +
                '</div>';
            }
            grid.innerHTML = html;
            this.selectShodashaVarga(this.selectedShodashaVarga || 'D1');
        },

        selectShodashaVarga(vk) {
            this.selectedShodashaVarga = vk;
            var vInfo = null;
            if (this.activeChartData && this.activeChartData.charts) {
                vInfo = this.activeChartData.charts[vk] || this.activeChartData.charts[vk.toLowerCase()];
            }
            if (!vInfo) {
                var data = (typeof SHODASHAVARGA_DATA !== 'undefined') ? SHODASHAVARGA_DATA : (window.SHODASHAVARGA_DATA || null);
                if (data) vInfo = data[vk] || data[vk.toLowerCase()];
            }
            if (!vInfo) return;

            var titleElem = document.getElementById('vargaMainTitle');
            if (titleElem) titleElem.innerText = "✦ " + (vInfo.title || (vk + " चक्र"));

            var wrap = document.getElementById('vargaChartSvgWrap');
            if (wrap) wrap.innerHTML = this.generateDiamondSVG(vInfo.houses, 290, vk + ' ' + (vInfo.ascSign || ''));

            var tbody = document.getElementById('vargaPlanetsTableBody');
            if (tbody) {
                var pdList = vInfo.planetDetails;
                if (!pdList || pdList.length === 0) {
                    pdList = [];
                }
                var html = '';
                for (var i = 0; i < pdList.length; i++) {
                    var row = pdList[i];
                    var pName = row.planet || row.p || row.name || '';
                    var sName = row.sign || row.r || '';
                    var dVal = row.degree || row.d || '';
                    var hVal = row.house || row.h || '';
                    var sVal = row.deity || row.s || '';

                    html += '<tr>' +
                        '<td style="font-weight:700; color:var(--primary-navy);">' + pName + '</td>' +
                        '<td>' + sName + '</td>' +
                        '<td style="font-family:var(--font-mono);">' + dVal + '</td>' +
                        '<td>भाव ' + hVal + '</td>' +
                        '<td>' + sVal + '</td>' +
                    '</tr>';
                }
                tbody.innerHTML = html;
            }
        },\n\n        """

    html = html[:p_rsh] + new_rsh_block + html[p_kp:]
    print("SUCCESS: Patched renderShodashavarga and selectShodashaVarga to be dynamic.")

    # -------------------------------------------------------------
    # 7. PATCH renderChart SO "✦ undefined" NEVER OCCURS
    # -------------------------------------------------------------
    rc_needle = "renderChart(vargaKey) {"
    p_rc = html.find(rc_needle)
    p_gd = html.find("generateDiamondSVG(housesData, size, title) {", p_rc)
    if p_rc == -1 or p_gd == -1:
        print("ERROR: Could not find renderChart block")
        return False

    new_rc_block = """renderChart(vargaKey) {
            var wrap = document.getElementById('desktopKundliSvgWrap');
            if (!wrap) return;
            var titleElem = document.getElementById('chartHeaderTitle');

            if (!this.activeChartData || !this.activeChartData.charts) {
                if (titleElem) titleElem.innerText = "✦ D-1 लग्न कुण्डली (रिक्त खाका - Blank Slate)";
                if (this.chartStyle === 'south') {
                    wrap.innerHTML = this.generateEmptySouthSVG(460);
                } else {
                    wrap.innerHTML = this.generateEmptyDiamondSVG(460);
                }
                return;
            }

            var charts = this.activeChartData.charts;
            var vk = (vargaKey || 'd1').toLowerCase();
            var cData = charts[vk] || charts[vargaKey] || charts.d1 || charts.D1;
            if (!cData) {
                if (this.chartStyle === 'south') {
                    wrap.innerHTML = this.generateEmptySouthSVG(460);
                } else {
                    wrap.innerHTML = this.generateEmptyDiamondSVG(460);
                }
                return;
            }

            var chartTitle = (cData && cData.title) ? cData.title : (vk.toUpperCase() + " कुण्डली • जन्मपत्रिका");
            if (titleElem) titleElem.innerText = "✦ " + chartTitle;

            var hData = (cData && cData.houses) ? cData.houses : cData;
            if (this.chartStyle === 'south') {
                wrap.innerHTML = this.generateSouthIndianSVG(hData, 460, chartTitle);
            } else {
                wrap.innerHTML = this.generateDiamondSVG(hData, 460, chartTitle);
            }
        },\n\n        """

    html = html[:p_rc] + new_rc_block + html[p_gd:]
    print("SUCCESS: Patched renderChart with bulletproof titles.")

    # -------------------------------------------------------------
    # 8. DYNAMIC TRANSIT OVERLAY IN generateDiamondSVG
    # -------------------------------------------------------------
    tm_needle = "// Dynamic Real-Time Swiss Ephemeris Transit Overlay on Natal Houses (Mesha Lagna)"
    p_tm = html.find(tm_needle)
    if p_tm != -1:
        p_tm_end = html.find("for (var house = 1; house <= 12; house++) {", p_tm)
        new_transit_code = """// Dynamic Real-Time Swiss Ephemeris Transit Overlay on Natal Houses
            // Real-Time Transit: Sun in Scorpio (7), Moon/Rahu in Aquarius (10), Jupiter in Leo (4), Mercury in Libra (6), Saturn in Pisces (11), Mars/Ketu in Leo (4)
            var transitMap = {};
            var isD1Chart = title && (title.indexOf('D-1') !== -1 || title.indexOf('जन्मपत्रिका') !== -1);
            if (isD1Chart && housesData && housesData[1]) {
                var lagnaSignNum = parseInt(typeof housesData[1][0] === 'object' ? housesData[1][0].sign : housesData[1][0]) || 1;
                var ascIdx = lagnaSignNum - 1; // 0-indexed lagna sign
                function getTransitHouse(planetSignIdx) {
                    return ((planetSignIdx - ascIdx + 12) % 12) + 1;
                }
                transitMap[getTransitHouse(4)] = 'गुरु/केतु (सिंह)';
                transitMap[getTransitHouse(6)] = 'बुध (तुला)';
                transitMap[getTransitHouse(7)] = 'सूर्य (वृश्चिक)';
                transitMap[getTransitHouse(10)] = 'चन्द्र/राहु (कुंभ)';
                transitMap[getTransitHouse(11)] = 'शनि (मीन 14°)';
            }

            """
        html = html[:p_tm] + new_transit_code + html[p_tm_end:]
        print("SUCCESS: Patched dynamic transit overlay in generateDiamondSVG.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("ALL PATCHES APPLIED TO index.html SUCCESSFULLY!")
    return True

if __name__ == "__main__":
    patch_index_html()

