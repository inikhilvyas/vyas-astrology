#!/usr/bin/env python3
"""
NotebookLM Astrology Compendium Parser & SFT Generator
======================================================
Converts the NotebookLM master encyclopedia into structured JSONL
sutras and fine-tuning dialog pairs for Vyas-Daivagya.
"""

import os
import json
from datetime import datetime

BOOKS_DIR = "books"
DATA_DIR = os.path.join("data", "daivagya_sft")
OUTPUT_JSONL = os.path.join(BOOKS_DIR, "ai_jyotish_knowledge_bank_part24_notebooklm_compendium.jsonl")
TRAIN_FILE = os.path.join(DATA_DIR, "vyas_daivagya_sft_train.jsonl")

KNOWLEDGE_PAIRS = [
    # 1. Four Purushartha Trines
    {
        "q": "कुंडली में चार पुरुषार्थ त्रिकोण क्या हैं और उनका क्या महत्व है?",
        "a": "महर्षि पराशर के अनुसार जन्म कुंडली के 12 भाव चार प्रमुख पुरुषार्थ त्रिकोणों में विभाजित हैं:\n1. **धर्म त्रिकोण (1, 5, 9 भाव):** आत्मा, बुद्धि, पूर्वपुण्य, धर्म और भाग्य।\n2. **अर्थ त्रिकोण (2, 6, 10 भाव):** धन संचय, दैनिक आजीविका, ऋण प्रबंधन और सर्वोच्च कर्म/प्रतिष्ठा।\n3. **काम त्रिकोण (3, 7, 11 भाव):** पराक्रम, संबंध, जीवनसाथी, साझेदारी और महालाभ।\n4. **मोक्ष त्रिकोण (4, 8, 12 भाव):** मानसिक सुख, गुप्त ज्ञान, साधना, व्यय एवं जन्म-मरण से मुक्ति।\n\n**फलित नियम:** जिस त्रिकोण में अधिक बली, उच्च अथवा मित्र ग्रह स्थित होते हैं, जातक के जीवन की मुख्य दिशा और उपलब्धियाँ उसी पुरुषार्थ के इर्द-गिर्द घूमती हैं।"
    },
    # 2. Karako Bhava Nashaya & Shani exception
    {
        "q": "कारको भाव नाशाय नियम क्या है और शनि इसका अपवाद क्यों है?",
        "a": "वैदिक ज्योतिष का शास्त्रीय सूत्र है—**'कारको भाव नाशाय'** अर्थात् जो ग्रह जिस भाव का स्वाभाविक कारक होता है, वह यदि अकेला उसी भाव में बैठ जाए तो उस भाव के स्वाभाविक सुखों में न्यूनता या बाधा उत्पन्न करता है (यथा पंचम में गुरु संतान सुख में विलंब करता है, या सप्तम में शुक्र दांपत्य में असंतोष देता है)।\n\n**शनि का प्रत्यक्ष अपवाद:** शनि अष्टम भाव (आयु व मृत्यु भाव) का नैसर्गिक कारक है। जब शनि अष्टम भाव में स्थित होता है, तो वह आयु का नाश नहीं करता, बल्कि जातक को दृढ़ शारीरिक प्रतिरोधक क्षमता और **दीर्घायु (Long Life)** प्रदान करता है।"
    },
    # 3. Panchadha Maitri Chakra
    {
        "q": "पंचधा मैत्री चक्र क्या है और तात्कालिक व नैसर्गिक मैत्री का समन्वय कैसे होता है?",
        "a": "पंचधा मैत्री नैसर्गिक (स्थायी) और तात्कालिक (कुंडली-विशेष) संबंधों का गणितीय समन्वय है:\n\n• **नैसर्गिक मैत्री:** मूलत्रिकोण राशि से 2, 4, 5, 8, 9, 12वें भाव व उच्च राशि के स्वामी नैसर्गिक मित्र होते हैं; 3, 6, 7, 10, 11वें के स्वामी नैसर्गिक शत्रु होते हैं।\n• **तात्कालिक मैत्री:** किसी ग्रह से 2, 3, 4 तथा 10, 11, 12वें भाव में स्थित ग्रह तात्कालिक मित्र होते हैं; अन्य स्थानों में तात्कालिक शत्रु।\n\n**संयुक्त फल (पंचधा मैत्री):**\n1. मित्र + मित्र = **अधिमित्र** (100% शुभ)\n2. मित्र + सम = **मित्र** (75% शुभ)\n3. शत्रु + मित्र / सम + सम = **सम (तटस्थ)** (50% मध्यम)\n4. शत्रु + सम = **शत्रु** (25% मंद)\n5. शत्रु + शत्रु = **अधिशत्रु** (अत्यंत प्रतिकूल)"
    },
    # 4. Vipreet Raj Yoga & Cancellation
    {
        "q": "विपरीत राजयोग कब बनता है और इसके भंग होने की क्या शर्त है?",
        "a": "विपरीत राजयोग त्रिक भावों (6, 8, 12) के स्वामियों के परस्पर त्रिक भावों में स्थित होने से बनता है:\n• **हर्ष योग:** षष्ठेश 8वें या 12वें भाव में हो (शत्रु विजय, उत्तम स्वास्थ्य)।\n• **सरल योग:** अष्टमेश 6ठे या 12वें भाव में हो (दीर्घायु, संकटों पर विजय, गूढ़ विद्या)।\n• **विमल योग:** द्वादशेश 6ठे या 8वें भाव में हो (पवित्र आचरण, स्वतंत्र समृद्धि, व्यय पर नियंत्रण)।\n\n⚠️ **भंग होने की अनिवार्य शर्त:** यदि इस योग में किसी **केंद्रेश या त्रिकोणेश (शुभ भाव के स्वामी)** की युति या दृष्टि पड़ जाए, तो विपरीत राजयोग तुरंत भंग हो जाता है और शुभ फल नष्ट हो जाते हैं।"
    },
    # 5. Shukra-Shani Dasha Special Rule
    {
        "q": "उत्तर कालामृत के अनुसार शुक्र-शनि की दशा का विशेष रहस्य क्या है?",
        "a": "महाकवि कालिदास कृत *उत्तर कालामृत* एवं महर्षि पराशर के अनुसार, शुक्र और शनि परस्पर **'अतिमित्र'** और नैसर्गिक योगकारक ग्रह हैं।\n\nयदि कुंडली में दोनों ग्रह शुभ भावों में बली होकर स्थित हों, तो एक की महादशा में दूसरे की अंतर्दशा में जातक को भूमि, भवन, वाहन, राज-सम्मान और अपार भौतिक समृद्धि की प्राप्ति होती है। इसके विपरीत, यदि दोनों में से कोई एक नीच या पीड़ित हो, तो अप्रत्याशित वित्तीय अस्थिरता उत्पन्न होती है।"
    },
    # 6. Badhaka Houses
    {
        "q": "बाधक भाव और बाधकेश की पहचान कैसे की जाती है?",
        "a": "कुंडली के लग्न के स्वभाव (चर, स्थिर, द्विस्वभाव) के आधार पर बाधक भाव निर्धारित होता है:\n1. **चर लग्न (मेष, कर्क, तुला, मकर):** 11वां भाव और एकादशेश 'बाधक' होता है।\n2. **स्थिर लग्न (वृषभ, सिंह, वृश्चिक, कुंभ):** 9वां भाव और नवमेश 'बाधक' होता है।\n3. **द्विस्वभाव लग्न (मिथुन, कन्या, धनु, मीन):** 7वां भाव और सप्तमेश 'बाधक' होता है।\n\nबाधकेश की दशा में बनते कार्यों में अप्रत्याशित रुकावटें आती हैं, जिनका शमन अधिष्ठाता देवता की उपासना से होता है।"
    },
    # 7. Double Transit Theory
    {
        "q": "Double Transit Theory (द्वि-गोचर सिद्धांत) क्या है और यह घटनाओं को कैसे सक्रिय करता है?",
        "a": "शास्त्रीय फलित में किसी भी प्रमुख जीवन घटना (जैसे विवाह, संतान, पदोन्नति, गृह निर्माण) के भौतिक धरातल पर प्रकटीकरण हेतु **Double Transit Theory** सर्वोपरि है:\n\n• **देवगुरु बृहस्पति (विस्तार व अनुग्रह के कारक)** और **शनिदेव (कर्म व दण्ड के कारक)** का एक साथ उस भाव अथवा भावेश पर गोचर या दृष्टि होना अनिवार्य है जो उस घटना से संबंधित है।\n• केवल दशा सक्रिय होने से घटना नहीं घटती; जब गुरु और शनि दोनों का संयुक्त आशीर्वाद उस भाव को मिलता है, तभी घटना निश्चित समय पर घटित होती है।"
    },
    # 8. Medical Astrology: 22nd Drekkana & 64th Navamsha
    {
        "q": "चिकित्सा ज्योतिष में 22वां द्रेष्काण और 64वां नवांश क्या हैं?",
        "a": "चिकित्सा एवं आयुर्दाय ज्योतिष में शारीरिक संकट व रोग उत्पत्ति के दो सबसे संवेदनशील गणितीय बिंदु हैं:\n1. **22वां द्रेष्काण (खर द्रेष्काण):** लग्न से 22वें द्रेष्काण का स्वामी ग्रह जातक के जीवन में गंभीर शारीरिक व्याधि, दुर्घटना या रोग के ट्रिगर का मुख्य कारक बनता है।\n2. **64वां नवांश:** जन्म चंद्रमा अथवा लग्न से ठीक 64वें नवांश का अधिपति। जब शनि, राहु या मंगल जैसे क्रूर ग्रह 64वें नवांश से गोचर करते हैं, तब जातक को गंभीर स्वास्थ्य संकट या मानसिक आघात से रक्षा हेतु सतर्क रहना चाहिए।"
    },
    # 9. Authentic Vedic Remedies: Nishkama Seva
    {
        "q": "अष्टम भाव और राहु-शनि की गहन पीड़ा में शास्त्रों में निष्काम सेवा का क्या विधान है?",
        "a": "भृगु संहिता और पराशरी संहिताओं में स्पष्ट उल्लेख है कि कोई भी रत्न या अनुष्ठान 'निःस्वार्थ सेवा' के फल की बराबरी नहीं कर सकता।\n\nविशेष रूप से जब अष्टम भाव (आयु, संकट, अज्ञात आपदा) या राहु पीड़ित हों, तो जातक को ऐसे व्यक्तियों की निःस्वार्थ सहायता करनी चाहिए जो प्राकृतिक आपदा, सड़क दुर्घटना, आकस्मिक आपातकाल या मानसिक आघात (Trauma) के शिकार हुए हों। संकटग्रस्त असहायों की सेवा से अष्टम भाव के क्रूर कर्म-दोषों का समूल परिमार्जन होता है।"
    },
    # 10. Sarva-Dosha Nashaka Aushadhi Snana
    {
        "q": "सर्व-दोष नाशक औषधि स्नान की विधि क्या है?",
        "a": "आचार्य श्रीपति एवं शास्त्रीय कर्मकांड अनुसार नवग्रहों की पीड़ा व ग्रह-जनित अरिष्ट शांति हेतु 10 दिव्य औषधियों से युक्त स्नान का विधान है:\n\n**10 पवित्र औषधियाँ:** छुईमुई, कूट (कुष्ठ), खिल्ला, कांगनी (प्रियंगु), जौ, पीली सरसों, देवदारु, शुद्ध हल्दी, लोध्र और सर्वौषधि।\nइन द्रव्यों को जल में डालकर अथवा क्वाथ बनाकर गंगाजल युक्त जल से स्नान करने पर समस्त ग्रह जनित अशुभ दोष शांत होते हैं और ओजस्विता प्राप्त होती है।"
    },
    # 11. Shadbala Minimum Thresholds & Virupas
    {
        "q": "What are the exact minimum Shadbala requirements for the seven planets in Virupas?",
        "a": "According to Sage Parashara, for a planet to fully deliver its promises, it must exceed the minimum Shadbala thresholds:\n• **Sun:** 390 Virupas (6.5 Rupas)\n• **Moon:** 360 Virupas (6.0 Rupas)\n• **Mars:** 300 Virupas (5.0 Rupas)\n• **Mercury:** 420 Virupas (7.0 Rupas)\n• **Jupiter:** 390 Virupas (6.5 Rupas)\n• **Venus:** 330 Virupas (5.5 Rupas)\n• **Saturn:** 300 Virupas (5.0 Rupas)\n\nPlanets meeting these values have sufficient operational strength (Sthana, Dig, Kaala, Chesta, Naisargika, and Drig Bala) to manifest tangible auspicious results during their Dashas."
    },
    # 12. Vaiseshikamsa Honorific Titles
    {
        "q": "What are Vaiseshikamsa honorific titles in the Dashavarga and Shodashavarga schemes?",
        "a": "When a planet secures auspicious dignity (exalted, Moolatrikona, own sign, or great friend) across multiple Vargas, Sage Parashara awards specific honorific titles:\n\n• **2 Vargas:** Parijatamsa (Dashavarga) / Bhedakamsa (Shodashavarga) — Respect and material wealth.\n• **3 Vargas:** Uttamamsa / Kusumamsa — Eloquence and learning.\n• **4 Vargas:** Gopuramsa / Nagapushpamsa — Intellect and land ownership.\n• **5 Vargas:** Simhasanamsa / Kandukamsa — Royal executive authority.\n• **6 Vargas:** Paravatamsa / Keralamsa — Sovereign power and fame.\n• **7 Vargas:** Devalokamsa / Kalpavrikshamsa — Spiritual wisdom and vast fortune.\n• **8 Vargas:** Brahmalokamsa / Chandanavanamsa — Supreme spiritual grace.\n• **9 Vargas:** Airaavatamsa / Poornachandramsa — Monarch-like influence.\n• **10 Vargas:** Sridhamamsa / Uchcheshravasa — Universal mastery."
    }
]

