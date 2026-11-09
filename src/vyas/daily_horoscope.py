"""Hyper-Personalised Daily Horoscope Engine (दैनिक व्यक्तिगत राशिफल).

Combines:
1. 27-Navatara Chakra (3-Paryaya: Janma, Sampat, Vipat, Kshema, Pratyari, Sadhak, Vadha, Mitra, Ati-Mitra)
   calibrated to realistic 40% - 75% relative bounds.
2. Active 5-Tier Vimshottari Running Dasha (MD -> AD -> PD -> SD -> PrD).
3. Shani Gochar (साढ़े साती - 3 चरण & ढैया - कंटक/अष्टम).
4. Chandra Gochar (विशेष रूप से चतुर्थ चन्द्रमा & चन्द्रअष्टम).
5. Location-precise astronomical Muhurta & Chaughadiya.
"""
from datetime import datetime, timezone
from typing import Dict, Tuple, Any
from vyas import constants
from vyas.ephem import planet_positions

NAVATARA_NAMES = [
    ("Janma (जन्म तारा)", "मिश्रित - शारीरिक व मानसिक सजगता रखें, दिन सामान्य रहेगा।", 54, "neutral"),
    ("Sampat (संपत तारा)", "शुभ - धन, संसाधन एवं नए कार्यों में अनुकूलता प्राप्त होगी।", 72, "good"),
    ("Vipat (विपत तारा)", "सावधानी - जोखिम भरे निवेश, विवाद व अनावश्यक यात्रा से बचें।", 44, "bad"),
    ("Kshema (क्षेम तारा)", "कल्याणकारी - पारिवारिक सुख, कार्य सिद्धि व मानसिक शांति।", 70, "good"),
    ("Pratyari (प्रत्यरि तारा)", "बाधा सूचक - विरोधियों से सतर्क रहें, नए निर्णय टालें।", 46, "bad"),
    ("Sadhak (साधक तारा)", "सिद्धिदायक - महत्वपूर्ण मीटिंग, साक्षात्कार व लक्ष्य प्राप्ति में प्रगति।", 74, "good"),
    ("Vadha (वध तारा)", "प्रतिकूल - स्वास्थ्य का विशेष ध्यान रखें, वाहन सतर्कता से चलाएं।", 40, "bad"),
    ("Mitra (मित्र तारा)", "सहयोगकारी - मित्रों से सहायता, सुखद संवाद व सौहार्द बना रहेगा।", 68, "good"),
    ("Ati-Mitra (अति-मित्र तारा)", "अति उत्तम - अटके कार्यों में गति व सम्मान प्राप्त होगा।", 73, "good")
]

NAVATARA_EN_MAP = {
    0: ("Janma (Birth Tara)", "Identity and mental state. Maintain calm and avoid hasty moves."),
    1: ("Sampat (Wealth Tara)", "Highly auspicious for financial growth, prosperity, and gains."),
    2: ("Vipat (Hazard Tara)", "Minor delays or hindrances. Double-check all commitments."),
    3: ("Kshema (Well-being Tara)", "Protection, comfort, domestic peace, and stable progress."),
    4: ("Pratyari (Obstacle Tara)", "Differing opinions possible. Keep discussions constructive."),
    5: ("Sadhak (Success Tara)", "Great for goal execution, professional accomplishments, and focus."),
    6: ("Vadha (Danger Tara)", "Extreme care advised. Defer speculative or high-risk bets."),
    7: ("Mitra (Friendly Tara)", "Cordiality, enjoyable conversations, and cooperative allies."),
    8: ("Ati-Mitra (Intimate Friendly Tara)", "Excellent - rapid progress in stalled tasks and widespread respect.")
}

