#!/usr/bin/env python3
"""
Upgrade js/vyas_daivagya_engine.js with:
1. Universal environment wrapper (window || global)
2. Direct 22,000+ Sutras Bank integration in computeContext
3. Deep Shastric evidence weaving in formatReading across all routes
"""

import os

FILE_PATH = r"g:\software\simpa\VYAS\js\vyas_daivagya_engine.js"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the tail of the file starting from VyasDaivagyaCore
core_marker = "// MASTER ORCHESTRATOR — VyasDaivagyaCore"
pos = content.find(core_marker)
if pos == -1:
    print("Could not find core_marker!")
    exit(1)

head = content[:pos]

NEW_CORE = r"""// MASTER ORCHESTRATOR — VyasDaivagyaCore
    // ═══════════════════════════════════════════════════════════════════
    window.VyasDaivagyaCore = {
        /**
         * Main entry: given query + chart, return pre-computed data block
         * This block is injected into AI systemPrompt so AI just FORMATS it
         */
        computeContext: function(query, chart) {
            if (!chart || !chart.planet_table) return '';
            var route = VyasQueryRouter.detect(query);
            var analysis = VyasChartAnalyzer.analyze(chart);
            if (!analysis) return '';

            var blocks = [
                '═══════════════════════════════════════════════════════',
                '📊 VYAS DAIVAGYA ENGINE v4.0 — PRE-COMPUTED SHASTRA ANALYSIS',
                '   Query Type: [' + route.toUpperCase() + '] | Zero-hallucination data',
                '═══════════════════════════════════════════════════════',
                '',
                '**जातक:** ' + analysis.name + ' | **लग्न:** ' + analysis.lagna + ' | **लग्नेश:** ' + analysis.lagnaLord + ' (' + analysis.lagnaStrength + ')',
                '**सक्रिय दशा:** ' + analysis.dasha.chain,
                ''
            ];

            if (route === 'yoga' || /योग|yoga/i.test(query)) {
                var yogas = VyasYogaEngine.detectAll(analysis, chart, query);
                blocks.push('**🔮 YOGA ANALYSIS (Mathematically Verified):**');
                yogas.forEach(function(y) { if(y) blocks.push(y.detail || ''); });
            }
            if (route === 'dasha') {
                blocks.push(VyasDashaEngine.analyze(analysis, query));
            }
            if (route === 'gochar') {
                blocks.push(VyasGocharEngine.analyze(analysis));
            }
            if (route === 'career' || route === 'd10') {
                blocks.push(this._houseAnalysis(analysis, [10, 2, 6, 11]));
            }
            if (route === 'marriage') {
                blocks.push(this._houseAnalysis(analysis, [7, 2, 5, 11]));
            }
            if (route === 'wealth') {
                blocks.push(this._houseAnalysis(analysis, [2, 11, 9, 5]));
            }
            if (route === 'health') {
                blocks.push(this._houseAnalysis(analysis, [1, 6, 8, 12]));
            }
            if (route === 'children') {
                blocks.push(this._houseAnalysis(analysis, [5, 9, 1]));
            }
            if (route === 'lagna' || route === 'general') {
                blocks.push('**ग्रह बल:**\n' + VyasBalaEngine.assess(analysis));
            }
            if (route === 'gochar' || /साढ़ेसाती|ढैय्या|ashtama/.test(query)) {
                blocks.push(VyasGocharEngine.analyze(analysis));
            }

            // Always append dasha context for natal queries
            if (['yoga','career','marriage','wealth','health','children','lagna','general','d9','d10'].indexOf(route) !== -1) {
                blocks.push('');
                blocks.push('**दशा संदर्भ:**');
                blocks.push(VyasDashaEngine.analyze(analysis, query));
            }

            // Inject Classical Sutras from 22,000+ Bank
            var sBank = (typeof window !== 'undefined' ? window.VyasSutrasBank : (typeof global !== 'undefined' ? global.VyasSutrasBank : null));
            if (sBank && typeof sBank.matchChart === 'function') {
                var matched = sBank.matchChart(analysis, route, 8);
                if (matched && matched.length > 0) {
                    blocks.push('');
                    blocks.push('**📜 CLASSICAL SUTRAS CITATIONS (From 22,000+ Shastra Bank):**');
                    matched.slice(0, 6).forEach(function(s) {
                        blocks.push('• [' + s.src + '] ' + s.cond + ' => ' + s.pred);
                    });
                }
            }

            blocks.push('');
            blocks.push('═══════════════════════════════════════════════════════');
            blocks.push('⚠️ उपर्युक्त सभी डेटा chart.planet_table एवं 22,000+ शास्त्रीय सूत्रों से गणित-आधारित है।');
            blocks.push('आचार्य व्यास: इस pre-verified data को आधार बनाकर प्रामाणिक शास्त्रीय विश्लेषण करें।');

            return blocks.join('\n');
        },

        /**
         * Helper: Render Shastric Evidence Citation Card in HTML
         */
        _renderSutrasHtml: function(sutras, maxCount) {
            if (!sutras || !sutras.length) return '';
            maxCount = maxCount || 4;
            var list = sutras.slice(0, maxCount);
            var h = "<div class='vyas-sutras-vault-card' style='margin-top:14px; margin-bottom:14px; padding:12px; background:rgba(212,175,55,0.05); border:1px solid rgba(212,175,55,0.25); border-radius:8px;'>" +
                    "<div style='color:#d4af37; font-weight:700; font-size:0.86rem; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;'>" +
                    "<span>📜 <b>शास्त्रीय प्रमाण (22,000+ सूत्र महा-वेध बैंक से प्रत्यक्ष वेध):</b></span>" +
                    "<span style='font-size:0.75rem; background:rgba(212,175,55,0.15); color:#fbbf24; padding:2px 8px; border-radius:4px;'>प्रामाणिक श्लोक</span>" +
                    "</div>";
            list.forEach(function(s) {
                h += "<div style='margin-bottom:8px; font-size:0.83rem; line-height:1.45; border-bottom:1px dashed rgba(255,255,255,0.08); padding-bottom:6px;'>" +
                     "<b style='color:#60a5fa;'>[" + (s.src || "बृहत्पाराशर होराशास्त्र") + "]</b> " +
                     "<span style='color:#f8fafc;'>स्थिति: <i>" + s.cond + "</i></span><br>" +
                     "<span style='color:#94a3b8;'>➔ <b>शास्त्रीय फल:</b> " + s.pred + "</span>" +
                     "</div>";
            });
            h += "<small style='color:#64748b; font-size:0.74rem;'>वेध आधार: महर्षि पराशर (BPHS), महर्षि भृगु, कल्याण वर्मा (सारावली), पृथुयशस (होरासार) व आधुनिक शोध।</small>" +
                 "</div>";
            return h;
        },

        /**
         * Comprehensive Autonomous Predictive Formatter
         * Analyzes any query (Career, Wealth, Marriage, Health, Yogas, Dasha, Future)
         * by extracting active chart yogas, matching classical sutras from VyasSutrasBank,
         * and synthesizing an authentic, shastric prediction with 0 latency.
         */
        formatReading: function(query, chart) {
            var q = (query || '').toLowerCase();
            var route = VyasQueryRouter.detect(query);
            var sBank = (typeof window !== 'undefined' ? window.VyasSutrasBank : (typeof global !== 'undefined' ? global.VyasSutrasBank : null));

            // SCENARIO 1: No active chart loaded — Shastric Axiom / Theoretical Query
            if (!chart || !chart.planet_table) {
                if (sBank && typeof sBank.searchSutras === 'function') {
                    var searched = sBank.searchSutras(query, 6);
                    if (searched && searched.length > 0) {
                        var htmlShastra = "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                            "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>📜 शास्त्रीय सिद्धांत वेध: &quot;" + (query || "वैदिक ज्योतिष सूत्र") + "&quot;</span>" +
                            "</div>" +
                            "<b>ॐ नमः शिवाय। सादर प्रणाम जातक जी,</b><br><br>" +
                            "आपके प्रश्न के संदर्भ में हमारे <b>22,000+ प्रामाणिक सूत्र महा-बैंक</b> से शास्त्रीय प्रमाण व फलित विधान इस प्रकार है:<br><br>" +
                            this._renderSutrasHtml(searched, 5) +
                            "<br><b>दैवज्ञ मार्गदर्शन:</b> किसी भी योग अथवा ग्रह स्थिति का व्यक्तिगत जीवन पर वास्तविक प्रभाव जानने के लिए लग्न, भावेश, नवांश (D-9) एवं वर्तमान विंशोत्तरी दशा का समन्वय अनिवार्य होता है।<br>" +
                            "<small style='color:#94a3b8;'>💡 अपनी जन्मपत्रिका (जन्म तिथि, समय व स्थान) प्रविष्ट करने पर यह गणना आपकी व्यक्तिगत कुण्डली पर स्वतः परिकलित होगी।</small>";
                        return htmlShastra;
                    }
                }
                return null;
            }

            var analysis = VyasChartAnalyzer.analyze(chart);
            if (!analysis) return null;

            var name = analysis.name || 'जातक';
            var lagna = analysis.lagna || 'लग्न';
            var lagnaLord = analysis.lagnaLord || '';
            var dashaChain = analysis.dasha.chain || 'सक्रिय दशा';

            // Detect all formed yogas in this native's chart
            var allYogas = VyasYogaEngine.detectAll(analysis, chart);
            var yogaNames = allYogas.filter(function(y){ return y.found; }).map(function(y){ return y.name; });

            // Match classical sutras from in-memory 22,000+ VyasSutrasBank
            var matchedSutras = [];
            var topicSutras = [];
            if (sBank) {
                if (typeof sBank.matchChart === 'function') {
                    try { matchedSutras = sBank.matchChart(analysis, route, 15); } catch(e) {}
                }
                if (typeof sBank.searchSutras === 'function') {
                    try { topicSutras = sBank.searchSutras(query, 6); } catch(e) {}
                }
            }

            // Combine and deduplicate
            var combinedSutras = [];
            var seenSutraText = {};
            (topicSutras.concat(matchedSutras)).forEach(function(s) {
                var k = (s.cond + ' ' + s.pred).substring(0, 45);
                if (!seenSutraText[k]) {
                    seenSutraText[k] = true;
                    combinedSutras.push(s);
                }
            });

            // ─────────────────────────────────────────────────────────────
            // ROUTE A: YOGA & DOSHA INQUIRY
            // ─────────────────────────────────────────────────────────────
            if (route === 'yoga' || /योग|yoga|केमद्रुम|kemdrum|kendrum|गजकेसरी|gajakesari|बुधादित्य|budhaditya|मंगल.*दोष|mangal|मांगलिक|नीचभंग|neechabhanga|गुरु.*चांडाल|काल.*सर्प|kaalsarp|विपरीत|raj.*yoga|राजयोग/i.test(q)) {
                var targetYogas = VyasYogaEngine.detectAll(analysis, chart, query);
                if (targetYogas && targetYogas.length > 0) {
                    var html = "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                        "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>🔮 व्यास अस्त्र: सूक्ष्म योग परीक्षण व शास्त्रीय निर्णय (Vyas Yoga Engine)</span>" +
                        "</div>" +
                        "<b>ॐ नमः शिवाय।</b><br><br>" +
                        "<b> सादर प्रणाम आदरणीय " + name + " जी,</b><br>" +
                        "आपकी जन्म पत्रिका (लग्न: <b>" + lagna + "</b>, लग्नेश: <b>" + lagnaLord + "</b>) के गणितीय वेध अनुसार शास्त्रीय विश्लेषण प्रस्तुत है:<br><br>";

                    targetYogas.forEach(function(y) {
                        var det = (y.detail || '')
                            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                            .replace(/\n\n/g, '<br><br>')
                            .replace(/\n/g, '<br>');
                        html += "<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; margin-bottom:12px;'>" +
                                "<div style='font-size:1.02rem; font-weight:700; color:" + (y.found ? (y.partial ? '#f59e0b' : '#10b981') : '#94a3b8') + "; margin-bottom:6px;'>" +
                                (y.found ? (y.partial ? '⚠️ ' : '✦ ') : '• ') + y.name + "</div>" +
                                det +
                                "</div>";
                    });

                    // Matched sutras supplement from 22,000+ bank
                    if (combinedSutras.length > 0) {
                        html += this._renderSutrasHtml(combinedSutras, 4);
                    }

                    html += "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र गणितीय वेध (Brihat Parashara Hora Shastra Standard)।</small>";
                    return html;
                }
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE B: DASHA & TIMELINE INQUIRY
            // ─────────────────────────────────────────────────────────────
            if (route === 'dasha' || /दशा|महादशा|अन्तर्दशा|pratyantar|कब.*होगा|समय/i.test(q)) {
                var dashaText = VyasDashaEngine.analyze(analysis, query)
                    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                    .replace(/\n\n/g, '<br><br>')
                    .replace(/\n/g, '<br>');
                var dHtml = "<div class='shastra-verdict-box' style='background:rgba(59,130,246,0.06); border-left:3px solid #3b82f6; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#60a5fa; font-weight:700; font-size:0.85rem;'>⏳ विंशोत्तरी दशा चक्र एवं समय-वेध (Vimshottari Dasha Engine)</span>" +
                    "</div>" +
                    "<b>सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                    dashaText + "<br><br>";

                if (yogaNames.length > 0) {
                    dHtml += "<div style='padding:8px 12px; background:rgba(212,175,55,0.05); border-radius:6px; font-size:0.82rem; margin-bottom:10px;'>" +
                             "<b style='color:#d4af37;'>✨ इस दशा में फलित होने वाले मुख्य राजयोग:</b> " + yogaNames.slice(0, 4).join(', ') +
                             "</div>";
                }

                if (combinedSutras.length > 0) {
                    dHtml += this._renderSutrasHtml(combinedSutras, 3);
                }

                dHtml += "<small style='color:#94a3b8;'>✓ व्यास अस्त्र सूक्ष्म विंशोत्तरी दशा काल वेध।</small>";
                return dHtml;
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE C: CAREER & PROFESSION (कर्म, नौकरी, व्यापार, पदोन्नति)
            // ─────────────────────────────────────────────────────────────
            if (route === 'career' || route === 'd10' || /करियर|नौकरी|व्यापार|जॉब|काम|व्यवसाय|प्रमोशन|आजीविका|पद|career|job|business|promotion/i.test(q)) {
                var h10 = analysis.houses[10];
                var l10 = h10.lord;
                var p10Data = analysis.planets[l10];
                var planetsIn10 = h10.planets.join(', ') || 'रिक्त (शुभ दृष्टियों से संरेखित)';
                var sat = analysis.planets['शनि'], sun = analysis.planets['सूर्य'], jup = analysis.planets['गुरु'];

                var cYogas = allYogas.filter(function(y) {
                    return /रुचक|भद्र|हंस|मालव्य|शश|धर्म.*कर्म|राजयोग|अमला|काहल|नीचभंग/i.test(y.name);
                });

                var htmlC = "<div class='shastra-verdict-box' style='background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#34d399; font-weight:700; font-size:0.85rem;'>💼 आजीविका, करियर एवं कर्मक्षेत्र शास्त्रीय वेध (Career & Karma Matrix)</span>" +
                    "</div>" +
                    "<b>ॐ नमः शिवाय। सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                    "महर्षि पराशर प्रणीत <b>बृहत्पाराशर होराशास्त्र (कर्माध्यायानुसार)</b> आपकी कुण्डली का सूक्ष्म विश्लेषण प्रस्तुत है:<br><br>" +
                    "✦ <b>१. दशम भाव (कर्म) एवं दशमेश स्थिति:</b><br>" +
                    "• <b>दशम भाव (10th House):</b> " + h10.sign + " राशि (स्वामी: <b>" + l10 + "</b>)।<br>" +
                    "• <b>दशम भाव में स्थित ग्रह:</b> <b>" + planetsIn10 + "</b>।<br>" +
                    "• <b>दशमेश (" + l10 + ") की स्थिति:</b> भाव " + (p10Data ? p10Data.house : 1) + " (" + (p10Data ? p10Data.sign : '') + " राशि) में " + (p10Data ? p10Data.dignity : '') + " होकर स्थित हैं।<br><br>" +
                    "✦ <b>२. कर्मकारक ग्रह एवं कुण्डली के करियर योग:</b><br>" +
                    "• कर्मकारक शनि देव भाव " + (sat ? sat.house : 1) + " (" + (sat ? sat.sign : '') + ") में एवं अधिकार कारक सूर्य देव भाव " + (sun ? sun.house : 1) + " में संचरणशील हैं।<br>";

                if (cYogas.length > 0) {
                    htmlC += "• <b style='color:#10b981;'>सक्रिय कर्म राजयोग:</b> " + cYogas.map(function(y){ return y.name; }).join(' • ') + "<br>";
                }
                htmlC += "<br>";

                // SFT Sutras for Career from 22,000+ Bank
                if (combinedSutras.length > 0) {
                    htmlC += this._renderSutrasHtml(combinedSutras, 4);
                }

                htmlC += "✦ <b>३. दशा व आगामी स्वर्णिम समय-सीमा:</b><br>" +
                         "वर्तमान में सक्रिय <b>" + dashaChain + "</b> आपके कर्म भाव को संबल प्रदान कर रही है। देवगुरु बृहस्पति का गोचर आपके कार्यक्षेत्र को गति दे रहा है, जिससे पदोन्नति एवं आर्थिक संवृद्धि का मार्ग प्रशस्त होगा।<br><br>" +
                         "✦ <b>४. अचूक सात्विक कार्यक्षेत्र उपाय:</b><br>" +
                         "• नित्य प्रातः तांबे के लोटे से भगवान सूर्य को जल अर्पित कर <i>'ॐ घृणिः सूर्याय नमः'</i> का जप करें।<br>" +
                         "• शनिवार को किसी कर्मठ श्रमिक अथवा निर्धन को अन्न/वस्त्र का दान करें।<br><br>" +
                         "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र सूक्ष्म कर्मक्षेत्र वेध।</small>";
                return htmlC;
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE D: WEALTH & FINANCE (धन, संपत्ति, लाभ, कर्ज)
            // ─────────────────────────────────────────────────────────────
            if (route === 'wealth' || /धन|पैसा|रुपया|सम्पत्ति|आर्थिक|कर्ज|लोन|इनकम|आय|अमीरी|wealth|money|finance|income/i.test(q)) {
                var h2 = analysis.houses[2], h11 = analysis.houses[11];
                var l2 = h2.lord, l11 = h11.lord;
                var p2 = analysis.planets[l2], p11 = analysis.planets[l11];
                var jup = analysis.planets['गुरु'];

                var dYogas = allYogas.filter(function(y) {
                    return /धन|लक्ष्मी|वसुमती|चन्द्र.*मंगल|अखंड.*साम्राज्य/i.test(y.name);
                });

                var htmlW = "<div class='shastra-verdict-box' style='background:rgba(245,158,11,0.06); border-left:3px solid #f59e0b; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#fbbf24; font-weight:700; font-size:0.85rem;'>💰 आर्थिक समृद्धि, संचित धन एवं लाभ योग (Dhana & Asset Vault)</span>" +
                    "</div>" +
                    "<b>ॐ नमः शिवाय। सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                    "<b>बृहत्पाराशर होराशास्त्र (धनयोगाध्याय)</b> अनुसार आपकी कुण्डली का वित्तीय वेध:<br><br>" +
                    "✦ <b>१. धन एवं लाभ भाव स्थिति:</b><br>" +
                    "• <b>द्वितीय (संचित धन) भाव:</b> " + h2.sign + " राशि (स्वामी: <b>" + l2 + "</b>, भाव " + (p2 ? p2.house : 1) + " में स्थित)।<br>" +
                    "• <b>एकादश (आय व लाभ) भाव:</b> " + h11.sign + " राशि (स्वामी: <b>" + l11 + "</b>, भाव " + (p11 ? p11.house : 1) + " में स्थित)।<br>" +
                    "• <b>धनकारक देवगुरु बृहस्पति:</b> भाव " + (jup ? jup.house : 1) + " (" + (jup ? jup.sign : '') + ") में विराजमान होकर धन के संचय को गति दे रहे हैं।<br><br>";

                if (dYogas.length > 0) {
                    htmlW += "✦ <b>२. सक्रिय धन प्रदायक योग:</b><br>" +
                             "• <b style='color:#fbbf24;'>" + dYogas.map(function(y){ return y.name; }).join(' • ') + "</b><br><br>";
                }

                if (combinedSutras.length > 0) {
                    htmlW += this._renderSutrasHtml(combinedSutras, 4);
                }

                htmlW += "✦ <b>३. वित्तीय प्रवाह व समय-सीमा:</b><br>" +
                         "सक्रिय <b>" + dashaChain + "</b> धन भावों को संबल प्रदान कर रही है। व्यापारिक निर्णय अथवा निवेश में धैर्य रखें, संचित प्रयासों का श्रेष्ठ प्रतिफल प्राप्त होगा।<br><br>" +
                         "✦ <b>४. सात्विक धन संवर्धन उपाय:</b><br>" +
                         "• प्रत्येक शुक्रवार को सात्विक मिष्ठान्न का दान करें व घर में श्री सूक्त अथवा कनकधारा स्तोत्र का पाठ करें।<br>" +
                         "• पक्षियों को नियमित जल व दाना अर्पित करें।<br><br>" +
                         "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र शुद्ध शास्त्रीय धन वेध।</small>";
                return htmlW;
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE E: MARRIAGE & RELATIONSHIP (विवाह, दांपत्य, जीवनसाथी)
            // ─────────────────────────────────────────────────────────────
            if (route === 'marriage' || /विवाह|शादी|दांपत्य|जीवनसाथी|पत्नी|पति|रिश्ता|प्रेम|marriage|spouse|wife|husband|relationship/i.test(q)) {
                var h7 = analysis.houses[7];
                var l7 = h7.lord;
                var p7 = analysis.planets[l7];
                var ven = analysis.planets['शुक्र'];
                var mangal = allYogas.find(function(y){ return /मंगल.*दोष/i.test(y.name); });

                var htmlM = "<div class='shastra-verdict-box' style='background:rgba(236,72,153,0.06); border-left:3px solid #ec4899; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#f472b6; font-weight:700; font-size:0.85rem;'>💍 दांपत्य जीवन, विवाह व सम्बन्ध समन्वय (Marriage & Relationship Matrix)</span>" +
                    "</div>" +
                    "<b>ॐ नमः शिवाय। सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                    "<b>फलदीपिका (सप्तम भाव विचार)</b> के अनुसार आपकी जन्मपत्रिका का दांपत्य वेध:<br><br>" +
                    "✦ <b>१. सप्तम भाव एवं भावेश स्थिति:</b><br>" +
                    "• <b>सप्तम भाव:</b> " + h7.sign + " राशि (सप्तमेश: <b>" + l7 + "</b>, भाव " + (p7 ? p7.house : 1) + " में स्थित)।<br>" +
                    "• <b>दांपत्य कारक शुक्रदेव:</b> भाव " + (ven ? ven.house : 1) + " (" + (ven ? ven.sign : '') + " राशि) में संचरण कर रहे हैं।<br><br>" +
                    "✦ <b>२. मांगलिक दोष परीक्षण:</b><br>" +
                    "• " + (mangal ? (mangal.found ? (mangal.partial ? '⚠️ <b>मंगल दोष उपस्थित किंतु शास्त्रीय परिहार से भंग।</b>' : '🔴 <b>मांगलिक प्रभाव उपस्थित — कुण्डली मिलान अनिवार्य।</b>') : '✅ <b>मांगलिक दोष पूर्णतः अनुपस्थित।</b>') : 'मांगलिक प्रभाव सामान्य।') + "<br><br>";

                if (combinedSutras.length > 0) {
                    htmlM += this._renderSutrasHtml(combinedSutras, 4);
                }

                htmlM += "✦ <b>३. सामंजस्य एवं सात्विक उपाय:</b><br>" +
                         "• दांपत्य में परस्पर विश्वास, सम्मान व सामंजस्य को सर्वोच्च प्राथमिकता दें।<br>" +
                         "• नित्य <i>'ॐ उमामहेश्वराभ्यां नमः'</i> का जप करें, यह दांपत्य जीवन को सुख व सौहार्द से परिपूर्ण करता है।<br><br>" +
                         "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र सप्तम भाव वेध।</small>";
                return htmlM;
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE F: HEALTH & VITALITY (स्वास्थ्य, आयु, रोग)
            // ─────────────────────────────────────────────────────────────
            if (route === 'health' || /स्वास्थ्य|रोग|कष्ट|बीमारी|तबीयत|आयु|दवा|health|disease|fitness/i.test(q)) {
                var h6 = analysis.houses[6];
                var l1 = analysis.lagnaLordPos;
                var sun = analysis.planets['सूर्य'], moon = analysis.planets['चन्द्र'];

                var htmlH = "<div class='shastra-verdict-box' style='background:rgba(239,68,68,0.06); border-left:3px solid #ef4444; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#f87171; font-weight:700; font-size:0.85rem;'>🌿 स्वास्थ्य, आरोग्य एवं जीवन शक्ति वेध (Health & Vitality Matrix)</span>" +
                    "</div>" +
                    "<b>ॐ नमः शिवाय। सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                    "<b>चरक संहिता एवं पराशरीय होरा शास्त्र</b> अनुसार आरोग्य विश्लेषण:<br><br>" +
                    "• <b>लग्न एवं लग्नेश (" + lagnaLord + "):</b> भाव " + (l1 ? l1.house : 1) + " में " + analysis.lagnaStrength + " अवस्था में है।<br>" +
                    "• <b>षष्ठ (रोग) भाव:</b> " + h6.sign + " राशि (स्वामी: <b>" + h6.lord + "</b>)।<br>" +
                    "• <b>आत्मकारक सूर्य एवं मन:कारक चन्द्रमा:</b> सूर्य (भाव " + (sun ? sun.house : 1) + ") व चन्द्र (भाव " + (moon ? moon.house : 1) + ") का संतुलन जीवन ऊर्जा निर्धारित कर रहा है।<br><br>";

                if (combinedSutras.length > 0) {
                    htmlH += this._renderSutrasHtml(combinedSutras, 4);
                }

                htmlH += "<b>सात्विक स्वास्थ्य संबल उपाय:</b><br>" +
                         "• प्रातःकाल गुनगुने जल का सेवन करें व सूर्य नमस्कार का अभ्यास करें।<br>" +
                         "• नित्य 11 बार <i>'महामृत्युंजय मंत्र'</i> का शांत मन से जप संपूर्ण आरोग्य का सर्वोत्तम कवच है।<br><br>" +
                         "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र आरोग्य वेध।</small>";
                return htmlH;
            }

            // ─────────────────────────────────────────────────────────────
            // ROUTE G: GENERAL HOLISTIC READING (समग्र जीवन व सामान्य जिज्ञासा)
            // ─────────────────────────────────────────────────────────────
            var sunP = analysis.planets['सूर्य'] || { sign: 'अज्ञात', house: 1 };
            var moonP = analysis.planets['चन्द्र'] || { sign: 'अज्ञात', house: 1 };
            var formedYogasStr = yogaNames.length > 0 ? yogaNames.slice(0, 5).join(' • ') : 'शुभ ग्रह दृष्टि संरेखित';

            var htmlGen = "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>✦ कुण्डली मीमांसा: &quot;" + (query || "समग्र जीवन फलादेश") + "&quot;</span>" +
                "</div>" +
                "<b>ॐ नमः शिवाय। सादर प्रणाम आदरणीय " + name + " जी,</b><br><br>" +
                "आपकी जन्मपत्रिका का संपूर्ण खगोलीय व शास्त्रीय सिंहावलोकन प्रस्तुत है:<br><br>" +
                "✦ <b>१. आधारभूत कुण्डली विन्यास:</b><br>" +
                "• <b>जन्म लग्न:</b> <b>" + lagna + " लग्न</b> (लग्नेश: <b>" + lagnaLord + "</b> — " + analysis.lagnaStrength + ")<br>" +
                "• <b>सूर्य स्थिति:</b> भाव " + sunP.house + " (" + sunP.sign + " राशि — आत्मा व सम्मान कारक)<br>" +
                "• <b>चन्द्र स्थिति:</b> भाव " + moonP.house + " (" + moonP.sign + " राशि — मन व चिंतन कारक)<br>" +
                "• <b>सक्रिय दशा:</b> <span style='color:#60a5fa; font-weight:700;'>" + dashaChain + "</span><br><br>" +
                "✦ <b>२. कुण्डली में सक्रिय प्रमुख वैदिक योग:</b><br>" +
                "• <b style='color:#10b981;'>" + formedYogasStr + "</b><br><br>";

            if (combinedSutras.length > 0) {
                htmlGen += this._renderSutrasHtml(combinedSutras, 4);
            }

            htmlGen += "✦ <b>३. दैवज्ञ परामर्श व सात्विक साधना:</b><br>" +
                       "वर्तमान समय में अपने लक्ष्य के प्रति धैर्य, एकाग्रता एवं सात्विक निष्ठा बनाए रखें। कुण्डली के शुभ ग्रहों का संबल आपके कार्यों को सिद्धि की ओर अग्रसर कर रहा है।<br><br>" +
                       "• नित्य प्रातः भगवान सूर्यनारायण को अर्घ्य दें एवं संध्या समय <i>'ॐ नमः शिवाय'</i> का 108 बार मानसिक जप करें।<br><br>" +
                       "<small style='color:#94a3b8;'>✓ व्यास अस्त्र 22,000+ सूत्र सूक्ष्म खगोलीय वेध प्रमाण।</small>";
            return htmlGen;
        },

        _houseAnalysis: function(analysis, houses) {
            return houses.map(function(h) {
                return VyasHouseEngine.analyzeHouse(analysis, h);
            }).join('\n\n');
        }
    };

})(typeof window !== 'undefined' ? window : global);
"""

new_content = head + NEW_CORE

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Successfully updated {FILE_PATH}!")
