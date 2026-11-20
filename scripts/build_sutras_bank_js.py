#!/usr/bin/env python3
"""
VYAS ASTRA — Client-Side Sutras Bank Generator
Extracts data/vyas_sutras_fast_index.json into js/vyas_sutras_bank.js
"""
import os, sys, json

BASE_DIR = r"g:\software\simpa\VYAS"
INDEX_PATH = os.path.join(BASE_DIR, "data", "vyas_sutras_fast_index.json")
OUTPUT_JS = os.path.join(BASE_DIR, "js", "vyas_sutras_bank.js")

print("Reading sutras index...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    sutra_db = json.load(f)

bank = {
    "planet_signs": {},
    "planet_houses": {},
    "yutis": {},
    "dignities": {}
}

for cat in ["planet_signs", "planet_houses", "yutis", "dignities"]:
    sub = sutra_db.get(cat, {})
    for k, v in sub.items():
        bank[cat][k] = []
        for s in v[:2]:
            cond = s.get("cond_hi", "").replace(". (कुंडली में यह स्थिति होने पर)", "").strip()
            pred = s.get("pred_hi", "").strip()
            src = s.get("src", "बृहत्पाराशर होराशास्त्र")
            domain = s.get("domain", "सामान्य")
            if cond and pred:
                bank[cat][k].append({
                    "cond": cond,
                    "pred": pred,
                    "src": src,
                    "domain": domain
                })

bank_json = json.dumps(bank, ensure_ascii=False)

TEMPLATE = r"""// ═══════════════════════════════════════════════════════════════════
// VYAS ASTRA — IN-MEMORY CLASSICAL SUTRAS DATA BANK v3.0
// Pre-indexed Shastric knowledge vault for instant client-side lookup
// Covers 108 signs, 108 houses, 36 conjunctions, and all dignities
// ═══════════════════════════════════════════════════════════════════

(function(window) {
    'use strict';

    var SUTRAS_DATA = __DATA__;

    window.VyasSutrasBank = {
        data: SUTRAS_DATA,

        /**
         * Match all classical sutras for a native's active chart
         * Returns an array of relevant matched sutras categorized by domain
         */
        matchChart: function(analysis, domainFilter) {
            if (!analysis || !analysis.planets) return [];
            var matched = [];
            var pMap = analysis.planets;
            var planetsList = ['सूर्य','चन्द्र','मंगल','बुध','गुरु','शुक्र','शनि','राहु','केतु'];
            var engMap = {
                'सूर्य': 'Sun', 'चन्द्र': 'Moon', 'मंगल': 'Mars', 'बुध': 'Mercury',
                'गुरु': 'Jupiter', 'शुक्र': 'Venus', 'शनि': 'Saturn', 'राहु': 'Rahu', 'केतु': 'Ketu'
            };
            var signEng = {
                'मेष': 'Aries', 'वृषभ': 'Taurus', 'मिथुन': 'Gemini', 'कर्क': 'Cancer',
                'सिंह': 'Leo', 'कन्या': 'Virgo', 'तुला': 'Libra', 'वृश्चिक': 'Scorpio',
                'धनु': 'Sagittarius', 'मकर': 'Capricorn', 'कुंभ': 'Aquarius', 'मीन': 'Pisces'
            };

            // 1. Planet in Sign Sutras
            planetsList.forEach(function(p) {
                var pd = pMap[p];
                if (pd && pd.sign) {
                    var key = (engMap[p] || p) + '_' + (signEng[pd.sign] || pd.sign);
                    var sList = SUTRAS_DATA.planet_signs[key] || [];
                    sList.forEach(function(s) {
                        matched.push({
                            type: 'ग्रह-राशि वेध',
                            planet: p,
                            factor: key,
                            cond: s.cond,
                            pred: s.pred,
                            src: s.src,
                            domain: s.domain
                        });
                    });
                }
            });

            // 2. Planet in House Sutras
            planetsList.forEach(function(p) {
                var pd = pMap[p];
                if (pd && pd.house) {
                    var key = (engMap[p] || p) + '_' + pd.house;
                    var sList = SUTRAS_DATA.planet_houses[key] || [];
                    sList.forEach(function(s) {
                        matched.push({
                            type: 'भाव फल वेध',
                            planet: p,
                            factor: key,
                            cond: s.cond,
                            pred: s.pred,
                            src: s.src,
                            domain: s.domain
                        });
                    });
                }
            });

            // 3. Yutis (Conjunctions)
            for (var i = 0; i < planetsList.length; i++) {
                for (var j = i + 1; j < planetsList.length; j++) {
                    var p1 = planetsList[i], p2 = planetsList[j];
                    var d1 = pMap[p1], d2 = pMap[p2];
                    if (d1 && d2 && d1.house === d2.house) {
                        var k1 = (engMap[p1] || p1) + '_' + (engMap[p2] || p2);
                        var k2 = (engMap[p2] || p2) + '_' + (engMap[p1] || p1);
                        var sList = SUTRAS_DATA.yutis[k1] || SUTRAS_DATA.yutis[k2] || [];
                        sList.forEach(function(s) {
                            matched.push({
                                type: 'ग्रह युति वेध',
                                planet: p1 + '+' + p2,
                                factor: k1,
                                cond: s.cond,
                                pred: s.pred,
                                src: s.src,
                                domain: s.domain
                            });
                        });
                    }
                }
            }

            if (domainFilter && domainFilter !== 'all' && domainFilter !== 'general') {
                var df = domainFilter.toLowerCase();
                var filtered = matched.filter(function(m) {
                    var d = (m.domain || '').toLowerCase();
                    return d.indexOf(df) !== -1 || (df === 'career' && /career|profession|आजीविका|कर्म/i.test(d)) ||
                           (df === 'wealth' && /wealth|finance|धन|आय/i.test(d)) ||
                           (df === 'marriage' && /marriage|relationship|दांपत्य|विवाह/i.test(d)) ||
                           (df === 'health' && /health|आयु|रोग/i.test(d));
                });
                if (filtered.length > 0) return filtered;
            }

            return matched;
        }
    };

})(typeof window !== 'undefined' ? window : global);
"""

final_js = TEMPLATE.replace("__DATA__", bank_json)
with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write(final_js)

print(f"Generated: {OUTPUT_JS} ({os.path.getsize(OUTPUT_JS) / 1024:.2f} KB)")
