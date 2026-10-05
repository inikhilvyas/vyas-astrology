"""Varga Predictions & Masters' Knowledge Engine (वर्ग कुंडलियों के फलित सूत्र एवं शीर्ष ज्योतिषियों का ज्ञान बैंक).

1. Varga Predictive Synthesizer:
   Evaluates D-9 (Navamsha), D-10 (Dashamsha), D-7 (Saptamsha), D-24 (Siddhamsha),
   and D-60 (Shashtyamsha) planetary placements in correlation with D-1 Lagna.
2. Masters' Astrological Formula Bank:
   - K.N. Rao (Double transit of Jupiter & Saturn for marriage/career timing)
   - Pt. Anil Acharya (Navamsha D-9 7th lord & Venus-Mars combinations for love marriage)
   - Dr. Sundeep Kochar (10th lord, Amatyakaraka, and career milestones)
   - Sanjay B. Jumaani (Core Numerology - Mulank, Bhagyank, Name alignment)
   - Deepak Kapoor (Prashna / Horary confirmation principles)
   - Dr. Prem Kumar Sharma & Acharya Indu Prakash (Spiritual & Vastu remedial alignment)
"""
from typing import Dict, List, Tuple
from vyas import constants

def predict_varga(varga_code: str, varga_asc_sign: int, varga_planets: Dict[str, dict], d1_asc_sign: int) -> Dict:
    """
    Generates tailored, high-accuracy predictive synthesis for a specific divisional chart.
    """
    predictions = []
    
    if varga_code == "D9":
        predictions.append("<b>वैवाहिक सुख व दांपत्य जीवन (Marriage & Partner):</b> ")
        ven = varga_planets.get("Venus", {})
        jup = varga_planets.get("Jupiter", {})
        h7_sign = (varga_asc_sign + 6) % 12
        h7_lord = constants.SIGN_LORD[h7_sign]
        
        predictions.append(f"• नवांश लग्न <b>{constants.SIGNS[varga_asc_sign]}</b> में स्थापित है। सप्तम भाव में <b>{constants.SIGNS[h7_sign]}</b> राशि आती है, जिसके स्वामी <b>{h7_lord}</b> हैं।")
        if ven.get("sign_index") in [1, 6, 11]:  # Taurus, Libra, Pisces
            predictions.append("• नवांश में शुक्र स्वराशि अथवा उच्च राशि में होकर अत्यंत रूपवान, सुसंस्कृत एवं निष्ठावान जीवनसाथी का योग बनाता है।")
        else:
            predictions.append(f"• शुक्र नवांश में {ven.get('sign_name', '')} राशि में स्थित है, जो दांपत्य में व्यावहारिक समझदारी व समन्वय की आवश्यकता दर्शाता है।")

        if jup.get("sign_index") in [3, 8, 11]: # Cancer, Sag, Pisces
            predictions.append("• गुरु नवांश में शुभ स्थिति में होकर विवाह उपरांत भाग्योदय और आध्यात्मिक संतोष का प्रबल प्रमाण देता है।")

    elif varga_code == "D10":
        predictions.append("<b>कार्यक्षेत्र, प्रतिष्ठा एवं करियर (Career & Professional Status):</b> ")
        sun = varga_planets.get("Sun", {})
        sat = varga_planets.get("Saturn", {})
        h10_sign = (varga_asc_sign + 9) % 12
        h10_lord = constants.SIGN_LORD[h10_sign]

        predictions.append(f"• दशमांश लग्न <b>{constants.SIGNS[varga_asc_sign]}</b> है। दशम भाव में <b>{constants.SIGNS[h10_sign]}</b> राशि (स्वामी: {h10_lord}) कर्मक्षेत्र में विशिष्ट नेतृत्व क्षमता दर्शाती है।")
        if sun.get("sign_index") in [0, 4]:
            predictions.append("• दशमांश में सूर्य मेष या सिंह में होने से शासन, प्रशासन, उच्च पद अथवा स्वतंत्र व्यवसाय में शीर्ष सफलता प्राप्त होती है।")
        if sat.get("sign_index") in [6, 9, 10]:
            predictions.append("• शनि दशमांश में अनुकूल होकर दीर्घकालीन प्रतिष्ठा, दृढ़ कर्मठता और निरंतर उन्नति का कारक है।")

    elif varga_code == "D7":
        predictions.append("<b>संतान सुख एवं वंश वृद्धि (Children & Lineage):</b> ")
        jup = varga_planets.get("Jupiter", {})
        predictions.append(f"• सप्तमांश लग्न {constants.SIGNS[varga_asc_sign]} पर गुरु व पंचमेश की शुभ रश्मियां संतान पक्ष से सुख, सम्मान और सद्गुणों की प्राप्ति कराती हैं।")

    elif varga_code == "D24":
        predictions.append("<b>उच्च विद्या, बौद्धिक क्षमता एवं अनुसंधान (Higher Education & Wisdom):</b> ")
        merc = varga_planets.get("Mercury", {})
        jup = varga_planets.get("Jupiter", {})
        predictions.append(f"• सिद्धांश (D24) में बुध व गुरु का समन्वय जातक को गहन विश्लेषणात्मक मेधा, त्वरित निर्णय क्षमता एवं शास्त्र/तकनीक में पारंगत बनाता है।")

    elif varga_code == "D60":
        predictions.append("<b>संचित कर्म, प्रारब्ध एवं पराशर सूक्ष्म फल (Past Life Karma & Destiny):</b> ")
        predictions.append("• पराशर मुनि के अनुसार D60 संचित कर्मों का अंतिम दर्पण है। शुभ देवताओं के प्रभाव से कठिन परिस्थितियों में भी अप्रत्याशित दैवीय सहायता प्राप्त होती है।")

    else:
        predictions.append(f"• वर्ग चार्ट {varga_code} का लग्न {constants.SIGNS[varga_asc_sign]} है। यह जीवन के संबंधित आयाम में सूक्ष्म शक्ति व स्थायित्व प्रदान करता है।")

    return {
        "varga": varga_code,
        "asc_sign": constants.SIGNS[varga_asc_sign],
        "narrative": "<br>".join(predictions)
    }

