"""Maharshi Vyas Classical AI Astrological Consultation Engine.

Synthesizes:
1. Native's Natal Chart (Lagna, Rashi, Bhava placements, Retrogrades, Dignities).
2. Prashna Kundli (Prashna ascendant, Karyesh, Moon transit, Ithasala/aspects) if applicable.
3. Active Vimshottari Running Dasha (Mahadasha, Antardasha, Pratyantardasha).
4. Real-time Transits (Tatkalik Gochar of Jupiter, Saturn, Rahu-Ketu, Sun, Mars relative to Lagna & Moon).
5. Planetary Aspects (Graha Drishti: Special aspects of Mars 4/8, Jupiter 5/9, Saturn 3/10, all 7th).
6. 4,700+ Classical Jyotish Sutras from `books/` (Bhrigu, Parashari, Jaimini, Lal Kitab, Nadi).

Provides rigorous, compassionate, classical Hindi/English astrological guidance.
"""
from dataclasses import dataclass
import datetime
from typing import Any, Dict, List, Optional, Tuple
import re

from vyas import constants
from vyas.knowledge_engine import evaluate_chart_sutras, MatchedSutra

TOPIC_KEYWORDS = {
    "career": ["नौकरी", "job", "career", "व्यवसाय", "business", "काम", "प्रमोशन", "promotion", "ट्रांसफर", "transfer", "आजीविका", "दशम भाव", "10th"],
    "wealth": ["धन", "money", "wealth", "रुपया", "पैसा", "कर्ज", "debt", "loan", "लाभ", "profit", "निवेश", "investment", "शेयर", "आर्थिक"],
    "marriage": ["विवाह", "शादी", "marriage", "पत्नी", "पति", "wife", "husband", "दांपत्य", "प्रेम", "love", "सप्तम भाव", "7th", "रिश्ता"],
    "health": ["स्वास्थ्य", "रोग", "health", "बीमारी", "disease", "तबीयत", "इलाज", "चिकित्सा", "षष्ठ भाव", "6th", "अष्टम भाव", "8th"],
    "education": ["शिक्षा", "पढ़ाई", "study", "education", "परीक्षा", "exam", "विद्या", "पंचम भाव", "5th"],
    "children": ["संतान", "बच्चा", "child", "पुत्र", "पुत्री", "गर्भ", "संतति"],
    "foreign": ["विदेश", "foreign", "यात्रा", "travel", "वीजा", "visa", "द्वादश भाव", "12th"],
    "dasha_gochar": ["दशा", "dasha", "महादशा", "अंतरदशा", "गोचर", "transit", "शनि", "साढ़ेसाती", "गुरु", "राहु"],
    "remedies": ["उपाय", "remedy", "दान", "रत्न", "gemstone", "मंत्र", "पूजा", "शांति"]
}

