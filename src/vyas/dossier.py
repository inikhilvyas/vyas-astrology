"""Normalized Chart Context & Comprehensive Planet and House Dossiers.

Operating Standard: Jyotishi-Style Systematic Analysis (BPHS & Classical Rules).
Separates:
1. Whole-Sign Houses (Parashari Bhavas).
2. KP / Placidus Cusps (Krishnamurti Padhdhati).
3. Bhava Chalit Occupancies.
4. Planet Dossiers (Dignity, Shadbala, Avastha, Combustion, Aspects, Varga confirmations).
5. House Dossiers (Lord condition, Occupants, Aspects, Bhavabala, Contradictions).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from vyas import constants
from vyas.chart import Chart, PlanetState, get_navamsha_analysis
from vyas.kp import calculate_placidus_cusps_sidereal, KPCusp
from vyas.shadbala import compute_shadbala, PlanetShadbala
from vyas.varga import calculate_vargas_detailed

# Classical Combustion Orbs from Sun (Surya) in degrees:
# Moon: 12°, Mars: 17°, Mercury: 14° (12° when retrograde),
# Jupiter: 11°, Venus: 10° (8° when retrograde), Saturn: 15°
COMBUSTION_ORBS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": 14.0,
    "Mercury_Retro": 12.0,
    "Jupiter": 11.0,
    "Venus": 10.0,
    "Venus_Retro": 8.0,
    "Saturn": 15.0
}

# Baladi Avasthas (BPHS ch. 45):
# Odd signs: 0-6 Bala (Infant), 6-12 Kumara (Youth), 12-18 Yuva (Adult/Full), 18-24 Vriddha (Old), 24-30 Mrita (Dead)
# Even signs: 0-6 Mrita, 6-12 Vriddha, 12-18 Yuva, 18-24 Kumara, 24-30 Bala
AVASTHAS_ODD = ["बाल (Bala - Infant 25%)", "कुमार (Kumara - Youth 50%)", "युवा (Yuva - Prime 100%)", "वृद्ध (Vriddha - Aged 10%)", "मृत (Mrita - Zero 0%)"]
AVASTHAS_EVEN = ["मृत (Mrita - Zero 0%)", "वृद्ध (Vriddha - Aged 10%)", "युवा (Yuva - Prime 100%)", "कुमार (Kumara - Youth 50%)", "बाल (Bala - Infant 25%)"]


@dataclass(frozen=True)
class PlanetDossier:
    planet: str
    longitude: float
    speed: float
    sign_index: int
    sign_name: str
    deg_in_sign: float
    nakshatra_name: str
    pada: int
    nakshatra_lord: str
    whole_sign_house: int
    kp_house: int
    is_retrograde: bool
    is_combust: bool
    combust_dist_deg: float
    avastha: str
    dignity: str  # Exalted, Moolatrikona, Own Sign, Friend, Neutral, Enemy, Debilitated
    functional_nature: str  # Yogakaraka, Kendra/Trikona Lord, Dusthana Lord, Maraka, Neutral
    shadbala_virupas: float
    shadbala_ratio: float
    is_shadbala_strong: bool
    aspects_cast_to_houses: List[int]
    aspects_received: List[str]
    conjunctions: List[str]
    d9_navamsha_sign: str
    d10_dashamsha_sign: str
    is_vargottama: bool
    is_pushkar_navamsha: bool


@dataclass(frozen=True)
class HouseDossier:
    house_num: int
    sign_index: int
    sign_name: str
    lord: str
    lord_placement_house: int
    lord_dignity: str
    lord_shadbala_ratio: float
    lord_is_strong: bool
    whole_sign_occupants: List[str]
    chalit_kp_occupants: List[str]
    aspecting_planets: List[str]
    bhavabala_virupas: float
    benefic_count: int
    malefic_count: int
    has_contradiction: bool
    contradiction_notes: List[str]


@dataclass
class NormalizedChartContext:
    chart: Chart
    birth_dt_utc: datetime
    lat: float
    lon: float
    whole_sign_houses: Dict[int, Any]
    kp_cusps: List[KPCusp]
    shadbala: Dict[str, PlanetShadbala]
    bhavabala: Dict[int, float]
    planet_dossiers: Dict[str, PlanetDossier]
    house_dossiers: Dict[int, HouseDossier]
    quality_flags: Dict[str, Any] = field(default_factory=dict)


def _get_planet_dignity(planet: str, sign_idx: int, deg_in_sign: float) -> str:
    """Evaluates classical planetary dignity."""
    if planet in ("Rahu", "Ketu"):
        # Rahu: Exalted in Taurus, Own in Aquarius, Debilitated in Scorpio
        # Ketu: Exalted in Scorpio, Own in Scorpio/Sagittarius, Debilitated in Taurus
        if planet == "Rahu":
            return "Exalted (उच्च)" if sign_idx == 1 else ("Own Sign (स्वक्षेत्री)" if sign_idx == 10 else ("Debilitated (नीच)" if sign_idx == 7 else "Neutral"))
        else:
            return "Exalted (उच्च)" if sign_idx == 7 else ("Debilitated (नीच)" if sign_idx == 1 else "Neutral")

    if planet in constants.EXALTATION:
        ex_sign, ex_deg = constants.EXALTATION[planet]
        deb_sign = (ex_sign + 6) % 12
        if sign_idx == ex_sign:
            return "Exalted (परम उच्च)" if abs(deg_in_sign - ex_deg) <= 3.0 else "Exalted (उच्च)"
        if sign_idx == deb_sign:
            return "Debilitated (परम नीच)" if abs(deg_in_sign - ex_deg) <= 3.0 else "Debilitated (नीच)"

    # Own sign check
    if constants.SIGN_LORD[sign_idx] == planet:
        # Check Moolatrikona
        # Sun: Leo 0-20, Moon: Taurus 3-30, Mars: Aries 0-12, Mercury: Virgo 15-20,
        # Jupiter: Sagittarius 0-10, Venus: Libra 0-15, Saturn: Aquarius 0-20
        mt_spans = {
            "Sun": (4, 0.0, 20.0), "Moon": (1, 3.0, 30.0), "Mars": (0, 0.0, 12.0),
            "Mercury": (5, 15.0, 20.0), "Jupiter": (8, 0.0, 10.0),
            "Venus": (6, 0.0, 15.0), "Saturn": (10, 0.0, 20.0)
        }
        if planet in mt_spans:
            mt_sign, mt_start, mt_end = mt_spans[planet]
            if sign_idx == mt_sign and mt_start <= deg_in_sign <= mt_end:
                return "Moolatrikona (मूलत्रिकोण)"
        return "Own Sign (स्वक्षेत्री)"

    # Friends / Enemies (Naisargika Sambandha)
    ruler = constants.SIGN_LORD[sign_idx]
    # Simple classical mapping:
    FRIENDS = {
        "Sun": ["Moon", "Mars", "Jupiter"], "Moon": ["Sun", "Mercury"],
        "Mars": ["Sun", "Moon", "Jupiter"], "Mercury": ["Sun", "Venus"],
        "Jupiter": ["Sun", "Moon", "Mars"], "Venus": ["Mercury", "Saturn"],
        "Saturn": ["Mercury", "Venus"]
    }
    ENEMIES = {
        "Sun": ["Venus", "Saturn"], "Moon": [],
        "Mars": ["Mercury"], "Mercury": ["Moon"],
        "Jupiter": ["Mercury", "Venus"], "Venus": ["Sun", "Moon"],
        "Saturn": ["Sun", "Moon", "Mars"]
    }
    if ruler in FRIENDS.get(planet, []):
        return "Friend Sign (मित्र राशि)"
    if ruler in ENEMIES.get(planet, []):
        return "Enemy Sign (शत्रु राशि)"
    return "Neutral Sign (सम राशि)"


def _get_functional_nature(planet: str, asc_sign: int) -> str:
    """Classifies functional role for the native's Lagna (Parashari rules)."""
    # Lagna Lord is always functional benefic
    lagna_lord = constants.SIGN_LORD[asc_sign]
    if planet == lagna_lord:
        return "लग्नेश (Lagna Lord - Primary Benefic)"

    # Yogakaraka check (lord of a Kendra AND a Trikona)
    # Taurus: Saturn (9 & 10), Libra: Saturn (4 & 5), Cancer: Mars (5 & 10), Leo: Mars (4 & 9)
    if (asc_sign == 1 and planet == "Saturn") or (asc_sign == 6 and planet == "Saturn") or \
       (asc_sign == 3 and planet == "Mars") or (asc_sign == 4 and planet == "Mars"):
        return "योगकारक (Yogakaraka - Supreme Benefic)"

    # Ruled houses
    ruled_houses = [(h_idx + 1) for h_idx in range(12) if constants.SIGN_LORD[(asc_sign + h_idx) % 12] == planet]
    
    # Marakas (2 and 7)
    is_maraka = any(h in (2, 7) for h in ruled_houses)
    # Dusthanas (6, 8, 12)
    is_dusthana = any(h in (6, 8, 12) for h in ruled_houses)
    # Trikonas (1, 5, 9)
    is_trikona = any(h in (1, 5, 9) for h in ruled_houses)

    if is_trikona:
        return f"त्रिकोणेश (Trikona Lord: {ruled_houses})"
    if is_maraka and is_dusthana:
        return f"मारक व त्रिकेश (Maraka & Dusthana Lord: {ruled_houses})"
    if is_maraka:
        return f"मारकेश (Maraka Lord: {ruled_houses})"
    if is_dusthana:
        return f"त्रिकेश (Dusthana Lord: {ruled_houses})"
    return f"भावेश (House Lord: {ruled_houses})"


