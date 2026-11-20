import os
import sys
import json
import sqlite3
import uuid

print("Starting knowledge ingestion pipeline for new treatises...")

db_paths = [
    'data/vyas_phalit_vault.db',
    'vyas_astra_elite_framework/backend/vyas_phalit_vault.db'
]

kp_sublord_sutras = [
    # 1st Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "1st Cusp Sub-Lord",
        "primary_factor": "Ascendant CSL",
        "planetary_condition": "1st Cusp Sub-Lord signifies 1, 11 houses without 6, 8, 12 affliction",
        "condition_hi": "प्रथम भाव का कस्पल सब-लॉर्ड 1, 11 भावों का कार्येश बने",
        "prediction_en": "Native enjoys extraordinary vitality, longevity, supreme health, self-confidence, and public renown.",
        "prediction_hi": "जातक दीर्घायु, अत्यंत स्वस्थ, ओजस्वी, आत्मविश्वासी एवं समाज में विशेष यश प्राप्त करने वाला होता है। निर्णय शक्ति दृढ़ होती है।",
        "life_domain": "Health & Personality",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Sub-lord in star of benefic strengthens resilience"
    },
    # 2nd Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "2nd Cusp Sub-Lord",
        "primary_factor": "2nd CSL Dhana",
        "planetary_condition": "2nd Cusp Sub-Lord signifies 2, 6, 11 houses",
        "condition_hi": "द्वितीय कस्प का सब-लॉर्ड 2, 6, 11 भावों का कार्येश बने",
        "prediction_en": "Enormous wealth accumulation, flourishing family assets, sound savings, and strong financial stability.",
        "prediction_hi": "अकूत धन संचय, बैंक बैलेंस, पैतृक संपत्ति व कुटुंब का सुख मिलता है। जातक की वाणी प्रभावशाली व आर्थिक स्थिति सुदृढ़ रहती है।",
        "life_domain": "Wealth & Family",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Direct connection to Jupiter or Venus amplifies prosperity"
    },
    # 3rd Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "3rd Cusp Sub-Lord",
        "primary_factor": "3rd CSL Sahaja",
        "planetary_condition": "3rd Cusp Sub-Lord signifies 3, 10, 11 houses",
        "condition_hi": "तृतीय कस्पल सब-लॉर्ड 3, 10, 11 भावों से जुड़े",
        "prediction_en": "High success in digital communications, IT, publishing, courageous contracts, and productive short travels.",
        "prediction_hi": "मीडिया, लेखन, सॉफ्टवेयर, डिजिटल संचार व मार्केटिंग में उच्च सफलता। भाई-बहनों का सहयोग व निर्भीक निर्णय क्षमता।",
        "life_domain": "Communication & Courage",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Mercury involvement grants high technological eloquence"
    },
    # 4th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "4th Cusp Sub-Lord",
        "primary_factor": "4th CSL Sukha",
        "planetary_condition": "4th Cusp Sub-Lord signifies 4, 11, 2 houses",
        "condition_hi": "चतुर्थ भाव का सब-लॉर्ड 4, 11, 2 भावों से संबंधित हो",
        "prediction_en": "Acquisition of palatial properties, luxury automobiles, academic degrees, and deep maternal bliss.",
        "prediction_hi": "भव्य मकान, श्रेष्ठ वाहन, कृषि भूमि एवं माता का भरपूर स्नेह। उच्च अकादमिक डिग्रियों की प्राप्ति होती है।",
        "life_domain": "Property & Mother",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Venus or Moon association guarantees luxury comforts"
    },
    # 5th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "5th Cusp Sub-Lord",
        "primary_factor": "5th CSL Putra & Buddhi",
        "planetary_condition": "5th Cusp Sub-Lord signifies 2, 5, 11 houses",
        "condition_hi": "पंचम भाव का कस्पल सब-लॉर्ड 2, 5, 11 भावों का कार्येश हो",
        "prediction_en": "Gift of brilliant, virtuous children, artistic genius, speculative gains, and awakening of poorvapunya.",
        "prediction_hi": "तेजस्वी व आज्ञाकारी संतान सुख, विलक्षण बौद्धिक प्रतिभा, शेयर मार्केट में लाभ तथा पूर्वजन्म के संचित पुण्यों का उदय।",
        "life_domain": "Children & Intelligence",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Jupiter or Mercury aspect gives divine mantra siddhi"
    },
    # 6th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "6th Cusp Sub-Lord",
        "primary_factor": "6th CSL Shatru & Roga",
        "planetary_condition": "6th Cusp Sub-Lord signifies 1, 5, 11 houses",
        "condition_hi": "षष्ठ भाव का कस्पल सब-लॉर्ड 1, 5, 11 भावों को इंगित करे",
        "prediction_en": "Triumphant victory in competitive examinations, swift debt clearance, vanquishing adversaries, and robust immunity.",
        "prediction_hi": "प्रतियोगी परीक्षाओं में शीर्ष सफलता, समस्त कर्जों से मुक्ति, मुकदमों व विरोधियों पर विजय तथा दीर्घकालीन निरोगी काया।",
        "life_domain": "Competitions & Health",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Mars or Saturn involvement provides ruthless execution"
    },
    # 7th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "7th Cusp Sub-Lord",
        "primary_factor": "7th CSL Kalatra",
        "planetary_condition": "7th Cusp Sub-Lord signifies 2, 7, 11 houses",
        "condition_hi": "सप्तम भाव का कस्पल सब-लॉर्ड 2, 7, 11 भावों का कार्येश हो",
        "prediction_en": "Blissful, timely marriage with cultured, supportive, and prosperous partner; highly lucrative business partnerships.",
        "prediction_hi": "सुलक्षणा, संस्कारी व समृद्ध जीवनसाथी की प्राप्ति। सुखद दाम्पत्य जीवन तथा व्यापारिक साझेदारियों में प्रचुर लाभ।",
        "life_domain": "Marriage & Business",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Venus or Jupiter connection ensures lifelong romance and harmony"
    },
    # 8th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "8th Cusp Sub-Lord",
        "primary_factor": "8th CSL Randhra",
        "planetary_condition": "8th Cusp Sub-Lord signifies 2, 8, 11 houses",
        "condition_hi": "अष्टम कस्पल सब-लॉर्ड 2, 8, 11 भावों से जुड़े",
        "prediction_en": "Unexpected legacies, inheritance windfalls, insurance profits, and exceptional mastery of astrology and occult sciences.",
        "prediction_hi": "अचानक वसीयत, बीमा, ससुराल पक्ष से धन लाभ तथा गूढ़ तंत्र-मंत्र-ज्योतिष अनुसंधान में अद्वितीय अंतर्दृष्टि।",
        "life_domain": "Occult & Legacy",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Ketu or Saturn involvement unlocks mystic intuition"
    },
    # 9th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "9th Cusp Sub-Lord",
        "primary_factor": "9th CSL Bhagya",
        "planetary_condition": "9th Cusp Sub-Lord signifies 1, 9, 11 houses",
        "condition_hi": "नवम कस्प का सब-लॉर्ड 1, 9, 11 भावों का फल दे",
        "prediction_en": "Supreme good fortune, higher philosophical learning, divine mentor protection, and prosperous foreign journeys.",
        "prediction_hi": "प्रबल भाग्योदय, उच्च आध्यात्मिक विद्या, पिता व गुरुजनों का वरदहस्त तथा सफल विदेश यात्राओं से अपार समृद्धि।",
        "life_domain": "Fortune & Dharma",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Jupiter connection elevates moral and philanthropic stature"
    },
    # 10th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "10th Cusp Sub-Lord",
        "primary_factor": "10th CSL Karma",
        "planetary_condition": "10th Cusp Sub-Lord signifies 2, 6, 10, 11 houses",
        "condition_hi": "दशम भाव का कस्पल सब-लॉर्ड 2, 6, 10, 11 का कार्येश हो",
        "prediction_en": "Pinnacle executive status, corporate authority, bureaucratic power, enterprise leadership, and enduring public fame.",
        "prediction_hi": "शासन-प्रशासन, उच्च कॉर्पोरेट पद, राजनीति अथवा बड़े उद्योग में शीर्ष प्रतिष्ठा। दूर-दूर तक यश व स्थायी पद-प्रतिष्ठा।",
        "life_domain": "Career & Reputation",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Sun or Mars lordship gives governmental administrative power"
    },
    # 11th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "11th Cusp Sub-Lord",
        "primary_factor": "11th CSL Labha",
        "planetary_condition": "11th Cusp Sub-Lord signifies 1, 2, 11 houses",
        "condition_hi": "एकादश भाव का कस्पल सब-लॉर्ड 1, 2, 11 का फल दे",
        "prediction_en": "Effortless fulfillment of all cherished ambitions, powerful elite networking, and multiple lucrative income streams.",
        "prediction_hi": "समस्त मनोकामनाओं की पूर्ण सिद्धि, प्रभावशाली मित्रों का सहयोग तथा आय के एक से अधिक स्थायी व प्रचुर स्रोत।",
        "life_domain": "Income & Desires",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Benefic sub-lord ensures smooth, unhindered cash flow"
    },
    # 12th Cusp Sub-Lord
    {
        "category": "KP Krishnamurti Stellar System",
        "sub_category": "12th Cusp Sub-Lord",
        "primary_factor": "12th CSL Moksha & Foreign",
        "planetary_condition": "12th Cusp Sub-Lord signifies 3, 9, 12 houses",
        "condition_hi": "द्वादश भाव का कस्पल सब-लॉर्ड 3, 9, 12 का कार्येश बने",
        "prediction_en": "Overseas permanent settlement, international career assignments, profound spiritual liberation (Moksha), and peaceful sleep.",
        "prediction_hi": "विदेश में स्थायी निवास व समृद्धि, बहुराष्ट्रीय कंपनियों में उच्च अवसर, आंतरिक ध्यान-साधना तथा पूर्ण मानसिक शांति।",
        "life_domain": "Foreign & Moksha",
        "source": "KP Reader III - Stellar Astrology",
        "strength_modifiers": "Moon or Rahu involvement accelerates foreign relocation"
    },
    # Karmavipaka Samhita
    {
        "category": "Karmavipaka Samhita",
        "sub_category": "Pitri Rin & Shraapa",
        "primary_factor": "Sun-Rahu 9th House",
        "planetary_condition": "Sun conjunct Rahu/Ketu in 9th house aspected by malefic Saturn",
        "condition_hi": "सूर्य-राहु की युति नवम भाव में अथवा नवमेश 8/12 में शनि पीड़ित",
        "prediction_en": "Ancestral debts causing career roadblocks, delayed progeny, and domestic anxiety, resolved through holy Shraddha.",
        "prediction_hi": "पूर्वजन्म के पितृ ऋण के कारण कार्यक्षेत्र में अचानक रुकावटें, पारिवारिक अशांति व वंश वृद्धि में विलंब। गया श्राद्ध से मुक्ति।",
        "life_domain": "Ancestral & Karma",
        "source": "Karmavipaka Samhita - Chapter 4",
        "strength_modifiers": "Relieved by Tripindi Shraddha and feeding crows on Amavasya"
    },
    {
        "category": "Karmavipaka Samhita",
        "sub_category": "Matri Rin & Shraapa",
        "primary_factor": "Moon-Ketu 4th House",
        "planetary_condition": "Moon afflicted by Ketu or Saturn in 4th/8th house",
        "condition_hi": "चन्द्रमा चतुर्थ या अष्टम में केतु या शनि द्वारा आक्रांत",
        "prediction_en": "Psychological mood swings, insomnia, and academic interruptions due to maternal karmic burdens, cleared by mother's blessing.",
        "prediction_hi": "मानसिक अवसाद, अनिद्रा तथा विद्या में व्यवधान। भगवान शिव के दुग्धाभिषेक तथा माता के चरण वंदना से परम शांति।",
        "life_domain": "Mental Peace & Health",
        "source": "Karmavipaka Samhita - Chapter 7",
        "strength_modifiers": "Chanting Mahamrityunjaya Mantra and offering silver to water cures distress"
    },
    # Bhrigu Nandi Nadi
    {
        "category": "Bhrigu Nandi Nadi",
        "sub_category": "Jeeva-Karma Yoga",
        "primary_factor": "Jupiter-Saturn Trine",
        "planetary_condition": "Jupiter and Saturn in 1-5-9 mutual trine",
        "condition_hi": "बृहस्पति (जीव) और शनि (कर्म) परस्पर त्रिकोण 1-5-9 में स्थित",
        "prediction_en": "Epoch-making professional authority, judicial wisdom, philanthropic leadership, and massive social influence after age 30.",
        "prediction_hi": "कार्यक्षेत्र में महान नीतिज्ञ, न्यायप्रिय, संगठनात्मक नेतृत्वकर्ता तथा 30 वर्ष की आयु के बाद ऐतिहासिक भाग्योदय।",
        "life_domain": "Career & Life Purpose",
        "source": "Bhrigu Nandi Nadi - R.G. Rao",
        "strength_modifiers": "Double transit of Saturn and Jupiter ignites peak golden periods"
    },
    {
        "category": "Bhrigu Nandi Nadi",
        "sub_category": "Dhana-Lakshmi Yoga",
        "primary_factor": "Jupiter-Venus Trine",
        "planetary_condition": "Jupiter and Venus in mutual trine or conjunction",
        "condition_hi": "गुरु और शुक्र परस्पर त्रिकोण अथवा युति में स्थित",
        "prediction_en": "Perpetual financial prosperity, artistic intelligence, luxurious conveyances, and unshakeable wealth generation.",
        "prediction_hi": "महालक्ष्मी योग: अकूत धन-संपत्ति, भव्य वाहन, कला-साहित्य-सॉफ्टवेयर में असाधारण प्रतिभा तथा राजसी ठाठ-बाट।",
        "life_domain": "Wealth & Luxury",
        "source": "Bhrigu Nandi Nadi - R.G. Rao",
        "strength_modifiers": "Reciting Sri Sukta multiplies asset accumulation"
    }
]

for db in db_paths:
    if os.path.exists(db):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        inserted = 0
        for s in kp_sublord_sutras:
            sid = f"SUTRA_CUSTOM_{uuid.uuid4().hex[:8].upper()}"
            # Check duplicate by condition_hi
            cur.execute("SELECT sutra_id FROM sutras WHERE condition_hi = ?", (s['condition_hi'],))
            if cur.fetchone():
                continue
            cur.execute("""
                INSERT INTO sutras (sutra_id, category, sub_category, primary_factor, planetary_condition, condition_hi, prediction_en, prediction_hi, life_domain, source, strength_modifiers)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sid,
                s['category'],
                s['sub_category'],
                s['primary_factor'],
                s['planetary_condition'],
                s['condition_hi'],
                s['prediction_en'],
                s['prediction_hi'],
                s['life_domain'],
                s['source'],
                s['strength_modifiers']
            ))
            inserted += 1
        conn.commit()
        cur.execute("SELECT count(*) FROM sutras")
        total = cur.fetchone()[0]
        conn.close()
        print(f"DB {db}: Inserted {inserted} new sutras. Total in DB: {total}")

print("Knowledge bank updated successfully!")
