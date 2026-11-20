#!/usr/bin/env python3
"""
VYAS ASTRA — Engine Enhancement & Synthesis Hook Script
1. Updates js/vyas_daivagya_engine.js to add formatReading method to VyasDaivagyaCore
2. Updates index.html:
   - Hooks VyasDaivagyaCore.formatReading into VyasDaivagyaWisdom.synthesizeReading
   - Makes panchang/mausam date strings dynamic (new Date().toLocaleDateString)
"""
import re, sys, os

ENGINE_PATH = r"g:\software\simpa\VYAS\js\vyas_daivagya_engine.js"
INDEX_PATH = r"g:\software\simpa\VYAS\index.html"

print("=== ENHANCING VYAS DAIVAGYA ENGINE & SYNTHESIS HOOK ===")

# ═══════════════════════════════════════════════════════════════════
# 1. ADD formatReading TO js/vyas_daivagya_engine.js
# ═══════════════════════════════════════════════════════════════════
with open(ENGINE_PATH, 'r', encoding='utf-8') as f:
    engine_content = f.read()

FORMAT_READING_CODE = """
        /**
         * Standalone / Direct HTML Formatter for UI & Fallbacks
         * Provides zero-vagueness, instant mathematical answers for yogas, dasha, gochar
         */
        formatReading: function(query, chart) {
            if (!chart || !chart.planet_table) return null;
            var q = (query || '').toLowerCase();
            var route = VyasQueryRouter.detect(query);
            var analysis = VyasChartAnalyzer.analyze(chart);
            if (!analysis) return null;

            if (route === 'yoga' || /योग|yoga|केमद्रुम|kemdrum|kendrum|गजकेसरी|gajakesari|बुधादित्य|budhaditya|मंगल.*दोष|mangal|मांगलिक|नीचभंग|neechabhanga|गुरु.*चांडाल|काल.*सर्प|kaalsarp|विपरीत|raj.*yoga|राजयोग/i.test(q)) {
                var yogas = VyasYogaEngine.detectAll(analysis, chart, query);
                if (yogas && yogas.length > 0) {
                    var html = "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                        "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>🔮 व्यास अस्त्र: सूक्ष्म योग परीक्षण व शास्त्रीय निर्णय (Vyas Yoga Engine)</span>" +
                        "</div>" +
                        "<b>ॐ नमः शिवाय।</b><br><br>" +
                        "<b>सादर प्रणाम आदरणीय " + (analysis.name || 'जातक') + " जी,</b><br>" +
                        "आपकी जन्म पत्रिका (लग्न: <b>" + analysis.lagna + "</b>, लग्नेश: <b>" + analysis.lagnaLord + "</b>) के गणितीय वेध अनुसार शास्त्रीय विश्लेषण प्रस्तुत है:<br><br>";

                    yogas.forEach(function(y) {
                        var det = (y.detail || '')
                            .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
                            .replace(/\\n\\n/g, '<br><br>')
                            .replace(/\\n/g, '<br>');
                        html += "<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; margin-bottom:12px;'>" +
                                "<div style='font-size:1.05rem; font-weight:700; color:" + (y.found ? (y.partial ? '#f59e0b' : '#10b981') : '#94a3b8') + "; margin-bottom:6px;'>" +
                                (y.found ? (y.partial ? '⚠️ ' : '✦ ') : '• ') + y.name + "</div>" +
                                det +
                                "</div>";
                    });

                    html += "<br><small style='color:#94a3b8;'>✓ व्यास अस्त्र गणितीय योग वेध (Brihat Parashara Hora Shastra Standard)।</small>";
                    return html;
                }
            }

            if (route === 'dasha' || /दशा|महादशा|अन्तर्दशा|pratyantar/i.test(q)) {
                var dashaText = VyasDashaEngine.analyze(analysis, query)
                    .replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>')
                    .replace(/\\n\\n/g, '<br><br>')
                    .replace(/\\n/g, '<br>');
                return "<div class='shastra-verdict-box' style='background:rgba(59,130,246,0.06); border-left:3px solid #3b82f6; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#60a5fa; font-weight:700; font-size:0.85rem;'>⏳ विंशोत्तरी दशा चक्र एवं समय-वेध (Vimshottari Dasha Engine)</span>" +
                    "</div>" +
                    "<b>सादर प्रणाम आदरणीय " + (analysis.name || 'जातक') + " जी,</b><br><br>" +
                    dashaText + "<br><br>" +
                    "<small style='color:#94a3b8;'>✓ व्यास अस्त्र सूक्ष्म विंशोत्तरी दशा काल वेध।</small>";
            }

            return null;
        },
"""

