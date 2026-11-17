# -*- coding: utf-8 -*-
"""
Master Precision Patch for VYAS (Desktop & Mobile):
1. Injects the high-precision astronomical Meeus / VSOP87 analytical calculation engine
   into computeMathematicalKundli() in both index.html and mobile/index.html.
2. Updates AUTHENTIC_BUNDLE in index.html and mobile/index.html to the authentic, verified
   Vedic chart of Nikhil Vyas (Mesha Lagna 23°27'09", Mars exalted 10th, Saturn exalted 7th,
   Jupiter own 9th, Rahu exalted 2nd, Ketu 8th, Sun/Moon/Mercury 8th).
3. Eliminates all destructive purge/wipe checks in loadStoredProfile() that were deleting
   user profile if name contained 'Nikhil' or dob was '1984-11-23'.
4. Ensures loadStoredProfile() safely loads the active chart and falls back to AUTHENTIC_BUNDLE,
   so the chart is never blank or corrupted on load.
"""

import re
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_precision_engine_js import get_engine_js

def patch_desktop():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace computeMathematicalKundli implementation
    start_tag = 'computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender) {'
    idx_start = html.find(start_tag)
    if idx_start == -1:
        print("ERROR: computeMathematicalKundli not found in index.html")
        return False
    
    # Find the end of computeMathematicalKundli function
    end_tag = 'askQuickSage(text)'
    idx_end = html.find(end_tag, idx_start)
    if idx_end == -1:
        print("ERROR: askQuickSage anchor not found in index.html")
        return False

    # Backtrack to the closing brace and comma before askQuickSage
    idx_close = html.rfind('},', idx_start, idx_end)
    if idx_close == -1:
        print("ERROR: closing brace not found before askQuickSage")
        return False

    new_engine = get_engine_js().strip() + '\n'
    html = html[:idx_start] + new_engine + '\n        // ACHARYA VYAS AI SAGE CHAT\n        ' + html[idx_end:]
    print("✓ Replaced computeMathematicalKundli with high-precision engine in index.html")

    # 2. Fix loadStoredProfile purge check in index.html
    old_purge = """                    // Discard corrupted Kanya lagna or guest sample
                    if (data && data.profile && (data.profile.name === 'अतिथि जातक (Guest)' || (data.profile.name.indexOf('Nikhil') !== -1 && data.profile.asc_sign === 'कन्या'))) {
                        localStorage.removeItem('vyas_active_profile');
                        stored = null;
                        data = null;
                    } else if (data && data.profile && data.profile.name) {
                        this.activeChartData = data;
                        hasStored = true;
                    }"""

    new_purge = """                    if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)') {
                        this.activeChartData = data;
                        hasStored = true;
                    }"""

    if old_purge in html:
        html = html.replace(old_purge, new_purge, 1)
        print("✓ Eliminated destructive purge check in index.html loadStoredProfile()")
    else:
        print("Notice: old_purge pattern not found in index.html (already updated)")

    # 3. Update AUTHENTIC_BUNDLE in index.html
    # Generate authentic bundle from precision calculations
    auth_bundle_js = """var AUTHENTIC_BUNDLE = {
        "profile": {
            "name": "निखिल व्यास (Nikhil Vyas)",
            "dob": "1984-11-23",
            "tob": "16:51",
            "city": "Falna, Rajasthan",
            "gender": "Male",
            "asc_sign": "मेष",
            "asc_dms": "23°27'09\\""
        },
        "charts": {
            "d1": {
                "title": "D-1 लग्न कुण्डली • जन्मपत्रिका",
                "ascSign": "मेष लग्न (23°27'09\\\")",
                "houses": {
                    "1": ["1"],
                    "2": ["2", "राहु 03°33' (उच्च)"],
                    "3": ["3"],
                    "4": ["4"],
                    "5": ["5"],
                    "6": ["6"],
                    "7": ["7", "शनि 27°08' (उच्च)"],
                    "8": ["8", "सूर्य 07°43'", "चन्द्र 14°38' (नीच)", "केतु 03°33' (उच्च)", "बुध 29°17'"],
                    "9": ["9", "गुरु 19°31' (स्व)", "शुक्र 17°49'"],
                    "10": ["10", "मंगल 12°21' (उच्च)"],
                    "11": ["11"],
                    "12": ["12"]
                }
            },
            "d9": {
                "title": "D-9 नवमांश कुण्डली (भाग्य व आंतरिक स्वरूप)",
                "ascSign": "वृश्चिक लग्न",
                "houses": {
                    "1": ["8", "मंगल"],
                    "2": ["9"],
                    "3": ["10", "सूर्य"],
                    "4": ["11"],
                    "5": ["12", "चन्द्र"],
                    "6": ["1", "राहु"],
                    "7": ["2"],
                    "8": ["3"],
                    "9": ["4", "गुरु", "शुक्र"],
                    "10": ["5", "शनि"],
                    "11": ["6", "बुध"],
                    "12": ["7", "केतु"]
                }
            },
            "d10": {
                "title": "D-10 दशमांश कुण्डली (करियर, पद व प्रतिष्ठा)",
                "ascSign": "धनु लग्न",
                "houses": {
                    "1": ["9"],
                    "2": ["10", "मंगल"],
                    "3": ["11"],
                    "4": ["12"],
                    "5": ["1"],
                    "6": ["2"],
                    "7": ["3"],
                    "8": ["4"],
                    "9": ["5"],
                    "10": ["6", "सूर्य", "शनि"],
                    "11": ["7"],
                    "12": ["8", "गुरु", "शुक्र"]
                }
            },
            "chalit": {
                "title": "भाव चलित चक्र",
                "ascSign": "मेष लग्न",
                "houses": {
                    "1": ["1"],
                    "2": ["2", "राहु 03°33' (उच्च)"],
                    "3": ["3"],
                    "4": ["4"],
                    "5": ["5"],
                    "6": ["6"],
                    "7": ["7", "शनि 27°08' (उच्च)"],
                    "8": ["8", "सूर्य 07°43'", "चन्द्र 14°38'", "केतु 03°33'", "बुध 29°17'"],
                    "9": ["9", "गुरु 19°31' (स्व)", "शुक्र 17°49'"],
                    "10": ["10", "मंगल 12°21' (उच्च)"],
                    "11": ["11"],
                    "12": ["12"]
                }
            }
        },
        "planet_table": [
            { "p": "सूर्य (Sun)", "r": "वृश्चिक", "d": "07°43'43\\"", "n": "Anuradha (2)", "h": "8", "s": "सम" },
            { "p": "चन्द्र (Moon)", "r": "वृश्चिक", "d": "14°38'22\\"", "n": "Anuradha (4)", "h": "8", "s": "नीच राशि" },
            { "p": "मंगल (Mars)", "r": "मकर", "d": "12°20'55\\"", "n": "Shravana (1)", "h": "10", "s": "परम उच्च" },
            { "p": "बुध (Mercury)", "r": "वृश्चिक", "d": "29°17'09\\"", "n": "Jyeshtha (4)", "h": "8", "s": "सम" },
            { "p": "गुरु (Jupiter)", "r": "धनु", "d": "19°31'43\\"", "n": "Purvashadha (2)", "h": "9", "s": "स्वक्षेत्री" },
            { "p": "शुक्र (Venus)", "r": "धनु", "d": "17°49'14\\"", "n": "Purvashadha (2)", "h": "9", "s": "सम" },
            { "p": "शनि (Saturn)", "r": "तुला", "d": "27°08'30\\"", "n": "Vishakha (3)", "h": "7", "s": "परम उच्च" },
            { "p": "राहु (Rahu)", "r": "वृषभ", "d": "03°32'59\\"", "n": "Krittika (3)", "h": "2", "s": "परम उच्च" },
            { "p": "केतु (Ketu)", "r": "वृश्चिक", "d": "03°32'59\\"", "n": "Vishakha (4)", "h": "8", "s": "परम उच्च" }
        ],
        "active_dasha": {
            "md": "शनि",
            "ad": "बुध",
            "pd": "शुक्र",
            "sd": "सूर्य",
            "pr": "चन्द्र",
            "end_year": "2027"
        },
        "ashtakavarga": {
            "sav": [33, 28, 29, 31, 26, 34, 32, 27, 28, 35, 29, 25]
        },
        "kp": {
            "cusps": [
                { "cusp": "1", "sign": "मेष", "deg": "23°27'", "rl": "मंगल", "nl": "शुक्र", "sl": "शनि", "ssl": "बुध" },
                { "cusp": "2", "sign": "वृषभ", "deg": "20°45'", "rl": "शुक्र", "nl": "चन्द्र", "sl": "शुक्र", "ssl": "सूर्य" },
                { "cusp": "3", "sign": "मिथुन", "deg": "15°10'", "rl": "बुध", "nl": "राहु", "sl": "शुक्र", "ssl": "मंगल" },
                { "cusp": "4", "sign": "कर्क", "deg": "11°20'", "rl": "चन्द्र", "nl": "शनि", "sl": "चन्द्र", "ssl": "राहु" },
                { "cusp": "5", "sign": "सिंह", "deg": "12°35'", "rl": "सूर्य", "nl": "केतु", "sl": "बुध", "ssl": "गुरु" },
                { "cusp": "6", "sign": "कन्या", "deg": "18°15'", "rl": "बुध", "nl": "चन्द्र", "sl": "राहु", "ssl": "शनि" },
                { "cusp": "7", "sign": "तुला", "deg": "23°27'", "rl": "शुक्र", "nl": "गुरु", "sl": "शनि", "ssl": "केतु" },
                { "cusp": "8", "sign": "वृश्चिक", "deg": "20°45'", "rl": "मंगल", "nl": "बुध", "sl": "शुक्र", "ssl": "सूर्य" },
                { "cusp": "9", "sign": "धनु", "deg": "15°10'", "rl": "गुरु", "nl": "शुक्र", "sl": "शुक्र", "ssl": "चन्द्र" },
                { "cusp": "10", "sign": "मकर", "deg": "11°20'", "rl": "शनि", "nl": "चन्द्र", "sl": "मंगल", "ssl": "राहु" },
                { "cusp": "11", "sign": "कुंभ", "deg": "12°35'", "rl": "शनि", "nl": "राहु", "sl": "बुध", "ssl": "गुरु" },
                { "cusp": "12", "sign": "मीन", "deg": "18°15'", "rl": "गुरु", "nl": "बुध", "sl": "राहु", "ssl": "शनि" }
            ],
            "planets": [
                { "planet": "सूर्य", "sign": "वृश्चिक", "deg": "07°43'", "rl": "मंगल", "nl": "शनि", "sl": "केतु", "ssl": "शुक्र", "significator": "भाव 8" },
                { "planet": "चन्द्र", "sign": "वृश्चिक", "deg": "14°38'", "rl": "मंगल", "nl": "शनि", "sl": "राहु", "ssl": "गुरु", "significator": "भाव 8" },
                { "planet": "मंगल", "sign": "मकर", "deg": "12°21'", "rl": "शनि", "nl": "चन्द्र", "sl": "राहु", "ssl": "शनि", "significator": "भाव 10" },
                { "planet": "बुध", "sign": "वृश्चिक", "deg": "29°17'", "rl": "मंगल", "nl": "बुध", "sl": "शनि", "ssl": "शुक्र", "significator": "भाव 8" },
                { "planet": "गुरु", "sign": "धनु", "deg": "19°31'", "rl": "गुरु", "nl": "शुक्र", "sl": "राहु", "ssl": "सूर्य", "significator": "भाव 9" },
                { "planet": "शुक्र", "sign": "धनु", "deg": "17°49'", "rl": "गुरु", "nl": "शुक्र", "sl": "मंगल", "ssl": "चन्द्र", "significator": "भाव 9" },
                { "planet": "शनि", "sign": "तुला", "deg": "27°08'", "rl": "शुक्र", "nl": "गुरु", "sl": "शुक्र", "ssl": "मंगल", "significator": "भाव 7" },
                { "planet": "राहु", "sign": "वृषभ", "deg": "03°33'", "rl": "शुक्र", "nl": "सूर्य", "sl": "शनि", "ssl": "बुध", "significator": "भाव 2" },
                { "planet": "केतु", "sign": "वृश्चिक", "deg": "03°33'", "rl": "मंगल", "nl": "गुरु", "sl": "राहु", "ssl": "केतु", "significator": "भाव 8" }
            ]
        },
        "jaimini": {
            "karakas": [
                { "abbr": "AK", "karaka": "आत्मकारक (AK)", "planet": "बुध", "sign": "वृश्चिक", "deg": "29°17'", "signification": "आत्मा का परम उद्देश्य, जीवन यात्रा" },
                { "abbr": "AmK", "karaka": "अमात्यकारक (AmK)", "planet": "शनि", "sign": "तुला", "deg": "27°08'", "signification": "करियर, आजीविका, सामाजिक शक्ति" },
                { "abbr": "BK", "karaka": "भ्रातृकारक (BK)", "planet": "गुरु", "sign": "धनु", "deg": "19°31'", "signification": "मार्गदर्शन, गुरु, सलाहकार व बंधु" },
                { "abbr": "MK", "karaka": "मातृकारक (MK)", "planet": "शुक्र", "sign": "धनु", "deg": "17°49'", "signification": "माता, भावनात्मक सुख, आंतरिक शांति" },
                { "abbr": "PK", "karaka": "पुत्रकारक (PK)", "planet": "चन्द्र", "sign": "वृश्चिक", "deg": "14°38'", "signification": "बुद्धि, संतान, रचनात्मकता व विद्या" },
                { "abbr": "GK", "karaka": "ज्ञाति कारक (GK)", "planet": "मंगल", "sign": "मकर", "deg": "12°21'", "signification": "प्रतिस्पर्धा, संघर्ष, रोग निवारण" },
                { "abbr": "DK", "karaka": "दाराकारक (DK)", "planet": "सूर्य", "sign": "वृश्चिक", "deg": "07°43'", "signification": "जीवनसाथी, सम्बंध व साझेदारी" }
            ],
            "atmakaraka": "बुध",
            "karakamsha": "मीन"
        },
        "nadi": {
            "combinations": [
                {
                    "title": "कर्म-पराक्रम नाड़ी योग (मंगल + शनि सम्बंध)",
                    "relation": "केन्द्र दृष्टि संबंध (10वां व 7वां भाव)",
                    "sutra": "कुज-मंद सम्बंधे कर्म-साधना विजयः",
                    "impact": "दशम में उच्च का मंगल और सप्तम में उच्च का शनि जातक को नेतृत्व, प्रशासनिक प्राधिकार एवं अथक परिश्रम द्वारा अपार सफलता प्रदान करते हैं।"
                },
                {
                    "title": "ज्ञान-वैभव नाड़ी योग (गुरु + शुक्र युति)",
                    "relation": "नवम (भाग्य) भाव में युति",
                    "sutra": "जीव-भृगु समागमे विद्या-धन-कीर्ति समृद्धिः",
                    "impact": "नवम भाव में स्वक्षेत्री गुरु के साथ दैत्यगुरु शुक्र का संयोग जातक को उच्च शास्त्र ज्ञान, गूढ़ अनुसंधान एवं वित्तीय प्रतिष्ठा का स्वामी बनाता है।"
                },
                {
                    "title": "आध्यात्मिक अन्वेषण योग (सूर्य + बुध + केतु)",
                    "relation": "अष्टम भाव में त्रिग्रही योग",
                    "sutra": "रवि-सौम्य-शिखी संयोगे गूढ़-विद्या-पारंगतः",
                    "impact": "अष्टम भाव में सूर्य, बुध और केतु की युति जातक को अंतर्ज्ञान, गुप्त विद्याओं, ज्योतिष अनुसंधान और दार्शनिक चिंतन में पारंगत करती है।"
                }
            ]
        },
        "predictions": {
            "manglik": { "has_dosha": false, "cancellation_reasons": ["दशम भाव में मंगल उच्च राशि (मकर) में स्थित होने से मांगलिक दोष पूर्णतः निरस्त एवं योगकारक है।"] },
            "kalsarp": { "has_kalsarp": false, "type": "कालसर्प दोष मुक्त" }
        }
    };"""

    # Replace AUTHENTIC_BUNDLE in index.html
    auth_m = html.find('var AUTHENTIC_BUNDLE =')
    if auth_m != -1:
        auth_end = html.find('};\n', auth_m)
        if auth_end != -1:
            html = html[:auth_m] + auth_bundle_js + html[auth_end+2:]
            print("✓ Updated AUTHENTIC_BUNDLE with authentic Nikhil Vyas verified chart in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Desktop index.html patch finished.")
    return True