def get_masters_knowledge_bank() -> List[Dict]:
    """Returns curated master formulas from India's greatest astrologers."""
    return [
        {
            "master": "के.एन. राव (K.N. Rao - Classical Legend)",
            "specialty": "डबल गोचर सिद्धांत (Double Transit) एवं चर दशा",
            "formula": "विवाह या संतान जैसी कोई भी प्रमुख जीवन घटना तभी घटित होती है जब गोचर के गुरु और शनि संयुक्त रूप से संबंधित भाव (7th या 5th) अथवा उसके स्वामी को दृष्टि या युति द्वारा सक्रिय करें।"
        },
        {
            "master": "पं. अनिल आचार्य (Pt. Anil Acharya)",
            "specialty": "नवांश (D-9) एवं प्रेम विवाह सूत्र",
            "formula": "D1 और D9 दोनों में शुक्र और मंगल का परस्पर दृष्टि संबंध या नवम-पंचम संबंध जातक को अत्यंत भावुक प्रेम संबंध एवं प्रेम विवाह की ओर अग्रसर करता है, बशर्ते 7वें भाव का स्वामी बली हो।"
        },
        {
            "master": "डॉ. संदीप कोचर (Dr. Sundeep Kochar)",
            "specialty": "करियर माइलस्टोन & अमात्यकारक (AmK)",
            "formula": "जैमिनी अमात्यकारक (AmK) ग्रह जब भी विंशोत्तरी की अंतर्दशा में आता है और D10 के दशम भाव से संबंध बनाता है, तो वह वर्ष जातक के करियर का 'गोल्डन पीरियड' साबित होता है।"
        },
        {
            "master": "संजय बी. जुमानी (Sanjay B. Jumaani)",
            "specialty": "अंक ज्योतिष संरेखण (Numerology Root & Destiny Harmony)",
            "formula": "जातक के जन्म मूलांक और भाग्यांक के मित्र अंकों के अनुसार यदि नाम के अक्षरों का कुल योग (Name Number) सेट किया जाए, तो जीवन में आ रहे अनावश्यक संघर्ष 70% तक घट जाते हैं।"
        },
        {
            "master": "पं. जी.डी. वशिष्ठ (G.D. Vashist - Lal Kitab)",
            "specialty": "अचूक एवं सरल घरेलू लाल किताब उपाय",
            "formula": "कुंडली में सोया हुआ ग्रह जब तक जागृत नहीं किया जाता, तब तक वह निष्क्रिय रहता है। पक्के घर के स्वामी की वस्तुओं का दान या घर में स्थापना कर उसे तुरंत सक्रिय किया जा सकता है।"
        },
        {
            "master": "दीपक कपूर (Deepak Kapoor)",
            "specialty": "प्रश्न ज्योतिष (Horary / Prashna Tantra)",
            "formula": "प्रश्न समय का लग्न कस्पल सब-लॉर्ड यदि कार्येश भाव (जैसे नौकरी के लिए 2, 6, 10, 11) से जुड़ा हो, तो जातक का अभीष्ट कार्य निश्चित रूप से शीघ्र सिद्ध होता है।"
        },
        {
            "master": "डॉ. प्रेम कुमार शर्मा & आचार्य इंदु प्रकाश",
            "specialty": "वास्तु दोष निवारण एवं आध्यात्मिक शांति",
            "formula": "कुंडली का चतुर्थ भाव घर के वास्तु का प्रतिनिधित्व करता है। यदि चतुर्थ भाव पीड़ित हो, तो ईशान कोण (North-East) को शुद्ध कर जल तत्व की स्थापना करने से गृह शांति प्राप्त होती है।"
        }
    ]