def calculate_navatara(natal_moon_nak_idx: int, transit_moon_nak_idx: int) -> Tuple[int, str, str, int, str]:
    distance_27 = (transit_moon_nak_idx - natal_moon_nak_idx + 27) % 27
    tara_idx = distance_27 % 9
    name, desc, score, category = NAVATARA_NAMES[tara_idx]
    paryaya = (distance_27 // 9) + 1
    return tara_idx, f"{name} (पर्याय {paryaya})", desc, score, category

def evaluate_shani_gochar(natal_moon_lon: float, today_date: datetime) -> Dict[str, Any]:
    """Computes exact Sade Sati and Dhaiya state based on transit Saturn."""
    try:
        t_utc = today_date if today_date.tzinfo else today_date.replace(tzinfo=timezone.utc)
        cur_pos = planet_positions(t_utc)
        transit_saturn_lon = cur_pos["Saturn"].longitude
    except Exception:
        transit_saturn_lon = 344.5  # Saturn in Meena / Kumbha border

    natal_moon_sign = int(natal_moon_lon // 30) % 12
    transit_saturn_sign = int(transit_saturn_lon // 30) % 12
    diff_from_moon = (transit_saturn_sign - natal_moon_sign + 12) % 12

    if diff_from_moon == 11:
        return {
            "has_shani_effect": True,
            "type": "साढ़े साती (प्रथम चरण)",
            "type_en": "Sade Sati (1st Phase - Inception)",
            "impact_score": -6,
            "is_adverse": True,
            "desc": "द्वादश भाव में शनि का संचरण (साढ़े साती की शुरुआत) - अकारण व्यय, दूरगामी योजनाएं व मानसिक भागदौड़ की स्थिति बनी रहती है।",
            "desc_en": "Saturn transiting 12th from Moon (Inception Phase) - Potential expenditure, distant plans, and restlessness."
        }
    elif diff_from_moon == 0:
        return {
            "has_shani_effect": True,
            "type": "साढ़े साती (द्वितीय चरण - शिखर)",
            "type_en": "Sade Sati (2nd Phase - Peak)",
            "impact_score": -9,
            "is_adverse": True,
            "desc": "जन्म चन्द्रमा पर शनि का प्रत्यक्ष संचरण (साढ़े साती शिखर) - कार्यभार, अनुशासन एवं धैर्य की परीक्षा। स्वास्थ्य व मनोबल का संतुलन रखें।",
            "desc_en": "Saturn directly over natal Moon (Peak Phase) - Test of patience, discipline, and stamina. Maintain emotional balance."
        }
    elif diff_from_moon == 1:
        return {
            "has_shani_effect": True,
            "type": "साढ़े साती (तृतीय चरण - उतरती)",
            "type_en": "Sade Sati (3rd Phase - Setting)",
            "impact_score": -5,
            "is_adverse": True,
            "desc": "द्वितीय भाव में शनि का गोचर (उतरती साढ़े साती) - आर्थिक नियंत्रण एवं वाणी में सौम्यता बनाए रखना हितकर रहेगा।",
            "desc_en": "Saturn in 2nd from Moon (Setting Phase) - Financial prudence and temperate speech recommended."
        }
    elif diff_from_moon == 3:
        return {
            "has_shani_effect": True,
            "type": "शनि की कंटक ढैया (चतुर्थ शनि)",
            "type_en": "Kantaka Dhaiya (4th Saturn)",
            "impact_score": -7,
            "is_adverse": True,
            "desc": "चतुर्थ भाव में शनि का गोचर (कंटक ढैया) - घरेलू उत्तरदायित्वों में वृद्धि, संपत्ति व मानसिक शांति हेतु सजगता आवश्यक।",
            "desc_en": "Saturn in 4th from Moon - Heightened domestic duties; focus on mental calm and peace."
        }
    elif diff_from_moon == 7:
        return {
            "has_shani_effect": True,
            "type": "शनि की अष्टम ढैया",
            "type_en": "Ashtama Dhaiya (8th Saturn)",
            "impact_score": -8,
            "is_adverse": True,
            "desc": "अष्टम भाव में शनि का गोचर (अष्टम ढैया) - आकस्मिक विघ्न, यात्रा व स्वास्थ्य के प्रति विशेष सावधानी अपेक्षित है।",
            "desc_en": "Saturn in 8th from Moon - Unanticipated roadblocks; exercise caution in travel and well-being."
        }
    else:
        return {
            "has_shani_effect": False,
            "type": "शनि गोचर अनुकूल/तटस्थ",
            "type_en": "Favourable / Neutral Saturn Transit",
            "impact_score": 0,
            "is_adverse": False,
            "desc": "वर्तमान में आपकी राशि पर शनि की साढ़े साती अथवा ढैया का कोई प्रत्यक्ष प्रतिकूल प्रभाव नहीं है।",
            "desc_en": "No adverse Sade Sati or Dhaiya transit active on your Moon sign at present."
        }

def evaluate_chandra_gochar(natal_moon_lon: float, transit_moon_lon: float) -> Dict[str, Any]:
    """Computes Moon's transit relative to natal Moon, with emphasis on 4th Moon & Chandrashtama."""
    natal_rashi = int(natal_moon_lon // 30) % 12
    transit_rashi = int(transit_moon_lon // 30) % 12
    cg_house = (transit_rashi - natal_rashi + 12) % 12 + 1

    chandra_gochar_data = {
        1: ("मानसिक ऊर्जा व आत्म-सजगता", "चन्द्रमा का जन्म राशि में संचरण मनोभावों को संवेदनशील बनाता है। अपने स्वास्थ्य व भोजन पर ध्यान दें।", 1, False, False, "Mental Energy & Awareness", "Moon in natal sign heightens emotions. Focus on nutrition and well-being."),
        2: ("धन एवं वाणी विचार", "द्वितीय भाव में चन्द्रमा आर्थिक लेन-देन व पारिवारिक संवाद का संकेत देता है। कटु वचनों से बचें।", 2, False, False, "Finances & Speech Consideration", "Moon in 2nd denotes financial discussions. Maintain gracious speech."),
        3: ("पराक्रम, भ्रातृ सुख व साहस", "तृतीय भाव में चन्द्रमा अत्यंत शुभ फलदायी होता है। पराक्रम व संपर्क शक्ति में वृद्धि होगी।", 5, False, False, "Enterprise, Siblings & Courage", "Moon in 3rd is highly favourable for proactive initiatives and communications."),
        4: ("चतुर्थ चन्द्रमा (सावधानी)", "⚠️ चतुर्थ भाव में चन्द्रमा मानसिक उद्वेग, घरेलू असंतोष या अनिद्रा का कारक बनता है। महत्वपूर्ण निर्णय धैर्य से लें व वाहन सावधानी से चलाएं।", -7, True, False, "4th Moon (Caution)", "⚠️ Moon in 4th may cause emotional turbulence. Decide patiently and drive carefully."),
        5: ("विद्या, बुद्धि व रचनात्मकता", "पंचम भाव में चन्द्रमा बौद्धिक क्षमता व निर्णय शक्ति को तीव्र करता है।", 3, False, False, "Intellect, Wisdom & Creativity", "Moon in 5th enhances creative intuition and sharp analytical insight."),
        6: ("शत्रु शमन, प्रतियोगिता व आरोग्य", "षष्ठ भाव में चन्द्रमा रोगों व विरोधियों पर विजय दिलाता है। शुभ गोचर फल।", 4, False, False, "Overcoming Hurdles & Vitality", "Moon in 6th brings triumph over competitors and resolving chronic issues."),
        7: ("साझेदारी, दांपत्य व जनसंपर्क", "सप्तम भाव में चन्द्रमा दांपत्य जीवन व व्यापारिक साझेदारों से समन्वय में सहायक होता है।", 2, False, False, "Partnerships & Alliances", "Moon in 7th promotes positive rapport with partners and associates."),
        8: ("चन्द्रअष्टम (अष्टम चन्द्रमा - विशेष सतर्कता)", "⚠️ अष्टम भाव में चन्द्रमा (चन्द्रअष्टम) मानसिक तनाव, कार्य-बाधा व अप्रत्याशित खर्च ला सकता है। आज जोखिम भरे कार्य टालें।", -9, False, True, "Chandrashtama (8th Moon - Vigilance)", "⚠️ Moon in 8th (Chandrashtama) can cause unexpected hurdles. Avoid high-risk actions."),
        9: ("भाग्य, धर्म व आत्मिक उन्नति", "नवम भाव में चन्द्रमा भाग्य का सहयोग देता है। धार्मिक चिंतन से बिगड़े काम बनेंगे।", 4, False, False, "Fortune, Virtue & Spiritual Alignment", "Moon in 9th unlocks providential support and purposeful endeavors."),
        10: ("कर्मक्षेत्र, प्रतिष्ठा व प्रभाव", "दशम भाव में चन्द्रमा कार्यक्षेत्र में आपकी प्रतिष्ठा व प्रभाव को बढ़ाता है।", 5, False, False, "Career, Prestige & Authority", "Moon in 10th expands professional influence and public recognition."),
        11: ("एकादश लाभ व अभीष्ट सिद्धि", "एकादश भाव में चन्द्रमा सभी प्रकार के मनोवांछित लाभ व मित्रों के सहयोग का प्रदाता होता है। उत्तम गोचर।", 6, False, False, "Gains, Desires & Networking", "Moon in 11th is superlative for realizing objectives and alliance support."),
        12: ("द्वादश चन्द्रमा (व्यय विचार)", "द्वादश भाव में चन्द्रमा व्यय की अधिकता व दूरस्थ कार्यों की संभावना बताता है। अनावश्यक भागदौड़ से बचें।", -4, False, False, "12th Moon (Expenditure / Distant Endeavors)", "Moon in 12th advises conserving reserves and monitoring expenditures.")
    }

    item = chandra_gochar_data.get(cg_house, ("गोचर प्रभाव", "गोचर ग्रह सामान्य परिणाम दे रहे हैं।", 0, False, False, "Transit Effect", "Planetary transits yielding moderate results."))
    title, desc, score_impact, is_4th, is_8th, title_en, desc_en = item
    return {
        "house": cg_house,
        "title": title,
        "title_en": title_en,
        "desc": desc,
        "desc_en": desc_en,
        "score_impact": score_impact,
        "is_fourth_moon": is_4th,
        "is_ashtama_moon": is_8th,
        "natal_rashi": constants.SIGNS_HI[natal_rashi],
        "natal_rashi_en": constants.SIGNS[natal_rashi],
        "transit_rashi": constants.SIGNS_HI[transit_rashi],
        "transit_rashi_en": constants.SIGNS[transit_rashi]
    }

def generate_daily_horoscope(natal_moon_lon: float, natal_asc_lon: float,
                             running_dasha: Any, transit_moon_lon: float,
                             today_date: datetime,
                             lat: float = 28.6139, lon: float = 77.2090, tz_hours: float = 5.5) -> Dict:
    """
    Synthesizes the complete personalised daily horoscope for the native
    with exact location-based Rahu Kaal, Abhijit Muhurta, Chaughadiya,
    Shani Gochar (Sade Sati/Dhaiya), Chandra Gochar (4th/8th Moon), and calibrated 40-75% score.
    """
    from vyas.panchang import get_muhurta_and_chaughadiya

    # 1. Parse Dasha Hierarchy with strict sanitization
    md_l, ad_l, pd_l, sd_l, prd_l = "", "", "", "", ""
    if isinstance(running_dasha, dict):
        md_l = running_dasha.get("mahadasha") or running_dasha.get("MD", {}).get("lord", "")
        ad_l = running_dasha.get("antardasha") or running_dasha.get("AD", {}).get("lord", "")
        pd_l = running_dasha.get("pratyantardasha") or running_dasha.get("PD", {}).get("lord", "")
        sd_l = running_dasha.get("sookshmadasha") or running_dasha.get("SD", {}).get("lord", "")
        prd_l = running_dasha.get("pranadasha") or running_dasha.get("PrD", {}).get("lord", "")
    else:
        s_raw = str(running_dasha).strip()
        if "{" in s_raw or "DashaNode" in s_raw:
            import re
            matches = re.findall(r"(?:'lord':\s*'|lord=')([A-Za-z]+)'", s_raw)
            if matches:
                unique_lords = []
                for m in matches:
                    if m not in unique_lords:
                        unique_lords.append(m)
                if len(unique_lords) >= 1: md_l = unique_lords[0]
                if len(unique_lords) >= 2: ad_l = unique_lords[1]
                if len(unique_lords) >= 3: pd_l = unique_lords[2]
                if len(unique_lords) >= 4: sd_l = unique_lords[3]
                if len(unique_lords) >= 5: prd_l = unique_lords[4]
        else:
            parts = [p.strip() for p in s_raw.replace("->", "-").replace("→", "-").split("-") if p.strip()]
            if len(parts) >= 1: md_l = parts[0]
            if len(parts) >= 2: ad_l = parts[1]
            if len(parts) >= 3: pd_l = parts[2]
            if len(parts) >= 4: sd_l = parts[3]
            if len(parts) >= 5: prd_l = parts[4]

    if not md_l: md_l = "Venus"
    if not ad_l: ad_l = "Saturn"

    md_hi = constants.PLANETS_HI.get(md_l, md_l)
    ad_hi = constants.PLANETS_HI.get(ad_l, ad_l)
    pd_hi = constants.PLANETS_HI.get(pd_l, pd_l)
    sd_hi = constants.PLANETS_HI.get(sd_l, sd_l)
    prd_hi = constants.PLANETS_HI.get(prd_l, prd_l)

    clean_lords_hi = [constants.PLANETS_HI.get(x, x) for x in [md_l, ad_l, pd_l] if x]
    running_dasha_str = " → ".join(clean_lords_hi) if clean_lords_hi else f"{md_hi} → {ad_hi}"

    # 2. Navatara Calculation (Calibrated Base 40-75%)
    natal_nak = int(natal_moon_lon // constants.NAKSHATRA_SPAN) % 27
    transit_nak = int(transit_moon_lon // constants.NAKSHATRA_SPAN) % 27
    tara_idx, tara_name, tara_desc, base_score, category = calculate_navatara(natal_nak, transit_nak)

    # 3. Shani Gochar (Sade Sati & Dhaiya)
    shani_res = evaluate_shani_gochar(natal_moon_lon, today_date)

    # 4. Chandra Gochar (4th & 8th Moon)
    cg_res = evaluate_chandra_gochar(natal_moon_lon, transit_moon_lon)

    # 5. Dasha Influence (Ascendant Functional Benefics/Malefics)
    asc_sign = int(natal_asc_lon // 30) % 12
    sign_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    lagna_lord = sign_lords[asc_sign]
    trine_lords = [sign_lords[(asc_sign + 4) % 12], sign_lords[(asc_sign + 8) % 12]]
    dusthana_lords = [sign_lords[(asc_sign + 5) % 12], sign_lords[(asc_sign + 7) % 12], sign_lords[(asc_sign + 11) % 12]]

    dasha_delta = 0
    if md_l == lagna_lord or md_l in trine_lords:
        dasha_delta += 4
    elif md_l in dusthana_lords:
        dasha_delta -= 3

    if ad_l == lagna_lord or ad_l in trine_lords:
        dasha_delta += 3
    elif ad_l in dusthana_lords:
        dasha_delta -= 2

    if pd_l and (pd_l == lagna_lord or pd_l in trine_lords):
        dasha_delta += 2
    elif pd_l in dusthana_lords:
        dasha_delta -= 1

    # Micro-dasha synergy (SD & PrD)
    if sd_l in ["Jupiter", "Venus", "Mercury", "Moon"]:
        dasha_delta += 1
    if prd_l in ["Jupiter", "Venus"]:
        dasha_delta += 1

    # 6. Synthesize Realistic Calibrated Overall Score (40% to 75% range)
    raw_score = base_score + shani_res["impact_score"] + cg_res["score_impact"] + dasha_delta
    # Strict clamping between 40 and 75 (up to 76 on extraordinary days, down to 38 on severe afflictions)
    overall_score = max(38, min(76, raw_score))

    # Domain sub-scores relative to overall_score
    career_score = max(40, min(75, overall_score + (3 if ("Sun" in [md_l, ad_l] or "Mars" in [md_l, ad_l] or "Jupiter" in [md_l, ad_l]) else -2)))
    wealth_score = max(38, min(75, overall_score + (3 if ("Venus" in [md_l, ad_l] or "Mercury" in [md_l, ad_l]) else -1)))
    love_score = max(40, min(74, overall_score + (2 if ("Venus" in [md_l, ad_l] or "Moon" in [md_l, ad_l]) else -2)))
    health_score = max(40, min(75, overall_score + (-5 if (cg_res["is_fourth_moon"] or cg_res["is_ashtama_moon"] or shani_res["has_shani_effect"]) else 2)))

    # Location-precise astronomical Muhurta & Chaughadiya
    try:
        loc_muhurta = get_muhurta_and_chaughadiya(today_date, lat, lon, tz_hours)
    except Exception:
        loc_muhurta = {
            "abhijit_muhurta": "-", "rahu_kalam": "-", "yamaganda": "-", "gulika_kalam": "-",
            "chaughadiya_day": [], "chaughadiya_night": [], "horas_day": [], "horas_night": []
        }

    # Daily Tailored Remedy
    if cg_res["is_ashtama_moon"]:
        daily_remedy = "आज चन्द्रअष्टम का प्रभाव है। महत्वपूर्ण निर्णय व विवाद टालें; ॐ नमः शिवाय का जप करें व शिवलिंग पर जल अर्पित करें।"
    elif cg_res["is_fourth_moon"]:
        daily_remedy = "आज चतुर्थ चन्द्रमा होने से मानसिक शांति हेतु माँ दुर्गा अथवा भगवान शिव का स्मरण करें; मीठा खाकर घर से निकलें।"
    elif shani_res["has_shani_effect"] and shani_res["is_adverse"]:
        daily_remedy = f"{shani_res['type']} के प्रभाव शमन हेतु सायंकाल पीपल के वृक्ष के नीचे तिल के तेल का दीपक प्रज्वलित करें अथवा हनुमान चालीसा का पाठ करें।"
    elif category == "bad":
        daily_remedy = "दिन थोड़ा सतर्कता का है। नए निवेश टालें, पक्षियों को दाना डालें व मन को शांत रखें।"
    else:
        daily_remedy = "दिन अनुकूल व कार्य सिद्धि दायक है। प्रातः इष्टदेव को नमन कर अपने मुख्य कार्यों की शुरुआत करें।"

    # 5-Tier Dasha formatted narrative
    dasha_parts_hi = []
    if md_hi: dasha_parts_hi.append(f"महादशा: {md_hi}")
    if ad_hi: dasha_parts_hi.append(f"अन्तर्दशा: {ad_hi}")
    if pd_hi: dasha_parts_hi.append(f"प्रत्यन्तर्दशा: {pd_hi}")
    if sd_hi: dasha_parts_hi.append(f"सूक्ष्म दशा: {sd_hi}")
    if prd_hi: dasha_parts_hi.append(f"प्राण दशा: {prd_hi}")
    dasha_full_text = " | ".join(dasha_parts_hi) if dasha_parts_hi else f"सक्रिय दशा: {md_hi}-{ad_hi}"

    # Master Synthesis
    master_synthesis = (
        f"आज गोचरस्थ चन्द्रमा आपकी जन्म राशि से {cg_res['house']}वें भाव ({cg_res['transit_rashi']} राशि, {constants.NAKSHATRAS[transit_nak]} नक्षत्र) में संचरण कर रहे हैं। "
        f"नवतारा चक्र के अनुसार यह आपकी कुण्डली पर '{tara_name}' निर्मित करता है ({tara_desc})। "
        f"वर्तमान में <b>{dasha_full_text}</b> का प्रभाव है। "
        f"शनि गोचर स्थिति: <b>{shani_res['type']}</b> ({shani_res['desc']})। "
        f"चन्द्र गोचर फल: <b>{cg_res['title']}</b> ({cg_res['desc']})। "
        f"समग्र खगोलीय समीकरणों के आधार पर आज का दिन संतुलित रूप से <b>{overall_score}% अनुकूल</b> परिलक्षित होता है।"
    )

    career_narrative = (
        f"कार्यक्षेत्र में {md_hi}-{ad_hi} दशा एवं {tara_name} के प्रभाव से व्यावहारिक दृष्टिकोण रखें। "
        f"{'योजनाओं को आगे बढ़ाने के लिए दिन सहायक है।' if career_score >= 65 else 'सहकर्मियों से समन्वय बनाए रखें और विवादों से बचें।'}"
    )
    wealth_narrative = (
        f"आर्थिक स्थिति में {wealth_score}% सापेक्ष संतुलन है। "
        f"{'सामान्य लेन-देन व पूर्व निवेश से लाभ संभव है।' if wealth_score >= 65 else 'अनावश्यक खर्चों व जोखिम भरे निवेश पर नियंत्रण रखना ही श्रेयस्कर रहेगा।'}"
    )
    love_narrative = (
        f"पारिवारिक एवं वैवाहिक संबंधों में {love_score}% सामंजस्य रहेगा। "
        f"{'संवाद में मधुरता व अपनों का स्नेह प्राप्त होगा।' if love_score >= 65 else 'छोटी-मोटी बातों को तूल न दें और धैर्यपूर्वक सुनें।'}"
    )
    health_narrative = (
        f"स्वास्थ्य एवं ऊर्जा सूचकांक {health_score}% है। "
        f"{'दिनचर्या संतुलित रहेगी।' if health_score >= 65 else 'पर्याप्त विश्राम लें और खान-पान में सुपाच्य आहार को प्राथमिकता दें।'}"
    )

    tara_en_item = NAVATARA_EN_MAP.get(tara_idx, ("Navatara Cycle", "Daily transit tara insight."))
    paryaya = ((transit_nak - natal_nak + 27) % 27 // 9) + 1
    tara_name_en = f"{tara_en_item[0]} (Tier {paryaya})"
    tara_desc_en = tara_en_item[1]

    daily_remedy_en = "Favourable day for purposeful tasks. Offer prayers to your Ishta Devata and initiate key goals with confidence."
    if cg_res["is_ashtama_moon"]:
        daily_remedy_en = "Chandrashtama is active today. Defer contentious arguments; chant 'Om Namah Shivaya' and practice mindful calm."
    elif cg_res["is_fourth_moon"]:
        daily_remedy_en = "4th Moon may cause restless thoughts. Meditate and start your day with a sweet offering for peaceful focus."
    elif shani_res["has_shani_effect"] and shani_res["is_adverse"]:
        daily_remedy_en = f"To pacify {shani_res.get('type_en', 'Saturn influence')}, light a sesame oil lamp or recite Hanuman Chalisa in the evening."
    elif category == "bad":
        daily_remedy_en = "Exercise extra patience today. Avoid speculative investments, feed birds, and maintain inner serenity."

    return {
        "today_str": today_date.strftime("%d %B %Y, %A"),
        "tara_name": tara_name,
        "tara_name_en": tara_name_en,
        "tara_desc": tara_desc,
        "tara_desc_en": tara_desc_en,
        "daily_remedy_en": daily_remedy_en,
        "remedy_en": daily_remedy_en,
        "overall_score": overall_score,
        "scores": {
            "career": career_score,
            "wealth": wealth_score,
            "love": love_score,
            "health": health_score
        },
        "narratives": {
            "career": career_narrative,
            "wealth": wealth_narrative,
            "love": love_narrative,
            "health": health_narrative,
            "synthesis": master_synthesis,
            "chandra_gochar_title": cg_res["title"],
            "chandra_gochar_desc": cg_res["desc"],
            "chandra_gochar_house": cg_res["house"],
            "shani_gochar_title": shani_res["type"],
            "shani_gochar_desc": shani_res["desc"],
            "dasha_full_text": dasha_full_text
        },
        "running_dasha": running_dasha_str,
        "dasha_chain_hi": {
            "MD": md_hi, "AD": ad_hi, "PD": pd_hi, "SD": sd_hi, "PrD": prd_hi
        },
        "shani_gochar": shani_res,
        "chandra_gochar": cg_res,
        "daily_remedy": daily_remedy,
        "remedy": daily_remedy,
        "natal_nakshatra": constants.NAKSHATRAS[natal_nak],
        "transit_nakshatra": constants.NAKSHATRAS[transit_nak],
        "natal_rashi": cg_res["natal_rashi"],
        "transit_rashi": cg_res["transit_rashi"],
        "amrit_vela": loc_muhurta.get("abhijit_muhurta", "11:45 AM - 12:35 PM"),
        "rahu_kalam": loc_muhurta.get("rahu_kalam", "01:30 - 03:00 PM"),
        "yamaganda": loc_muhurta.get("yamaganda", "-"),
        "gulika_kalam": loc_muhurta.get("gulika_kalam", "-"),
        "brahma_muhurta": loc_muhurta.get("brahma_muhurta", "-"),
        "chaughadiya_day": loc_muhurta.get("chaughadiya_day", []),
        "chaughadiya_night": loc_muhurta.get("chaughadiya_night", [])
    }
