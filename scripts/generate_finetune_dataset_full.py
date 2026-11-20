#!/usr/bin/env python3
"""
VYAS ASTRA — Complete Jyotish SFT Dataset Generator (Full Scale)
Processes all 10,917 normalized sutras from vyas_sutras_fast_index.json
plus verified SFT multi-turn buffer and curated yoga deep-dives.

Produces:
data/finetune_vyas_astrologer_full.jsonl (Standard OpenAI / Groq JSONL)
"""
import os, sys, json, random, re

BASE_DIR = r"g:\software\simpa\VYAS"
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "finetune_vyas_astrologer_full.jsonl")

SYSTEM_PROMPT = (
    "आप आचार्य व्यास (Aacharya Vyas) हैं — महर्षि पराशर, जैमिनी, भृगु, एवं 'प्रश्न मार्ग' के मूर्धन्य वैदिक दैवज्ञ। "
    "आपका ज्ञान शुद्ध खगोलीय गणित एवं प्रामाणिक शास्त्रीय सूत्रों पर आधारित है। "
    "सदा जातक को 'आप/आपका' कहकर अत्यंत आदरपूर्वक सम्बोधित करें (पुत्र/वत्स/तुम वर्जित है)। "
    "स्पष्ट, तर्कसंगत, निर्भीक, सत्यनिष्ठ एवं सात्विक वैदिक उपाय युक्त फलकथन प्रस्तुत करें।"
)

# Phrasing variations for natural user queries
QUERY_TEMPLATES_SIGN = [
    "मेरी कुण्डली में {factor} {clean_cond} है। इसका मेरे जीवन पर क्या प्रभाव पड़ेगा?",
    "यदि जन्म पत्रिका में {factor} {clean_cond} हो तो शास्त्र अनुसार क्या फल मिलता है?",
    "कृपया बताइए कि {clean_cond} होने पर जातक का स्वभाव और भाग्य कैसा रहता है?",
    "मेरी कुण्डली में {clean_cond} की स्थिति है। करियर और आर्थिक स्थिति पर इसका क्या असर होगा?",
]

QUERY_TEMPLATES_HOUSE = [
    "मेरी पत्रिका में {clean_cond} है। इसका क्या फल होगा?",
    "भाव विवेचन अनुसार {clean_cond} होने से जीवन में क्या प्रभाव पड़ता है?",
    "यदि कुण्डली में {clean_cond} विद्यमान हो, तो किस प्रकार के शुभ-अशुभ फल प्राप्त होते हैं?",
    "आचार्य जी, मेरी कुण्डली में {clean_cond} है। कृपया शास्त्रीय विश्लेषण बताएं।",
]

QUERY_TEMPLATES_YUTI = [
    "कुण्डली में {clean_cond} की युति का क्या प्रभाव होता है?",
    "मेरी पत्रिका में {clean_cond} एक साथ बैठे हैं। इसका क्या परिणाम होगा?",
    "शास्त्रों के अनुसार {clean_cond} की युति जातक को कैसा फल प्रदान करती है?",
    "{clean_cond} की युति होने पर क्या विशेष सावधानी या उपाय करना चाहिए?",
]

QUERY_TEMPLATES_DIGNITY = [
    "मेरी कुण्डली में {clean_cond} की स्थिति है। इसका क्या शास्त्रीय अर्थ है?",
    "ग्रह बल के अनुसार {clean_cond} होने पर क्या फल मिलता है?",
    "{clean_cond} के प्रभाव और निवारण के उपाय बताएं।",
]

def clean_condition(cond):
    c = cond.replace(". (कुंडली में यह स्थिति होने पर)", "").strip()
    c = re.sub(r"\s+", " ", c)
    return c

records = []
seen_queries = set()

def add_record(user_query, assistant_reply, category="general"):
    uq = user_query.strip()
    if uq in seen_queries:
        return
    seen_queries.add(uq)
    records.append({
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": uq},
            {"role": "assistant", "content": assistant_reply.strip()}
        ],
        "category": category
    })

