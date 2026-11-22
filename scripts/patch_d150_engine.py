# scripts/patch_d150_engine.py
import re

d150_code = """
                    // D150 Nadiamsha (12' arc = 0.2° per division, 150 divisions per sign)
                    var d150_part = Math.min(149, Math.floor(deg / 0.2));
                    var nadiIdx = d150_part;
                    if (pSign % 3 === 0) { // Chara (Movable: Aries, Cancer, Libra, Cap)
                        nadiIdx = d150_part;
                    } else if (pSign % 3 === 1) { // Sthira (Fixed: Taurus, Leo, Scorpio, Aqu)
                        nadiIdx = 149 - d150_part;
                    } else { // Dvisvabhava (Dual: Gemini, Virgo, Sag, Pisces)
                        nadiIdx = (75 + d150_part) % 150;
                    }
                    var bhaga = (deg % 0.2 < 0.1) ? "पूर्व भाग" : "उत्तर भाग";
                    var nadiName = "नाड्यांश #" + (nadiIdx + 1) + " (" + bhaga + ")";
                    var d150_sign = (pSign + d150_part) % 12;
                    addV("D150", 150, d150_sign, (deg * 150.0) % 30.0, nadiName);
"""

files = ['js/vyas_astronomical_engine.js', 'android_app/app/src/main/assets/js/vyas_astronomical_engine.js']

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    if '"D150"' in content:
        print(f"D150 already exists in {fp}")
        continue

    # 1. Insert calculation after D60
    target_d60_calc = 'addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);'
    if target_d60_calc in content:
        content = content.replace(target_d60_calc, target_d60_calc + "\n" + d150_code)

    # 2. Insert title in VARGA_TITLES
    target_title = 'D60: "D-60 षष्ट्यंश चक्र (पूर्व जन्म प्रारब्ध व सम्पूर्ण फल निर्णय)"'
    replacement_title = 'D60: "D-60 षष्ट्यंश चक्र (पूर्व जन्म प्रारब्ध व सम्पूर्ण फल निर्णय)",\n                    D150: "D-150 नाड्यांश चक्र (सूक्ष्म प्रारब्ध, १२\' कला अंश व जीवन-रहस्य)"'
    content = content.replace(target_title, replacement_title)

    # 3. Add to vKeys
    content = content.replace('["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]',
                              '["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60", "D150"]')

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"SUCCESS: Patched D150 into {fp}")
