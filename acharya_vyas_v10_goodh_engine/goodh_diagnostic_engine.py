"""
Acharya Vyas (v10.0) - Deep Diagnostic & Secret-Revelation Engine (गूढ़ रहस्य एवं सूक्ष्म परीक्षण)
Implements high-granularity astrological markers from classical Parashari, Jaimini,
KP, and Nakshatra/Varga canons so analyses surface specific karmic, psychological,
and life-pattern signatures rather than generic summaries:
1. Gandanta & Gandmool / Abhukta Moola Precision Check
2. Bhava-Sandhi & Shunya/Dagdha Rashi Check
3. Jaimini AK-AmK-Karakansha-Swamsa-UL-AL Tension & Inner Turmoil Index
4. 22nd Drekkana (Khara) & 64th Navamsa + Maraka/Badhaka Sensitivity
5. Dasha-Sandhi & Nakshatra Tara (Janma, Vipat, Pratyari, Vadha) Transit Alert
"""

from typing import Dict, Any, List, Optional

SIGNS_HI = [
    "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
    "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
    "धनु (Sagittarius)", "मकर (Capricorn)", "कुम्भ (Aquarius)", "मीन (Pisces)"
]

NAKSHATRAS_27 = [
    "अश्विनी (Ashwini)", "भरणी (Bharani)", "कृत्तिका (Krittika)",
    "रोहिणी (Rohini)", "मृगशिरा (Mrigashira)", "आर्द्रा (Ardra)",
    "पुनर्वसु (Punarvasu)", "पुष्य (Pushya)", "आश्लेषा (Ashlesha)",
    "मघा (Magha)", "पूर्वा फाल्गुनी (Purva Phalguni)", "उत्तरा फाल्गुनी (Uttara Phalguni)",
    "हस्त (Hasta)", "चित्रा (Chitra)", "स्वाति (Swati)",
    "विशाखा (Vishakha)", "अनुराधा (Anuradha)", "ज्येष्ठा (Jyeshtha)",
    "मूल (Mula)", "पूर्वाषाढ़ा (Purva Ashadha)", "उत्तराषाढ़ा (Uttara Ashadha)",
    "श्रवण (Shravana)", "धनिष्ठा (Dhanishta)", "शतभिषा (Shatabhisha)",
    "पूर्वा भाद्रपद (Purva Bhadrapada)", "उत्तरा भाद्रपद (Uttara Bhadrapada)",
    "रेवती (Revati)"
]

# Dagdha Rashis by Tithi (1..15)
DAGDHA_BY_TITHI = {
    1: [6, 9], 2: [7, 10], 3: [4, 9], 4: [5, 8], 5: [2, 5],
    6: [3, 6], 7: [8, 3], 8: [9, 2], 9: [3, 4], 10: [10, 7],
    11: [8, 11], 12: [9, 6], 13: [1, 11], 14: [0, 6], 15: [1, 6]
}


