# scripts/replace_authentic_bundle.py
import json

kalapurusha_bundle = {
    "profile": {
        "name": "कालपुरुष चक्र",
        "dob": "0001-01-01",
        "tob": "06:00 AM",
        "city": "उज्जयिनी (Ujjain)",
        "lat": 23.1765,
        "lon": 75.7885,
        "gender": "Universal",
        "asc_sign": "मेष",
        "asc_dms": "00°00'00\""
    },
    "charts": {
        "d1": {
            "title": "D-1 लग्न कुण्डली • कालपुरुष प्राकृतिक चक्र",
            "ascSign": "मेष लग्न (00°00'00\")",
            "houses": {
                "1": ["1", "सूर्य 10°00' (उच्च)"],
                "2": ["2", "चन्द्र 03°00' (उच्च)", "राहु 15°00' (उच्च)"],
                "3": ["3"],
                "4": ["4", "गुरु 05°00' (उच्च)"],
                "5": ["5"],
                "6": ["6", "बुध 15°00' (उच्च)"],
                "7": ["7", "शनि 20°00' (उच्च)"],
                "8": ["8", "केतु 15°00' (उच्च)"],
                "9": ["9"],
                "10": ["10", "मंगल 28°00' (उच्च)"],
                "11": ["11"],
                "12": ["12", "शुक्र 27°00' (उच्च)"]
            }
        },
        "d9": {
            "title": "D-9 नवमांश कुण्डली (प्राकृतिक चक्र)",
            "ascSign": "मेष लग्न",
            "houses": {
                "1": ["1", "सूर्य"], "2": ["2"], "3": ["3"], "4": ["4", "गुरु"],
                "5": ["5"], "6": ["6", "बुध"], "7": ["7", "शनि"], "8": ["8"],
                "9": ["9"], "10": ["10", "मंगल"], "11": ["11"], "12": ["12", "शुक्र"]
            }
        },
        "d10": {
            "title": "D-10 दशमांश कुण्डली (प्राकृतिक चक्र)",
            "ascSign": "मेष लग्न",
            "houses": {
                "1": ["1"], "2": ["2"], "3": ["3"], "4": ["4"], "5": ["5"], "6": ["6"],
                "7": ["7"], "8": ["8"], "9": ["9"], "10": ["10", "मंगल"], "11": ["11"], "12": ["12"]
            }
        },
        "chalit": {
            "title": "भाव चलित चक्र",
            "ascSign": "मेष लग्न",
            "houses": {
                "1": ["1"], "2": ["2"], "3": ["3"], "4": ["4"], "5": ["5"], "6": ["6"],
                "7": ["7"], "8": ["8"], "9": ["9"], "10": ["10"], "11": ["11"], "12": ["12"]
            }
        }
    },
    "planet_table": [
        {"p": "सूर्य (Sun)", "r": "मेष", "d": "10°00'00\"", "n": "Ashwini (3)", "h": "1", "s": "परम उच्च"},
        {"p": "चन्द्र (Moon)", "r": "वृषभ", "d": "03°00'00\"", "n": "Krittika (2)", "h": "2", "s": "परम उच्च"},
        {"p": "मंगल (Mars)", "r": "मकर", "d": "28°00'00\"", "n": "Dhanishta (2)", "h": "10", "s": "परम उच्च"},
        {"p": "बुध (Mercury)", "r": "कन्या", "d": "15°00'00\"", "n": "Hasta (2)", "h": "6", "s": "परम उच्च"},
        {"p": "गुरु (Jupiter)", "r": "कर्क", "d": "05°00'00\"", "n": "Pushya (1)", "h": "4", "s": "परम उच्च"},
        {"p": "शुक्र (Venus)", "r": "मीन", "d": "27°00'00\"", "n": "Revati (4)", "h": "12", "s": "परम उच्च"},
        {"p": "शनि (Saturn)", "r": "तुला", "d": "20°00'00\"", "n": "Swati (4)", "h": "7", "s": "परम उच्च"},
        {"p": "राहु (Rahu)", "r": "वृषभ", "d": "15°00'00\"", "n": "Rohini (2)", "h": "2", "s": "उच्च राशि"},
        {"p": "केतु (Ketu)", "r": "वृश्चिक", "d": "15°00'00\"", "n": "Anuradha (4)", "h": "8", "s": "उच्च राशि"}
    ],
    "ashtakavarga": {
        "sav": [28, 30, 29, 32, 27, 34, 31, 26, 29, 33, 30, 27]
    },
    "kp": {
        "cusps": [],
        "planets": []
    },
    "jaimini": {
        "karakas": [],
        "atmakaraka": "सूर्य",
        "karakamsha": "मेष"
    },
    "nadi": {
        "combinations": [
            {
                "title": "प्राकृतिक कालपुरुष नाड़ी योग",
                "relation": "नैसर्गिक 1-5-9 त्रिकोण",
                "sutra": "धर्मे च कर्माणि च सर्व सिद्धिः",
                "impact": "कालपुरुष चक्र ब्रह्मांडीय संतुलन का प्रतीक है।"
            }
        ]
    },
    "predictions": {
        "bhavas": []
    }
}

json_str = json.dumps(kalapurusha_bundle, ensure_ascii=False)

def replace_in_file(filepath, var_name):
    print(f"Replacing {var_name} in {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    prefix = f"{var_name} = "
    start = text.find(prefix)
    if start != -1:
        end = text.find(';\n', start)
        if end != -1:
            text = text[:start + len(prefix)] + json_str + text[end:]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  ✓ Replaced {var_name} in {filepath}")
        else:
            print(f"  ! Semicolon not found after {var_name}")
    else:
        print(f"  ! Prefix {prefix} not found")

replace_in_file('index.html', 'var AUTHENTIC_BUNDLE')
replace_in_file('mobile/index.html', 'window.AUTHENTIC_BUNDLE')