def build_normalized_chart_context(
    chart: Chart,
    birth_dt_utc: datetime,
    lat: float,
    lon: float,
    birth_time_confidence: str = "High"
) -> NormalizedChartContext:
    """Builds a single, verified, immutable calculation context with Planet and House dossiers."""
    from vyas import ephem
    birth_dt_utc = ephem.ensure_utc(birth_dt_utc, "birth_dt_utc")

    # 1. Whole Sign Houses
    whole_sign_houses = chart.get_whole_sign_houses()
    asc_sign = chart.ascendant_sign

    # 2. KP Placidus Cusps
    kp_cusps = calculate_placidus_cusps_sidereal(birth_dt_utc, lat, lon)

    # 3. Shadbala & Bhavabala
    shadbala_map, bhavabala_map = compute_shadbala(chart, birth_utc=birth_dt_utc)

    # 4. Sun Longitude for Combustion
    sun_lon = chart.planets["Sun"].longitude if "Sun" in chart.planets else 0.0

    # 5. Build Planet Dossiers
    planet_dossiers: Dict[str, PlanetDossier] = {}
    planets_by_sign: Dict[int, List[str]] = {s: [] for s in range(12)}
    for p_name, p in chart.planets.items():
        planets_by_sign[p.sign_index].append(p_name)

    for p_name, p in chart.planets.items():
        ws_house = chart.get_house_of_planet(p_name)

        # KP Placidus house of planet
        kp_house = 1
        for i in range(12):
            c_curr = kp_cusps[i].longitude
            c_next = kp_cusps[(i + 1) % 12].longitude
            span = (c_next - c_curr) % 360.0
            pos = (p.longitude - c_curr) % 360.0
            if pos < span:
                kp_house = kp_cusps[i].cusp_num
                break

        # Combustion check
        is_combust = False
        combust_dist = ((p.longitude - sun_lon + 180.0) % 360.0) - 180.0
        abs_combust_dist = abs(combust_dist)
        if p_name not in ("Sun", "Rahu", "Ketu"):
            key = f"{p_name}_Retro" if (p.is_retrograde and f"{p_name}_Retro" in COMBUSTION_ORBS) else p_name
            orb = COMBUSTION_ORBS.get(key, 12.0)
            is_combust = abs_combust_dist <= orb

        # Baladi Avastha
        deg_in_sign = p.longitude % 30.0
        av_idx = min(4, int(deg_in_sign // 6.0))
        avastha = AVASTHAS_ODD[av_idx] if (p.sign_index % 2 == 0) else AVASTHAS_EVEN[av_idx]

        # Dignity & Functional Nature
        dignity = _get_planet_dignity(p_name, p.sign_index, deg_in_sign)
        func_nature = _get_functional_nature(p_name, asc_sign)

        # Shadbala Info
        sh_obj = shadbala_map.get(p_name)
        sh_virupas = sh_obj.total_virupas if sh_obj else 0.0
        sh_ratio = sh_obj.strength_ratio if sh_obj else 1.0
        sh_strong = sh_ratio >= 1.0

        # Aspects Cast (Parashari)
        # All planets aspect 7th house (opposition)
        # Mars special: 4th & 8th
        # Jupiter special: 5th & 9th
        # Saturn special: 3rd & 10th
        aspects_cast_h = [(ws_house + 6 - 1) % 12 + 1]
        if p_name == "Mars":
            aspects_cast_h.extend([(ws_house + 3 - 1) % 12 + 1, (ws_house + 7 - 1) % 12 + 1])
        elif p_name == "Jupiter":
            aspects_cast_h.extend([(ws_house + 4 - 1) % 12 + 1, (ws_house + 8 - 1) % 12 + 1])
        elif p_name == "Saturn":
            aspects_cast_h.extend([(ws_house + 2 - 1) % 12 + 1, (ws_house + 9 - 1) % 12 + 1])

        # Conjunctions (Same whole-sign house)
        conjunctions = [other for other in planets_by_sign[p.sign_index] if other != p_name]

        # Aspects Received
        aspects_received = []
        for other_name, other_p in chart.planets.items():
            if other_name == p_name:
                continue
            diff_signs = (p.sign_index - other_p.sign_index + 12) % 12
            # 7th aspect is 6 signs away
            if diff_signs == 6:
                aspects_received.append(other_name)
            elif other_name == "Mars" and diff_signs in (3, 7):
                aspects_received.append(other_name)
            elif other_name == "Jupiter" and diff_signs in (4, 8):
                aspects_received.append(other_name)
            elif other_name == "Saturn" and diff_signs in (2, 9):
                aspects_received.append(other_name)

        # Navamsha & Varga confirmation
        d9_analysis = get_navamsha_analysis(p.longitude)
        vargas = calculate_vargas_detailed(p.longitude)
        d10_sign = vargas["D10"].sign_name

        planet_dossiers[p_name] = PlanetDossier(
            planet=p_name,
            longitude=p.longitude,
            speed=p.speed,
            sign_index=p.sign_index,
            sign_name=p.sign_name,
            deg_in_sign=deg_in_sign,
            nakshatra_name=p.nakshatra_name,
            pada=p.pada,
            nakshatra_lord=p.nakshatra_lord,
            whole_sign_house=ws_house,
            kp_house=kp_house,
            is_retrograde=p.is_retrograde,
            is_combust=is_combust,
            combust_dist_deg=round(abs_combust_dist, 2),
            avastha=avastha,
            dignity=dignity,
            functional_nature=func_nature,
            shadbala_virupas=sh_virupas,
            shadbala_ratio=sh_ratio,
            is_shadbala_strong=sh_strong,
            aspects_cast_to_houses=sorted(aspects_cast_h),
            aspects_received=sorted(aspects_received),
            conjunctions=conjunctions,
            d9_navamsha_sign=d9_analysis["nav_sign_name"],
            d10_dashamsha_sign=d10_sign,
            is_vargottama=d9_analysis["is_vargottama"],
            is_pushkar_navamsha=d9_analysis["is_pushkar_nav"]
        )

    # 6. Build House Dossiers & Contradiction Detection
    house_dossiers: Dict[int, HouseDossier] = {}
    for h in range(1, 13):
        h_sign = (asc_sign + h - 1) % 12
        h_lord = constants.SIGN_LORD[h_sign]
        lord_dossier = planet_dossiers.get(h_lord)

        ws_occ = [p for p in chart.planets if chart.get_house_of_planet(p) == h]
        chalit_occ = [p_name for p_name, d in planet_dossiers.items() if d.kp_house == h]

        # Aspects on House
        aspecting_pls = []
        for p_name, d in planet_dossiers.items():
            if h in d.aspects_cast_to_houses:
                aspecting_pls.append(p_name)

        # Benefic / Malefic counts
        benefics = {"Jupiter", "Venus"}
        if "Moon" in planet_dossiers and not planet_dossiers["Moon"].dignity.startswith("Debilitated"):
            benefics.add("Moon")
        if "Mercury" in planet_dossiers and not planet_dossiers["Mercury"].is_combust:
            benefics.add("Mercury")

        malefics = {"Saturn", "Mars", "Rahu", "Ketu", "Sun"}

        b_count = sum(1 for p in ws_occ if p in benefics) + sum(1 for p in aspecting_pls if p in benefics)
        m_count = sum(1 for p in ws_occ if p in malefics) + sum(1 for p in aspecting_pls if p in malefics)

        # Contradiction Detection (BPHS / Jyotish Principles)
        contradictions = []
        if lord_dossier:
            # Case 1: Exalted Lord placed in Dusthana (6, 8, 12)
            if "Exalted" in lord_dossier.dignity and lord_dossier.whole_sign_house in (6, 8, 12):
                contradictions.append(f"भावेश ({h_lord}) उच्च राशि में है किन्तु त्रिक भाव ({lord_dossier.whole_sign_house}H) में स्थित है।")
            # Case 2: Debilitated Lord but aspected by strong Jupiter
            if "Debilitated" in lord_dossier.dignity and "Jupiter" in lord_dossier.aspects_received:
                contradictions.append(f"भावेश ({h_lord}) नीचस्थ है किन्तु देवगुरु की अमृत दृष्टि से नीचभंग / रक्षा प्राप्त है।")
            # Case 3: Benefic occupants in house but lord is combust/weak
            if b_count > 0 and lord_dossier.is_combust:
                contradictions.append(f"भाव में शुभ ग्रह उपस्थित हैं किन्तु भावेश ({h_lord}) सूर्य के निकट अस्त है।")
            # Case 4: Shift between Whole-Sign and Chalit
            if ws_occ != chalit_occ:
                contradictions.append(f"चलित भेद: राशि कुण्डली में ग्रह स्थिति {ws_occ} है जबकि भाव चलित में {chalit_occ} है।")

        has_contra = len(contradictions) > 0

        house_dossiers[h] = HouseDossier(
            house_num=h,
            sign_index=h_sign,
            sign_name=constants.SIGNS_HI[h_sign],
            lord=h_lord,
            lord_placement_house=lord_dossier.whole_sign_house if lord_dossier else 1,
            lord_dignity=lord_dossier.dignity if lord_dossier else "Unknown",
            lord_shadbala_ratio=lord_dossier.shadbala_ratio if lord_dossier else 1.0,
            lord_is_strong=lord_dossier.is_shadbala_strong if lord_dossier else True,
            whole_sign_occupants=ws_occ,
            chalit_kp_occupants=chalit_occ,
            aspecting_planets=aspecting_pls,
            bhavabala_virupas=bhavabala_map.get(h, 300.0),
            benefic_count=b_count,
            malefic_count=m_count,
            has_contradiction=has_contra,
            contradiction_notes=contradictions
        )

    # 7. Quality Flags
    # Check boundary proximity (within 0°30' of sign edge)
    boundary_proximity = any(p.longitude % 30.0 < 0.5 or p.longitude % 30.0 > 29.5 for p in chart.planets.values())
    asc_boundary = (chart.ascendant_longitude % 30.0 < 0.5 or chart.ascendant_longitude % 30.0 > 29.5)
    
    # D60 is safe only if birth time confidence is High and Lagna is not on boundary edge
    d60_safe = (birth_time_confidence == "High" and not asc_boundary)

    quality_flags = {
        "engine": "Swiss Ephemeris Core (pyswisseph)",
        "precision": "Sub-arcsecond NASA-grade",
        "birth_time_confidence": birth_time_confidence,
        "ascendant_boundary_warning": asc_boundary,
        "planet_boundary_warning": boundary_proximity,
        "d60_interpretation_safe": d60_safe,
        "calculation_valid": True
    }

    return NormalizedChartContext(
        chart=chart,
        birth_dt_utc=birth_dt_utc,
        lat=lat,
        lon=lon,
        whole_sign_houses=whole_sign_houses,
        kp_cusps=kp_cusps,
        shadbala=shadbala_map,
        bhavabala=bhavabala_map,
        planet_dossiers=planet_dossiers,
        house_dossiers=house_dossiers,
        quality_flags=quality_flags
    )
