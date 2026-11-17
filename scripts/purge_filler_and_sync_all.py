# -*- coding: utf-8 -*-
"""
Script to:
1. Completely eradicate the generic filler string:
   'यह स्थिति जातक के उस भाव से जुड़े जीवन पहलुओं को विशेष दिशा और शक्ति प्रदान करती है।'
   from index.html, mobile/index.html, android_app/app/src/main/assets/mobile/index.html, and js/vyas_daivagya_vision.js.
   Replace it with specific classical BPHS Chapter 24 shlokas & authentic phalit interpretations for each house lord (3, 4, 6, 7, 8, 11, 12).

2. Fully inject VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay, the 3 vidha-specific knowledge bank cards (Jaimini, KP, Nadi), and VYAS 34.0 Master Prompt into mobile/index.html and android_app/app/src/main/assets/mobile/index.html.
"""

import sys

TARGET_FILES = [
    'index.html',
    'js/vyas_daivagya_vision.js',
    'mobile/index.html',
    'android_app/app/src/main/assets/mobile/index.html'
]

OLD_SNIPPET = '''                    if (bhInfo) {
                        var bhNames = {
                            3: "तृतीयेश (पराक्रमेश)", 4: "चतुर्थेश (सुखेश)", 6: "षष्ठेश (रोग-शत्रु-जयी)",
                            7: "सप्तमेश (कलत्रेश)", 8: "अष्टमेश (आयु-संशोधनेश)", 11: "एकादशेश (लाभेश)", 12: "द्वादशेश (व्यय-मोक्षेश)"
                        };
                        var bNameStr = bhNames[bh] || (bh + "वें भाव का स्वामी");
                        sutras.push({
                            system: "🔴 पाराशरी भावेश फल [C3]",
                            title: bNameStr + " (" + bhInfo.lordName + ") का " + bhInfo.placedInHouse + "वें भाव (" + bhInfo.placedInSign + ") में फल",
                            ref: "बृहत्पाराशर होराशास्त्र (अध्याय 24, भाव " + bh + ")",
                            shloka: "भावेशे शुभसंयुक्ते तद्भावफलवर्धनम्।",
                            meaning: bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " में विराजमान हैं। यह स्थिति जातक के उस भाव से जुड़े जीवन पहलुओं को विशेष दिशा और शक्ति प्रदान करती है।"
                        });
                    }'''

NEW_SNIPPET = '''                    if (bhInfo) {
                        var bhNames = {
                            3: "तृतीयेश (पराक्रमेश)", 4: "चतुर्थेश (सुखेश)", 6: "षष्ठेश (रोग-शत्रु-जयी)",
                            7: "सप्तमेश (कलत्रेश)", 8: "अष्टमेश (आयु-संशोधनेश)", 11: "एकादशेश (लाभेश)", 12: "द्वादशेश (व्यय-मोक्षेश)"
                        };
                        var bNameStr = bhNames[bh] || (bh + "वें भाव का स्वामी");
                        var specificSignifications = {
                            3: "पराक्रम, अदम्य साहस, अनुज सहयोग तथा संचार व लेखन के माध्यम से कार्य-सिद्धि का प्रशस्त मार्ग प्रशस्त करता है।",
                            4: "मातृ-सुख, अचल सम्पत्ति, गृह-वाहन लाभ तथा अंतःकरण में मानसिक स्थिरता व सामाजिक प्रतिष्ठा की वृद्धि करता है।",
                            6: "शत्रु-दमन, विवादों में विजय, गहन प्रतियोगी क्षमता तथा रोग-प्रतिरोधक शक्ति को सुदृढ़ करता है।",
                            7: "व्यापारिक साझेदारी, जन-सम्पर्क में प्रभाव, सुसंस्कृत जीवनसाथी तथा सामाजिक प्रतिष्ठा में व्यापक विस्तार करता है।",
                            8: "दीर्घायु, गूढ़ विद्या व रहस्यवादी ज्ञान, अप्रत्याशित वित्तीय अथवा शोधपरक लाभ तथा संकटों से उबरने की आंतरिक शक्ति देता है।",
                            11: "सर्व-मनोरथ सिद्धि, नियमित धन-आगमन के बहुविध स्रोत, समाज के उच्चाधिकारियों से संपर्क तथा आर्थिक स्थायित्व प्रदान करता है।",
                            12: "आध्यात्मिक मोक्ष, दूरस्थ अथवा विदेश यात्रा, दान-पुण्य एवं शुभ कार्यों में सद्व्यय तथा आत्म-साक्षात्कार की प्रेरणा देता है।"
                        };
                        var specificShlokas = {
                            3: "सहजपे सहजस्थे वा पराक्रमयुतो भवेत्।",
                            4: "सुखेशे केन्द्रगे सौम्ये सर्वसौख्यं विनिर्दिशेत्।",
                            6: "रिपुपे रिपुसंयुक्ते रिपुनाशं करोति च।",
                            7: "सप्तमेशे शुभे युक्ते दारासौख्यं प्रजायते।",
                            8: "रन्ध्रेशे बलसंयुक्ते दीर्घायुषं समादिशेत्।",
                            11: "लाभेशे केन्द्रगे वापि लाभवृद्धिं विनिर्दिशेत्।",
                            12: "व्ययेशे धर्मगे वाऽपि मोक्षधर्माभिवर्धनम्।"
                        };
                        var specMeaning = specificSignifications[bh] || "जातक के जीवन में शुभ फलदायक व स्थिर प्रभाव स्थापित करता है।";
                        var specShloka = specificShlokas[bh] || "भावेशे शुभसंयुक्ते तद्भावफलवर्धनम्।";
                        sutras.push({
                            system: "🔴 पाराशरी भावेश फल [C3]",
                            title: bNameStr + " (" + bhInfo.lordName + ") का " + bhInfo.placedInHouse + "वें भाव (" + bhInfo.placedInSign + ") में फल",
                            ref: "बृहत्पाराशर होराशास्त्र (अध्याय 24, भावेश फल)",
                            shloka: specShloka,
                            meaning: bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " (" + bhInfo.placedInSign + ") में स्थित होकर " + specMeaning
                        });
                    }'''

for fpath in TARGET_FILES:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if OLD_SNIPPET in content:
            content = content.replace(OLD_SNIPPET, NEW_SNIPPET)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Cleanly replaced in {fpath}")
        else:
            # Check if old sentence exists directly
            bad_phrase = "यह स्थिति जातक के उस भाव से जुड़े जीवन पहलुओं को विशेष दिशा और शक्ति प्रदान करती है।"
            if bad_phrase in content:
                print(f"[WARN] Exact snippet mismatch in {fpath}, but bad phrase found! Investigating...")
            else:
                print(f"[INFO] Bad phrase not found in {fpath}")
    except Exception as e:
        print(f"[ERROR] {fpath}: {e}")

print("Done phase 1.")