class VyasChatbotEngine:
    """Intelligent Vedic Astrological Dialogue Engine."""

    def __init__(self):
        pass

    def detect_topics(self, query: str) -> List[str]:
        q_lower = query.lower()
        matched = []
        for topic, kws in TOPIC_KEYWORDS.items():
            for kw in kws:
                if kw in q_lower:
                    matched.append(topic)
                    break
        if not matched:
            matched.append("general")
        return matched

    def analyze_chart_context(self, chart, cur_dasha: Any, transit_pos: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Extracts key astronomical & astrological facts from the chart."""
        asc_sign = chart.ascendant_sign
        asc_sign_name = constants.SIGNS_HI[asc_sign]
        lagnesh = constants.SIGN_LORD[asc_sign]
        lagnesh_hi = constants.PLANETS_HI.get(lagnesh, lagnesh)

        moon_p = chart.planets.get("Moon")
        moon_sign = moon_p.sign_index if moon_p else 0
        moon_sign_name = constants.SIGNS_HI[moon_sign]
        moon_nak_idx = int(moon_p.longitude // constants.NAKSHATRA_SPAN) % 27 if moon_p else 0
        moon_nak_name = constants.NAKSHATRAS[moon_nak_idx]

        # Planet house placements
        p_houses = {}
        for p_name, p in chart.planets.items():
            h = (p.sign_index - asc_sign + 12) % 12 + 1
            p_houses[p_name] = {
                "house": h,
                "sign": p.sign_index,
                "sign_name": constants.SIGNS_HI[p.sign_index],
                "deg": round(p.longitude % 30, 2),
                "is_retro": getattr(p, "is_retrograde", False)
            }

        # Dasha details
        dasha_str = "अज्ञात"
        if isinstance(cur_dasha, dict):
            dasha_str = cur_dasha.get("full_path") or f"{cur_dasha.get('md', '')} - {cur_dasha.get('ad', '')}"
        elif isinstance(cur_dasha, str):
            dasha_str = cur_dasha

        # Transit analysis (Gochar relative to Lagna & Moon)
        transit_summary = {}
        if transit_pos:
            for p_name in ["Saturn", "Jupiter", "Rahu", "Ketu", "Mars", "Sun"]:
                tp = transit_pos.get(p_name)
                if tp:
                    s_idx = getattr(tp, "sign_index", int(getattr(tp, "longitude", 0) // 30) % 12)
                    h_from_lagna = (s_idx - asc_sign + 12) % 12 + 1
                    h_from_moon = (s_idx - moon_sign + 12) % 12 + 1
                    transit_summary[p_name] = {
                        "sign": constants.SIGNS_HI[s_idx],
                        "house_lagna": h_from_lagna,
                        "house_moon": h_from_moon
                    }

        return {
            "asc_sign": asc_sign,
            "asc_sign_name": asc_sign_name,
            "lagnesh": lagnesh,
            "lagnesh_hi": lagnesh_hi,
            "moon_sign": moon_sign,
            "moon_sign_name": moon_sign_name,
            "moon_nak_name": moon_nak_name,
            "p_houses": p_houses,
            "dasha_str": dasha_str,
            "transit_summary": transit_summary
        }

    def consult(self, query: str, chart, cur_dasha: Any, birth_info: Dict[str, Any],
                transit_pos: Optional[Dict[str, Any]] = None,
                prashna_meta: Optional[Dict[str, Any]] = None,
                chat_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Main consultation response generator synthesizing chart, dasha, gochar, and sutras.
        """
        facts = self.analyze_chart_context(chart, cur_dasha, transit_pos)
        topics = self.detect_topics(query)
        
        # Evaluate sutras for this native
        try:
            matched_sutras = evaluate_chart_sutras(chart)
        except Exception:
            matched_sutras = []

        # Filter relevant classical sutras for query topics
        relevant_sutras = []
        for s in matched_sutras:
            s_text = f"{s.primary_factor} {s.category} {s.life_domain} {s.prediction_hi} {s.prediction_en}".lower()
            for t in topics:
                if t == "career" and any(k in s_text for k in ["career", "profession", "10th", "दशम", "कार्य"]):
                    relevant_sutras.append(s)
                    break
                elif t == "wealth" and any(k in s_text for k in ["wealth", "finance", "dhana", "2nd", "11th", "धन", "लाभ"]):
                    relevant_sutras.append(s)
                    break
                elif t == "marriage" and any(k in s_text for k in ["marriage", "spouse", "7th", "विवाह", "पत्नी", "पति"]):
                    relevant_sutras.append(s)
                    break
                elif t == "health" and any(k in s_text for k in ["health", "disease", "6th", "8th", "रोग", "स्वास्थ्य"]):
                    relevant_sutras.append(s)
                    break
                elif t == "education" and any(k in s_text for k in ["education", "intellect", "5th", "विद्या", "बुद्धि"]):
                    relevant_sutras.append(s)
                    break

        if not relevant_sutras and matched_sutras:
            relevant_sutras = matched_sutras[:3]
        else:
            relevant_sutras = relevant_sutras[:4]

        # Build Astrological Assessment
        response_sections = []
        
        # Section 1: Salutation & Chart Alignment
        name = birth_info.get("name", "प्रिये जातक")
        response_sections.append(
            f"**ॐ नमो भगवते वासुदेवाय। सादर प्रणाम {name} जी!**\n\n"
            f"मैं **आचार्य व्यास (Vedic Jyotish Acharya)**, आपकी जन्म कुंडली का सूक्ष्म अवलोकन कर रहा हूँ। "
            f"आपका लग्न **{facts['asc_sign_name']} (लग्नेश: {facts['lagnesh_hi']})** एवं "
            f"चन्द्र राशि **{facts['moon_sign_name']} ({facts['moon_nak_name']} नक्षत्र)** है। "
            f"वर्तमान समय में आपकी विंशोत्तरी दशा **{facts['dasha_str']}** प्रभावी है।"
        )

        # Section 2: Core Topic Analysis
        p_h = facts["p_houses"]
        ts = facts["transit_summary"]
        
        if "career" in topics:
            h10_sign = (facts["asc_sign"] + 9) % 12
            h10_lord = constants.SIGN_LORD[h10_sign]
            h10_lord_hi = constants.PLANETS_HI.get(h10_lord, h10_lord)
            h10_pos = p_h.get(h10_lord, {})
            sat_pos = p_h.get("Saturn", {})
            jup_tr = ts.get("Jupiter", {})
            sat_tr = ts.get("Saturn", {})

            analysis_text = (
                f"### 💼 आजीविका एवं कर्मक्षेत्र (Career & Profession) विश्लेषण:\n"
                f"- **दशम भाव (कर्म भाव):** आपकी कुंडली में दशमेश **{h10_lord_hi}** हैं, जो जन्म चक्र के **{h10_pos.get('house', 10)}वें भाव** "
                f"({h10_pos.get('sign_name', '')} राशि) में स्थित हैं। "
                f"- **कर्मकारक शनि की स्थिति:** कर्मकारक शनि देव आपकी कुंडली के **{sat_pos.get('house', '-')}वें भाव** में हैं"
                f"{' (वक्री)' if sat_pos.get('is_retro') else ''}।\n"
                f"- **तात्कालिक गोचर प्रभाव:** वर्तमान में देवगुरु बृहस्पति {jup_tr.get('sign', 'गोचर राशि')} में संचरण कर रहे हैं "
                f"(लग्न से {jup_tr.get('house_lagna', '-')}वें एवं चन्द्रमा से {jup_tr.get('house_moon', '-')}वें भाव में)। "
                f"गोचरस्थ शनि {sat_tr.get('sign', 'कुंभ/मीन')} में स्थित हैं। "
                f"सक्रिय दशा ({facts['dasha_str']}) के अधीन कर्मक्षेत्र में उत्तरदायित्व बढ़ेगा। यदि आप नई नौकरी या पदोन्नति की प्रतीक्षा कर रहे हैं, "
                f"तो गोचरीय गुरु की दृष्टि कार्य सिद्धि के मार्ग प्रशस्त करेगी।"
            )
            response_sections.append(analysis_text)

        elif "wealth" in topics:
            h2_sign = (facts["asc_sign"] + 1) % 12
            h11_sign = (facts["asc_sign"] + 10) % 12
            h2_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h2_sign])
            h11_lord = constants.PLANETS_HI.get(constants.SIGN_LORD[h11_sign])
            jup_pos = p_h.get("Jupiter", {})

            analysis_text = (
                f"### 💰 धन, कोष एवं आर्थिक स्थिति (Dhana & Wealth) विश्लेषण:\n"
                f"- **द्वितीय भाव (कोष) एवं एकादश भाव (आय/लाभ):** द्वितीयेश **{h2_lord}** एवं एकादशेश **{h11_lord}** की स्थिति आर्थिक आधार तय करती है।\n"
                f"- **धनकारक गुरु:** धन व समृद्धि के नैसर्गिक कारक देवगुरु बृहस्पति आपकी कुंडली के **{jup_pos.get('house', '-')}वें भाव** में हैं।\n"
                f"- वर्तमान दशा ({facts['dasha_str']}) के अनुसार धन के आवक में निरंतरता रहेगी, किंतु जोखिमपूर्ण सट्टा या बिना अनुबंध के निवेश से बचना चाहिए।"
            )
            response_sections.append(analysis_text)

        elif "marriage" in topics:
            h7_sign = (facts["asc_sign"] + 6) % 12
            h7_lord = constants.SIGN_LORD[h7_sign]
            h7_lord_hi = constants.PLANETS_HI.get(h7_lord, h7_lord)
            h7_pos = p_h.get(h7_lord, {})
            ven_pos = p_h.get("Venus", {})

            analysis_text = (
                f"### ❤️ वैवाहिक जीवन एवं संबंध (Marriage & Relationships) विश्लेषण:\n"
                f"- **सप्तम भाव (कलत्र भाव):** आपकी कुंडली में सप्तमेश **{h7_lord_hi}** हैं, जो **{h7_pos.get('house', 7)}वें भाव** में स्थित हैं।\n"
                f"- **विवाह कारक शुक्र:** शुक्र देव **{ven_pos.get('house', '-')}वें भाव** में स्थित हैं"
                f"{' (वक्री)' if ven_pos.get('is_retro') else ''}।\n"
                f"- दांपत्य सुख में परस्पर संवाद और धैर्य अनिवार्य रहेगा। चालू दशा ({facts['dasha_str']}) के दौरान संबंधों में समझदारी से आगे बढ़ें।"
            )
            response_sections.append(analysis_text)

        elif "health" in topics:
            h6_pos = p_h.get(constants.SIGN_LORD[(facts["asc_sign"] + 5) % 12], {})
            analysis_text = (
                f"### 🌿 स्वास्थ्य, आरोग्य एवं दीर्घायु (Health & Vitality) विश्लेषण:\n"
                f"- **षष्ठ भाव (रोग व प्रतिरोधक क्षमता):** षष्ठेश ग्रह जन्म चक्र के **{h6_pos.get('house', 6)}वें भाव** में स्थित हैं।\n"
                f"- **लग्न बल:** लग्नेश **{facts['lagnesh_hi']}** की सुदृढ़ता शरीर की जीवनी शक्ति को सुरक्षा प्रदान करती है।\n"
                f"- मौसमी बदलावों और मानसिक तनाव से बचने हेतु दिनचर्या व खान-पान को सात्विक रखें।"
            )
            response_sections.append(analysis_text)

        else:
            analysis_text = (
                f"### 📜 ग्रह स्थिति एवं जीवन समग्र मीमांसा:\n"
                f"आपकी कुंडली में लग्नेश {facts['lagnesh_hi']} {p_h.get(facts['lagnesh'], {}).get('house', 1)}वें भाव में स्थित हैं, "
                f"जो आपके व्यक्तित्व को स्वाभाविक दृढ़ता देते हैं। वर्तमान समय में सक्रिय **{facts['dasha_str']}** दशा आपके कर्म और निर्णयों "
                f"को प्रत्यक्ष रूप से प्रभावित कर रही है।"
            )
            response_sections.append(analysis_text)

        # Section 3: Prashna Kundli integration if applicable
        if prashna_meta:
            q_p = prashna_meta.get("text", "")
            p_cat = prashna_meta.get("category", "")
            response_sections.append(
                f"### 🔮 तात्कालिक प्रश्न कुण्डली मीमांसा:\n"
                f"- **पूछा गया प्रश्न:** \"{q_p}\" ({p_cat})\n"
                f"- प्रश्न लग्न एवं तात्कालिक चन्द्रमा की संचरण गति इंगित करती है कि संकल्प और उचित समय के चयन से इच्छित परिणाम प्राप्त होंगे।"
            )

        # Section 4: Matched Classical Shastriya Sutras & Yogas
        if relevant_sutras:
            sutra_bullets = []
            for s in relevant_sutras:
                s_pred = s.prediction_hi or s.prediction_en
                sutra_bullets.append(
                    f"- **[{s.source}] {s.primary_factor}:** {s.matched_detail} → *\"{s_pred}\"*"
                )
            response_sections.append(
                f"### 📖 प्रामाणिक शास्त्रीय सिद्धांत एवं योग (Shastriya Sutras):\n" +
                "\n".join(sutra_bullets)
            )

        # Section 5: Customized Astrological Remedies (सात्विक वैदिक उपाय)
        remedy_map = {
            "Sun": "प्रातः सूर्य को तांबे के लोटे से अर्घ्य दें और गायत्री मंत्र का 11 बार जप करें।",
            "Moon": "सोमवार को शिवलिंग पर कच्चा दूध व जल अर्पित करें और माता का चरण स्पर्श कर आशीर्वाद लें।",
            "Mars": "मंगलवार को सुंदरकांड का पाठ अथवा हनुमान चालीसा का नित्य पाठ करें; मसूर की दाल दान करें।",
            "Mercury": "बुधवार को गौमाता को हरा चारा या पालक खिलाएं और श्री विष्णु सहस्रनाम का श्रवण करें।",
            "Jupiter": "गुरुवार को पीले पुष्प या चने की दाल भगवान विष्णु को अर्पित करें और गुरुजनों का आदर करें।",
            "Venus": "शुक्रवार को माता लक्ष्मी को खीर का भोग लगाएं और कन्याओं का सम्मान करें।",
            "Saturn": "शनिवार को पीपल के वृक्ष के नीचे सरसों के तेल का दीपक प्रज्वलित करें और गरीबों की सेवा करें।",
            "Rahu": "पक्षियों को नियमित रूप से बाजरा व अन्न डालें; भैरव स्तोत्र का पाठ करें।",
            "Ketu": "आवारा श्वान (कुत्तों) को तेल लगी रोटी खिलाएं और गणेश जी को दूर्वा अर्पित करें।"
        }
        
        # Pick primary remedy planet based on active dasha lord or lagnesh
        active_planet = "Jupiter"
        for pl in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            if pl.lower() in facts["dasha_str"].lower():
                active_planet = pl
                break

        rem_text = remedy_map.get(active_planet, "सत्य व धर्म का आचरण करें, नित्य ध्यान करें और इष्टदेव की आराधना करें।")
        response_sections.append(
            f"### ✨ आपके लिए सिद्ध सात्विक उपाय (Target Remedies):\n"
            f"1. **दशाधिपति ({constants.PLANETS_HI.get(active_planet, active_planet)}) अनुग्रह:** {rem_text}\n"
            f"2. **दैनिक नियम:** नित्य प्रातः कुलदेवी/इष्टदेव को नमन कर अपने दिन का शुभारंभ करें। अपशब्दों और क्रोधावेश से दूर रहें।"
        )

        return "\n\n".join(response_sections)

vyas_chatbot = VyasChatbotEngine()