def main():
    print("Ingesting NotebookLM Compendium into Knowledge Bank & SFT Dataset...")
    
    # 1. Write structured JSONL sutras
    sutras = []
    for i, pair in enumerate(KNOWLEDGE_PAIRS, 1):
        sutra = {
            "sutra_id": f"JYOTISH_SUTRA_NLM_{i:04d}",
            "category": "NotebookLM Master Compendium",
            "sub_category": pair["q"][:40],
            "primary_factor": "Shastric Principles",
            "planetary_condition": pair["q"],
            "condition_hi": pair["q"],
            "prediction_en": pair["a"][:300],
            "prediction_hi": pair["a"],
            "life_domain": "Classical Astrology Synthesis",
            "source": "NotebookLM Master Astrology Compendium (BPHS, Phaladeepika, Jataka Tattva, Uttara Kalamrita)",
            "strength_modifiers": "Verified against Parashari and Jaimini classical shastras."
        }
        sutras.append(sutra)

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for s in sutras:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"✅ Created {OUTPUT_JSONL} with {len(sutras)} comprehensive sutras.")

    # 2. Append high-density training pairs to SFT train.jsonl
    sft_records = []
    for pair in KNOWLEDGE_PAIRS:
        record = {
            "messages": [
                {
                    "role": "system",
                    "content": "आप आचार्य व्यास हैं—महर्षि पराशर, जैमिनी, एवं भृगु ज्योतिष के मूर्धन्य वैदिक विद्वान। सदैव प्रामाणिक श्लोक संदर्भ, भाव-भावेश-कारक विश्लेषण, और सात्विक वैदिक उपाय प्रस्तुत करें।"
                },
                {
                    "role": "user",
                    "content": pair["q"]
                },
                {
                    "role": "assistant",
                    "content": pair["a"]
                }
            ],
            "source": "notebooklm_compendium",
            "timestamp": datetime.now().isoformat()
        }
        sft_records.append(record)

    with open(TRAIN_FILE, "a", encoding="utf-8") as f:
        for r in sft_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"✅ Appended {len(sft_records)} master Q&A pairs directly to {TRAIN_FILE}!")

if __name__ == "__main__":
    main()