# 1. LOAD SFT BUFFER
sft_buffer_path = os.path.join(BASE_DIR, "data", "daivagya_sft", "auto_update_buffer.jsonl")
if os.path.exists(sft_buffer_path):
    print("Loading SFT buffer...")
    with open(sft_buffer_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            try:
                item = json.loads(line.strip())
                if "messages" in item and len(item["messages"]) >= 3:
                    add_record(item["messages"][1]["content"], item["messages"][2]["content"], category="sft_real")
            except:
                pass
    print(f"  Loaded {len(records)} from SFT buffer.")

# 2. PROCESS SUTRAS FAST INDEX (ALL ENTRIES)
fast_index_path = os.path.join(BASE_DIR, "data", "vyas_sutras_fast_index.json")
if os.path.exists(fast_index_path):
    print("Processing all sutras from vyas_sutras_fast_index.json ...")
    with open(fast_index_path, "r", encoding="utf-8") as f:
        sutra_db = json.load(f)

    # 2a. Planet in Signs
    for key, sutras in sutra_db.get("planet_signs", {}).items():
        for i, s in enumerate(sutras):
            cond_hi = s.get("cond_hi", "")
            pred_hi = s.get("pred_hi", "")
            if not cond_hi or not pred_hi or len(pred_hi) < 5: continue
            factor = s.get("factor", "ग्रह")
            src = s.get("src", "बृहत् पराशर होरा शास्त्र")
            domain = s.get("domain", "जीवन फल")
            clean_c = clean_condition(cond_hi)
            
            tmpl = QUERY_TEMPLATES_SIGN[i % len(QUERY_TEMPLATES_SIGN)]
            q = tmpl.format(factor=factor, clean_cond=clean_c)
            
            reply = (
                f"सादर प्रणाम!\n\n"
                f"वैदिक ज्योतिषीय वेध एवं **{src}** के प्रामाणिक सिद्धांत अनुसार:\n\n"
                f"• **शास्त्रीय स्थिति:** {clean_c}\n"
                f"• **फलकथन निर्णय ({domain}):** {pred_hi}\n\n"
                f"**शास्त्रीय दैवज्ञ मार्गदर्शन:**\n"
                f"इस ग्रह स्थिति का पूर्ण प्रकटीकरण सम्बन्धित भाव के भावेश (अधिपति), शुभ दृष्टियों तथा महादशा-अन्तर्दशा चक्र पर निर्भर करता है। यदि ग्रह पर शुभ ग्रहों (गुरु/शुक्र/बली बुध) का प्रभाव हो तो फल में अत्यधिक वृद्धि होती है।\n\n"
                f"**सात्विक उपाय:** सम्बन्धित ग्रह के मूल बीज मंत्र का मानसिक जप करें तथा प्रतिदिन सूर्य देव को जल अर्पित करें।"
            )
            add_record(q, reply, category="planet_sign")

    # 2b. Planet in Houses
    for key, sutras in sutra_db.get("planet_houses", {}).items():
        for i, s in enumerate(sutras):
            cond_hi = s.get("cond_hi", "")
            pred_hi = s.get("pred_hi", "")
            if not cond_hi or not pred_hi or len(pred_hi) < 5: continue
            src = s.get("src", "बृहत् पराशर होरा शास्त्र")
            domain = s.get("domain", "भाव फल")
            clean_c = clean_condition(cond_hi)

            tmpl = QUERY_TEMPLATES_HOUSE[i % len(QUERY_TEMPLATES_HOUSE)]
            q = tmpl.format(clean_cond=clean_c)

            reply = (
                f"सादर प्रणाम!\n\n"
                f"महर्षि पराशर कृत **{src}** के भाव विवेचन नियमानुसार:\n\n"
                f"• **भाव स्थिति:** {clean_c}\n"
                f"• **मुख्य फलदेश ({domain}):** {pred_hi}\n\n"
                f"**दैवज्ञ विवेचना:**\n"
                f"भाव में स्थित ग्रह उस भाव के कारकत्व को संचालित करता है। शुभ भावेश से युति या दृष्टि होने पर यह स्थिति अत्यंत कल्याणकारी सिद्ध होती है।\n\n"
                f"**सात्विक जीवनशैली उपाय:** अपने कर्म और आचरण को सात्विक रखें एवं कुलदेवता अथवा इष्टदेव की नियमित आराधना करें।"
            )
            add_record(q, reply, category="planet_house")

    # 2c. Yutis (Conjunctions)
    for key, sutras in sutra_db.get("yutis", {}).items():
        for i, s in enumerate(sutras):
            cond_hi = s.get("cond_hi", "")
            pred_hi = s.get("pred_hi", "")
            if not cond_hi or not pred_hi or len(pred_hi) < 5: continue
            src = s.get("src", "नाड़ी ज्योतिष संग्रह")
            clean_c = clean_condition(cond_hi)

            tmpl = QUERY_TEMPLATES_YUTI[i % len(QUERY_TEMPLATES_YUTI)]
            q = tmpl.format(clean_cond=clean_c)

            reply = (
                f"सादर प्रणाम!\n\n"
                f"**{src}** के युति तत्व सिद्धांत अनुसार:\n\n"
                f"• **ग्रह युति संयोग:** {clean_c}\n"
                f"• **फलकथन:** {pred_hi}\n\n"
                f"**युति विश्लेषण:** दो ग्रहों की युति में दोनों की परस्पर अंश दूरी (Degree of closeness) अति महत्वपूर्ण होती है। यदि दोनों ग्रह 6 अंश के भीतर हों तो यह युति जातक के जीवन को गहराई से प्रभावित करती है।\n\n"
                f"**शास्त्रीय संबल:** नित्य प्रातः ॐ नमः शिवाय का 1 माला जप मानसिक शांति व ऊर्जा संतुलन हेतु सर्वश्रेष्ठ है।"
            )
            add_record(q, reply, category="yuti")

    # 2d. Dignities
    for key, sutras in sutra_db.get("dignities", {}).items():
        for i, s in enumerate(sutras):
            cond_hi = s.get("cond_hi", "")
            pred_hi = s.get("pred_hi", "")
            if not cond_hi or not pred_hi or len(pred_hi) < 5: continue
            src = s.get("src", "सारावली एवं फलदीपिका")
            clean_c = clean_condition(cond_hi)

            tmpl = QUERY_TEMPLATES_DIGNITY[i % len(QUERY_TEMPLATES_DIGNITY)]
            q = tmpl.format(clean_cond=clean_c)

            reply = (
                f"सादर प्रणाम!\n\n"
                f"शास्त्रीय ग्रंथ **{src}** के ग्रह अवस्था विवेचन अनुसार:\n\n"
                f"• **ग्रह अवस्था:** {clean_c}\n"
                f"• **फलकथन निर्णय:** {pred_hi}\n\n"
                f"**दैवज्ञ उपाय:** ग्रह की निर्बलता अथवा नीच अवस्था होने पर सम्बन्धित ग्रह की वस्तुओं का दान तथा उसके अधिदेवता की उपासना से शुभत्व प्राप्त होता है।"
            )
            add_record(q, reply, category="dignity")

    print(f"  Total records after processing all sutras: {len(records)}")

# 3. APPEND CURATED HIGH-IMPACT YOGA SAMPLES (ALL 50+ VEDIC YOGAS)
from curate_50_yogas import ALL_50_YOGAS_CURATED
for q, a in ALL_50_YOGAS_CURATED:
    add_record(q, a, category="yoga_curated_50")

from generate_finetune_dataset import yoga_curated
for q, a in yoga_curated:
    add_record(q, a, category="yoga_curated")

print(f"\nFinal Total Dataset Size: {len(records):,} records")

# Write out full JSONL
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"Generated: {OUTPUT_FILE}")
print(f"Size: {size_mb:.2f} MB")

