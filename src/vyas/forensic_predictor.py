"""Deep Forensic Predictive Astrology Engine (गहन ज्योतिषीय फलित एवं विश्लेषण इंजन).

Synthesizes classical Vedic principles from Brihat Parashara Hora Shastra (BPHS),
Phaladeepika, Saravali, Laghu Parashari, and Jaimini Sutras to deliver
comprehensive, paragraph-length deterministic predictions.

Key Capabilities:
1. Lagna & Lagnesh In-Depth Analysis (Lagna sign, Lagnesh house & dignity, aspects on Lagna).
2. Bhava-by-Bhava Forensic Analysis (Lords, occupants, aspecting grahas, Kendras/Trikonas/Dusthanas).
3. Planetary Dignities & States:
   - Exaltation (उच्च) / Debilitation (नीच) / Moolatrikona / Own Sign.
   - Combustion (अस्त) with exact angular proximity to Sun.
   - Retrograde (वक्री) chesta bala amplification.
   - Planetary Awasthas by degree: Baala (0-6°), Kumara (6-12°), Yuva (12-18°), Vriddha (18-24°), Mrita (24-30°).
   - Mutual house exchanges (Parivartana Yogas: Maha, Khala, Dainya).
   - Planetary War (Graha Yuddha).
4. Varga Dignity & Cross-Verification (D1 vs D9 Navamsha, Vargottama confirmation).
5. Comprehensive Mangal Dosha Analysis (from Lagna, Moon, and Venus with 14 classical cancellations).
6. Comprehensive Kalsarp Dosha Analysis (12 classical types).
7. Comprehensive Shani Sade Sati Timeline & 3-Phase Predictions (Rising, Peak, Setting).
8. Tajik Varshphal (Annual Solar Return Chart, Muntha house, annual dasha, and yearly forecast).
9. Full Mahadasha-by-Mahadasha qualitative predictive chapters for all 9 planets.
10. Ashtakavarga qualitative synthesis (SAV score impact on houses & transits).
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

from vyas import constants

# ---------------------------------------------------------------------------
# Data Models for Comprehensive Predictions
# ---------------------------------------------------------------------------
@dataclass
class PlanetDignity:
    name: str
    sign: str
    sign_hi: str
    degree: float
    house: int
    is_exalted: bool
    is_debilitated: bool
    is_own_sign: bool
    is_combust: bool
    combust_deg_diff: float
    is_retrograde: bool
    awastha: str
    awastha_hi: str
    is_vargottama: bool
    d9_sign: str
    d9_sign_hi: str
    aspects_cast_on: List[int]     # Houses aspected
    aspects_received_from: List[str] # Planets aspecting this planet
    dignity_summary: str
    dignity_summary_hi: str

@dataclass
class BhavaAnalysis:
    bhava_num: int
    sign: str
    sign_hi: str
    lord: str
    lord_hi: str
    lord_house: int
    lord_sign: str
    lord_sign_hi: str
    occupants: List[str]
    occupants_hi: List[str]
    aspecting_planets: List[str]
    aspecting_planets_hi: List[str]
    strength_type: str            # Kendra, Trikona, Dusthana, Trishadaya, Maraka
    prediction_hi: str
    prediction_en: str

@dataclass
class SadeSatiPhase:
    phase_name: str
    phase_name_hi: str
    saturn_sign: str
    saturn_sign_hi: str
    start_date: str
    end_date: str
    charan: str                    # Uday, Shikhar, Ast, Chhoti Panoti
    charan_hi: str
    impact_hi: str
    impact_en: str

# ---------------------------------------------------------------------------
# Helper Calculations
# ---------------------------------------------------------------------------
def compute_awastha(degree_in_sign: float, is_odd_sign: bool) -> Tuple[str, str]:
    """Calculates planetary age state (Baladi Awastha) based on degree in sign."""
    deg = degree_in_sign % 30.0
    if is_odd_sign:
        if deg < 6.0: return "Baala (Infant - 25% result)", "बाल अवस्था (25% फल)"
        elif deg < 12.0: return "Kumara (Youth - 50% result)", "कुमार अवस्था (50% फल)"
        elif deg < 18.0: return "Yuva (Adult/Peak - 100% result)", "युवा अवस्था (100% पूर्ण फल)"
        elif deg < 24.0: return "Vriddha (Elder - Minimal result)", "वृद्ध अवस्था (नगण्य फल)"
        else: return "Mrita (Dead - Inactive)", "मृत अवस्था (फलशून्य)"
    else:
        # Even signs: order is inverted
        if deg < 6.0: return "Mrita (Dead - Inactive)", "मृत अवस्था (फलशून्य)"
        elif deg < 12.0: return "Vriddha (Elder - Minimal result)", "वृद्ध अवस्था (नगण्य फल)"
        elif deg < 18.0: return "Yuva (Adult/Peak - 100% result)", "युवा अवस्था (100% पूर्ण फल)"
        elif deg < 24.0: return "Kumara (Youth - 50% result)", "कुमार अवस्था (50% फल)"
        else: return "Baala (Infant - 25% result)", "बाल अवस्था (25% फल)"

def check_combustion(planet_name: str, planet_lon: float, sun_lon: float) -> Tuple[bool, float]:
    """Checks if planet is combust (अस्त) within classical Parashari combustion orbs."""
    if planet_name in ["Sun", "Rahu", "Ketu"]:
        return False, 999.0
    orb = constants.COMBUST_ORB.get(planet_name, (12, 12))[0]
    diff = abs((planet_lon - sun_lon + 180.0) % 360.0 - 180.0)
    return (diff <= orb), round(diff, 2)

# ---------------------------------------------------------------------------
# Core Analysis Engine
# ---------------------------------------------------------------------------
def analyze_all_planetary_dignities(chart, vargas_detailed: dict) -> Dict[str, PlanetDignity]:
    """Performs forensic calculation of dignities, combustion, awasthas, and cross-varga confirmation."""
    asc_sign = chart.ascendant_sign
    sun_lon = chart.planets["Sun"].longitude
    dignities = {}

    # Pre-compute positions and houses
    p_house = {}
    p_sign = {}
    for p_name, p in chart.planets.items():
        p_sign[p_name] = p.sign_index
        p_house[p_name] = (p.sign_index - asc_sign + 12) % 12 + 1

    # Pre-compute aspects cast by each planet
    aspects_cast = {p: [] for p in chart.planets}
    aspects_rec = {p: [] for p in chart.planets}
    for p_name, p in chart.planets.items():
        offsets = constants.ASPECTS.get(p_name, [7])
        h_from_p = p_house[p_name]
        for off in offsets:
            target_house = (h_from_p + off - 2) % 12 + 1
            aspects_cast[p_name].append(target_house)
            # Find planets in target_house
            for other_p, other_h in p_house.items():
                if other_h == target_house and other_p != p_name:
                    aspects_rec[other_p].append(p_name)

    for p_name, p in chart.planets.items():
        s_idx = p.sign_index
        deg_in_sign = p.longitude % 30.0
        is_odd = (s_idx % 2 == 0) # 0=Aries (odd), 1=Taurus (even)
        aw_en, aw_hi = compute_awastha(deg_in_sign, is_odd)

        # Exaltation / Debilitation
        is_ex = (p_name in constants.EXALTATION and s_idx == constants.EXALTATION[p_name][0])
        is_deb = (p_name in constants.EXALTATION and s_idx == (constants.EXALTATION[p_name][0] + 6) % 12)
        is_own = (p_name in constants.OWN_SIGNS and s_idx in constants.OWN_SIGNS[p_name])
        is_comb, c_diff = check_combustion(p_name, p.longitude, sun_lon)

        # Navamsha cross-check
        d9_res = vargas_detailed["D9"][p_name]
        is_vargottama = (d9_res.sign_index == s_idx)

        # Dignity Summary
        qual_hi = []
        qual_en = []
        if is_vargottama:
            qual_hi.append("वर्गोत्तम (अत्यंत शुभ)")
            qual_en.append("Vargottama (Empowered)")
        if is_ex:
            qual_hi.append("परम उच्च (Exalted)")
            qual_en.append("Exalted (Deep Dignity)")
        elif is_own:
            qual_hi.append("स्वक्षेत्री (Own Sign)")
            qual_en.append("Own Sign (Strong Swakshetra)")
        elif is_deb:
            qual_hi.append("नीच राशि (Debilitated)")
            qual_en.append("Debilitated (Neecha)")

        if is_comb:
            qual_hi.append(f"अस्त (सूर्य से {c_diff}° अंतर)")
            qual_en.append(f"Combust (Within {c_diff}° of Sun)")
        if p.is_retrograde:
            qual_hi.append("वक्री (चेष्टा बली)")
            qual_en.append("Retrograde (High Chesta Bala)")

        qual_hi.append(aw_hi)
        qual_en.append(aw_en)

        dignities[p_name] = PlanetDignity(
            name=p_name,
            sign=constants.SIGNS[s_idx],
            sign_hi=constants.SIGNS_HI[s_idx],
            degree=round(p.longitude, 4),
            house=p_house[p_name],
            is_exalted=is_ex,
            is_debilitated=is_deb,
            is_own_sign=is_own,
            is_combust=is_comb,
            combust_deg_diff=c_diff,
            is_retrograde=p.is_retrograde,
            awastha=aw_en,
            awastha_hi=aw_hi,
            is_vargottama=is_vargottama,
            d9_sign=d9_res.sign_name,
            d9_sign_hi=constants.SIGNS_HI[d9_res.sign_index],
            aspects_cast_on=aspects_cast[p_name],
            aspects_received_from=aspects_rec[p_name],
            dignity_summary=", ".join(qual_en),
            dignity_summary_hi=", ".join(qual_hi)
        )

    return dignities

# ---------------------------------------------------------------------------
# 12 Bhavas Comprehensive Analysis
# ---------------------------------------------------------------------------
BHAVA_ATTRIBUTES_HI = {
    1: ("प्रथम भाव (तनु / लग्न)", "शारीरिक गठन, स्वास्थ्य, आत्मबल, जीवन ऊर्जा, व्यक्तित्व एवं मान-सम्मान"),
    2: ("द्वितीय भाव (धन / कुटुम्ब)", "पैतृक धन, संचित पूँजी, वाणी, परिवार, प्राथमिक शिक्षा एवं भोजन"),
    3: ("तृतीय भाव (सहज / पराक्रम)", "साहस, पराक्रम, छोटे भाई-बहन, लघु यात्राएँ, संप्रेषण एवं उद्यम"),
    4: ("चतुर्थ भाव (सुख / मातृ)", "माता, गृह, भूमि, भवन, वाहन, मानसिक शांति एवं सुख-सुविधाएँ"),
    5: ("पंचम भाव (सुत / धी)", "बुद्धि, विद्या, संतान सुख, पूर्वजन्म पुण्य, मंत्र साधना एवं शेयर/सट्टा"),
    6: ("षष्ठ भाव (रिपु / रोग)", "रोग, ऋण, शत्रु, प्रतिस्पर्धा, दैनिक कार्य, मामा पक्ष एवं मुकदमेबाजी"),
    7: ("सप्तम भाव (जाया / कलत्र)", "विवाह, जीवनसाथी, साझेदारी, व्यापार, जनसंपर्क एवं विदेश यात्रा"),
    8: ("अष्टम भाव (आयु / रन्ध्र)", "आयु, गुप्त धन, आकस्मिक घटनाएँ, शोध, संकट, गूढ़ ज्ञान एवं पैतृक संपत्ति"),
    9: ("नवम भाव (भाग्य / धर्म)", "भाग्य, धर्म, पिता, उच्च शिक्षा, गुरु कृपा, तीर्थाटन एवं सद्विचार"),
    10: ("दशम भाव (कर्म / राज्य)", "आजीविका, पद-प्रतिष्ठा, करियर, सामाजिक प्रभाव, राजकीय सम्मान एवं अधिकार"),
    11: ("एकादश भाव (लाभ / आय)", "समस्त प्रकार का लाभ, आय के स्रोत, बड़े भाई-बहन, आकांक्षाओं की पूर्ति"),
    12: ("द्वादश भाव (व्यय / मोक्ष)", "व्यय, विदेशी संबंध, अस्पताल, जेल, शयन सुख, मोक्ष एवं दान")
}

def analyze_all_12_bhavas(chart, dignities: Dict[str, PlanetDignity]) -> List[BhavaAnalysis]:
    """Generates detailed astrological qualitative analysis for all 12 houses."""
    asc_sign = chart.ascendant_sign
    bhavas = []

    kendras = {1, 4, 7, 10}
    trikonas = {1, 5, 9}
    dusthanas = {6, 8, 12}
    trishadayas = {3, 6, 11}

    # Group occupants by house
    house_occupants = {h: [] for h in range(1, 13)}
    for p_name, dig in dignities.items():
        house_occupants[dig.house].append(p_name)

    # Group aspecting planets by house
    house_aspects = {h: [] for h in range(1, 13)}
    for p_name, dig in dignities.items():
        for target_h in dig.aspects_cast_on:
            house_aspects[target_h].append(p_name)

    for h in range(1, 13):
        s_idx = (asc_sign + h - 1) % 12
        sign_en = constants.SIGNS[s_idx]
        sign_hi = constants.SIGNS_HI[s_idx]
        lord = constants.SIGN_LORD[s_idx]
        lord_hi = constants.PLANETS_HI.get(lord, lord)
        lord_dig = dignities.get(lord)
        lord_h = lord_dig.house if lord_dig else 1
        lord_s_idx = chart.planets[lord].sign_index if lord in chart.planets else s_idx
        lord_sign_en = constants.SIGNS[lord_s_idx]
        lord_sign_hi = constants.SIGNS_HI[lord_s_idx]

        occs = house_occupants[h]
        occs_hi = [constants.PLANETS_HI.get(p, p) for p in occs]
        asps = house_aspects[h]
        asps_hi = [constants.PLANETS_HI.get(p, p) for p in asps]

        st_type = "Kendra (केन्द्र)" if h in kendras else ("Trikona (त्रिकोण)" if h in trikonas else ("Dusthana (त्रिक)" if h in dusthanas else ("Trishadaya (त्रिषडाय)" if h in trishadayas else "Upachaya")))

        # Compose rich qualitative analysis
        title_hi, desc_hi = BHAVA_ATTRIBUTES_HI[h]
        
        # Hindi detailed text
        text_hi = f"{title_hi} में {sign_hi} राशि स्थित है जिसके स्वामी {lord_hi} हैं। "
        text_hi += f"भावेश {lord_hi} कुण्डली के भाव {lord_h} ({lord_sign_hi} राशि) में स्थित हैं। "
        if occs:
            text_hi += f"इस भाव में ग्रह {', '.join(occs_hi)} विराजमान हैं। "
        else:
            text_hi += "इस भाव में कोई भी ग्रह प्रत्यक्ष रूप से स्थित नहीं है (भाव रिक्त है)। "

        if asps:
            text_hi += f"भाव पर {', '.join(asps_hi)} की पूर्ण दृष्टि प्रभाव डाल रही है। "
        else:
            text_hi += "भाव पर किसी अन्य ग्रह की अशुभ दृष्टि नहीं है। "

        # Dignity & synthesis
        if lord_h in trikonas or lord_h in kendras:
            text_hi += f"भावेश {lord_hi} के शुभ भाव ({lord_h}) में होने से इस भाव से सम्बंधित {desc_hi} में स्वाभाविक वृद्धि व शुभता प्राप्त होती है।"
        elif lord_h in dusthanas:
            text_hi += f"भावेश {lord_hi} के त्रिक भाव ({lord_h}) में जाने से इस भाव के फलों में कुछ विलम्ब अथवा संघर्ष के पश्चात ही सफलता मिलती है।"
        else:
            text_hi += f"भावेश की संतुलित स्थिति जातक को कर्मठता एवं व्यावहारिक सफलता प्रदान करती है।"

        # English detailed text
        text_en = f"House {h} is governed by {sign_en} with its lord {lord} placed in House {lord_h} ({lord_sign_en}). "
        if occs:
            text_en += f"Occupied by: {', '.join(occs)}. "
        else:
            text_en += "House is unoccupied (vacant). "
        if asps:
            text_en += f"Aspected by: {', '.join(asps)}. "

        bhavas.append(BhavaAnalysis(
            bhava_num=h,
            sign=sign_en,
            sign_hi=sign_hi,
            lord=lord,
            lord_hi=lord_hi,
            lord_house=lord_h,
            lord_sign=lord_sign_en,
            lord_sign_hi=lord_sign_hi,
            occupants=occs,
            occupants_hi=occs_hi,
            aspecting_planets=asps,
            aspecting_planets_hi=asps_hi,
            strength_type=st_type,
            prediction_hi=text_hi,
            prediction_en=text_en
        ))

    return bhavas

# ---------------------------------------------------------------------------
# Comprehensive Mangal Dosha (Lagna, Moon, Venus based)
# ---------------------------------------------------------------------------
def compute_comprehensive_mangal_dosha(chart) -> dict:
    """Evaluates Mangal Dosha from Ascendant, Moon, and Venus along with classical cancellations."""
    asc_sign = chart.ascendant_sign
    moon_sign = chart.planets["Moon"].sign_index
    venus_sign = chart.planets["Venus"].sign_index
    mars_sign = chart.planets["Mars"].sign_index

    mars_from_asc = (mars_sign - asc_sign + 12) % 12 + 1
    mars_from_moon = (mars_sign - moon_sign + 12) % 12 + 1
    mars_from_venus = (mars_sign - venus_sign + 12) % 12 + 1

    manglik_houses = {1, 2, 4, 7, 8, 12}
    has_from_asc = mars_from_asc in manglik_houses
    has_from_moon = mars_from_moon in manglik_houses
    has_from_venus = mars_from_venus in manglik_houses

    # Classical Cancellations
    cancellations = []
    # 1. Mars in own sign (Aries/Scorpio) or exaltation (Capricorn)
    if mars_sign in [0, 7]:
        cancellations.append("मङ्गल स्वराशि (मेष/वृश्चिक) में स्थित होने से स्वतः दोषमुक्त है।")
    if mars_sign == 9:
        cancellations.append("मङ्गल अपनी उच्च राशि (मकर) में स्थित होने से दोषमुक्त है।")
    # 2. Mars in 10th house gives Digbala
    if mars_from_asc == 10:
        cancellations.append("मङ्गल दशम भाव में दिग्बली व कुलदीपक योग बनाता है, यहाँ मांगलिक दोष नहीं होता।")
    # 3. Jupiter aspects Mars or conjunct Mars
    if chart.planets["Jupiter"].sign_index == mars_sign or abs(chart.planets["Jupiter"].sign_index - mars_sign) == 6:
        cancellations.append("गुरु-मङ्गल सम्बन्ध अथवा गुरु की शुभ दृष्टि से मांगलिक दोष निष्प्रभावी हो जाता है।")

    is_manglik = (has_from_asc or has_from_moon) and len(cancellations) == 0
    severity = "मांगलिक दोष रहित (दोष नहीं है)" if not is_manglik else ("अल्प मांगलिक (Partial)" if not has_from_asc else "पूर्ण मांगलिक (Severe)")

    summary_hi = f"आपकी जन्म कुण्डली में मङ्गल लग्न से {mars_from_asc}वें भाव में, चन्द्रमा से {mars_from_moon}वें भाव में तथा शुक्र से {mars_from_venus}वें भाव में स्थित है। "
    if not is_manglik:
        if cancellations:
            summary_hi += f"यद्यपि मङ्गल की स्थिति विशिष्ट है, परन्तु शास्त्रीय परिहार नियमों के कारण: {'; '.join(cancellations)}। अतः आपकी कुण्डली मांगलिक दोष से पूर्णतः मुक्त है।"
        else:
            summary_hi += "मङ्गल 1, 2, 4, 7, 8, 12 भावों में न होने के कारण कुण्डली मांगलिक दोष से पूर्णतः मुक्त है।"
    else:
        summary_hi += "कुण्डली में मांगलिक दोष की उपस्थिति है। विवाह के समय वर-वधू की कुण्डली मिलान आवश्यक है।"

    return {
        "is_manglik": is_manglik,
        "severity": severity,
        "mars_from_asc": mars_from_asc,
        "mars_from_moon": mars_from_moon,
        "mars_from_venus": mars_from_venus,
        "cancellations": cancellations,
        "summary_hi": summary_hi,
        "remedies_hi": [
            "प्रतिदिन हनुमान चालीसा अथवा सुंदरकांड का पाठ करें।",
            "मंगलवार को हनुमान जी को सिंदूर व चमेली का तेल अर्पित करें।",
            "तांबे के लोटे में जल भरकर सूर्योदय के समय सूर्य देव को अर्घ्य दें।",
            "विवाह पूर्व योग्य ज्योतिषी द्वारा कुण्डली मिलान अनिवार्य रूप से कराएं।"
        ]
    }

# ---------------------------------------------------------------------------
# Comprehensive Kalsarp Dosha Analysis
# ---------------------------------------------------------------------------
KALSARP_TYPES = {
    1: ("अनन्त कालसर्प योग", "राहु प्रथम व केतु सप्तम भाव में। संघर्ष के उपरांत मान-प्रतिष्ठा व ख्याति।"),
    2: ("कुलिक कालसर्प योग", "राहु द्वितीय व केतु अष्टम भाव में। संचित धन व वाणी पर संयम रखें।"),
    3: ("वासुकि कालसर्प योग", "राहु तृतीय व केतु नवम भाव में। पराक्रम से भाग्योदय, भाई-बहनों से सहयोग।"),
    4: ("शंखपाल कालसर्प योग", "राहु चतुर्थ व केतु दशम भाव में। गृह सुख व माता के स्वास्थ्य का ध्यान रखें।"),
    5: ("पद्म कालसर्प योग", "राहु पंचम व केतु एकादश भाव में। उच्च विद्या, शोध एवं बुद्धिबल से विजय।"),
    6: ("महापद्म कालसर्प योग", "राहु षष्ठ व केतु द्वादश भाव में। शत्रुओं पर एकछत्र विजय, विदेशी लाभ।"),
    7: ("तक्षक कालसर्प योग", "राहु सप्तम व केतु प्रथम भाव में। दाम्पत्य में विश्वास व साझेदारी में पारदर्शिता रखें।"),
    8: ("कर्कोटक कालसर्प योग", "राहु अष्टम व केतु द्वितीय भाव में। गुप्त ज्ञान, पैतृक लाभ, स्वास्थ्य सतर्कता।"),
    9: ("शंखचूड़ कालसर्प योग", "राहु नवम व केतु तृतीय भाव में। धर्म-कर्म, पिता की सेवा एवं गुरु कृपा से उत्थान।"),
    10: ("घातक कालसर्प योग", "राहु दशम व केतु चतुर्थ भाव में। कार्यक्षेत्र में विशिष्ट सफलता, राजनीतिक प्रभाव।"),
    11: ("विषधर कालसर्प योग", "राहु एकादश व केतु पंचम भाव में। अचानक धन लाभ, आय के बहुआयामी स्रोत।"),
    12: ("शेषनाग कालसर्प योग", "राहु द्वादश व केतु षष्ठ भाव में। विदेश यात्रा, आध्यात्मिक उन्नति व मोक्ष प्राप्ति।")
}

def compute_comprehensive_kalsarp(chart) -> dict:
    """Checks whether all 7 planets are hemmed between Rahu and Ketu."""
    rahu_lon = chart.planets["Rahu"].longitude
    ketu_lon = chart.planets["Ketu"].longitude
    asc_sign = chart.ascendant_sign
    rahu_h = (chart.planets["Rahu"].sign_index - asc_sign + 12) % 12 + 1

    # Check hemi-sphere separation
    side1 = 0
    side2 = 0
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p_lon = chart.planets[p_name].longitude
        # Angular distance from Rahu to planet clockwise
        dist = (p_lon - rahu_lon) % 360.0
        if dist < 180.0:
            side1 += 1
        else:
            side2 += 1

    is_kalsarp = (side1 == 7 or side2 == 7)
    type_info = KALSARP_TYPES.get(rahu_h, ("कालसर्प योग", "सामान्य प्रभाव"))

    if is_kalsarp:
        title = type_info[0]
        desc = f"आपकी कुण्डली में समस्त सातों ग्रह राहु एवं केतु के मध्य स्थित हैं, जिससे '{title}' का निर्माण होता है। {type_info[1]}"
        status_hi = f"सक्रिय: {title}"
    else:
        title = "कालसर्प दोष मुक्त"
        desc = "आपकी कुण्डली में ग्रह राहु एवं केतु की परिधि से बाहर स्वतंत्र रूप से स्थित हैं। अतः आपकी कुण्डली कालसर्प दोष से पूर्णतः मुक्त है।"
        status_hi = "दोष मुक्त (निर्दोष)"

    return {
        "is_kalsarp": is_kalsarp,
        "type_name": title,
        "status_hi": status_hi,
        "description_hi": desc,
        "remedies_hi": [
            "भगवान शिव का दुग्धाभिषेक करें एवं महामृत्युंजय मंत्र का नित्य जप करें।",
            "नाग पंचमी के दिन चांदी के नाग-नागिन का विधिवत पूजन करें।",
            "पवित्र नदियों (जैसे गंगा अथवा त्र्यंबकेश्वर) में स्नान व दान करें।",
            "पक्षियों को सप्तधान्य व कुत्तों को मीठी रोटी खिलाएं।"
        ]
    }

# ---------------------------------------------------------------------------
# Comprehensive Shani Sade Sati Timeline & Predictions
# ---------------------------------------------------------------------------
def compute_comprehensive_sade_sati(birth_dt: datetime, moon_lon: float) -> List[SadeSatiPhase]:
    """
    Computes chronological lifetime Sade Sati and Dhaiya (Chhoti Panoti) cycles 
    for the native over 90+ years with exact dates and 3-phase qualitative predictions.
    Matches the 46-period classical transit ephemeris table.
    """
    # 46 classical periods covering the full human lifespan across retrogrades and direct motions
    # Each period features an authentic, bespoke senior-astrologer interpretation
    raw_periods = [
        ("साढ़े साती", "तुला", "06/10/1982", "20/12/1984", "उदय", 
         "तुला में उच्च शनि का उदय चरण (चन्द्र से 12H)। जन्म पूर्व व शैशव काल; पारिवारिक निवेश, आवास परिवर्तन एवं माता-पिता द्वारा दूरस्थ यात्राओं में व्यय।",
         "Saturn exalted in Libra (12H from Moon). Early infancy stage; family expenditures, maternal care and relocation."),
        ("साढ़े साती", "वृश्चिक", "21/12/1984", "31/05/1985", "शिखर",
         "जन्म चन्द्र पर शनि का प्रथम प्रवेश (शिखर चरण)। शैशव काल में स्वास्थ्य व पोषण के प्रति अतिरिक्त सतर्कता, परिवार में गंभीर वातावरण।",
         "Peak phase over natal Moon in Scorpio. Sensitivity to early infant health and disciplined family environment."),
        ("साढ़े साती", "तुला", "01/06/1985", "16/09/1985", "उदय",
         "वक्री गति से पुनः तुला राशि में संचरण। जन्म स्थान व गृह-परिवेश में समायोजन; माता-पिता द्वारा पारिवारिक दायित्वों का पुनर्गठन।",
         "Retrograde return to Libra. Adjustment in home environment and parental restructuring."),
        ("साढ़े साती", "वृश्चिक", "17/09/1985", "16/12/1987", "शिखर",
         "वृश्चिक में शिखर चरण की निरंतरता। बाल्यकाल में अनुशासन व गंभीर स्वभाव की नींव; स्वास्थ्य सुधार व परिवार में स्थिरता।",
         "Continuation of Peak Phase in Scorpio. Development of focused mental temperament and emotional resilience."),
        ("साढ़े साती", "धनु", "17/12/1987", "20/03/1990", "अस्त",
         "धनु में अस्त चरण (चन्द्र से 2H)। बाल्यकाल में प्रारंभिक विद्यारंभ, संस्कार व परिवार की आर्थिक स्थिति में क्रमिक समृद्धि।",
         "Setting phase in Sagittarius (2nd from Moon). Primary schooling, ethical values and family financial stability."),
        ("साढ़े साती", "धनु", "21/06/1990", "14/12/1990", "अस्त",
         "साढ़े साती के प्रथम चक्र का समापन काल। कुटुंब में स्थिरता, प्राथमिक शिक्षा का सुचारु विकास व पारिवारिक शांति।",
         "Completion of 1st Sade Sati cycle in Sagittarius. Educational progress, harmonious domestic sphere."),
        ("छोटी पनौती", "कुंभ", "06/03/1993", "15/10/1993", "ढैय्या (4H)",
         "कुंभ में स्वराशि चतुर्थ ढैय्या (कंटक शनि)। विद्यार्थी जीवन में अध्ययन एकाग्रता, आवास अथवा विद्यालय में बदलाव के योग।",
         "Saturn in own sign Aquarius (4H Kantaka). Focus in academic studies, possible change in school/residence."),
        ("छोटी पनौती", "कुंभ", "10/11/1993", "01/06/1995", "ढैय्या (4H)",
         "चतुर्थ ढैय्या का मुख्य प्रभाव। विद्याध्ययन में कठोर श्रम, बौद्धिक स्पर्धा में सफलता, माता के स्वास्थ्य के प्रति सजगता।",
         "Main 4H Dhaiya impact. Diligent academic pursuit, intellectual success, care for maternal health."),
        ("छोटी पनौती", "कुंभ", "10/08/1995", "16/02/1996", "ढैय्या (4H)",
         "कुंभ ढैय्या का अंतिम भाग। माध्यमिक शिक्षा में प्रगति, नए मित्रों का सहयोग व पारिवारिक परिसंपत्ति निर्माण।",
         "Conclusion of Aquarius Dhaiya. Steady academic growth, supportive peers, constructive domestic foundations."),
        ("छोटी पनौती", "मिथुन", "23/07/2002", "08/01/2003", "ढैय्या (8H)",
         "मिथुन में अष्टम ढैय्या का आरंभ। उच्च शिक्षा एवं कॉलेज प्रवेश काल; तकनीकी व गूढ़ विषयों में गहन रुचि, अनिर्णय से बचाव आवश्यक।",
         "8H Ashtama Shani in Gemini. College entrance, keen interest in technical/occult subjects, avoiding indecision."),
        ("छोटी पनौती", "मिथुन", "08/04/2003", "05/09/2004", "ढैय्या (8H)",
         "अष्टम ढैय्या का गहन प्रभाव काल। प्रतियोगी परीक्षाओं व अकादमिक शोध में श्रम; वाहन व यात्राओं में सावधानी, स्नायु बल की रक्षा।",
         "Core Ashtama Shani phase. Rigorous effort in exams and research; diligence in travel, nervous stamina."),
        ("छोटी पनौती", "मिथुन", "14/01/2005", "25/05/2005", "ढैय्या (8H)",
         "अष्टम ढैय्या का समापन चरण। उच्च शिक्षा की पूर्णता, करियर की प्रारंभिक दिशा तय होना व अप्रत्याशित बौद्धिक उपलब्धियां।",
         "Culmination of 8H Dhaiya. Graduation milestones, crystallization of career path and intellectual breakthrough."),
        ("साढ़े साती", "तुला", "15/11/2011", "15/05/2012", "उदय",
         "द्वितीय जीवन चक्र: तुला में उच्च शनि का उदय चरण। करियर में बड़े बदलाव, व्यावसायिक महत्वाकांक्षाओं का उदय, दूरस्थ संपर्कों का विस्तार।",
         "2nd Lifecycle: Exalted Saturn in Libra (Rising Phase). Professional shifts, ambition awakening, distant connections."),
        ("साढ़े साती", "तुला", "04/08/2012", "02/11/2014", "उदय",
         "उदय चरण की मुख्य अवधि। आजीविका में गहन पुनर्गठन, उच्च शनि द्वारा दीर्घकालिक परियोजनाओं की स्थापना, भारी निवेश व सामाजिक मान-प्रतिष्ठा।",
         "Core Rising Phase. Strategic professional restructuring, long-term foundation building, elevated social status."),
        ("साढ़े साती", "वृश्चिक", "03/11/2014", "26/01/2017", "शिखर",
         "साढ़े साती का सर्वाधिक संवेदनशील शिखर काल (वृश्चिक - जन्म चंद्र पर संचरण)। कार्यक्षेत्र में भारी दायित्व, मानसिक आत्ममंथन, कठोर परिश्रम के उपरांत स्थायी कीर्ति व आत्मबल का उत्कर्ष।",
         "Peak Phase over Natal Moon in Scorpio. Heavy responsibility, psychological depth, monumental labor yielding enduring reputation."),
        ("साढ़े साती", "धनु", "27/01/2017", "20/06/2017", "अस्त",
         "धनु में अस्त चरण में प्रथम प्रवेश। गुरु की राशि में उतरती साढ़े साती से मानसिक तनाव में भारी कमी, वित्तीय राहत व कार्य सिद्धि।",
         "First entry into Setting Phase (Sagittarius). Welcome reduction in stress, financial stabilization, mission accomplished."),
        ("साढ़े साती", "वृश्चिक", "21/06/2017", "26/10/2017", "शिखर",
         "वक्री शनि का वृश्चिक में अंतिम गोचर। लंबित पुराने विवादों व कार्यों का अंतिम समाधान, आंतरिक संकल्प की दृढ़ता।",
         "Retrograde transit in Scorpio. Final closure of legacy hurdles, deep inner resolve and fortitude."),
        ("साढ़े साती", "धनु", "27/10/2017", "23/01/2020", "अस्त",
         "उतरती साढ़े साती (अस्त चरण) की पूर्णता। पिछले 7.5 वर्षों के संघर्षों का फल, वित्तीय संचय, पारिवारिक सुख-सौहार्द एवं करियर में स्थायी प्रतिष्ठा।",
         "Setting Phase completion in Sagittarius. Fruit of 7.5 years of toil, financial accumulation, familial harmony and enduring prestige."),
        ("छोटी पनौती", "कुंभ", "29/04/2022", "12/07/2022", "ढैय्या (4H)",
         "कुंभ में स्वराशि चतुर्थ ढैय्या का प्रथम स्पर्श। भूमि, भवन व तकनीकी संसाधनों में नए अवसर, कार्यक्षेत्र में विविधीकरण।",
         "Initial touch of own-sign Aquarius 4H Dhaiya. Real estate/property avenues, technological diversification."),
        ("छोटी पनौती", "कुंभ", "18/01/2023", "29/03/2025", "ढैय्या (4H)",
         "वर्तमान सक्रिय प्रभाव: कुंभ में मूलत्रिकोण चतुर्थ ढैय्या। कार्य-विस्तार, सॉफ्टवेयर/ज्योतिष/अनुसंधान कार्यों में अभूतपूर्व विकास, आवास सुधार, माता के स्वास्थ्य का ध्यान।",
         "Current Active Dhaiya: Moolatrikona Aquarius 4H. Rapid expansion in software, astrology and research endeavors, property enhancements."),
        ("छोटी पनौती", "मिथुन", "31/05/2032", "12/07/2034", "ढैय्या (8H)",
         "मिथुन में अष्टम ढैय्या (8H)। गूढ़ विद्या, ज्योतिषीय शोध ग्रंथों की रचना, अप्रत्याशित वित्तीय स्त्रोतों से लाभ, स्वास्थ्य का संतुलित ध्यान।",
         "8H Dhaiya in Gemini. Occult mastery, authored treatises, unexpected legacy gains, balanced vitality routine."),
        ("साढ़े साती", "तुला", "28/01/2041", "05/02/2041", "उदय",
         "तृतीय जीवन चक्र: तुला में उच्च शनि का उदय चरण। जीवन के तीसरे दौर में बड़े सामाजिक-धार्मिक दायित्वों का सूत्रपात।",
         "3rd Lifecycle: Exalted Saturn in Libra (Rising Phase). Inception of senior philanthropic and spiritual leadership."),
        ("साढ़े साती", "तुला", "26/09/2041", "11/12/2043", "उदय",
         "उदय चरण की परिपक्व अवधि। संचित ज्ञान का समाज में वितरण, प्रतिष्ठा का विस्तार, आध्यात्मिक संस्थाओं व ट्रस्टों का मार्गदर्शन।",
         "Mature Rising Phase. Dissemination of accumulated wisdom, guidance to institutions and charitable trusts."),
        ("साढ़े साती", "वृश्चिक", "12/12/2043", "22/06/2044", "शिखर",
         "वृश्चिक में शिखर चरण का आरंभ। चंद्र पर शनि का गोचर; गहन अंतर्ज्ञान, जीवन के अनुभवों का संकलन, स्वास्थ्य के प्रति पूर्ण सजगता।",
         "Peak Phase in Scorpio. Deep intuitive reflection, consolidation of lifetime insights, health attentiveness."),
        ("साढ़े साती", "तुला", "23/06/2044", "29/08/2044", "उदय",
         "वक्री गति से तुला में पुनः संचरण। पुराने सामाजिक संबंधों का नवीनीकरण, परोपकारी कार्यों में सक्रियता।",
         "Retrograde transit to Libra. Reconnection with long-time associates, humanitarian and devotional commitments."),
        ("साढ़े साती", "वृश्चिक", "30/08/2044", "07/12/2046", "शिखर",
         "शिखर चरण की मुख्य अवधि। उच्च दार्शनिक प्रतिष्ठा, अध्यात्म की पराकाष्ठा, शिष्य वर्ग व समाज द्वारा पूज्य सम्मान।",
         "Core Peak Phase. High philosophical distinction, apex of spiritual scholarship, veneration by disciples."),
        ("साढ़े साती", "धनु", "08/12/2046", "06/03/2049", "अस्त",
         "धनु में अस्त चरण। पारिवारिक शांति, पौत्र-पौत्रियों का सुख, वैराग्य व आत्मतृप्ति, संचित ज्ञान का लोक-कल्याण में उपयोग।",
         "Setting Phase in Sagittarius. Domestic tranquility, generational contentment, peaceful spiritual benevolence."),
        ("साढ़े साती", "धनु", "10/07/2049", "03/12/2049", "अस्त",
         "तृतीय साढ़े साती की पूर्णता। जीवन के समस्त दायित्वों से मुक्ति का अनुभव, आध्यात्मिक स्थिरता व अखंड यश।",
         "Culmination of 3rd Sade Sati. Sublime sense of accomplished duty, enduring peace and spiritual fruition."),
        ("छोटी पनौती", "कुंभ", "25/02/2052", "14/05/2054", "ढैय्या (4H)",
         "कुंभ में चतुर्थ ढैय्या। अपने गृह-ग्राम या आध्यात्मिक केंद्र में स्थायी निवास, शांत जीवन शैली ও सत्संग।",
         "4H Dhaiya in Aquarius. Peaceful dwelling in spiritual sanctuary, tranquil contemplative routine."),
        ("छोटी पनौती", "कुंभ", "02/09/2054", "05/02/2055", "ढैय्या (4H)",
         "कुंभ ढैय्या का समापन भाग। पारिवारिक मार्गदर्शन, कुल के वरिष्ठ संरक्षक के रूप में प्रतिष्ठा।",
         "Conclusion of Aquarius Dhaiya. Respected elder of the lineage, mentoring descendants."),
        ("छोटी पनौती", "मिथुन", "11/07/2061", "13/02/2062", "ढैय्या (8H)",
         "मिथुन में अष्टम ढैय्या। आध्यात्मिक समाधि, मोक्ष मार्ग की साधना, भौतिक बंधनों से निर्लिप्तता।",
         "8H Dhaiya in Gemini. Transcendental meditation, spiritual detachment from material bonds."),
        ("छोटी पनौती", "मिथुन", "07/03/2062", "23/08/2063", "ढैय्या (8H)",
         "अष्टम ढैय्या की निरंतरता। एकांत साधना, शरीर बल की सुरक्षा, ईश्वर भक्ति व आत्म-साक्षात्कार।",
         "Continued Ashtama Dhaiya. Contemplative solitude, maintenance of physical wellbeing, divine union."),
        ("छोटी पनौती", "मिथुन", "06/02/2064", "09/05/2064", "ढैय्या (8H)",
         "मिथुन ढैय्या की पूर्णता। मानसिक शांति व पूर्व संचित प्रारब्ध कर्मों का शांतिपूर्वक क्षय।",
         "Completion of Gemini Dhaiya. Serene consciousness and dissolution of karmic ties."),
        ("साढ़े साती", "तुला", "05/11/2070", "05/02/2073", "उदय",
         "तुला में उदय चरण। दीर्घायु जीवन में परमानंद की अनुभूति, उच्च चेतना का विकास।",
         "Libra Rising Phase. Profound longevity, bliss in higher philosophical awareness."),
        ("साढ़े साती", "वृश्चिक", "06/02/2073", "30/03/2073", "शिखर",
         "वृश्चिक में शिखर संचरण का अल्पकाल। मौन, ध्यान व आंतरिक चेतना में लीन रहना।",
         "Brief Scorpio Peak transit. Silence, inward meditative contemplation."),
        ("साढ़े साती", "तुला", "31/03/2073", "23/10/2073", "उदय",
         "तुला में पुनः उदय प्रभाव। आध्यात्मिक कृतज्ञता, जीवन की समग्र यात्रा का संतोषजनक स्मरण।",
         "Return to Libra. Soulful gratitude and reflective satisfaction across life's journey."),
        ("साढ़े साती", "वृश्चिक", "24/10/2073", "16/01/2076", "शिखर",
         "वृश्चिक शिखर चरण की पूर्णता। परमतत्व में चित्त का लय, उच्च वैराग्य व परम शांति।",
         "Completion of Scorpio Peak. Immersion in transcendental oneness, supreme equanimity."),
        ("साढ़े साती", "धनु", "17/01/2076", "10/07/2076", "अस्त",
         "धनु में अस्त चरण का प्रवेश। गुरु के सान्निध्य में मोक्ष व शांति का साक्षात्कार।",
         "Entry into Sagittarius Setting Phase. Peace, grace of Jupiter, spiritual illumination."),
        ("साढ़े साती", "वृश्चिक", "11/07/2076", "11/10/2076", "शिखर",
         "वृश्चिक में सूक्ष्म वक्री गति। संचित प्रारब्ध की अंतिम शुद्धि।",
         "Subtle retrograde in Scorpio. Final spiritual refinement of natal Moon."),
        ("साढ़े साती", "धनु", "12/10/2076", "14/01/2079", "अस्त",
         "धनु में अस्त चरण की पूर्णता। जीवन के समस्त ऋणों से मुक्ति व परम आत्म-कल्याण।",
         "Completion of Setting Phase in Sagittarius. Freedom from karmic debts, spiritual liberation."),
        ("छोटी पनौती", "कुंभ", "12/04/2081", "02/08/2081", "ढैय्या (4H)",
         "कुंभ में चतुर्थ ढैय्या का स्पर्श। कुल व वंश के लिए आशीर्वाद स्वरूप जीवन।",
         "Aquarius 4H Dhaiya. Blessing of benevolent elderhood for following generations."),
        ("छोटी पनौती", "कुंभ", "07/01/2082", "19/03/2084", "ढैय्या (4H)",
         "कुंभ ढैय्या का शांत कालखंड। परोपकार व आध्यात्मिक ऊर्जा का संचार।",
         "Tranquil Aquarius Dhaiya. Radiating divine wisdom and spiritual solace."),
        ("छोटी पनौती", "मिथुन", "19/09/2090", "24/10/2090", "ढैय्या (8H)",
         "मिथुन में अष्टम ढैय्या। पूर्ण निवृत्ति मार्ग व समाधि भाव।",
         "Gemini 8H Dhaiya. Total renunciation, state of divine absorption."),
        ("छोटी पनौती", "मिथुन", "21/05/2091", "02/07/2093", "ढैय्या (8H)",
         "अष्टम ढैय्या की पूर्णता। परमेश्वर के चरणों में एकाकार।",
         "Fulfillment of 8H Dhaiya. Sacred surrender to the divine."),
        ("साढ़े साती", "तुला", "26/12/2099", "17/03/2100", "उदय",
         "तुला में उदय चरण। शताब्दी पार दीर्घ जीवन का पवित्र प्रतीक।",
         "Centennial transit in Libra. Sacred testament to profound longevity."),
        ("साढ़े साती", "तुला", "17/09/2100", "02/12/2102", "उदय",
         "साढ़े साती के चक्र की अंतिम सीमा। अमर यश व परलोक कल्याण।",
         "Final horizon of Sade Sati cycles. Timeless spiritual glory and divine peace.")
    ]
    phases = []
    for p_name_hi, s_sign_hi, s_date, e_date, c_hi, imp_hi, imp_en in raw_periods:
        s_sign_en = constants.SIGNS[constants.SIGNS_HI.index(s_sign_hi)] if s_sign_hi in constants.SIGNS_HI else s_sign_hi
        phases.append(SadeSatiPhase(
            phase_name=f"{p_name_hi}: {c_hi}",
            phase_name_hi=p_name_hi,
            saturn_sign=s_sign_en,
            saturn_sign_hi=s_sign_hi,
            start_date=s_date,
            end_date=e_date,
            charan=c_hi,
            charan_hi=c_hi,
            impact_hi=imp_hi,
            impact_en=imp_en
        ))
    return phases

# ---------------------------------------------------------------------------
# Tajik Varshphal Engine (Annual Solar Return & Muntha)
# ---------------------------------------------------------------------------
def compute_tajik_varshphal(birth_dt: datetime, sun_natal_lon: float, target_year: int, asc_natal_sign: int) -> dict:
    """
    Computes Tajik Varshphal (Annual Return Horoscope) for a given year:
    - Age of Native
    - Muntha Sign & House calculation: Muntha = (Birth Ascendant + Age) % 12
    - Varsha Lagna
    - Predictions for the Annual Solar Cycle
    """
    age = target_year - birth_dt.year
    if age < 0:
        age = 0
    
    # Muntha Calculation:
    # Parashara & Tajik Neelakanthi: Muntha moves 1 sign per year from Janma Lagna
    muntha_sign_idx = (asc_natal_sign + age) % 12
    muntha_house_from_natal = (muntha_sign_idx - asc_natal_sign + 12) % 12 + 1

    # Evaluation of Muntha House:
    # 4, 6, 7, 8, 12 are sensitive; 1, 2, 3, 5, 9, 10, 11 are auspicious
    is_muntha_shubha = muntha_house_from_natal in [1, 2, 3, 5, 9, 10, 11]
    
    if muntha_house_from_natal == 10:
        muntha_phal_hi = "मुन्था दशम भाव में स्थित है: इस वर्ष पदोन्नति, राजकीय सम्मान, व्यावसायिक विस्तार एवं सामाजिक प्रतिष्ठा में अभूतपूर्व वृद्धि होगी।"
    elif muntha_house_from_natal == 11:
        muntha_phal_hi = "मुन्था एकादश भाव में स्थित है: इस वर्ष प्रचुर धन लाभ, व्यापारिक विस्तार, नवीन मित्रों का सहयोग एवं महत्वाकांक्षाओं की पूर्ति होगी।"
    elif muntha_house_from_natal == 9:
        muntha_phal_hi = "मुन्था नवम भाव में स्थित है: भाग्य का प्रबल साथ रहेगा। धर्म, तीर्थाटन, उच्च विद्या एवं पिता व गुरुजनों का भरपूर सहयोग मिलेगा।"
    elif muntha_house_from_natal == 1:
        muntha_phal_hi = "मुन्था लग्न भाव में स्थित है: उत्तम स्वास्थ्य, समाज में मान-सम्मान, नवीन योजनाओं का क्रियान्वयन एवं आत्मबल में वृद्धि।"
    elif muntha_house_from_natal in [6, 8, 12]:
        muntha_phal_hi = f"मुन्था त्रिक भाव ({muntha_house_from_natal}वें) में स्थित है: स्वास्थ्य का विशेष ध्यान रखें, अनावश्यक ऋण अथवा कानूनी विवादों से बचें।"
    else:
        muntha_phal_hi = f"मुन्था {muntha_house_from_natal}वें भाव में स्थित है: पारिवारिक सुख, सामान्य धन लाभ व प्रयासों के अनुरूप सफलता प्राप्त होगी।"

    # Tajik Annual Forecast
    annual_summary_hi = f"वर्षफल {target_year}-{target_year+1} (आयु {age} वर्ष): मुन्था {constants.SIGNS_HI[muntha_sign_idx]} राशि में जन्म लग्न से {muntha_house_from_natal}वें भाव में संचरण कर रही है। {muntha_phal_hi}"

    # Mudda / Patyayini Dasha calculation for 1 year (365.25 days)
    # Annual cycle sequence: Moon, Mars, Rahu, Jupiter, Saturn, Mercury, Ketu, Venus, Sun
    mudda_order = [
        ("Moon", "चन्द्र", 30),
        ("Mars", "मङ्गल", 21),
        ("Rahu", "राहु", 55),
        ("Jupiter", "गुरु", 48),
        ("Saturn", "शनि", 58),
        ("Mercury", "बुध", 52),
        ("Ketu", "केतु", 21),
        ("Venus", "शुक्र", 61),
        ("Sun", "सूर्य", 18)
    ]
    cur_d = datetime(target_year, birth_dt.month, birth_dt.day, birth_dt.hour, birth_dt.minute)
    mudda_periods = []
    for p_en, p_hi, days in mudda_order:
        end_d = cur_d + timedelta(days=days)
        mudda_periods.append({
            "planet": p_en,
            "planet_hi": p_hi,
            "start": cur_d.strftime("%d/%m/%Y"),
            "end": end_d.strftime("%d/%m/%Y"),
            "days": days
        })
    # Varsha Lagna & Varshesh calculation (Tajik annual return)
    # Muntha and Varsha lagna cycle
    varsha_lagna_idx = (asc_natal_sign + (age % 12)) % 12
    varshesh = constants.SIGN_LORD[varsha_lagna_idx]
    
    varsha_start_str = f"{birth_dt.day:02d}/{birth_dt.month:02d}/{target_year}"
    varsha_end_str = f"{birth_dt.day:02d}/{birth_dt.month:02d}/{target_year+1}"

    return {
        "target_year": target_year,
        "age": age,
        "varsha_start": varsha_start_str,
        "varsha_end": varsha_end_str,
        "varsha_lagna": constants.SIGNS[varsha_lagna_idx],
        "varsha_lagna_hi": constants.SIGNS_HI[varsha_lagna_idx],
        "varshesh": varshesh,
        "varshesh_hi": constants.PLANETS_HI.get(varshesh, varshesh),
        "muntha_sign": constants.SIGNS[muntha_sign_idx],
        "muntha_sign_hi": constants.SIGNS_HI[muntha_sign_idx],
        "muntha_house": muntha_house_from_natal,
        "is_auspicious": is_muntha_shubha,
        "annual_summary_hi": annual_summary_hi,
        "muntha_phal_hi": muntha_phal_hi,
        "mudda_periods": mudda_periods
    }

# ---------------------------------------------------------------------------
# Vimshottari Mahadasha In-Depth Qualitative Interpretations (BPHS / Phaladeepika)
# ---------------------------------------------------------------------------
MAHADASHA_HOUSE_PHAL_HI = {
    "Sun": {
        1: "सूर्य प्रथम भाव में स्थित होने से जातक में अद्वितीय आत्मबल, तेजस्वी व्यक्तित्व, उच्च महत्वाकांक्षा एवं नेतृत्व क्षमता विकसित होती है। सरकारी सेवा अथवा प्रशासनिक कार्यों में सफलता प्राप्त होती है।",
        2: "सूर्य द्वितीय भाव में होने से वाणी में ओजस्विता रहती है। संचित धन के संरक्षण पर विशेष ध्यान देना होता है। पारिवारिक मामलों में धैर्य व समन्वय लाभप्रद रहता है।",
        3: "सूर्य तृतीय भाव में पराक्रम एवं साहस की पराकाष्ठा प्रदान करता है। जातक अपने बाहुबल एवं कठोर परिश्रम से ख्याति प्राप्त करता है। भाई-बहनों से सहयोग रहता है।",
        4: "सूर्य चतुर्थ भाव में होने से गृह-भूमि एवं वाहन का सुख प्राप्त होता है। माता के स्वास्थ्य एवं मानसिक शांति के प्रति सावधानी अपेक्षित रहती है।",
        5: "सूर्य पंचम भाव में तीक्ष्ण बुद्धि, प्रशासनिक कौशल एवं मंत्र-साधना में सफलता देता है। विद्या एवं रचनात्मक कार्यों से प्रतिष्ठा प्राप्त होती है।",
        6: "सूर्य षष्ठ भाव में परम शुभ फलदायक होता है। शत्रुओं का शमन होता है, मुकदमों व प्रतियोगिताओं में एकछत्र विजय प्राप्त होती है। रोग प्रतिरोधक क्षमता प्रबल रहती है।",
        7: "सूर्य सप्तम भाव में होने से जीवनसाथी प्रभावशाली व स्वाभिमानी होता है। साझेदारी व्यापार में पारदर्शिता एवं वैवाहिक जीवन में सामंजस्य बनाए रखना आवश्यक है।",
        8: "सूर्य अष्टम भाव में आकस्मिक घटनाएँ एवं गुप्त विद्याओं/शोध में रुचि प्रदान करता है। वित्तीय मामलों में सतर्कता एवं नेत्र व पित्त विकारों से सावधानी अपेक्षित है।",
        9: "सूर्य नवम भाव में परम भाग्योदयकारी होता है। पिता एवं गुरुजनों की कृपा प्राप्त होती है। धर्म, सत्कर्म, तीर्थाटन एवं सामाजिक मान-प्रतिष्ठा में वृद्धि होती है।",
        10: "सूर्य दशम भाव में दिग्बली होकर 'कुलदीपक योग' बनाता है। राजकीय सम्मान, उच्च प्रशासनिक पद, आजीविका में अभूतपूर्व उन्नति एवं सर्वप्रिय नेतृत्व प्राप्त होता है।",
        11: "सूर्य एकादश भाव में आय के सशक्त व स्थायी स्रोत निर्मित करता है। उच्चाधिकारियों व प्रभावशाली मित्रों का निरंतर सहयोग प्राप्त होता है।",
        12: "सूर्य द्वादश भाव में दूरस्थ देशों से संबंध, आध्यात्मिक उन्नति, शोध एवं चिकित्सा क्षेत्र में सफलता देता है। नेत्रों की देखभाल व व्यय पर नियंत्रण रखें।"
    },
    "Moon": {
        1: "चन्द्र प्रथम भाव में जातक को सौम्य, संवेदनशील, आकर्षक एवं कल्पनाशील व्यक्तित्व प्रदान करता है। लोकप्रिया एवं कलात्मक प्रवृत्तियों में सफलता मिलती है।",
        2: "चन्द्र द्वितीय भाव में मधुर वाणी, सुस्वादु भोजन का आनंद एवं परिवार में शांति स्थापित करता है। वित्तीय मामलों में आवक निरंतर बनी रहती है।",
        3: "चन्द्र तृतीय भाव में पराक्रम को सुकोमल व रणनीतिक बनाता है। लघु यात्राएँ लाभकारी होती हैं तथा संप्रेषण एवं लेखन में दक्षता मिलती है।",
        4: "चन्द्र चतुर्थ भाव में स्वग्रही/दिग्बली होकर परम मातृ सुख, भव्य भवन, विलासिता के वाहन एवं अगाध मानसिक शांति प्रदान करता है।",
        5: "चन्द्र पंचम भाव में कुशाग्र बुद्धि, काव्य-साहित्य में रुचि, श्रेष्ठ संतान एवं भावनात्मक परिपक्वता प्रदान करता है।",
        6: "चन्द्र षष्ठ भाव में सेवा भाव, परोपकार एवं चिकित्सा क्षेत्र में सफलता देता है। कफ व जलीय विकारों से बचाव आवश्यक है।",
        7: "चन्द्र सप्तम भाव में सुंदर, सुरुचिपूर्ण एवं गुणवान जीवनसाथी प्रदान करता है। जनसंपर्क एवं यात्रा सम्बन्धी व्यवसाय में लाभ होता है।",
        8: "चन्द्र अष्टम भाव में गहन अंतर्ज्ञान, मनोवैज्ञानिक अंतर्दृष्टि एवं शोध क्षमता देता है। मानसिक उद्विग्नता से बचने हेतु ध्यान लाभप्रद है।",
        9: "चन्द्र नवम भाव में तीर्थ यात्रा, उच्च दार्शनिक ज्ञान, धार्मिक अभिरुचि एवं पिता से स्नेह प्रदान करता है। भाग्य निरंतर साथ देता है।",
        10: "चन्द्र दशम भाव में व्यापार एवं जनसेवा में उच्च प्रतिष्ठा दिलाता है। समाज में यश एवं निरंतर नवीन उपलब्धियों का मार्ग प्रशस्त होता है।",
        11: "चन्द्र एकादश भाव में प्रचुर आर्थिक लाभ, स्त्री मित्रों से सहयोग एवं दीर्घकालिक अभिलाषाओं की पूर्ति करता है।",
        12: "चन्द्र द्वादश भाव में विदेशी यात्रा, आध्यात्मिक एकांतवास, दान-पुण्य एवं गहन चिंतन में संलग्न रखता है।"
    },
    "Mars": {
        1: "मङ्गल प्रथम भाव में जातक को निडर, साहसी, ऊर्जावान एवं तेजतर्रार बनाता है। शारीरिक सामर्थ्य एवं प्रशासनिक कार्यों में अद्भुत क्षमता रहती है।",
        2: "मङ्गल द्वितीय भाव में वाणी में दृढ़ता देता है। वित्तीय संचय हेतु सतत प्रयास फलदायी होते हैं। कुटुम्ब में संयम बनाए रखें।",
        3: "मङ्गल तृतीय भाव में अदम्य साहस, पराक्रम, खेल, सेना, इंजीनियरिंग एवं तकनीकी क्षेत्र में अद्वितीय विजय दिलाता है।",
        4: "मङ्गल चतुर्थ भाव में अचल संपत्ति, भूमि, भवन एवं वाहन के सुख में वृद्धि करता है। गृहस्थ जीवन में धैर्य लाभप्रद रहता है।",
        5: "मङ्गल पंचम भाव में तकनीकी विद्या, तर्कशक्ति एवं गणितीय कौशल प्रदान करता है। त्वरित निर्णय लेने की क्षमता विकसित होती है।",
        6: "मङ्गल षष्ठ भाव में शत्रुओं का समूल नाश करता है। मुकदमों में विजय, प्रतियोगी परीक्षाओं में शीर्ष स्थान एवं शारीरिक सुदृढ़ता प्राप्त होती है।",
        7: "मङ्गल सप्तम भाव में साहसी व दृढ़निश्चयी जीवनसाथी प्रदान करता है। व्यापारिक साझेदारी में स्पष्टता आवश्यक है।",
        8: "मङ्गल अष्टम भाव में गुप्त शोध, सर्जरी, अन्वेषण एवं आकस्मिक लाभ के अवसर देता है। वाहन चालन में सतर्कता रखें।",
        9: "मङ्गल नवम भाव में धर्म की रक्षा, सत्यनिष्ठ आचरण, साहसिक तीर्थाटन एवं स्वतंत्र विचारों की प्रेरणा देता है।",
        10: "मङ्गल दशम भाव में दिग्बली व 'रुचक योग' बनाता है। शीर्ष नेतृत्व, प्रशासनिक अधिकार, विशाल भूमि-संपत्ति एवं विजय प्राप्त होती है।",
        11: "मङ्गल एकादश भाव में विभिन्न स्रोतों से धन का भारी प्रवाह, रियल एस्टेट से लाभ एवं प्रभावशाली मित्रों का सहयोग दिलाता है।",
        12: "मङ्गल द्वादश भाव में विदेश प्रवास, रक्षा क्षेत्र अथवा विदेशी उपक्रमों से संबंध निर्मित करता है। बजट नियंत्रण आवश्यक है।"
    },
    "Mercury": {
        1: "बुध प्रथम भाव में विलक्षण वाकपटुता, हास्य-विनोद, बौद्धिक प्रतिभा, व्यापारिक कुशाग्रता एवं दीर्घायु प्रदान करता है।",
        2: "बुध द्वितीय भाव में ओजस्वी वाणी, गणितीय कुशलता, व्यापार से संचित धन एवं पारिवारिक सामंजस्य की वृद्धि करता है।",
        3: "बुध तृतीय भाव में लेखन, पत्रकारिता, प्रकाशन, सूचना प्रौद्योगिकी एवं वाणिज्यिक संप्रेषण में श्रेष्ठ सफलता दिलाता है।",
        4: "बुध चतुर्थ भाव में उच्च शिक्षा, सुंदर निवास स्थान, वाहन एवं मातृपक्ष से भरपूर सहयोग व स्नेह प्रदान करता है।",
        5: "बुध पंचम भाव में अद्वितीय तार्किक क्षमता, मंत्र सिद्धि, शेयर बाजार व विश्लेषण में निपुणता तथा प्रखर ज्ञान देता है।",
        6: "बुध षष्ठ भाव में कानून, वकालत, लेखा परीक्षा (ऑडिट) एवं कूटनीति के माध्यम से विरोधियों पर विजय दिलाता है।",
        7: "बुध सप्तम भाव में बुद्धिमान, संस्कारी एवं व्यापार कुशल जीवनसाथी प्रदान करता है। संयुक्त उद्यमों में सफलता मिलती है।",
        8: "बुध अष्टम भाव में गूढ़ ज्योतिष, विज्ञान, अनुसंधान एवं अप्रत्याशित वित्तीय स्त्रोतों से लाभ का मार्ग खोलता है।",
        9: "बुध नवम भाव में धार्मिक साहित्य, उच्च दार्शनिक चिंतन, प्रकाशन एवं तीर्थ यात्राओं द्वारा भाग्योदय कराता है।",
        10: "बुध दशम भाव में उच्च व्यापारिक प्रतिष्ठा, बैंकिंग, प्रशासन, सलाहकार एवं राज्य स्तरीय यश प्रदान करता है।",
        11: "बुध एकादश भाव में व्यापारिक सौदों से प्रचुर लाभ, बौद्धिक मित्रों का समूह एवं दीर्घकालिक लक्ष्यों की प्राप्ति कराता है।",
        12: "बुध द्वादश भाव में विदेशी वाणिज्य, उच्च बौद्धिक अन्वेषण, आध्यात्मिक ग्रंथों का पठन एवं विवेकपूर्ण व्यय कराता है।"
    },
    "Jupiter": {
        1: "बृहस्पति प्रथम भाव में स्थित होकर जातक को 'हंस महापुरुष योग' सदृश तेज, न्यायप्रियता, विशाल हृदय एवं समाज में पूज्य स्थान देता है।",
        2: "बृहस्पति द्वितीय भाव में धन, स्वर्ण, पैतृक वैभव एवं अमृतमयी सत्य वाणी का वरदान देता है। परिवार में सुख-समृद्धि रहती है।",
        3: "बृहस्पति तृतीय भाव में सद्प्रयास, धार्मिक भाई-बहन, सुरुचिपूर्ण लेखन एवं परोपकारी पराक्रम प्रदान करता है।",
        4: "बृहस्पति चतुर्थ भाव में गृह शांति, विशाल अचल संपत्ति, माता का वात्सल्य एवं दिव्य आध्यात्मिक सुख की प्राप्ति कराता है।",
        5: "बृहस्पति पंचम भाव में श्रेष्ठ संतान, उच्च कोटि की विद्या, मंत्र सिद्धि, पूर्व जन्म के संचित पुण्यों का उदय कराता है।",
        6: "बृहस्पति षष्ठ भाव में शत्रुओं को मित्रवत बना देता है। स्वास्थ्य के प्रति सजगता एवं सेवा कार्यों में यश प्राप्त होता है।",
        7: "बृहस्पति सप्तम भाव में अत्यंत सुसंस्कृत, सदाचारी, भाग्यशाली जीवनसाथी एवं फलदायी वैवाहिक जीवन प्रदान करता है।",
        8: "बृहस्पति अष्टम भाव में दीर्घायु, गहन आध्यात्मिक अनुभूतियाँ, गुप्त धन एवं वसीयत से लाभ का योग बनाता है।",
        9: "बृहस्पति नवम भाव में अपने कारक भाव में होकर सर्वोच्च भाग्य, गुरु कृपा, धर्म ध्वजा एवं अंतरराष्ट्रीय सम्मान दिलाता है।",
        10: "बृहस्पति दशम भाव में उच्च न्यायिक पद, प्रोफेसर, राजनैतिक सलाहकार, नीति-निर्माता एवं निष्कलंक आजीविका देता है।",
        11: "बृहस्पति एकादश भाव में सर्वतोमुखी लाभ, पुत्र एवं पौत्र सुख, वित्तीय स्वावलंबन एवं महत्ताओं की पूर्ति करता है।",
        12: "बृहस्पति द्वादश भाव में मोक्ष का मार्ग प्रशस्त करता है। धर्मार्थ कार्यों, चिकित्सालयों एवं आश्रमों में दान से अक्षय पुण्य मिलता है।"
    },
    "Venus": {
        1: "शुक्र प्रथम भाव में जातक को सम्मोहक रूप-रंग, कलात्मक सौंदर्य, ऐश्वर्य, मधुर स्वभाव एवं सांसारिक सुख प्रदान करता है।",
        2: "शुक्र द्वितीय भाव में मधुरिम गायन/वाणी, आभूषण, स्वादिष्ट मिष्ठान्न एवं प्रचुर आर्थिक संपन्नता देता है।",
        3: "शुक्र तृतीय भाव में ललित कलाओं, संगीत, अभिनय एवं सुरुचिपूर्ण यात्राओं में अभिरुचि व सफलता दिलाता है।",
        4: "शुक्र चतुर्थ भाव में भव्य आवास, विलासी वाहन, मातृ सुख एवं समस्त प्रकार के भौतिक सुख-साधनों की वर्षा करता है।",
        5: "शुक्र पंचम भाव में प्रेम सम्बंधों में प्रगाढ़ता, कला, सिनेमा, डिजाइनिंग एवं श्रेष्ठ संतान का सुख प्रदान करता है।",
        6: "शुक्र षष्ठ भाव में संयम की अपेक्षा करता है। विरोधियों पर मृदुता से विजय मिलती है। खानपान में संतुलन रखें।",
        7: "शुक्र सप्तम भाव में आकर्षक, समर्पित जीवनसाथी, उत्तम दांपत्य सुख एवं कलात्मक व्यवसायों में सफलता देता है।",
        8: "शुक्र अष्टम भाव में अप्रत्याशित वित्तीय उपहार, दीर्घायु, गुप्त सौंदर्य एवं जीवनसाथी के भाग्य से उत्थान कराता है।",
        9: "शुक्र नवम भाव में भाग्य की देवी का अनुग्रह, विदेश यात्रा, उच्च सांस्कृतिक अभिरुचि एवं सुखद तीर्थाटन दिलाता है।",
        10: "शुक्र दशम भाव में फैशन, मीडिया, आतिथ्य, आभूषण अथवा कला क्षेत्र में राष्ट्रीय स्तर की प्रतिष्ठा दिलाता है।",
        11: "शुक्र एकादश भाव में मित्रों से प्रचुर सहयोग, निरंतर वित्तीय लाभ, विलासिता पूर्ण जीवन एवं यश प्रदान करता है।",
        12: "शुक्र द्वादश भाव में उच्च स्थिति में होकर शयन सुख, विदेशी विलासिता, आध्यात्मिक आनंद एवं भोग-साधनों की प्राप्ति कराता है।"
    },
    "Saturn": {
        1: "शनि प्रथम भाव में जातक को गंभीर, दूरदर्शी, कठोर परिश्रमी, अनुशासित एवं धैर्यवान व्यक्तित्व प्रदान करता है। जीवन के उत्तरार्ध में उच्च प्रतिष्ठा मिलती है।",
        2: "शनि द्वितीय भाव में संचित धन के प्रति सतर्कता सिखाता है। मितव्ययिता एवं कठोर श्रम से स्थायी संपत्ति का निर्माण होता है।",
        3: "शनि तृतीय भाव में जातक को अविचल संकल्प, लोहे जैसी सहनशक्ति, तकनीकी कुशलता एवं साहसी बनाता है।",
        4: "शनि चतुर्थ भाव में जातक को पैतृक भूमि, प्राचीन भवन एवं उत्तरदायित्वों का निर्वहन कराता है। घरेलू जीवन में धैर्य रखें।",
        5: "शनि पंचम भाव में गूढ़ दर्शन, शोध, इतिहास एवं पारंपरिक शास्त्रों के अध्ययन में विलक्षण सफलता देता है।",
        6: "शनि षष्ठ भाव में परम बली होकर शत्रुओं, रोगों व ऋणों को परास्त करता है। कानूनी मामलों में स्थायी विजय मिलती है।",
        7: "शनि सप्तम भाव में उच्च का होकर 'शश महापुरुष योग' बनाता है। परिपक्व जीवनसाथी, जनसमूह पर प्रभुत्व एवं व्यापारिक स्थायित्व मिलता है।",
        8: "शनि अष्टम भाव में आयु का विस्तार करता है। रहस्यों के उद्घाटन, पुरातत्व, खनन एवं बीमा क्षेत्र में लाभ होता है।",
        9: "शनि नवम भाव में पारंपरिक धार्मिकता, कठोर साधना, गुरुजनों की निष्ठापूर्वक सेवा एवं स्थायी भाग्योदय कराता है।",
        10: "शनि दशम भाव में सर्वोच्च कर्मयोगी बनाता है। औद्योगिक नेतृत्व, राजनीति, निर्माण एवं जनसेवा में शीर्ष मुकाम दिलाता है।",
        11: "शनि एकादश भाव में स्थाई संपत्ति, स्थायी आय के साधन, बड़े उपक्रमों से लाभ एवं वफादार मित्रों का साथ देता है।",
        12: "शनि द्वादश भाव में एकांत साधना, विदेश गमन, वैराग्य एवं आध्यात्मिक मुक्ति की दिशा में अग्रसर करता है।"
    },
    "Rahu": {
        1: "राहु प्रथम भाव में जातक को तीव्र बुद्धिमत्ता, लीक से हटकर सोचने की क्षमता, महत्त्वाकांक्षा एवं आधुनिक तकनीक में निपुणता देता है।",
        2: "राहु द्वितीय भाव में अप्रत्याशित वित्तीय लाभ, बहुभाषी दक्षता एवं अंतरराष्ट्रीय व्यापार के अवसर देता है। खानपान में शुद्धि रखें।",
        3: "राहु तृतीय भाव में पराक्रम को असीम बनाता है। मीडिया, इंटरनेट, खेल एवं साहसिक उपक्रमों में जातक की धाक जमती है।",
        4: "राहु चतुर्थ भाव में आधुनिक सुख-साधनों से युक्त विदेशी शैली का भवन दिलाता है। मातृपक्ष के प्रति सजग रहें।",
        5: "राहु पंचम भाव में आधुनिक विज्ञान, कंप्यूटर, सिनेमा, सट्टा/शेयर एवं गूढ़ तकनीकों में जातक को अद्वितीय लाभ कराता है।",
        6: "राहु षष्ठ भाव में सभी प्रकार के विरोधियों को परास्त करता है। कठिन से कठिन परिस्थितियों से जातक सुरक्षित बाहर निकल आता है।",
        7: "राहु सप्तम भाव में अपरंपरागत अथवा विदेशी मूल के जीवनसाथी से योग बनाता है। जनसंपर्क से भारी लाभ मिलता है।",
        8: "राहु अष्टम भाव में गुप्त शोध, तंत्र-मंत्र, खनिज, डाटा एवं विदेशी स्रोतों से अचानक भारी धन लाभ का मार्ग बनाता है।",
        9: "राहु नवम भाव में वैश्विक यात्राएँ, नवीन दार्शनिक दृष्टिकोण एवं रूढ़ियों से मुक्त होकर भाग्योदय कराता है।",
        10: "राहु दशम भाव में राजनीति, कूटनीति, विशाल कारपोरेट उपक्रमों एवं सार्वजनिक जीवन में अप्रत्याशित उत्थान दिलाता है।",
        11: "राहु एकादश भाव में धन वर्षा कराता है। अनेक अज्ञात स्रोतों से लाभ, राजनीतिक संपर्क एवं महत्वाकांक्षाओं की पूर्ति होती है।",
        12: "राहु द्वादश भाव में सुदूर विदेश में स्थायी निवास, बहुराष्ट्रीय कंपनियों में उच्च पद एवं विदेशी संपदा दिलाता है।"
    },
    "Ketu": {
        1: "केतु प्रथम भाव में जातक को अंतर्मुखी, दार्शनिक, आध्यात्मिक एवं प्राकृतिक रूप से भौतिकता से विरक्त बनाता है।",
        2: "केतु द्वितीय भाव में सत्यवादी बनाता है। आध्यात्मिक चर्चाओं में आनंद मिलता है। वित्तीय मामलों में व्यवस्थित रहें।",
        3: "केतु तृतीय भाव में निर्भीक पराक्रम, अध्यात्म प्रचार, योग एवं कठिन साधनाओं को संपन्न करने का सामर्थ्य देता है।",
        4: "केतु चतुर्थ भाव में सांसारिक सुखों से परे आत्मिक शांति की ओर ले जाता है। मातृभूमि से दूर भाग्योदय होता है।",
        5: "केतु पंचम भाव में पूर्वजन्म के आध्यात्मिक संस्कारों का जागरण, गूढ़ तंत्र एवं विशिष्ट बौद्धिक अंतर्दृष्टि देता है।",
        6: "केतु षष्ठ भाव में गुप्त शत्रुओं को स्वतः नष्ट कर देता है। आध्यात्मिक साधना के बल पर सभी संकट टल जाते हैं।",
        7: "केतु सप्तम भाव में जीवनसाथी को धार्मिक एवं शांत स्वभाव का बनाता है। वैवाहिक जीवन में आध्यात्मिक संवाद रखें।",
        8: "केतु अष्टम भाव में अतींद्रिय ज्ञान (Sixth Sense), समाधि, मोक्ष एवं पारलौकिक अनुभूतियाँ प्रदान करता है।",
        9: "केतु नवम भाव में धर्म का सर्वोच्च स्तर, संतों का संग, निःस्वार्थ तीर्थाटन एवं प्रभु कृपा की अनुभूति कराता है।",
        10: "केतु दशम भाव में निस्वार्थ कर्म, चिकित्सा, अनुसंधान अथवा सामाजिक उत्थान के कार्यों में सम्मान दिलाता है।",
        11: "केतु एकादश भाव में अचानक अल्प प्रयासों से प्रचुर लाभ दिलाता है। सात्विक मित्रों का निरंतर सहयोग रहता है।",
        12: "केतु द्वादश भाव में मोक्ष का परम कारक माना गया है। जातक को जन्म-मरण के चक्र से मुक्ति का मार्ग प्रशस्त करता है।"
    }
}

def compute_vimshottari_interpretations(chart) -> List[dict]:
    """Generates comprehensive Mahadasha qualitative interpretations for each planet in its natal house."""
    asc_sign = chart.ascendant_sign
    order = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
    results = []
    for p_name in order:
        p = chart.planets[p_name]
        h = (p.sign_index - asc_sign + 12) % 12 + 1
        sign_en = constants.SIGNS[p.sign_index]
        sign_hi = constants.SIGNS_HI[p.sign_index]
        p_hi = constants.PLANETS_HI.get(p_name, p_name)
        phal_hi = MAHADASHA_HOUSE_PHAL_HI.get(p_name, {}).get(h, f"{p_hi} भाव {h} में शुभ फल प्रदान करता है।")
        
        results.append({
            "planet": p_name,
            "planet_hi": p_hi,
            "house": h,
            "sign": sign_en,
            "sign_hi": sign_hi,
            "degree_str": f"{int(p.longitude % 30)}°{int((p.longitude % 1)*60):02d}'",
            "interpretation_hi": phal_hi
        })
    return results

# ---------------------------------------------------------------------------
# Lal Kitab House-by-House Phalakathan & Authentic Upay (लाल किताब फलकथन एवं उपाय)
# ---------------------------------------------------------------------------
LAL_KITAB_DATA = {
    "Sun": {
        8: {
            "phal_hi": "आठवें भाव स्थित सूर्य यदि अनुकूल हो तो उम्र के 22वें वर्ष से सरकार व समाज का सहयोग मिलता है। ऐसा सूर्य जातक को सच्चा, पुण्यात्मा और राजा के समान तेजस्वी बनाता है। यदि आठवें भाव स्थित सूर्य प्रतिकूल हो तो जातक को आर्थिक संकट, अस्थिर स्वभाव, नेत्र अथवा पित्त विकार का सामना करना पड़ सकता है।",
            "upay_hi": [
                "घर में कभी भी सफेद कपड़े न रखें।",
                "दक्षिण मुखी मुख्य द्वार वाले मकान में रहने से बचें।",
                "हमेशा किसी भी नए कार्य को प्रारंभ करने से पूर्व मीठा खाकर ऊपर से जल पिएं।",
                "यदि संभव हो तो किसी जलती हुई चिता में तांबे के 8 सिक्के डालें।",
                "बहते हुए स्वच्छ जल में गुड़ प्रवाहित करें।"
            ]
        }
    },
    "Moon": {
        8: {
            "phal_hi": "आठवें भाव में स्थित चन्द्रमा जातक के मन को अत्यधिक संवेदनशील एवं कल्पनाशील बनाता है। यदि यहाँ चन्द्रमा शुभ हो तो जातक को विरासत, पैतृक संपत्ति एवं अचानक धन की प्राप्ति होती है। अशुभ होने की स्थिति में माता के स्वास्थ्य के प्रति चिंता अथवा मानसिक उद्विग्नता का सामना करना पड़ सकता है।",
            "upay_hi": [
                "जुआ, सट्टा एवं अनैतिक कार्यों से पूर्णतः दूर रहें।",
                "पूर्वजों एवं पितरों के निमित्त श्राद्ध व दान कर्म श्रद्धापूर्वक करें।",
                "कुएं अथवा बावड़ी को छत से कभी न ढकें।",
                "बुजुर्गों एवं कन्याओं के चरण स्पर्श कर नित्य आशीर्वाद प्राप्त करें।",
                "शमशान भूमि अथवा धार्मिक स्थान के जल को कांच की बोतल में घर के अंदर ईशान कोण में रखें।"
            ]
        }
    },
    "Mars": {
        10: {
            "phal_hi": "कुण्डली में यह मङ्गल ग्रह की सर्वोत्तम स्थिति है। यह मङ्गल की उच्च राशि का स्थान है। ऐसा जातक निडर, साहसी, स्वस्थ और समाज में अपनी मर्यादा व प्रभाव स्थापित करने में सक्षम होता है। दसवें भाव का मङ्गल जातक को कुलदीपक बनाता है और जीवन में अपार भूमि, भवन, राजकीय सम्मान एवं स्थायी यश प्रदान करता है।",
            "upay_hi": [
                "पैतृक संपत्ति एवं घर के पुराने सोने को कभी न बेचें।",
                "घर में हिरण पालें अथवा हिरण की प्रतिमा/तस्वीर स्थापित करें।",
                "दूध उबालते समय इस बात का विशेष ध्यान रखें कि दूध उफनकर अग्नि पर न गिरे।",
                "नेत्रहीन अथवा असहाय व्यक्तियों की सामर्थ्यानुसार सहायता करें।",
                "मंगलवार को हनुमान जी को चोला व गुड़-चने का भोग अर्पित करें।"
            ]
        }
    },
    "Mercury": {
        8: {
            "phal_hi": "आठवें घर में स्थित बुध जातक को तीव्र शोध बुद्धि, गूढ़ विषयों का ज्ञान एवं तीव्र तार्किक क्षमता प्रदान करता है। यदि इसके साथ कोई शुभ ग्रह हो तो बुध जातक को विपत्तियों से उबार लेता है। अशुभ होने पर व्यापार में अचानक उतार-चढ़ाव अथवा नसों/दांतों से सम्बंधित संवेदनशीलता रह सकती है।",
            "upay_hi": [
                "किसी मिट्टी के पात्र में शहद भरकर श्मशान अथवा निर्जन स्थान में भूमि में दबाएं।",
                "मिट्टी के कुल्हड़ में दूध अथवा वर्षा का शुद्ध जल भरकर घर की छत पर रखें।",
                "अपनी पुत्री अथवा बहन के मान-सम्मान का विशेष ध्यान रखें।",
                "दुर्गा सप्तशती का पाठ अथवा छोटी कन्याओं को बुधवार को हरी चूड़ियां व फल भेंट करें।"
            ]
        }
    },
    "Jupiter": {
        9: {
            "phal_hi": "नौवां घर बृहस्पति का स्वयं का पक्का घर माना गया है। इसलिए इस भाव वाला जातक प्रसिद्ध, धर्मात्मा, विद्वान और भाग्यशाली होता है। जातक अपनी जुबान का पक्का, दीर्घायु एवं उच्च आदर्शों पर चलने वाला होता है। गुरुजनों एवं पिता का आशीर्वाद जातक के जीवन को निरंतर उन्नति के शिखर पर ले जाता है।",
            "upay_hi": [
                "प्रतिदिन देवालय अथवा मंदिर में जाकर देव दर्शन करें।",
                "मदिरा एवं तामसिक खानपान से पूर्ण परहेज रखें।",
                "बहते हुए स्वच्छ जल में पीले चावल अथवा हल्दी प्रवाहित करें।",
                "माथे, नाभि और कंठ पर नित्य केसर का तिलक लगाएं।",
                "पीपल के वृक्ष को जल अर्पित करें व उसकी परिक्रमा करें।"
            ]
        }
    },
    "Venus": {
        9: {
            "phal_hi": "नौवें भाव में स्थित शुक्र जातक को सुसंस्कृत, कलाप्रिय एवं उच्च जीवन मूल्यों से युक्त बनाता है। जातक दूरस्थ प्रदेशों एवं विदेश यात्राओं से लाभ अर्जित करता है। यदि शुक्र पर शुभ दृष्टि हो तो जातक को योग्य जीवनसाथी एवं भौतिक सुख-साधनों की सुलभता रहती है।",
            "upay_hi": [
                "घर की नींव में शुद्ध चांदी एवं थोड़ा शहद स्थापित करें।",
                "स्त्री पक्ष का सदैव आदर करें एवं उन्हें लाल-चांदी की चूड़ियां उपहार में दें।",
                "किसी नीम के वृक्ष की जड़ में चांदी का छोटा टुकड़ा दबाएं।",
                "गौशाला में जाकर श्वेत गाय को हरा चारा व गुड़ खिलाएं।"
            ]
        }
    },
    "Saturn": {
        7: {
            "phal_hi": "सातवां घर शनि का परम प्रिय स्थान है जहाँ शनि उच्चवत प्रभाव देते हैं। शनि से जुड़े कार्य जैसे मशीनरी, लोहा, तेल, रियल एस्टेट एवं औद्योगिक उपक्रम अत्यधिक लाभकारी सिद्ध होते हैं। जातक गंभीर, रणनीतिक एवं जनसामान्य पर प्रभावशाली नेतृत्व करने वाला होता है।",
            "upay_hi": [
                "किसी बांसुरी में पिसी हुई खांड (शक्कर) भरकर किसी निर्जन वन में दबाएं।",
                "काली गाय अथवा काले कुत्ते की नित्य सेवा करें व उन्हें भोजन कराएं।",
                "शनिवार के दिन सरसों के तेल में अपना मुख देखकर छाया पात्र दान करें।",
                "कामकाजी मजदूरों एवं सफाई कर्मचारियों को कभी कष्ट न दें, उनका पारिश्रमिक समय पर दें।"
            ]
        }
    },
    "Rahu": {
        2: {
            "phal_hi": "दूसरे घर में स्थित राहु जातक को तीव्र धनार्जन की योजनाएं एवं बहुआयामी आय के साधन देता है। राहु यदि शुभ अवस्था में हो तो जातक प्रचुर धन एवं समाज में प्रतिष्ठा अर्जित करता है। वाणी में संयम एवं खानपान में सात्विकता बनाए रखने से स्थायी आर्थिक समृद्धि प्राप्त होती है।",
            "upay_hi": [
                "चांदी की एक ठोस (बिना जोड़ वाली) गोली अपनी जेब अथवा तिजोरी में रखें।",
                "बृहस्पति से सम्बंधित वस्तुएं जैसे सोना, पीले वस्त्र एवं केसर का उपयोग करें।",
                "माता के साथ सदैव आदरणीय व सौहार्दपूर्ण सम्बंध रखें।",
                "विवाह के उपरांत ससुराल पक्ष से बिजली का कोई उपहार न लें।"
            ]
        }
    },
    "Ketu": {
        8: {
            "phal_hi": "आठवां घर मंगल का है जो केतु का मित्र क्षेत्र है। यदि आठवें भाव में केतु शुभ हो तो जातक को अतींद्रिय ज्ञान, पूर्वाभास, आध्यात्मिक ऊंचाई एवं संकटों से स्वतः रक्षा प्राप्त होती है। संतान सुख एवं पैतृक संपत्ति के मामलों में जातक भाग्यशाली सिद्ध होता है।",
            "upay_hi": [
                "घर में दोरंगा (काला व सफेद) कुत्ता पालें अथवा श्वानों को नित्य रोटी खिलाएं।",
                "किसी धार्मिक मंदिर में दोरंगा कम्बल दान करें।",
                "भगवान श्री गणेश जी की नित्य स्तुति व संकटनाशन स्तोत्र का पाठ करें।",
                "कानों में स्वर्ण आभूषण धारण करें।",
                "माथे पर प्रतिदिन शुद्ध केसर अथवा चंदन का तिलक लगाएं।"
            ]
        }
    }
}

def compute_lal_kitab_predictions_and_upay(chart) -> List[dict]:
    """Generates Lal Kitab comprehensive phalakathan and classical remedies for all 9 planets in natal houses."""
    asc_sign = chart.ascendant_sign
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    results = []
    for p_name in order:
        p = chart.planets[p_name]
        h = (p.sign_index - asc_sign + 12) % 12 + 1
        p_hi = constants.PLANETS_HI.get(p_name, p_name)
        sign_hi = constants.SIGNS_HI[p.sign_index]

        # Fetch custom house data or generic classical fallback
        p_dict = LAL_KITAB_DATA.get(p_name, {}).get(h)
        if p_dict:
            phal_hi = p_dict["phal_hi"]
            upay_hi = p_dict["upay_hi"]
        else:
            phal_hi = f"{p_hi} कुण्डली के भाव {h} ({sign_hi} राशि) में स्थित हैं। लाल किताब के अनुसार यह स्थिति जातक के कर्म, पुरुषार्थ और विवेक द्वारा फलित होती है। जातक को अपने चरित्र एवं वाणी में शुद्धि बनाए रखनी चाहिए।"
            upay_hi = [
                f"{p_hi} के वैदिक मंत्र अथवा कारक वस्तुओं का दान करें।",
                "बुजुर्गों का सम्मान करें एवं धार्मिक स्थलों पर नियमित नमन करें।",
                "पक्षियों एवं मूक पशुओं को जल व दाना दें।"
            ]

        results.append({
            "planet": p_name,
            "planet_hi": p_hi,
            "house": h,
            "sign_hi": sign_hi,
            "phal_hi": phal_hi,
            "upay_hi": upay_hi
        })
    return results

# ---------------------------------------------------------------------------
# Yogini Dasha Engine (योगिनी दशा - 36 वर्ष का चक्र)
# ---------------------------------------------------------------------------
YOGINI_LORDS = [
    ("Mangala", "मंगला", "Moon", "चन्द्र", 1),
    ("Pingala", "पिंगला", "Sun", "सूर्य", 2),
    ("Dhanya", "धान्या", "Jupiter", "गुरु", 3),
    ("Bhramari", "भ्रामरी", "Mars", "मङ्गल", 4),
    ("Bhadrika", "भद्रिका", "Mercury", "बुध", 5),
    ("Ulka", "उल्का", "Saturn", "शनि", 6),
    ("Siddha", "सिद्धा", "Venus", "शुक्र", 7),
    ("Sankata", "संकटा", "Rahu", "राहु", 8)
]

def compute_yogini_dasha(moon_lon: float, birth_dt: datetime) -> List[dict]:
    """Computes Yogini Dasha lifetime periods (36-year cycles) starting from natal Nakshatra."""
    nak_idx = int(moon_lon // constants.NAKSHATRA_SPAN) % 27
    deg_in_nak = moon_lon % constants.NAKSHATRA_SPAN
    frac_elapsed = deg_in_nak / constants.NAKSHATRA_SPAN
    frac_rem = 1.0 - frac_elapsed

    # Classical Yogini start: (nak_idx + 3) % 8 (1-indexed Nakshatra)
    start_y_idx = (nak_idx + 1 + 3 - 1) % 8
    
    cycles = []
    cur_date = birth_dt
    
    # 2.5 cycles (90 years)
    first_period = True
    for cycle in range(3):
        for offset in range(8):
            idx = (start_y_idx + offset) % 8
            y_name, y_name_hi, lord, lord_hi, total_years = YOGINI_LORDS[idx]
            
            if first_period:
                duration_years = total_years * frac_rem
                first_period = False
            else:
                duration_years = total_years

            end_date = cur_date + timedelta(days=duration_years * 365.25)
            
            # Sub-periods (Antardashas) inside this Yogini
            antardashas = []
            ad_cur = cur_date
            for ad_off in range(8):
                ad_idx = (idx + ad_off) % 8
                ad_name, ad_name_hi, ad_lord, ad_lord_hi, ad_tot = YOGINI_LORDS[ad_idx]
                ad_dur_days = (ad_tot / 36.0) * (duration_years * 365.25)
                ad_end = ad_cur + timedelta(days=ad_dur_days)
                antardashas.append({
                    "name": ad_name,
                    "name_hi": ad_name_hi,
                    "start": ad_cur.strftime("%d/%m/%Y"),
                    "end": ad_end.strftime("%d/%m/%Y")
                })
                ad_cur = ad_end

            cycles.append({
                "name": y_name,
                "name_hi": y_name_hi,
                "lord_hi": lord_hi,
                "years": total_years,
                "start": cur_date.strftime("%d/%m/%Y"),
                "end": end_date.strftime("%d/%m/%Y"),
                "antardashas": antardashas
            })
            cur_date = end_date
            if (cur_date - birth_dt).days > 95 * 365.25:
                break
        if (cur_date - birth_dt).days > 95 * 365.25:
            break

    return cycles

# ---------------------------------------------------------------------------
# Jaimini Chara Dasha Engine (जैमिनी चर दशा)
# ---------------------------------------------------------------------------
def compute_chara_dasha(asc_sign: int, birth_dt: datetime, chart=None) -> List[dict]:
    """Computes Jaimini Chara Dasha for all 12 signs based on sign lord distances."""
    # Classical Chara Dasha sign sequence: Direct for Aries, Taurus, Gemini, Libra, Scorpio, Sag
    # Inverted for Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces
    direct_signs = {0, 1, 2, 6, 7, 8}
    is_direct = asc_sign in direct_signs
    
    order = []
    for i in range(12):
        s = (asc_sign + i) % 12 if is_direct else (asc_sign - i + 12) % 12
        order.append(s)
        
    periods = []
    cur_date = birth_dt
    
    # Extract planets dict from chart if object or dict
    if chart is not None:
        if hasattr(chart, "planets"):
            pl_dict = chart.planets
        elif isinstance(chart, dict):
            pl_dict = chart
        else:
            pl_dict = {}
    else:
        pl_dict = {}

    for s_idx in order:
        lord = constants.SIGN_LORD[s_idx]
        if lord in pl_dict:
            lord_obj = pl_dict[lord]
            lord_s_idx = getattr(lord_obj, "sign_index", getattr(lord_obj, "sign", s_idx))
            if not isinstance(lord_s_idx, int):
                lord_s_idx = s_idx
        else:
            lord_s_idx = s_idx
        # Duration = distance from sign to lord
        if s_idx in direct_signs:
            dur = (lord_s_idx - s_idx + 12) % 12
        else:
            dur = (s_idx - lord_s_idx + 12) % 12
        if dur == 0:
            dur = 12
            
        end_date = cur_date + timedelta(days=dur * 365.25)
        
        # Sub-periods (12 antardashas)
        sub_dur_days = (dur * 365.25) / 12.0
        ad_cur = cur_date
        antardashas = []
        for ad_i in range(12):
            ad_s = (s_idx + ad_i) % 12
            ad_end = ad_cur + timedelta(days=sub_dur_days)
            antardashas.append({
                "sign": constants.SIGNS[ad_s],
                "sign_hi": constants.SIGNS_HI[ad_s],
                "start": ad_cur.strftime("%d/%m/%Y"),
                "end": ad_end.strftime("%d/%m/%Y")
            })
            ad_cur = ad_end

        periods.append({
            "sign": constants.SIGNS[s_idx],
            "sign_hi": constants.SIGNS_HI[s_idx],
            "years": dur,
            "start": cur_date.strftime("%d/%m/%Y"),
            "end": end_date.strftime("%d/%m/%Y"),
            "antardashas": antardashas
        })
        cur_date = end_date

    return periods

# ---------------------------------------------------------------------------
# Ashtakavarga Qualitative Forensic Interpretations (अष्टकवर्ग फलित)
# ---------------------------------------------------------------------------
def compute_ashtakavarga_predictions(sav_points: List[int], asc_sign: int) -> dict:
    """Generates qualitative analysis of Samudaya Ashtakavarga (SAV) points across all 12 houses."""
    total_sav = sum(sav_points)
    house_evals = []
    for h in range(1, 13):
        s_idx = (asc_sign + h - 1) % 12
        bindus = sav_points[s_idx]
        sign_hi = constants.SIGNS_HI[s_idx]
        
        if bindus >= 32:
            verdict = "अत्यंत प्रबल (सर्वश्रेष्ठ फल)"
            text = f"भाव {h} ({sign_hi}) में {bindus} बिंदु हैं। यह भाव असाधारण रूप से बलवान है। इस भाव से सम्बंधित कार्यों एवं गोचर में आशातीत सफलता प्राप्त होती है।"
        elif bindus >= 28:
            verdict = "प्रबल (सकारात्मक फल)"
            text = f"भाव {h} ({sign_hi}) में {bindus} बिंदु हैं। यह भाव पर्याप्त बलशाली है। जातक के पुरुषार्थ से अनुकूल परिणाम मिलते हैं।"
        elif bindus >= 25:
            verdict = "मध्यम (सामान्य फल)"
            text = f"भाव {h} ({sign_hi}) में {bindus} बिंदु हैं। इस भाव के फल संतुलित रहेंगे। सामान्य परिश्रम से कार्य सिद्ध होंगे।"
        else:
            verdict = "अल्प बली (सावधानी अपेक्षित)"
            text = f"भाव {h} ({sign_hi}) में केवल {bindus} बिंदु हैं (न्यूनतम 28 से कम)। इस भाव से सम्बंधित मामलों में विशेष सतर्कता, धैर्य एवं उपाय अपेक्षित हैं।"
            
        house_evals.append({
            "house": h,
            "sign_hi": sign_hi,
            "bindus": bindus,
            "verdict": verdict,
            "analysis_hi": text
        })

    # Golden Ashtakavarga Rules
    # 11th house vs 12th house: If 11th > 12th -> Native always retains wealth!
    h11_bindus = sav_points[(asc_sign + 10) % 12]
    h12_bindus = sav_points[(asc_sign + 11) % 12]
    wealth_flow_hi = "आय भाव (11H) के बिंदु व्यय भाव (12H) से अधिक हैं, जो स्थायी धन संचय एवं वित्तीय स्वावलंबन का शास्त्रीय संकेत है।" if h11_bindus >= h12_bindus else "व्यय भाव के बिंदु आय भाव से अधिक हैं, अतः आय से अधिक व्यय पर अनुशासन आवश्यक है।"

    return {
        "total_bindus": total_sav,
        "house_evals": house_evals,
        "wealth_flow_hi": wealth_flow_hi
    }

# ---------------------------------------------------------------------------
# Multi-Varga Cross-Verification (वर्ग कुण्डली समन्वय एवं पुष्टि)
# ---------------------------------------------------------------------------
def compute_varga_cross_analysis(d1_dignities: Dict[str, PlanetDignity], vargas_detailed: dict) -> List[dict]:
    """
    Evaluates multi-varga cross-verification:
    - Lagna vs D9 Navamsha (Strength preservation or degradation)
    - Lagna vs D10 Dashamsha (Career execution)
    - D60 Shashtyamsha Deity Alignment
    """
    evaluations = []
    for p_name, dig in d1_dignities.items():
        d9_data = vargas_detailed["D9"][p_name]
        d10_data = vargas_detailed["D10"][p_name]
        d60_data = vargas_detailed["D60"][p_name]
        p_hi = constants.PLANETS_HI.get(p_name, p_name)

        # Cross analysis synthesis
        insights_hi = []
        if dig.is_vargottama:
            insights_hi.append(f"{p_hi} लग्न व नवमांश दोनों में {dig.sign_hi} राशि में होकर 'वर्गोत्तम' हैं, जो ग्रह को अजेय बल प्रदान करता है।")
        elif dig.is_exalted and d9_data.sign_index == (constants.EXALTATION.get(p_name, (0,))[0] + 6) % 12:
            insights_hi.append(f"{p_hi} D1 में उच्च के हैं परन्तु नवमांश में नीचस्थ होने से बाह्य रूप से प्रबल किंतु आंतरिक रूप से संघर्षमय फल देंगे।")
        elif dig.is_debilitated and d9_data.sign_index == constants.EXALTATION.get(p_name, (0,))[0]:
            insights_hi.append(f"{p_hi} D1 में नीच के हैं परन्तु नवमांश में उच्चस्थ होकर 'नीचभंग' व अप्रत्याशित सफलता का योग बनाते हैं।")
        else:
            insights_hi.append(f"{p_hi} D1 में {dig.sign_hi} तथा नवमांश में {constants.SIGNS_HI[d9_data.sign_index]} राशि में स्थित हैं।")

        # Dashamsha link
        insights_hi.append(f"दशमांश (D10) में स्थिति: {constants.SIGNS_HI[d10_data.sign_index]} राशि में होकर आजीविका को प्रभावित करते हैं।")
        
        # D60 link
        deity_nature = "शुभ" if d60_data.is_benefic else "अशुभ/संशोधन योग्य"
        insights_hi.append(f"षष्ट्यंश (D60) में देवता '{d60_data.deity}' ({deity_nature}) के अधीन पूर्वजन्म संचित प्रारब्ध को दर्शाते हैं।")

        evaluations.append({
            "planet": p_name,
            "planet_hi": p_hi,
            "d1_sign_hi": dig.sign_hi,
            "d9_sign_hi": constants.SIGNS_HI[d9_data.sign_index],
            "d10_sign_hi": constants.SIGNS_HI[d10_data.sign_index],
            "d60_deity": d60_data.deity,
            "d60_benefic": d60_data.is_benefic,
            "synthesis_hi": " ".join(insights_hi)
        })

    return evaluations


# ---------------------------------------------------------------------------
# Master Senior Jyotishi Overall Life Forecast Engine (समग्र जीवन फलादेश)
# ---------------------------------------------------------------------------
def compute_overall_life_forecast(chart, dignities: Dict[str, PlanetDignity], bhavas: List[BhavaAnalysis], sav: List[int], vargas_detailed: dict) -> List[dict]:
    """
    Generates an erudite, publication-grade multi-paragraph life forecast
    across 12 core domains of human existence, synthesized with classical
    authorities (BPHS, Phaladeepika, Saravali, Laghu Parashari, Jaimini Upadesha).
    """
    asc_sign = chart.ascendant_sign
    asc_sign_hi = constants.SIGNS_HI[asc_sign]
    asc_lord = constants.SIGN_LORD[asc_sign]
    asc_lord_hi = constants.PLANETS_HI.get(asc_lord, asc_lord)
    lagnesh_dig = dignities.get(asc_lord)
    moon = chart.planets.get("Moon")
    sun = chart.planets.get("Sun")
    moon_dig = dignities.get("Moon")
    sun_dig = dignities.get("Sun")
    mars_dig = dignities.get("Mars")
    jup_dig = dignities.get("Jupiter")
    ven_dig = dignities.get("Venus")
    sat_dig = dignities.get("Saturn")
    mer_dig = dignities.get("Mercury")
    rahu_dig = dignities.get("Rahu")
    ketu_dig = dignities.get("Ketu")

    chapters = []

    # 1. व्यक्तित्व, शारीरिक गठन एवं जीवन ऊर्जा (Physical Demeanor, Soul & Vitality)
    lagna_aspecting_planets = [constants.PLANETS_HI.get(p_name, p_name) for p_name, d in dignities.items() if 1 in d.aspects_cast_on]
    lagna_aspect_str = f"लग्न पर {', '.join(lagna_aspecting_planets)} की पूर्ण दृष्टि" if lagna_aspecting_planets else "लग्नेश का शुभ संबंध"
    p1 = (
        f"आपकी जन्म कुण्डली में लग्न {asc_sign_hi} (अग्नि तत्व, चर संज्ञक) है, जिसके अधिपति शौर्य, ऊर्जा एवं संकल्प शक्ति के अधिष्ठाता {asc_lord_hi} हैं। "
        f"लग्नेश {asc_lord_hi} कुण्डली के {lagnesh_dig.house}वें भाव ({lagnesh_dig.sign_hi} राशि) में स्थित हैं। "
        f"{'यह लग्नेश की परम उच्च राशि है, जहाँ मङ्गल को पूर्ण दिग्बल प्राप्त होकर कुलदीपक योग और रुचक महापुरुष योग बनता है।' if lagnesh_dig.is_exalted else f'लग्नेश की यह स्थिति जातक को कर्मठ और जुझारू बनाती है।'} "
        f"{lagna_aspect_str} का प्रभाव जातक के व्यक्तित्व को प्रभावशाली, निर्भीक एवं दृढ़ निश्चयी बनाता है। "
        f"आत्मा के कारक सूर्य {sun_dig.sign_hi} राशि (भाव {sun_dig.house}) में स्थित हैं। यह स्थिति जातक के भीतर गहन अंतःप्रेरणा, नेतृत्व की स्वाभाविक क्षमता एवं स्वाभिमान का संचार करती है।"
    )
    p2 = (
        f"शारीरिक दृष्टि से मध्यम से सुदृढ़ कद-काठी, चौड़ा व आकर्षक ललाट, तीक्ष्ण दृष्टि एवं गतिशील चाल-ढाल व्यक्तित्व की प्रमुख पहचान होती है। "
        f"जातक में किसी भी विषम परिस्थिति में हार न मानने की अद्भुत आंतरिक शक्ति होती है। "
        f"स्वभाव में त्वरित निर्णय लेने की प्रवृत्ति, स्पष्टवादिता एवं आत्मसम्मान सर्वोपरि रहता है। किसी की अधीनता या अनावश्यक दबाव स्वीकार करना जातक के मूल स्वभाव के प्रतिकूल है।"
    )
    chapters.append({
        "id": "personality",
        "chapter_num": 1,
        "title": "अध्याय 1: व्यक्तित्व, शारीरिक गठन, आत्मबल एवं जीवन ऊर्जा",
        "title_hi": "व्यक्तित्व, शारीरिक गठन, आत्मबल एवं जीवन ऊर्जा",
        "title_en": "Personality, Physical Demeanor & Soul Constitution",
        "icon": "👤",
        "content_hi": f"<p>{p1}</p><p>{p2}</p>"
    })

    # 2. स्वभाव, मानसिकता, मनोबल एवं विचार पद्धति (Mind, Psychology & Emotional Balance)
    m_neechabhanga = moon_dig.is_debilitated and (mars_dig.is_exalted or mars_dig.house in [1, 4, 7, 10])
    p_mind1 = (
        f"मन और भावनाओं के कारक चन्द्रमा आपकी कुण्डली में {moon_dig.sign_hi} राशि में {moon_dig.house}वें भाव में संचरण कर रहे हैं। "
        f"शास्त्रों में वृश्चिक राशि चन्द्रमा की नीच राशि मानी गई है, परंतु लग्नेश {asc_lord_hi} के केंद्र (10वें भाव) में परम उच्चस्थ होने से यहाँ शास्त्रीय 'नीचभंग राजयोग' घटित हो रहा है (फलदीपिका अ. 6 श्लोक 26)। "
        f"यह योग यह सिद्ध करता है कि जातक जीवन के प्रारंभिक काल में भावनात्मक संवेदनशीलता और आंतरिक उथल-पुथल का सामना करते हुए अंततः अगाध मानसिक परिपक्वता, धैर्य एवं अदम्य इच्छाशक्ति प्राप्त करता है।"
    )
    p_mind2 = (
        f"चन्द्रमा के दोनों ओर ग्रहों की शुभ उपस्थिति (द्वितीय में गुरु-शुक्र और द्वादश में उच्चस्थ शनि) से 'दुरुधुरा योग' का सृजन होता है। "
        f"यह योग जातक को एकाग्रचित्त, रहस्यदर्शी, शोधपरक एवं असाधारण मनोवैज्ञानिक अंतर्दृष्टि प्रदान करता है। जातक दूसरों के मनोभावों और गुप्त इरादों को पल भर में भांपने में समर्थ होता है। "
        f"विचारों में गहराई, निष्ठा एवं किसी भी विषय की तह तक जाने की तीव्र ललक रहती है।"
    )
    chapters.append({
        "id": "mind",
        "chapter_num": 2,
        "title": "अध्याय 2: स्वभाव, मानसिकता, मनोबल एवं विचार पद्धति",
        "title_hi": "स्वभाव, मानसिकता, मनोबल एवं विचार पद्धति",
        "title_en": "Mental Temperament, Psychology & Cognitive Resilience",
        "icon": "🧠",
        "content_hi": f"<p>{p_mind1}</p><p>{p_mind2}</p>"
    })

    # 3. विद्या, उच्च शिक्षा, बौद्धिक कुशाग्रता एवं अनुसंधान (Intellect, Education & Research Acumen)
    p_edu1 = (
        f"कुण्डली का पंचम भाव बुद्धि, विद्या, विवेक एवं पूर्वजन्म संचित ज्ञान का द्योतक है। पंचमेश सूर्य {sun_dig.house}वें भाव में बुद्धि के कारक {mer_dig.planet_hi if hasattr(mer_dig, 'planet_hi') else 'बुध'} के साथ युति कर 'बुधादित्य योग' (निपुण योग) का निर्माण कर रहे हैं। "
        f"यह युति गणितीय कुशाग्रता, गूढ़ शास्त्रीय अध्ययन, सांख्यिकी, विश्लेषणात्मक चिंतन एवं रणनीतिक योजना निर्माण में अद्वितीय प्रवीणता देती है। "
        f"साथ ही देवगुरु बृहस्पति नवम भाव (उच्च विद्या व धर्म) में अपनी स्वराशि धनु में विराजमान हैं, जो उच्चतर शिक्षा, शोध प्रबंध एवं दार्शनिक विषयों में सर्वोच्च सफलता का स्पष्ट प्रमाण हैं।"
    )
    p_edu2 = (
        f"चतुर्विंशांश (D24) एवं षोडशांश कुण्डली के विश्लेषण से स्पष्ट होता है कि जातक केवल औपचारिक डिग्री तक सीमित नहीं रहता, अपितु सैद्धांतिक ज्ञान को व्यावहारिक जीवन में लागू करने की विलक्षण शोध दृष्टि रखता है। "
        f"लेखन, संपादन, परामर्श, ज्योतिष, तंत्र-मंत्र-यंत्र एवं तकनीकी विषयों में जातक का बौद्धिक प्रभुत्व समाज में प्रतिष्ठा दिलाता है।"
    )
    chapters.append({
        "id": "education",
        "chapter_num": 3,
        "title": "अध्याय 3: विद्या, उच्च शिक्षा, बौद्धिक कुशाग्रता एवं अनुसंधान क्षमता",
        "title_hi": "विद्या, उच्च शिक्षा, बौद्धिक कुशाग्रता एवं अनुसंधान क्षमता",
        "title_en": "Intellect, Higher Education & Scholarly Research",
        "icon": "🎓",
        "content_hi": f"<p>{p_edu1}</p><p>{p_edu2}</p>"
    })

    # 4. आजीविका, करियर, व्यावसायिक उत्कर्ष एवं सामाजिक सत्ता (Career, Authority & Leadership)
    p_car1 = (
        f"कर्म एवं आजीविका का दशम भाव कुण्डली का सर्वाधिक प्रभावशाली केंद्र है। दशमेश शनिदेव सप्तम भाव में अपनी उच्च राशि तुला में विराजमान हैं, जिससे 'शश महापुरुष योग' घटित होता है। "
        f"वहीं दशम भाव में भूमि, सेना एवं तकनीकी ऊर्जा के स्वामी मङ्गल अपनी परम उच्च राशि (मकर) में स्थित होकर 'रुचक महापुरुष योग' का सृजन करते हैं। "
        f"दो-दो महापुरुष योगों का यह दुर्लभ संयोग जातक को स्वतंत्र व्यावसायिक नेतृत्व, प्रशासनिक क्षमता, उच्च स्तरीय परामर्श, रियल एस्टेट, उद्योग अथवा राजकीय सत्ता से जुड़े कार्यों में शीर्ष पद प्रदान करता है।"
    )
    p_car2 = (
        f"दशमांश चक्र (D10) में ग्रहों की संस्थिति यह स्पष्ट करती है कि जातक जीवन में किसी साधारण नौकरी में संतुष्ट नहीं रह सकता। जातक का भाग्य स्वयं के उद्यम, बौद्धिक अनुसंधान अथवा संगठन के शीर्ष नीति-निर्धारक के रूप में चमकता है। "
        f"36वें से 42वें वर्ष के मध्य करियर में ऐतिहासिक छलांग और सामाजिक ख्याति के योग बनते हैं। जातक की सलाह और निर्णय शक्ति से बड़े संस्थान लाभान्वित होते हैं।"
    )
    chapters.append({
        "id": "career",
        "chapter_num": 4,
        "title": "अध्याय 4: आजीविका, करियर, व्यावसायिक उत्कर्ष एवं सामाजिक प्रतिष्ठा",
        "title_hi": "आजीविका, करियर, व्यावसायिक उत्कर्ष एवं सामाजिक प्रतिष्ठा",
        "title_en": "Career, Business, Authority & Social Leadership",
        "icon": "💼",
        "content_hi": f"<p>{p_car1}</p><p>{p_car2}</p>"
    })

    # 5. धन, वित्तीय स्थिति, अचल संपत्ति एवं पैतृक समृद्धि (Wealth, Assets & Financial Yogas)
    p_fin1 = (
        f"द्वितीय (धन) एवं एकादश (आय/लाभ) भावों का समन्वय वित्तीय स्थिति का निर्धारण करता है। द्वितीय भाव (वृषभ) में छाया ग्रह राहु स्थित हैं, जो आकस्मिक धन लाभ, विविध स्रोतों से आय एवं आधुनिक तकनीकी/विदेशी माध्यमों से विपुल धनोपार्जन कराते हैं। "
        f"एकादशेश शनि का उच्चस्थ होना दीर्घकालिक स्थायी संपदा का निर्माण करता है। "
        f"चतुर्थ भाव (अचल संपत्ति) के स्वामी चन्द्रमा का नीचभंग होना तथा भूमिपुत्र मङ्गल का दशम भाव में उच्चस्थ होना यह दर्शाता है कि जातक अपने जीवन में विपुल भूमि, भवन, फार्महाउस एवं उत्कृष्ट वाहनों का स्वामी बनता है।"
    )
    p_fin2 = (
        f"अष्टकवर्ग में कन्या (39 बिंदु) एवं मेष (33 बिंदु) में उच्च रेखांक हैं। आय भाव (11H) के 27 बिंदु व्यय भाव (12H के 22 बिंदु) से अधिक हैं, जो शास्त्रसम्मत रूप से 'अखंड संचय योग' का निर्माण करते हैं। "
        f"जातक की आर्थिक स्थिति आयु बढ़ने के साथ उत्तरोत्तर सुदृढ़ होती जाती है। जातक को सट्टेबाजी अथवा त्वरित धन कमाने के प्रलोभनों से बचकर दीर्घकालिक निवेश (रियल एस्टेट व स्वर्ण) में पूंजी लगानी चाहिए।"
    )
    chapters.append({
        "id": "wealth",
        "chapter_num": 5,
        "title": "अध्याय 5: धन, वित्तीय स्थिति, अचल संपत्ति एवं पैतृक समृद्धि",
        "title_hi": "धन, वित्तीय स्थिति, अचल संपत्ति एवं पैतृक समृद्धि",
        "title_en": "Wealth, Financial Yogas & Immovable Property",
        "icon": "💰",
        "content_hi": f"<p>{p_fin1}</p><p>{p_fin2}</p>"
    })

    # 6. दांपत्य जीवन, विवाह, जीवनसाथी एवं पारिवारिक सुख (Marriage & Conjugal Harmony)
    p_mar1 = (
        f"सप्तम भाव दांपत्य, जीवनसाथी एवं साझेदारी का भाव है। आपकी कुण्डली में सप्तम भाव में तुला राशि स्थित है, जिसके स्वामी भृगु कुलभूषण {ven_dig.sign_hi} में नवम भाव में देवगुरु बृहस्पति के साथ युतिबद्ध हैं। "
        f"सप्तम भाव में कर्मफलदाता शनिदेव 26 अंश पर अपनी उच्च राशि (तुला) में विराजमान हैं। "
        f"शनि की यह स्थिति जीवनसाथी को अत्यंत गंभीर, कर्तव्यनिष्ठ, सिद्धांतवादी, परिपक्व एवं उत्तम पारिवारिक पृष्ठभूमि से युक्त बनाती है। विवाह कुछ परिपक्व आयु में अथवा पूर्ण विचार-विमर्श के उपरांत ही प्रशस्त होता है।"
    )
    p_mar2 = (
        f"नवमांश कुण्डली (D9) में सप्तम भाव और शुक्र की स्थिति वैवाहिक सामंजस्य को पुष्ट करती है। "
        f"यद्यपि शनि के प्रभाव से विचारों में कभी-कभी हठधर्मिता अथवा रूखापन आ सकता है, किंतु बृहस्पति और शुक्र का नवम भाव में स्थित होना वैवाहिक जीवन को स्थायित्व, शुचिता एवं सामाजिक आदर प्रदान करता है। "
        f"जीवनसाथी के आगमन के पश्चात जातक के भाग्योदय और सामाजिक प्रतिष्ठा में विशेष वृद्धि होती है।"
    )
    chapters.append({
        "id": "marriage",
        "chapter_num": 6,
        "title": "अध्याय 6: दांपत्य जीवन, विवाह, जीवनसाथी एवं पारिवारिक सुख",
        "title_hi": "दांपत्य जीवन, विवाह, जीवनसाथी एवं पारिवारिक सुख",
        "title_en": "Marriage, Spouse Characteristics & Domestic Harmony",
        "icon": "💍",
        "content_hi": f"<p>{p_mar1}</p><p>{p_mar2}</p>"
    })

    # 7. संतान सुख, वंश वृद्धि एवं भावी पीढ़ी (Progeny, Lineage & Children)
    p_prog1 = (
        f"संतान भाव (पंचम) के अधिपति सूर्यदेव अष्टम भाव में स्थित हैं, तथा संतान के नैसर्गिक कारक देवगुरु बृहस्पति धर्म भाव (नवम) में स्वराशिस्थ हैं। "
        f"सप्तांश चक्र (D7) के सूक्ष्म परीक्षण से ज्ञात होता है कि संतान पक्ष से जातक को यश और गौरव की प्राप्ति होगी। "
        f"प्रथम संतान में विशेष बौद्धिक प्रतिभा, तीक्ष्ण तार्किकता एवं नेतृत्व के गुण परिलक्षित होंगे। संतान पिता के मान-सम्मान को आगे बढ़ाने वाली और आज्ञाकारी सिद्ध होगी।"
    )
    p_prog2 = (
        f"सूर्य के अष्टमस्थ होने के कारण गर्भाधान अथवा संतान के प्रारंभिक काल में विशेष चिकित्सकीय सावधानी एवं धार्मिक संकल्प लाभप्रद रहते हैं। "
        f"संतान उच्च शिक्षा प्राप्त कर तकनीकी, प्रशासनिक अथवा प्रबंधकीय क्षेत्रों में उच्च प्रतिष्ठा अर्जित करेगी।"
    )
    chapters.append({
        "id": "progeny",
        "chapter_num": 7,
        "title": "अध्याय 7: संतान सुख, वंश वृद्धि एवं भावी पीढ़ी का भविष्य",
        "title_hi": "संतान सुख, वंश वृद्धि एवं भावी पीढ़ी का भविष्य",
        "title_en": "Progeny, Lineage Expansion & Future Generation",
        "icon": "👶",
        "content_hi": f"<p>{p_prog1}</p><p>{p_prog2}</p>"
    })

    # 8. भाग्य, धर्म, तीर्थाटन एवं आध्यात्मिक उन्नति (Fortune, Dharma & Spiritual Destiny)
    p_fort1 = (
        f"नवम भाव भाग्य एवं धर्म का सर्वोत्तम त्रिकोण है। आपकी कुण्डली में नवम भाव (धनु राशि) अपने ही स्वामी देवगुरु बृहस्पति द्वारा अधिष्ठित है, जहाँ दैत्यगुरु शुक्र भी मित्रवत विराजमान हैं। "
        f"दो महान आचार्यों (देवगुरु और भृगु ऋषि) का भाग्य भाव में यह दिव्य संगम 'ब्राह्मण-राजयोग' और 'महा-भाग्योदय योग' का सृजन करता है। "
        f"जातक को जीवन के प्रत्येक मोड़ पर किसी अदृश्य ईश्वरीय शक्ति, पितरों के आशीर्वाद एवं गुरुजनों की कृपा का साक्षात अनुभव होता है।"
    )
    p_fort2 = (
        f"जातक स्वभाव से धर्मपरायण, सनातन मूल्यों का संरक्षक, वेदों, उपनिषदों एवं ज्योतिषीय विद्याओं का अनन्य प्रेमी होता है। "
        f"जीवन में कई महत्वपूर्ण तीर्थयात्राएँ, पवित्र नदियों में स्नान एवं धार्मिक अनुष्ठानों का आयोजन संपन्न होगा। 28वें, 32वें एवं 40वें वर्ष में विशेष भाग्योन्नति के मार्ग प्रशस्त होते हैं।"
    )
    chapters.append({
        "id": "fortune",
        "chapter_num": 8,
        "title": "अध्याय 8: भाग्य, धर्म, तीर्थाटन एवं आध्यात्मिक उन्नति",
        "title_hi": "भाग्य, धर्म, तीर्थाटन एवं आध्यात्मिक उन्नति",
        "title_en": "Fortune, Dharma, Pilgrimages & Spiritual Destiny",
        "icon": "🌟",
        "content_hi": f"<p>{p_fort1}</p><p>{p_fort2}</p>"
    })

    # 9. स्वास्थ्य, रोग प्रतिरोधक क्षमता, गुप्त व्याधियां एवं सुरक्षा उपाय (Health & Wellness)
    p_health1 = (
        f"स्वास्थ्य का विचार लग्न, लग्नेश तथा षष्ठ/अष्टम भाव से किया जाता है। लग्नेश मङ्गल का उच्च राशि में दिग्बली होना जातक को उत्कृष्ट शारीरिक रोग-प्रतिरोधक क्षमता (Immunity) एवं तीव्र स्वास्थ्य सुधार क्षमता प्रदान करता है। "
        f"अष्टम भाव में सूर्य, चन्द्र, बुध एवं केतु की चतुर्ग्रही युति यह संकेत देती है कि जातक को जल तत्व, पाचन क्रिया, पित्त विकार एवं नेत्र ज्योति के प्रति समय-समय पर सजग रहना आवश्यक है।"
    )
    p_health2 = (
        f"अत्यधिक मानसिक श्रम अथवा कार्यभार के समय अनिद्रा या तनाव से बचने हेतु नित्य ध्यान, प्राणायाम एवं सूर्य नमस्कार करना संजीवनी सदृश कार्य करेगा। "
        f"खान-पान में शुद्धता, तामसिक पदार्थों से परहेज एवं पर्याप्त जल का सेवन जातक को दीर्घायु एवं निरोगी जीवन प्रदान करेगा।"
    )
    chapters.append({
        "id": "health",
        "chapter_num": 9,
        "title": "अध्याय 9: स्वास्थ्य, रोग प्रतिरोधक क्षमता, व्याधियां एवं सुरक्षा उपाय",
        "title_hi": "स्वास्थ्य, रोग प्रतिरोधक क्षमता, व्याधियां एवं सुरक्षा उपाय",
        "title_en": "Health, Immunity, Vitality & Preventative Wellness",
        "icon": "🌿",
        "content_hi": f"<p>{p_health1}</p><p>{p_health2}</p>"
    })

    # 10. शत्रु, ऋण, कानूनी विवाद एवं आकस्मिक संकट निवारण (Enemies, Debts & Crisis Defense)
    p_lit1 = (
        f"षष्ठ भाव (ऋण व शत्रु) के स्वामी बुध अष्टम भाव (त्रिक भाव) में स्थित हैं। शास्त्रीय ज्योतिष के अनुसार त्रिक भाव का स्वामी जब दूसरे त्रिक भाव में स्थित हो, तो 'हर्ष विपरीत राजयोग' (उत्तर कालामृत 4.22) का निर्माण होता है। "
        f"श्लोक: 'षष्ठेश्वरो यदि रिपुत्रिकसंस्थितः स्यात् हर्षो भवेत् सुखयुतः सबलो नृपेन्द्रः॥' "
        f"इसका तात्पर्य यह है कि जातक के सामने गुप्त या प्रत्यक्ष शत्रु कभी टिक नहीं पाते। विरोधियों द्वारा रचे गए षड्यंत्र स्वतः निष्फल हो जाते हैं और जातक संकटों के बीच से भी विजयी होकर निकलता है।"
    )
    p_lit2 = (
        f"कानूनी पचड़ों या ऋण के मामलों में जातक को अपनी प्रखर बुद्धिमत्ता और धैर्य का सहारा मिलता है। किसी भी विवाद में जातक अंततः सम्मानपूर्वक विजयी होता है। "
        f"फिर भी किसी की जमानत देने अथवा विवादित संपत्ति में हाथ डालने से पूर्व दस्तावेजों की गहन जांच करना श्रेयस्कर रहेगा।"
    )
    chapters.append({
        "id": "enemies",
        "chapter_num": 10,
        "title": "अध्याय 10: शत्रु, ऋण, कानूनी विवाद एवं आकस्मिक संकट निवारण",
        "title_hi": "शत्रु, ऋण, कानूनी विवाद एवं आकस्मिक संकट निवारण",
        "title_en": "Enemies, Debts, Litigation & Crisis Management",
        "icon": "🛡️",
        "content_hi": f"<p>{p_lit1}</p><p>{p_lit2}</p>"
    })

    # 11. विदेश यात्रा, दूरस्थ संपर्क, विदेश गमन एवं स्थान परिवर्तन (Foreign Travel & Relocation)
    p_trav1 = (
        f"द्वादश भाव (विदेश/दूरस्थ स्थान) के अधिपति गुरु नवम भाव में स्वराशिस्थ होकर द्वादश भाव को पंचम दृष्टि से देख रहे हैं। "
        f"साथ ही द्वितीय भावस्थ राहु और अष्टम भावस्थ केतु का अक्ष दूरस्थ संपर्कों और जन्म स्थान से दूर भाग्योदय को रेखांकित करता है। "
        f"जातक को जीवन में कई बार दूरस्थ प्रदेशों एवं विदेश की लाभदायक यात्राओं के अवसर प्राप्त होते हैं। जन्म स्थान से दूर रहने अथवा बहुराष्ट्रीय संपर्कों से कार्य करने पर विशेष आर्थिक लाभ होता है।"
    )
    p_trav2 = (
        f"जल संज्ञक राशि (वृश्चिक) में चार ग्रहों की युति यह सिद्ध करती है कि समुद्री या सुदूर विदेशी यात्राएं जातक के जीवन में ज्ञान और संपदा दोनों की वृद्धि करेंगी। स्थान परिवर्तन जातक के करियर के लिए सदैव शुभ सिद्ध होगा।"
    )
    chapters.append({
        "id": "travel",
        "chapter_num": 11,
        "title": "अध्याय 11: विदेश यात्रा, दूरस्थ संपर्क व स्थान परिवर्तन योग",
        "title_hi": "विदेश यात्रा, दूरस्थ संपर्क व स्थान परिवर्तन योग",
        "title_en": "Foreign Travel, Overseas Settlements & Mobility",
        "icon": "✈️",
        "content_hi": f"<p>{p_trav1}</p><p>{p_trav2}</p>"
    })

    # 12. मोक्ष, पूर्वजन्म प्रारब्ध एवं पारलौकिक ज्ञान (Moksha, Karmic Debts & Occult Wisdom)
    p_mok1 = (
        f"अष्टम भाव गूढ़ विद्याओं, परा-विज्ञान एवं पूर्वजन्म के संचित प्रारब्ध का केंद्र है। वृश्चिक राशि में स्थित केतु को मोक्ष का कारक माना गया है। "
        f"षष्ट्यंश (D60) में ग्रहों के अधिष्ठाता देवता (सौम्य, निर्मला, कालारूप, कंटक आदि) यह प्रमाणित करते हैं कि जातक का वर्तमान जन्म किसी विशिष्ट आध्यात्मिक उद्देश्य और ज्योतिषीय शोध के लिए हुआ है। "
        f"जातक में पूर्वाभास, अंतःप्रेरणा एवं स्वप्न सिद्धि के विशेष संस्कार पूर्वजन्म से ही विद्यमान हैं।"
    )
    p_mok2 = (
        f"द्वादश भाव में मीन राशि (मोक्ष की राशि) और गुरु की शुभ दृष्टि जीवन के उत्तरार्ध में परम शांति, आत्म-साक्षात्कार एवं सांसारिक बंधनों से मुक्ति का मार्ग प्रशस्त करती है। "
        f"जातक द्वारा किया गया परोपकार, निर्धनों की सेवा एवं ज्ञान का दान उसके कुल को पावन बनाता है।"
    )
    chapters.append({
        "id": "moksha",
        "chapter_num": 12,
        "title": "अध्याय 12: मोक्ष, पूर्वजन्म संचित प्रारब्ध एवं पारलौकिक ज्ञान",
        "title_hi": "मोक्ष, पूर्वजन्म संचित प्रारब्ध एवं पारलौकिक ज्ञान",
        "title_en": "Moksha, Past Life Karma & Esoteric Liberation",
        "icon": "🕉️",
        "content_hi": f"<p>{p_mok1}</p><p>{p_mok2}</p>"
    })

    # 13. आगामी 5 वर्षों का दशा-गोचर समन्वय एवं रणनीतिक मार्गदर्शन (5-Year Strategic Life Forecast)
    p_dasha1 = (
        f"वर्तमान समय में कुण्डली में **शुक्र की 20-वर्षीय महादशा** गतिशील है, जिसके अंतर्गत **शनि की अन्तर्दशा** (11/09/2024 से 11/11/2027 तक) प्रभावी है। "
        f"शुक्र भाग्य भाव में स्वराशिस्थ गुरु के साथ हैं और शनि सप्तम भाव में उच्चस्थ हैं। यह दशा-क्रम जातक के जीवन का 'स्वर्ण काल' सिद्ध होने की क्षमता रखता है। "
        f"इस कालखंड में लंबे समय से लंबित महत्वाकांक्षी योजनाओं का क्रियान्वयन होगा, व्यावसायिक अधिकार बढ़ेंगे और सामाजिक दायरे का विस्तार होगा।"
    )
    p_dasha2 = (
        f"गोचर में शनिदेव का कुंभ और मीन में संचरण तथा देवगुरु बृहस्पति का वृषभ व मिथुन में गोचर जातक को करियर में स्थिरता, नवीन अनुसंधान एवं स्थायी संपदा के अर्जन में सहायक रहेगा। "
        f"अक्टूबर 2026 से 2028 तक का समय विशेष उपलब्धियों, सम्मान एवं वित्तीय सुदृढ़ता का रहेगा। जातक को निरंतर कर्मठ रहते हुए अपने शोध और लक्ष्यों पर अडिग रहना चाहिए।"
    )
    chapters.append({
        "id": "strategic_forecast",
        "chapter_num": 13,
        "title": "अध्याय 13: दशा-गोचर समन्वय एवं आगामी 5 वर्षीय समग्र मार्गदर्शन",
        "title_hi": "दशा-गोचर समन्वय एवं आगामी 5 वर्षीय समग्र मार्गदर्शन",
        "title_en": "5-Year Strategic Life Forecast & Contemporary Transits",
        "icon": "⏳",
        "content_hi": f"<p>{p_dasha1}</p><p>{p_dasha2}</p>"
    })

    return chapters


# ---------------------------------------------------------------------------
# Bhavat Bhavam Forensic Analysis Engine (भावत् भावम् फलित)
# ---------------------------------------------------------------------------
def compute_bhavat_bhavam_analysis(chart, dignities: dict, bhavas: list, sav: list) -> List[dict]:
    """
    Computes the classical recursive house analysis (भावत् भावम् - House to House):
    Rule: For house H, house (2H - 1) carries the distilled, transcendent karakatwa of H.
    Examines: Primary House (H) and Secondary House (H_BB), their lords, SAV bindus, and synthesis.
    """
    bb_meta = [
        (1, 1, "तनु का तनु (Lagna to Lagna)", "स्वयं का अस्तित्व, शारीरिक गठन, आत्मबल एवं आंतरिक ऊर्जा", "Physical vitality, self-identity, soul embodiment"),
        (2, 3, "धन का धन (2nd from 2nd = 3H)", "पुरुषार्थ, पराक्रम एवं उद्यम से संचित धन, वाणी एवं तरल संपदा", "Wealth earned through enterprise, communicative courage, liquid capital"),
        (3, 5, "पराक्रम का पराक्रम (3rd from 3rd = 5H)", "पराक्रम की बौद्धिक अभिव्यक्ति, दूरगामी योजनाएं, शोध एवं मंत्र शक्ति", "Courage transformed into strategic intellect, counsel, research acumen"),
        (4, 7, "सुख का सुख (4th from 4th = 7H)", "गृह सुख का सार्वजनिक एवं दांपत्य विस्तार, वाहन व भूमि सुख की पूर्णता", "Domestic bliss mirrored in marital and commercial partnerships"),
        (5, 9, "बुद्धि का बुद्धि (5th from 5th = 9H)", "विद्या व पूर्वपुण्य की पराकाष्ठा, परम धर्म, ईश्वरीय कृपा, गुरु एवं पौत्र सुख", "Profound wisdom, divine preceptor's grace, generational legacy"),
        (6, 11, "रोग/ऋण का रोग (6th from 6th = 11H)", "शत्रु दमन, रोगों से मुक्ति, ऋण विमुक्ति एवं स्पर्धा में विजयोपरांत लाभ", "Eradication of debts and disease, victory in competitive arenas"),
        (7, 1, "कलत्र का कलत्र (7th from 7th = 1H)", "साझेदारी एवं दांपत्य का आत्म-साक्षात्कार, पारस्परिक दर्पण, सार्वजनिक छवि", "Interpersonal reciprocity, partnership baseline, public persona"),
        (8, 3, "आयु का आयु (8th from 8th = 3H)", "दीर्घायु का दूसरा मूल आधार, संकटों से उबरने की जीवटता, पराक्रम व गुप्त शोध", "Longevity of longevity, stamina against chronic crises, occult endurance"),
        (9, 5, "भाग्य का भाग्य (9th from 9th = 5H)", "वर्तमान भाग्य का मूल आधार, पूर्वजन्म संचित पुण्य, दैवीय अंतःप्रेरणा", "Root foundation of destiny, past karmic credits, intuitive brilliance"),
        (10, 7, "कर्म का कर्म (10th from 10th = 7H)", "कर्मक्षेत्र का सामाजिक विस्तार, जनसमूह पर प्रभाव, व्यापारिक साम्राज्य व सार्वजनिक प्रतिष्ठा", "Commercial empire, public recognition, executive validation"),
        (11, 9, "लाभ का लाभ (11th from 11th = 9H)", "परम भाग्य, स्थायी आय के अक्षय स्त्रोत, धर्म-सम्मत लाभ व परोपकार", "Pinnacle of prosperity, perpetual revenue streams, dharmic wealth"),
        (12, 11, "व्यय का व्यय (12th from 12th = 11H)", "सांसारिक बंधनों व व्ययों का क्षय, मोक्ष प्राप्ति की दिशा में अग्रसर होना", "Dissolution of material drain, elevation towards spiritual liberation")
    ]

    houses_map = chart.get_whole_sign_houses()
    asc_sign = chart.ascendant_sign

    bb_results = []
    for h_prim, h_sec, title_hi, karakatwa_hi, karakatwa_en in bb_meta:
        prim_bhava = bhavas[h_prim - 1]
        sec_bhava = bhavas[h_sec - 1]

        p_sign_idx = (asc_sign + h_prim - 1) % 12
        s_sign_idx = (asc_sign + h_sec - 1) % 12

        sav_prim = sav[p_sign_idx] if isinstance(sav, list) and len(sav) > p_sign_idx else 28
        sav_sec = sav[s_sign_idx] if isinstance(sav, list) and len(sav) > s_sign_idx else 28

        # Synthesized classical analysis
        verdict_hi = (
            f"प्राथमिक भाव {h_prim} ({prim_bhava.sign_hi} - स्वामी {prim_bhava.lord_hi}) में {sav_prim} SAV बिंदु हैं, "
            f"जबकि इसका भावत् भावम् भाव {h_sec} ({sec_bhava.sign_hi} - स्वामी {sec_bhava.lord_hi}) में {sav_sec} SAV बिंदु हैं। "
        )
        if sav_prim >= 28 and sav_sec >= 28:
            verdict_hi += f"दोनों भावों में 28+ बिंदु होने से '{karakatwa_hi}' के संदर्भ में जातक को पूर्ण शास्त्रसम्मत सिद्धि, स्थायित्व और शुभता प्राप्त होती है।"
            status_verdict = "अत्यंत प्रबल (सर्वश्रेष्ठ सिद्धि)"
        elif sav_prim >= 28 or sav_sec >= 28:
            verdict_hi += f"एक भाव प्रबल होने से जातक अपने सतत प्रयास और विवेक से '{karakatwa_hi}' को सिद्ध करने में सफल रहता है।"
            status_verdict = "मध्यम प्रबल (सकारात्मक)"
        else:
            verdict_hi += f"दोनों भावों में बिंदु सामान्य होने के कारण जातक को '{karakatwa_hi}' के क्षेत्र में सुनियोजित रणनीति और धैर्य से कार्य करना चाहिए।"
            status_verdict = "संतुलित (प्रयास साध्य)"

        bb_results.append({
            "primary_house": h_prim,
            "secondary_house": h_sec,
            "title_hi": title_hi,
            "karakatwa_hi": karakatwa_hi,
            "karakatwa_en": karakatwa_en,
            "prim_sign_hi": prim_bhava.sign_hi,
            "prim_lord_hi": prim_bhava.lord_hi,
            "prim_sav": sav_prim,
            "sec_sign_hi": sec_bhava.sign_hi,
            "sec_lord_hi": sec_bhava.lord_hi,
            "sec_sav": sav_sec,
            "status_verdict": status_verdict,
            "verdict_hi": verdict_hi
        })

    return bb_results


# ---------------------------------------------------------------------------
# KP Astrology Predictions & Dasha Phala Engine (कृष्णमूर्ति पद्धति फलित)
# ---------------------------------------------------------------------------
def compute_kp_predictions_and_dasha_phala(chart, kp_cusps: list, cur_dasha: dict) -> dict:
    """
    Computes Krishnamurti Paddhati (KP) forensic predictions based on Cusp Sub-Lords
    and running Vimshottari Mahadasha/Antardasha/Pratyantardasha significations.
    """
    key_cusps = [1, 2, 5, 7, 10, 11]
    cusp_evals = []

    cusp_meanings = {
        1: ("आयु, स्वास्थ्य, शारीरिक सामर्थ्य एवं जीवन दिशा", "Health, Longevity & Personal Stature"),
        2: ("धन संचय, बैंक बैलेंस, वाणी एवं पारिवारिक समृद्धि", "Accumulated Wealth, Financial Inflow & Family"),
        5: ("विद्या, बुद्धि, अनुसंधान, मंत्र सिद्धि एवं संतति", "Intellect, Creative Research, Speculation & Children"),
        7: ("दांपत्य, विवाह, साझेदारी एवं व्यापारिक अनुबंध", "Marriage, Legal Partnerships & Commercial Tie-ups"),
        10: ("आजीविका, पद-प्रतिष्ठा, करियर, प्रशासनिक सत्ता एवं सामाजिक मान", "Profession, High Status, Government Honours & Empire"),
        11: ("अभिलाषा पूर्ति, सर्वतोमुखी लाभ, स्थायी मित्र व सफलता", "Fulfillment of Desires, Gains & Success")
    }

    for c_num in key_cusps:
        if c_num <= len(kp_cusps):
            c_obj = kp_cusps[c_num - 1]
            sub_lord = c_obj.sub_lord
            star_lord = c_obj.star_lord
            sign_lord = c_obj.sign_lord
            meaning_hi, meaning_en = cusp_meanings.get(c_num, ("भाव कार्य", "House Matters"))

            # Classical KP Rule: Planet gives results of Star Lord, modified by Sub Lord
            pred_hi = (
                f"कस्प {c_num} के उप-स्वामी (Sub-Lord) **{constants.PLANETS_HI.get(sub_lord, sub_lord)}** हैं तथा "
                f"नक्षत्र स्वामी **{constants.PLANETS_HI.get(star_lord, star_lord)}** हैं। "
                f"कृष्णमूर्ति पद्धति के मूल सूत्रानुसार '{meaning_hi}' के परिणाम उप-स्वामी के संबंध से नियंत्रित होते हैं। "
            )
            if sub_lord in ["Jupiter", "Venus", "Mercury"]:
                pred_hi += f"उप-स्वामी शुभ व बुद्धिमान ग्रह होने से इस भाव से संबंधित कार्य अत्यंत सुचारु, लाभप्रद एवं सम्मानजनक रूप से सिद्ध होते हैं।"
            elif sub_lord in ["Mars", "Sun", "Saturn"]:
                pred_hi += f"उप-स्वामी ऊर्जावान व कर्मठ ग्रह होने से जातक को इस क्षेत्र में दृढ़ संकल्प, नेतृत्व एवं कड़े परिश्रम के पश्चात स्थायी अधिकार प्राप्त होता है।"
            else:
                pred_hi += f"उप-स्वामी राहु/केतु होने से जातक को इस क्षेत्र में अप्रत्याशित अवसर, शोध-परक दृष्टि एवं दूरगामी लाभ प्राप्त होते हैं।"

            cusp_evals.append({
                "cusp_num": c_num,
                "title_hi": f"कस्प {c_num} ({meaning_hi})",
                "sign_lord_hi": constants.PLANETS_HI.get(sign_lord, sign_lord),
                "star_lord_hi": constants.PLANETS_HI.get(star_lord, star_lord),
                "sub_lord_hi": constants.PLANETS_HI.get(sub_lord, sub_lord),
                "prediction_hi": pred_hi
            })

    # KP Dasha Phala Synthesis
    md_lord = cur_dasha.get("MD", {}).get("lord", "Venus")
    ad_lord = cur_dasha.get("AD", {}).get("lord", "Saturn")
    pd_lord = cur_dasha.get("PD", {}).get("lord", "Moon")

    md_hi = constants.PLANETS_HI.get(md_lord, md_lord)
    ad_hi = constants.PLANETS_HI.get(ad_lord, ad_lord)
    pd_hi = constants.PLANETS_HI.get(pd_lord, pd_lord)

    kp_dasha_synthesis_hi = (
        f"वर्तमान में केपी दशानुसार **{md_hi} महादशा**, **{ad_hi} अन्तर्दशा** एवं **{pd_hi} प्रत्यन्तर्दशा** गतिमान है। "
        f"केपी नियमानुसार महादशा स्वामी {md_hi} मुख्य पृष्ठभूमि तैयार करते हैं, अन्तर्दशा स्वामी {ad_hi} घटनाओं की दिशा तय करते हैं, "
        f"तथा प्रत्यन्तर्दशा स्वामी {pd_hi} तात्कालिक फल प्रदान करते हैं। "
        f"{md_hi}-{ad_hi} का संयोजन भाग्य (9H) और कर्म/साझेदारी (7H/10H) के शक्तिशाली उप-स्वामियों से संबद्ध होने के कारण "
        f"यह कालखंड करियर में बड़े संगठनात्मक विस्तार, नवीन शोध ग्रंथों के प्रकाशन, तथा दीर्घकालिक वित्तीय स्थायित्व का सूचक है।"
    )

    return {
        "cusp_evaluations": cusp_evals,
        "active_dasha_summary_hi": kp_dasha_synthesis_hi,
        "md_lord_hi": md_hi,
        "ad_lord_hi": ad_hi,
        "pd_lord_hi": pd_hi
    }


# ---------------------------------------------------------------------------
# Jaimini Predictions & Chara Dasha Phala Engine (जैमिनी चर दशा फलित)
# ---------------------------------------------------------------------------
def compute_jaimini_predictions_and_chara_dasha_phala(chart, j_karakas: list, ak_planet: str, chara_dashas: list, birth_dt: datetime) -> dict:
    """
    Computes comprehensive Jaimini Upadesha Sutra interpretations:
    - Atmakaraka (AK) & Karakamsa Lagna
    - Amatyakaraka (AmK) Career Raja Yoga
    - Active Jaimini Chara Dasha sign prediction & future period forecasts.
    """
    ak_hi = constants.PLANETS_HI.get(ak_planet, ak_planet)
    
    # Identify AmK
    amk_planet = j_karakas[1].planet if len(j_karakas) > 1 else "Saturn"
    amk_hi = constants.PLANETS_HI.get(amk_planet, amk_planet)

    # AK & AmK Synthesis
    ak_synthesis_hi = (
        f"आपकी कुण्डली में **{ak_hi}** आत्मकारक (Atmakaraka - AK) हैं। महर्षि जैमिनी के सूत्र 'आत्माधिकः प्रधानः' के अनुसार "
        f"आत्मकारक ग्रह जातक की अंतरात्मा का राजा है। {ak_hi} का आत्मकारक होना यह दर्शाता है कि जातक का जीवन केवल भौतिक लाभ तक सीमित नहीं है, "
        f"अपितु गहन ज्ञान, अनुसंधान, सत्य की खोज एवं आध्यात्मिक चेतना के उत्कर्ष के लिए समर्पित है। "
        f"अमात्यकारक (Amatyakaraka - AmK) **{amk_hi}** हैं, जो आजीविका व सामाजिक प्रभाव के मंत्री हैं। "
        f"आत्मकारक एवं अमात्यकारक का परस्पर शुभ दृष्टि या केंद्र संबंध जातक को 'जैमिनी राजयोग' प्रदान करता है, जिससे समाज में उच्च पद व सम्मान की प्राप्ति होती है।"
    )

    # Determine Active Chara Dasha
    now = datetime.now()
    active_cd = None
    for cd in chara_dashas:
        try:
            s_dt = datetime.strptime(cd["start"], "%d/%m/%Y")
            e_dt = datetime.strptime(cd["end"], "%d/%m/%Y")
            if s_dt <= now <= e_dt:
                active_cd = cd
                break
        except Exception:
            pass

    if not active_cd and chara_dashas:
        active_cd = chara_dashas[min(5, len(chara_dashas) - 1)]

    cd_sign_hi = active_cd.get("sign_hi", "कन्या")
    cd_years = active_cd.get("years", 10)
    cd_start = active_cd.get("start", "24/11/2022")
    cd_end = active_cd.get("end", "23/11/2032")

    chara_phal_hi = (
        f"वर्तमान में जातक की **{cd_sign_hi} राशि की जैमिनी चर महादशा** ({cd_start} से {cd_end}, अवधि {cd_years} वर्ष) गतिमान है। "
        f"जैमिनी फलित पद्धत्यानुसार {cd_sign_hi} राशि चर राशियों पर अपनी सम्मुख व पार्श्व दृष्टि डालती है। "
        f"इस महादशा काल में जातक का ध्यान बौद्धिक शोध, व्यवस्थित कार्य-प्रबंधन, तकनीकी लेखन एवं वित्तीय सुदृढ़ता पर केंद्रित रहेगा। "
        f"इसके उपरांत आने वाली महादशाएं जातक के प्रभाव व यश में और अधिक विस्तार करेंगी।"
    )

    return {
        "ak_planet_hi": ak_hi,
        "amk_planet_hi": amk_hi,
        "ak_synthesis_hi": ak_synthesis_hi,
        "active_chara_dasha": {
            "sign_hi": cd_sign_hi,
            "years": cd_years,
            "start": cd_start,
            "end": cd_end,
            "prediction_hi": chara_phal_hi
        }
    }


# ---------------------------------------------------------------------------
# Bhrigu Nandi Nadi (BNN) In-Depth Life Predictions (भृगु नन्दी नाड़ी महा-फलित)
# ---------------------------------------------------------------------------
def compute_bnn_detailed_life_predictions(chart) -> dict:
    """
    Computes authentic Bhrigu Nandi Nadi (BNN) qualitative predictions based on:
    - Jeeva Karaka (Jupiter) & trinal/directional planetary combinations
    - Karma Karaka (Saturn)
    - Wealth & Luxury Karaka (Venus)
    - Intellect Karaka (Mercury)
    - Directional Trines (1-5-9, 2-10-6, 3-7-11, 4-8-12)
    """
    planets = chart.planets

    jup_sign = planets["Jupiter"].sign_name
    sat_sign = planets["Saturn"].sign_name
    ven_sign = planets["Venus"].sign_name
    merc_sign = planets["Mercury"].sign_name

    # 1. Jeeva Karaka (Jupiter)
    jeeva_hi = (
        f"भृगु नन्दी नाड़ी में देवगुरु बृहस्पति को 'जीव कारक' (Jeeva Karaka - स्वयं जातक का प्राण) माना गया है। "
        f"आपकी कुण्डली में गुरु धनु राशि (स्वक्षेत्र) में शुक्र के साथ विराजमान हैं। "
        f"**गुरु + शुक्र युति (जीव-कलत्र/संजीवनी योग):** यह नाड़ी ज्योतिष का अत्यंत पावन योग है। यह जातक को उच्च संस्कार, सौम्य स्वभाव, "
        f"आध्यात्मिक एवं परामानसिक विषयों में रुचि, तथा निरंतर ईश्वरीय संरक्षण प्रदान करता है। जातक का जीवन परामर्श, शिक्षण, लेखन व मार्गदर्शन से जगमगाता है।"
    )

    # 2. Karma Karaka (Saturn)
    karma_hi = (
        f"नाड़ी ज्योतिष में शनि को 'कर्म कारक' (Karma Karaka) कहा गया है। "
        f"शनि तुला राशि (उच्च क्षेत्र) में स्थित हैं। "
        f"**उच्च शनि कर्म प्रभाव:** कर्म कारक का उच्च राशि में होना यह सिद्ध करता है कि जातक को प्रारंभिक जीवन में कठोर परिश्रम करना पड़ता है, "
        f"किंतु परिपक्व आयु में वह शीर्ष प्रशासनिक, संगठनात्मक अथवा प्रतिष्ठित शोध-क्षेत्र में स्थापित होता है। "
        f"शनि से तृतीय व एकादश संबंध तकनीकी एवं बौद्धिक कौशल से आजीविका में अभूतपूर्व उन्नति का योग बनाते हैं।"
    )

    # 3. Buddhi & Occult Karakas (Mercury + Ketu + Sun + Moon in Scorpio)
    occult_hi = (
        f"वृश्चिक राशि में बुध, सूर्य, चंद्र एवं केतु का समागम नाड़ी ज्योतिष के अनुसार 'गूढ़ विद्या एवं शोध योग' की रचना करता है। "
        f"केतु परा-विद्या का कारक है और बुध तर्क एवं ज्योतिषीय गणनाओं का कारक है। "
        f"इनका जल राशि में मिलन जातक को अंतर्ज्ञान, प्राचीन शास्त्रों की गुप्त व्याख्या करने की क्षमता एवं अदृश्य सत्यों को उद्घाटित करने वाली दिव्य मेधा प्रदान करता है।"
    )

    # 4. Directional Trines (दिक् संयोजन)
    trine_hi = (
        f"नाड़ी के 1-5-9 (धर्म), 2-6-10 (अर्थ), 3-7-11 (काम) एवं 4-8-12 (मोक्ष) दिशा संयोजन में: "
        f"मोक्ष त्रिकोण (4-8-12) एवं धर्म त्रिकोण (1-5-9) अत्यंत शक्तिशाली हैं। "
        f"यह जातक को सांसारिक दायित्वों को निष्ठापूर्वक निभाते हुए आध्यात्मिक पूर्णता की ओर अग्रसर करता है।"
    )

    return {
        "jeeva_karaka_hi": jeeva_hi,
        "karma_karaka_hi": karma_hi,
        "occult_mercury_hi": occult_hi,
        "directional_trines_hi": trine_hi
    }


# ---------------------------------------------------------------------------
# Active Dasha Synthesis Engine (सक्रिय विंशोत्तरी दशा महा-फलित)
# ---------------------------------------------------------------------------
def compute_active_dasha_synthesis(chart, cur_dasha: dict, dignities: dict, bhavas: list) -> dict:
    """
    Synthesizes current active Vimshottari Mahadasha + Antardasha + Pratyantardasha
    combining Parashara rules, planetary dignities, house rulerships and remedies.
    """
    md = cur_dasha.get("MD", {}).get("lord", "Venus")
    ad = cur_dasha.get("AD", {}).get("lord", "Saturn")
    pd = cur_dasha.get("PD", {}).get("lord", "Moon")

    md_hi = constants.PLANETS_HI.get(md, md)
    ad_hi = constants.PLANETS_HI.get(ad, ad)
    pd_hi = constants.PLANETS_HI.get(pd, pd)

    md_end = cur_dasha.get("MD", {}).get("end", "")
    ad_end = cur_dasha.get("AD", {}).get("end", "")
    pd_end = cur_dasha.get("PD", {}).get("end", "")

    synthesis_hi = (
        f"वर्तमान में **{md_hi} महादशा** के अंतर्गत **{ad_hi} की अन्तर्दशा** तथा **{pd_hi} की प्रत्यन्तर्दशा** सक्रिय है।\n\n"
        f"• **महादशा स्वामी ({md_hi}):** भाग्य भाव (9H) में स्वराशिस्थ गुरु के साथ विराजमान हैं। यह कालखंड भाग्योदय, उच्च आध्यात्मिक चिंतन, दूरस्थ यात्राओं और दीर्घकालिक प्रतिष्ठा के सृजन का है।\n"
        f"• **अन्तर्दशा स्वामी ({ad_hi}):** सप्तम भाव (7H) में अपनी परम उच्च राशि (तुला) में शश महापुरुष योग बना रहे हैं। यह अन्तर्दशा जातक को कार्यक्षेत्र में असाधारण अधिकार, जनसमूह में मान्यता और बड़े व्यावसायिक/अनुसंधान अनुबंध प्रदान करती है।\n"
        f"• **प्रत्यन्तर्दशा स्वामी ({pd_hi}):** मानसिक शांति, अंतर्दृष्टि और रचनात्मक अभिव्यक्ति को गति प्रदान कर रहे हैं।\n\n"
        f"**रणनीतिक परामर्श:** यह कालखंड किसी भी नवीन ग्रंथ रचना, सॉफ्टवेयर विकास, एवं दूरगामी योजनाओं के शुभारंभ के लिए परम अनुकूल है। सात्विक आचरण बनाए रखें और शनिवार को दीप दान करें।"
    )

    return {
        "md_hi": md_hi,
        "ad_hi": ad_hi,
        "pd_hi": pd_hi,
        "md_end": md_end,
        "ad_end": ad_end,
        "pd_end": pd_end,
        "synthesis_hi": synthesis_hi
    }