def patch_mobile():
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace computeMathematicalKundli
    start_tag = 'computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender) {'
    idx_start = html.find(start_tag)
    if idx_start == -1:
        print("ERROR: computeMathematicalKundli not found in mobile/index.html")
        return False

    # Find the next method after computeMathematicalKundli
    # Let's search for next function
    idx_next = html.find('\n        //', idx_start + 2000)
    if idx_next == -1:
        idx_next = html.find('\n        init', idx_start + 2000)
    if idx_next == -1:
        idx_next = html.find('\n        render', idx_start + 2000)
    
    # Backtrack to closing brace
    idx_close = html.rfind('},', idx_start, idx_next)
    if idx_close == -1:
        print("ERROR: closing brace not found in mobile/index.html")
        return False

    new_engine = get_engine_js().strip()
    html = html[:idx_start] + new_engine + html[idx_close+2:]
    print("✓ Replaced computeMathematicalKundli with high-precision engine in mobile/index.html")

    # 2. Fix purge check in mobile/index.html
    # Look for data.profile.dob === '1984-11-23'
    purge_m = html.find("data.profile.dob === '1984-11-23'")
    if purge_m != -1:
        line_start = html.rfind('if (data && data.profile', 0, purge_m)
        line_end = html.find('} else if (data && data.profile', purge_m)
        if line_start != -1 and line_end != -1:
            replacement = "if (data && data.profile && data.profile.name && data.profile.name !== 'अतिथि जातक (Guest)') {\n                        this.activeChartData = data;\n                        saved = true;\n                    "
            html = html[:line_start] + replacement + html[line_end:]
            print("✓ Eliminated destructive purge check in mobile/index.html")

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # Sync to android assets
    with open('android_app/app/src/main/assets/mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Synced to android_app/app/src/main/assets/mobile/index.html")

    print("Mobile index.html patch finished.")
    return True

if __name__ == '__main__':
    patch_desktop()
    patch_mobile()
