"""Jaimini Astrology Engine (Jaimini Upadesha Sutras Standards).

Computes:
1. 7 Chara Karakas (चर कारक):
   - Atmakaraka (AK - आत्मकारक: Soul / Core Destiny)
   - Amatyakaraka (AmK - अमात्यकारक: Career / Advisor)
   - Bhratrikaraka (BK - भ्रातृकारक: Siblings / Guru)
   - Matrikaraka (MK - मातृकारक: Mother / Real Estate)
   - Putrakaraka (PK - पुत्रकारक: Children / Intellect)
   - Gnatikaraka (GK - ज्ञातिकारक: Obstacles / Cousins / Disease)
   - Darakaraka (DK - दाराकारक: Spouse / Partnerships)
2. Karakamsha Lagna (कारकांश लग्न): Navamsha sign of Atmakaraka.
3. 12 Arudha Padas (आरूढ़ पद): AL (Arudha Lagna), UL (Upapada / A12), A2 to A11 with classical exceptions.
4. Jaimini Chara Dasha year lengths.
"""
from typing import Dict, List, Tuple, NamedTuple
from vyas import constants
from vyas.varga import calculate_vargas_detailed

class CharaKaraka(NamedTuple):
    karaka_name: str
    abbreviation: str
    planet: str
    degree_in_sign: float
    dms_str: str
    sign_name: str
    signification: str

def format_dms(deg_val: float) -> str:
    d = int(deg_val)
    rem = (deg_val - d) * 60.0
    m = int(rem)
    s = int(round((rem - m) * 60.0))
    if s >= 60:
        m += 1
        s = 0
    if m >= 60:
        d += 1
        m = 0
    return f"{d:02d}°{m:02d}'{s:02d}\""

def compute_chara_karakas(planets: dict) -> Tuple[List[CharaKaraka], str, str]:
    """
    Computes 7 Chara Karakas sorted by descending degrees inside the sign (0 to 30).
    Returns (karakas_list, atmakaraka_planet, karakamsha_sign).
    """
    candidates = []
    # 7 classical planets (Sun to Saturn)
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        p = planets[p_name]
        deg_in_sign = p.longitude % 30.0
        candidates.append((p_name, deg_in_sign, p.sign_name, p.longitude))
        
    # Sort descending by degree
    candidates.sort(key=lambda x: x[1], reverse=True)

    karaka_roles = [
        ("Atmakaraka", "AK", "Soul, King of the Chart, Life Purpose, Ultimate Destiny"),
        ("Amatyakaraka", "AmK", "Prime Minister, Career, Professional Achievement, Intellect"),
        ("Bhratrikaraka", "BK", "Siblings, Gurus, Guides, Comrades, Spiritual Path"),
        ("Matrikaraka", "MK", "Mother, Sustenance, Nourishment, Immovable Properties"),
        ("Putrakaraka", "PK", "Children, Creative Intellect, Mantras, Past Merit"),
        ("Gnatikaraka", "GK", "Obstacles, Competitors, Debts, Illness, Ancestral Struggle"),
        ("Darakaraka", "DK", "Spouse, Partners, Marital Union, Material Desires")
    ]

    karakas: List[CharaKaraka] = []
    ak_planet = candidates[0][0]
    ak_lon = candidates[0][3]

    for i in range(7):
        role_name, abbr, sig = karaka_roles[i]
        p_name, deg, sign_name, lon = candidates[i]
        karakas.append(CharaKaraka(
            karaka_name=role_name,
            abbreviation=abbr,
            planet=p_name,
            degree_in_sign=deg,
            dms_str=format_dms(deg),
            sign_name=sign_name,
            signification=sig
        ))

    # Karakamsha Lagna = Navamsha sign of Atmakaraka
    ak_vargas = calculate_vargas_detailed(ak_lon)
    karakamsha_sign = ak_vargas["D9"].sign_name

    return karakas, ak_planet, karakamsha_sign

def compute_arudha_padas(chart) -> Dict[str, str]:
    """
    Computes the 12 Arudha Padas (A1/AL to A12/UL) using Jaimini/Parashara rules.
    Rule: If Arudha falls in same house or 7th, add 10 houses.
    """
    asc_sign = chart.ascendant_sign
    planets = chart.planets

    padas = {}
    pada_names = {
        1: "AL (Arudha Lagna - Image / Public Stature)",
        2: "A2 (Dhanarudha - Manifested Wealth)",
        3: "A3 (Bhatrarudha - Siblings / Enterprise)",
        4: "A4 (Matrarudha / Sukharudha - Property)",
        5: "A5 (Putrarudha - Creative Stature)",
        6: "A6 (Shatruarudha - Manifested Litigation)",
        7: "A7 (Dararudha - Visible Partnerships)",
        8: "A8 (Mrityurarudha - Vulnerability)",
        9: "A9 (Bhagyarudha - Visible Fortune)",
        10: "A10 (Rajyarudha - Career Elevation)",
        11: "A11 (Labharudha - Actualized Gains)",
        12: "UL (Upapada Lagna - Spouse / Marriage)"
    }

    for h in range(1, 13):
        h_sign = (asc_sign + h - 1) % 12
        h_lord = constants.SIGN_LORD[h_sign]
        lord_sign = planets[h_lord].sign_index

        # Distance from house to its lord
        dist = (lord_sign - h_sign + 12) % 12
        raw_arudha_sign = (lord_sign + dist) % 12

        # Check classical exceptions: if raw arudha is in h_sign (dist=0) or in 7th from h_sign (dist=6)
        if raw_arudha_sign == h_sign:
            final_sign = (raw_arudha_sign + 9) % 12 # 10th from it
        elif (raw_arudha_sign - h_sign + 12) % 12 == 6:
            final_sign = (raw_arudha_sign + 9) % 12
        else:
            final_sign = raw_arudha_sign

        padas[f"A{h}"] = {
            "title": pada_names[h],
            "sign": constants.SIGNS[final_sign],
            "sign_hi": constants.SIGNS_HI[final_sign],
            "house_from_lagna": (final_sign - asc_sign + 12) % 12 + 1
        }

    return padas


def compute_chara_dasha(*args, **kwargs) -> list:
    """Delegates to forensic_predictor.compute_chara_dasha with flexible argument signature."""
    from . import forensic_predictor
    # Signature 1: compute_chara_dasha(planets, asc_sign, birth_dt)
    if len(args) == 3 and isinstance(args[0], dict) and isinstance(args[1], int):
        planets, asc_sign, birth_dt = args
        return forensic_predictor.compute_chara_dasha(asc_sign, birth_dt, chart=planets)
    # Signature 2: compute_chara_dasha(asc_sign, birth_dt, chart=None)
    elif len(args) >= 2 and isinstance(args[0], int):
        asc_sign = args[0]
        birth_dt = args[1]
        chart = args[2] if len(args) > 2 else kwargs.get("chart")
        return forensic_predictor.compute_chara_dasha(asc_sign, birth_dt, chart)
    else:
        asc_sign = kwargs.get("asc_sign", 0)
        birth_dt = kwargs.get("birth_dt", None)
        chart = kwargs.get("chart", None)
        return forensic_predictor.compute_chara_dasha(asc_sign, birth_dt, chart)