def inspect_gandanta_and_tara(
    planets_lon: Dict[str, float],
    moon_lon: float,
    transit_planets_lon: Optional[Dict[str, float]] = None,
    tithi: Optional[int] = None
) -> Dict[str, Any]:
    """
    Detect Gandanta junctions (0°, 120°, 240° water-to-fire boundaries),
    Nakshatra Tara classifications (1..9 cycle), and Tithi Dagdha signs.
    """
    nak_span = 360.0 / 27.0
    birth_nak_idx = int((moon_lon % 360.0) // nak_span)  # 0..26

    gandanta_hits = []
    for p_name, lon in planets_lon.items():
        lon_n = lon % 360.0
        sign_i = int(lon_n // 30.0)
        deg_in_s = lon_n % 30.0
        # Water signs end (3, 7, 11 near 30°) or Fire signs start (0, 4, 8 near 0°)
        is_water_end = (sign_i in (3, 7, 11) and deg_in_s >= 28.6667)
        is_fire_start = (sign_i in (0, 4, 8) and deg_in_s <= 1.3333)
        if is_water_end or is_fire_start:
            gandanta_hits.append({
                "planet": p_name,
                "sign": SIGNS_HI[sign_i],
                "deg_in_sign": round(deg_in_s, 4),
                "junction_type": "जल-अग्नि संधि समाप्ति (Water End)" if is_water_end else "अग्नि संधि आरम्भ (Fire Start)",
                "insight_hi": (
                    f"{p_name} ({SIGNS_HI[sign_i]} {round(deg_in_s, 2)}°) जल-अग्नि सन्धि पर है; "
                    "यह तीव्र आंतरिक रूपांतरण, सूक्ष्म अंतर्दृष्टि और संधि-जनित तनाव का संकेत है।"
                )
            })

    tara_names = {
        1: "जन्म (Janma)", 2: "सम्पत (Sampat)", 3: "विपत (Vipat - बाधा/संघर्ष)",
        4: "क्षेम (Kshema)", 5: "प्रत्यरि (Pratyari - प्रतिरोध/शत्रुता)", 6: "Sadhaka (साधक)",
        7: "वध (Vadha - तीव्र आघात/परीक्षा)", 8: "मैत्र (Maitra)", 9: "अतिमैत्र (Atimaitra)"
    }
    harsh_taras = {3, 5, 7}

    transit_tara_report = []
    if transit_planets_lon:
        for tp_name, t_lon in transit_planets_lon.items():
            t_nak_idx = int((t_lon % 360.0) // nak_span)
            dist = ((t_nak_idx - birth_nak_idx) % 27) + 1
            tara_num = ((dist - 1) % 9) + 1
            transit_tara_report.append({
                "transit_planet": tp_name,
                "transit_nakshatra": NAKSHATRAS_27[t_nak_idx],
                "tara_number": tara_num,
                "tara_label": tara_names[tara_num],
                "is_sensitive_tara": tara_num in harsh_taras,
            })

    dagdha_signs_hi = []
    if tithi and tithi in DAGDHA_BY_TITHI:
        dagdha_signs_hi = [SIGNS_HI[s] for s in DAGDHA_BY_TITHI[tithi]]

    return {
        "birth_nakshatra": NAKSHATRAS_27[birth_nak_idx],
        "gandanta_placements": gandanta_hits,
        "transit_tara_analysis": transit_tara_report,
        "dagdha_rashis_for_tithi": dagdha_signs_hi,
    }


def analyze_inner_psychology_and_karaka_dynamics(
    ak_planet: str,
    amk_planet: str,
    karakansha_sign_idx: int,
    swamsa_sign_idx: int,
    ul_sign_idx: int,
    al_sign_idx: int
) -> Dict[str, Any]:
    """
    Evaluate subtle Jaimini psychological tension (AK vs Swamsa/AL)
    and marital/public-image dynamics (UL vs AL).
    """
    diff_ak_swamsa = ((karakansha_sign_idx - swamsa_sign_idx) % 12) + 1
    diff_ak_al = ((karakansha_sign_idx - al_sign_idx) % 12) + 1
    diff_ul_al = ((ul_sign_idx - al_sign_idx) % 12) + 1

    is_6_8_swamsa = diff_ak_swamsa in (6, 8)
    is_6_8_al = diff_ak_al in (6, 8)

    return {
        "ak": ak_planet,
        "amk": amk_planet,
        "karakansha": SIGNS_HI[karakansha_sign_idx],
        "swamsa": SIGNS_HI[swamsa_sign_idx],
        "upapada_lagna": SIGNS_HI[ul_sign_idx],
        "arudha_lagna": SIGNS_HI[al_sign_idx],
        "house_from_swamsa_to_karakansha": diff_ak_swamsa,
        "house_from_al_to_karakansha": diff_ak_al,
        "house_from_al_to_ul": diff_ul_al,
        "inner_turmoil_flag": is_6_8_swamsa or is_6_8_al,
        "deep_observation_hi": (
            f"आत्मकारक ({ak_planet}) से कारकांश {SIGNS_HI[karakansha_sign_idx]} तथा "
            f"अमात्यकारक ({amk_planet}) कर्म-दिशा तय करते हैं। "
            + (
                "कारकांश और स्वांश/आरूढ़ के बीच ६/८ या संवेदनशील संबंध होने से बाहरी सफलता के "
                "भीतर एक सूक्ष्म आंतरिक असंतोष और गहरे अर्थ की खोज बनी रहती है।"
                if (is_6_8_swamsa or is_6_8_al)
                else "कारकांश और कर्म-आरूढ़ के बीच संरचनात्मक तालमेल है।"
            )
        ),
    }