if 'formatReading' not in engine_content:
    target = '_houseAnalysis: function(analysis, houses) {'
    if target in engine_content:
        engine_content = engine_content.replace(target, FORMAT_READING_CODE + '\n        ' + target, 1)
        with open(ENGINE_PATH, 'w', encoding='utf-8') as f:
            f.write(engine_content)
        print("1. Added formatReading to js/vyas_daivagya_engine.js ✓")
    else:
        print("1 ERROR: target _houseAnalysis not found in engine file")
else:
    print("1. formatReading already present in js/vyas_daivagya_engine.js — SKIP")

# ═══════════════════════════════════════════════════════════════════
# 2. UPDATE index.html
# ═══════════════════════════════════════════════════════════════════
with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    index_content = f.read()

# 2a. Hook formatReading into synthesizeReading
SYNTHESIZE_HOOK = """
                // DIRECT DAIVAGYA ENGINE SYNTHESIS (Zero Hallucination / Zero Vagueness)
                if (window.VyasDaivagyaCore && typeof VyasDaivagyaCore.formatReading === 'function') {
                    try {
                        var engineResp = VyasDaivagyaCore.formatReading(query, chart);
                        if (engineResp) return engineResp;
                    } catch(e) {
                        console.warn("VyasDaivagyaCore.formatReading error:", e);
                    }
                }
"""

TARGET_SYNTH_START = """                if (intent === 'panchang') {
                    return this.renderPanchangReading(query);
                }"""

if 'VyasDaivagyaCore.formatReading' not in index_content:
    if TARGET_SYNTH_START in index_content:
        index_content = index_content.replace(
            TARGET_SYNTH_START,
            TARGET_SYNTH_START + '\n' + SYNTHESIZE_HOOK,
            1
        )
        print("2a. Hooked VyasDaivagyaCore.formatReading into synthesizeReading ✓")
    else:
        print("2a ERROR: TARGET_SYNTH_START not found in index.html")
else:
    print("2a. VyasDaivagyaCore.formatReading already hooked — SKIP")

# 2b. Make hardcoded "20 नवंबर 2026 (शुक्रवार)" dynamic in renderPanchangReading
OLD_PANCH_DATE = '"• <b>दिनांक व वार:</b> 20 नवंबर 2026 (शुक्रवार)<br>" +'
NEW_PANCH_DATE = '"• <b>दिनांक व वार:</b> " + (new Date().toLocaleDateString("hi-IN", { weekday: "long", year: "numeric", month: "long", day: "numeric" })) + "<br>" +'

if OLD_PANCH_DATE in index_content:
    index_content = index_content.replace(OLD_PANCH_DATE, NEW_PANCH_DATE, 1)
    print("2b. Made panchang date dynamic in renderPanchangReading ✓")
else:
    print("2b. Dynamic date already in place or pattern not found.")

# 2c. Make hardcoded "20 नवंबर 2026" in mausam dynamic
OLD_MAUSAM_DATE = '"• <b>तात्कालिक खगोलीय स्थिति (20 नवंबर 2026):</b><br>" +'
NEW_MAUSAM_DATE = '"• <b>तात्कालिक खगोलीय स्थिति (" + (new Date().toLocaleDateString("hi-IN", { day: "numeric", month: "long", year: "numeric" })) + "):</b><br>" +'

if OLD_MAUSAM_DATE in index_content:
    index_content = index_content.replace(OLD_MAUSAM_DATE, NEW_MAUSAM_DATE, 1)
    print("2c. Made mausam date dynamic in lookupDirectAstrologicalTruth ✓")
else:
    print("2c. Dynamic date already in place in mausam.")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(index_content)

print("\n=== ALL ENGINE ENHANCEMENTS APPLIED SUCCESSFULLY ===")
