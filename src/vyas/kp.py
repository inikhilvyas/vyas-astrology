"""KP Astrology Engine: Placidus Cusps, 5-Level Sub-Lords, 4-Step Significators, and Ruling Planets.

Calculates:
1. Exact Placidus House Cusps (1 to 12) with degree, minute, second.
2. Sign Lord (RL), Star Lord (NL), Sub Lord (SL), Sub-Sub Lord (SSL), SSS-Lord (SSSL).
3. KP 4-Step Planetary & House Significators (A, B, C, D levels).
4. Ruling Planets (RP) at epoch:
   - Day Lord (Vara)
   - Moon Sign Lord & Star Lord
   - Ascendant Sign Lord & Star Lord
   - Rahu/Ketu representations
"""
from typing import Dict, List, Tuple, NamedTuple, Optional
from datetime import datetime, timezone, timedelta
import math

from vyas import constants
from vyas import ephem

def get_dasha_proportion(planet: str) -> float:
    return constants.VIMSHOTTARI_YEARS[planet] / 120.0

class KPCusp(NamedTuple):
    cusp_num: int
    longitude: float       # 0 to 360
    sign_index: int      # 0 to 11
    sign_name: str
    deg_in_sign: float
    dms_str: str
    sign_lord: str       # RL
    star_lord: str       # NL
    sub_lord: str        # SL
    sub_sub_lord: str    # SSL
    sub_sub_sub_lord: str # SSSL
    sub_sub_sub_sub_lord: str = "" # SSSSL (Level 5)
    sub_sub_sub_sub_sub_lord: str = "" # SSSSSL (Level 6)

def format_dms(deg_val: float) -> str:
    deg_in_sign = deg_val % 30.0
    d = int(deg_in_sign)
    rem = (deg_in_sign - d) * 60.0
    m = int(rem)
    s = int(round((rem - m) * 60.0))
    if s >= 60:
        m += 1
        s = 0
    if m >= 60:
        d += 1
        m = 0
    return f"{d:02d}°{m:02d}'{s:02d}\""

def calculate_sub_lords(longitude: float, depth: int = 6) -> Dict[str, str]:
    """
    Calculates nested Lords for a given longitude based on KP Astrology proportional math.
    Depth 1 = Star Lord (NL)
    Depth 2 = Sub Lord (SL)
    Depth 3 = Sub-Sub Lord (SSL)
    Depth 4 = Sub-Sub-Sub Lord (SSSL)
    Depth 5 = Sub-Sub-Sub-Sub Lord (SSSSL)
    Depth 6 = Sub-Sub-Sub-Sub-Sub Lord (SSSSSL)
    """
    lon = longitude % 360.0
    nak_idx = int(lon // constants.NAKSHATRA_SPAN) % 27
    star_lord = constants.VIMSHOTTARI_ORDER[nak_idx % 9]
    
    lords = {
        "L1_Star": star_lord,
        "NL": star_lord,
        "SL": "",
        "SSL": "",
        "SSSL": "",
        "SSSSL": "",
        "SSSSSL": ""
    }
    
    current_lord = star_lord
    current_span = constants.NAKSHATRA_SPAN
    deg_passed = lon % constants.NAKSHATRA_SPAN
    
    for level in range(2, depth + 1):
        start_idx = constants.VIMSHOTTARI_ORDER.index(current_lord)
        lower_bound = 0.0
        found_lord = ""
        
        for i in range(9):
            idx = (start_idx + i) % 9
            candidate = constants.VIMSHOTTARI_ORDER[idx]
            candidate_span = current_span * get_dasha_proportion(candidate)
            
            if lower_bound + candidate_span > deg_passed or i == 8:
                found_lord = candidate
                deg_passed -= lower_bound
                current_span = candidate_span
                break
                
            lower_bound += candidate_span
            
        lords[f"L{level}"] = found_lord
        if level == 2: lords["SL"] = found_lord
        elif level == 3: lords["SSL"] = found_lord
        elif level == 4: lords["SSSL"] = found_lord
        elif level == 5: lords["SSSSL"] = found_lord
        elif level == 6: lords["SSSSSL"] = found_lord
        current_lord = found_lord
        
    return lords

def _solve_placidus_cusp(ramc: float, lat: float, eps: float, d_offset: float, f_factor: float) -> float:
    """
    Solves Placidus cusp longitude iteratively.
    ramc: right ascension of MC in radians
    lat: geographic latitude in radians
    eps: obliquity in radians
    d_offset: RAMC offset (e.g. +30 deg for 11th, +60 deg for 12th)
    f_factor: 1/3 for 11th/3rd, 2/3 for 12th/2nd
    """
    r_target = (ramc + d_offset) % (2.0 * math.pi)
    # Initial estimate of RA
    ra = r_target
    
    for _ in range(15):
        # Declination for this RA
        sin_dec = math.sin(eps) * math.sin(ra)
        dec = math.asin(max(-0.9999, min(0.9999, sin_dec)))
        # Semidiurnal arc calculation
        val = -math.tan(lat) * math.tan(dec)
        val = max(-0.9999, min(0.9999, val))
        ad = math.asin(val) # ascensional difference
        
        # Next RA approximation based on Placidus proportionality
        ra_next = (r_target + f_factor * ad) % (2.0 * math.pi)
        if abs(ra_next - ra) < 1e-6:
            ra = ra_next
            break
        ra = ra_next
        
    # Convert RA to Ecliptic Longitude
    tan_lon = math.sin(ra) / (math.cos(ra) * math.cos(eps) - math.tan(dec) * math.sin(eps))
    lon = math.atan2(math.sin(ra) * math.cos(eps) + math.tan(dec) * math.sin(eps), math.cos(ra))
    return (math.degrees(lon)) % 360.0

def calculate_placidus_cusps_sidereal(dt_utc: datetime, lat: float, lon: float) -> List[KPCusp]:
    """
    Computes the 12 Placidus house cusps sidereally using the active ayanamsa.
    """
    t = ephem._t(dt_utc)
    ramc_deg = (t.gast * 15.0 + lon) % 360.0
    eps_deg = ephem.obliquity_deg(t.tt)
    ay = ephem.lahiri_ayanamsa(t.tt)
    
    ramc_rad = math.radians(ramc_deg)
    lat_rad = math.radians(lat)
    eps_rad = math.radians(eps_deg)
    
    # Tropical MC (10th cusp)
    mc_trop = math.degrees(math.atan2(math.tan(ramc_rad), math.cos(eps_rad))) % 360.0
    if abs((mc_trop - ramc_deg + 180) % 360 - 180) > 90:
        mc_trop = (mc_trop + 180.0) % 360.0
        
    # Tropical Ascendant (1st cusp)
    asc_trop = ephem.ascendant_tropical(ramc_deg, lat, eps_deg)
    
    # Calculate tropical intermediate cusps
    try:
        # Cusp 11: offset +30°, factor 1/3
        c11_trop = _solve_placidus_cusp(ramc_rad, lat_rad, eps_rad, math.radians(30.0), 1.0/3.0)
        # Cusp 12: offset +60°, factor 2/3
        c12_trop = _solve_placidus_cusp(ramc_rad, lat_rad, eps_rad, math.radians(60.0), 2.0/3.0)
        # Cusp 2: offset +120°, factor 2/3
        c2_trop = _solve_placidus_cusp(ramc_rad, lat_rad, eps_rad, math.radians(120.0), 2.0/3.0)
        # Cusp 3: offset +150°, factor 1/3
        c3_trop = _solve_placidus_cusp(ramc_rad, lat_rad, eps_rad, math.radians(150.0), 1.0/3.0)
    except Exception:
        # Safe Porphyry / Equal division fallback if high polar latitude causes non-convergence
        c11_trop = (mc_trop + ((asc_trop - mc_trop) % 360.0) / 3.0) % 360.0
        c12_trop = (mc_trop + 2.0 * ((asc_trop - mc_trop) % 360.0) / 3.0) % 360.0
        ic_trop = (mc_trop + 180.0) % 360.0
        c2_trop = (asc_trop + ((ic_trop - asc_trop) % 360.0) / 3.0) % 360.0
        c3_trop = (asc_trop + 2.0 * ((ic_trop - asc_trop) % 360.0) / 3.0) % 360.0

    trop_cusps = {
        1: asc_trop,
        2: c2_trop,
        3: c3_trop,
        4: (mc_trop + 180.0) % 360.0,
        5: (c11_trop + 180.0) % 360.0,
        6: (c12_trop + 180.0) % 360.0,
        7: (asc_trop + 180.0) % 360.0,
        8: (c2_trop + 180.0) % 360.0,
        9: (c3_trop + 180.0) % 360.0,
        10: mc_trop,
        11: c11_trop,
        12: c12_trop,
    }
    
    results: List[KPCusp] = []
    for num in range(1, 13):
        sid_lon = (trop_cusps[num] - ay) % 360.0
        sign_idx = int(sid_lon // 30.0) % 12
        deg_in_sign = sid_lon % 30.0
        
        subs = calculate_sub_lords(sid_lon, depth=6)
        c = KPCusp(
            cusp_num=num,
            longitude=sid_lon,
            sign_index=sign_idx,
            sign_name=constants.SIGNS[sign_idx],
            deg_in_sign=deg_in_sign,
            dms_str=format_dms(sid_lon),
            sign_lord=constants.SIGN_LORD[sign_idx],
            star_lord=subs["NL"],
            sub_lord=subs["SL"],
            sub_sub_lord=subs["SSL"],
            sub_sub_sub_lord=subs.get("SSSL", ""),
            sub_sub_sub_sub_lord=subs.get("SSSSL", ""),
            sub_sub_sub_sub_sub_lord=subs.get("SSSSSL", "")
        )
        results.append(c)
        
    return results

def get_house_of_longitude(lon: float, cusps: List[KPCusp]) -> int:
    """
    Finds which Placidus house (1 to 12) a given sidereal longitude falls into.
    """
    lon = lon % 360.0
    for i in range(12):
        curr_c = cusps[i].longitude
        next_c = cusps[(i + 1) % 12].longitude
        
        span = (next_c - curr_c) % 360.0
        pos = (lon - curr_c) % 360.0
        
        if pos < span:
            return cusps[i].cusp_num
    return 1

def compute_kp_significators(planets: dict, cusps: List[KPCusp]) -> Dict[str, dict]:
    """
    Computes KP 4-Step Significators for all 9 planets:
    Level A: Houses occupied by planets residing in the Star Lord's constellations.
    Level B: House occupied by the planet itself.
    Level C: Houses owned by planets residing in the Star Lord's constellations.
    Level D: Houses owned by the planet itself (by cusp placement).
    """
    # 1. Map planet -> occupied house
    planet_house = {}
    for p_name, p_state in planets.items():
        planet_house[p_name] = get_house_of_longitude(p_state.longitude, cusps)
        
    # 2. Map planet -> owned houses (which cusp has planet as Sign Lord)
    planet_owned_houses = {p: [] for p in constants.PLANETS}
    for c in cusps:
        planet_owned_houses[c.sign_lord].append(c.cusp_num)
        
    # 3. Map planet -> star lord
    planet_nl = {}
    for p_name, p_state in planets.items():
        subs = calculate_sub_lords(p_state.longitude, depth=2)
        planet_nl[p_name] = subs["NL"]
        
    significators = {}
    for p_name, p_state in planets.items():
        nl = planet_nl[p_name]
        
        lvl_a = [planet_house[nl]] if nl in planet_house else []
        lvl_b = [planet_house[p_name]]
        lvl_c = planet_owned_houses.get(nl, [])
        lvl_d = planet_owned_houses.get(p_name, [])
        
        all_houses = sorted(list(set(lvl_a + lvl_b + lvl_c + lvl_d)))
        
        significators[p_name] = {
            "house_occupied": planet_house[p_name],
            "star_lord": nl,
            "lvl_A": lvl_a,
            "lvl_B": lvl_b,
            "lvl_C": lvl_c,
            "lvl_D": lvl_d,
            "all_signified": all_houses
        }
        
    return significators

def get_ruling_planets(dt_local: datetime, lat: float, lon: float, tz_hours: float, 
                       moon_lon: float, asc_lon: float) -> dict:
    """
    Calculates Krishnamurti Ruling Planets (RP) at a specific query or birth time.
    """
    wd = (dt_local.weekday() + 1) % 7
    day_lord = constants.VARA_LORD[wd] if hasattr(constants, 'VARA_LORD') else ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"][wd]
    
    # Moon lords
    moon_sign_idx = int(moon_lon // 30.0) % 12
    moon_subs = calculate_sub_lords(moon_lon, depth=2)
    moon_rl = constants.SIGN_LORD[moon_sign_idx]
    moon_nl = moon_subs["NL"]
    
    # Ascendant lords
    asc_sign_idx = int(asc_lon // 30.0) % 12
    asc_subs = calculate_sub_lords(asc_lon, depth=2)
    asc_rl = constants.SIGN_LORD[asc_sign_idx]
    asc_nl = asc_subs["NL"]
    
    return {
        "Day_Lord": day_lord,
        "Moon_Sign_Lord": moon_rl,
        "Moon_Star_Lord": moon_nl,
        "Ascendant_Sign_Lord": asc_rl,
        "Ascendant_Star_Lord": asc_nl,
        "RP_Summary": f"{asc_nl} (Lagna Star), {asc_rl} (Lagna Sign), {moon_nl} (Moon Star), {moon_rl} (Moon Sign), {day_lord} (Day Lord)"
    }


class KPPlanet(NamedTuple):
    planet: str
    planet_hi: str
    longitude: float
    sign_index: int
    sign_name: str
    deg_in_sign: float
    dms_str: str
    sign_lord: str       # RL
    star_lord: str       # NL
    sub_lord: str        # SL
    sub_sub_lord: str    # SSL
    sub_sub_sub_lord: str # SSSL
    sub_sub_sub_sub_lord: str # SSSSL
    sub_sub_sub_sub_sub_lord: str # SSSSSL
    house_occupied: int


def calculate_planet_kp_lords(planets: dict, cusps: Optional[List[KPCusp]] = None) -> List[KPPlanet]:
    """
    Computes KP lords down to Level 6 (RL, NL, SL, SSL, SSSL, SSSSL, SSSSSL) for each planet.
    """
    res = []
    for p_name in constants.PLANETS:
        if p_name not in planets:
            continue
        p_state = planets[p_name]
        lon = p_state.longitude % 360.0
        sign_idx = int(lon // 30.0) % 12
        deg_in_sign = lon % 30.0
        
        subs = calculate_sub_lords(lon, depth=6)
        h_occ = get_house_of_longitude(lon, cusps) if cusps else (sign_idx + 1)
        
        res.append(KPPlanet(
            planet=p_name,
            planet_hi=constants.PLANETS_HI.get(p_name, p_name),
            longitude=lon,
            sign_index=sign_idx,
            sign_name=constants.SIGNS[sign_idx],
            deg_in_sign=deg_in_sign,
            dms_str=format_dms(lon),
            sign_lord=constants.SIGN_LORD[sign_idx],
            star_lord=subs.get("NL", ""),
            sub_lord=subs.get("SL", ""),
            sub_sub_lord=subs.get("SSL", ""),
            sub_sub_sub_lord=subs.get("SSSL", ""),
            sub_sub_sub_sub_lord=subs.get("SSSSL", ""),
            sub_sub_sub_sub_sub_lord=subs.get("SSSSSL", ""),
            house_occupied=h_occ
        ))
    return res


def compute_kp_4fold_house_significators(planets: dict, cusps: List[KPCusp], planet_significators: Optional[dict] = None) -> dict:
    """
    Computes KP 4-Fold Significators (चतुर्विध कार्येश):
    Level A: Planets in the Star of occupants of the house (परम शक्तिशाली)
    Level B: Occupants of the house (शक्तिशाली)
    Level C: Planets in the Star of the house lord (मध्यम)
    Level D: Lord of the house (सामान्य)

    Returns:
    {
        "house_significators": {1..12: {level_a, level_b, level_c, level_d, all_significators, house_lord, occupants}},
        "planet_significators": planet_significators
    }
    """
    if planet_significators is None:
        planet_significators = compute_kp_significators(planets, cusps)
        
    house_occupants = {h: [] for h in range(1, 13)}
    for p_name, p_state in planets.items():
        if p_name in constants.PLANETS:
            h = get_house_of_longitude(p_state.longitude, cusps)
            house_occupants[h].append(p_name)
            
    house_lords = {}
    for c in cusps:
        house_lords[c.cusp_num] = c.sign_lord

    planet_star = {}
    for p_name, p_state in planets.items():
        if p_name in constants.PLANETS:
            subs = calculate_sub_lords(p_state.longitude, depth=2)
            planet_star[p_name] = subs["NL"]

    house_sig = {}
    for h in range(1, 13):
        h_lord = house_lords.get(h, "")
        occ = house_occupants.get(h, [])
        
        # Level A: Planets in the star of any occupant of house h
        lvl_a = [p for p, st_lord in planet_star.items() if st_lord in occ]
        # Level B: Occupants of house h
        lvl_b = occ
        # Level C: Planets in the star of the house lord
        lvl_c = [p for p, st_lord in planet_star.items() if st_lord == h_lord]
        # Level D: Lord of house h
        lvl_d = [h_lord] if h_lord else []
        
        all_sig = []
        for pl in (lvl_a + lvl_b + lvl_c + lvl_d):
            if pl not in all_sig:
                all_sig.append(pl)
                
        house_sig[h] = {
            "house_num": h,
            "house_lord": h_lord,
            "occupants": occ,
            "level_a": lvl_a,
            "level_b": lvl_b,
            "level_c": lvl_c,
            "level_d": lvl_d,
            "all_significators": all_sig
        }
        
    return {
        "house_significators": house_sig,
        "planet_significators": planet_significators
    }


def evaluate_kp_house_promises(cusps: List[KPCusp], planet_significators: dict, planets: dict) -> List[dict]:
    """
    Evaluates KP House Promises (कुण्डली में किस बात का प्रॉमिस है और क्या नहीं) across 9 core life areas:
    Uses primary cusp Sub-Lord and Star-Lord significations vs positive/negative houses.
    """
    cusp_map = {c.cusp_num: c for c in cusps}
    
    events = [
        {
            "id": "marriage",
            "title_hi": "विवाह एवं दाम्पत्य जीवन (Marriage & Union)",
            "icon": "💍",
            "primary_cusp": 7,
            "favorable_houses": [2, 7, 11],
            "detrimental_houses": [1, 6, 10],
            "description": "विवाह का प्रॉमिस सप्तम भाव के कस्प उप-स्वामी (Cusp Sub-Lord) एवं उसके नक्षत्र स्वामी द्वारा 2 (कुटुम्ब वृद्धि), 7 (जीवनसाथी) एवं 11 (इच्छा पूर्ति) भावों के संबंध से निर्धारित होता है। 1, 6, 10 भाव अलगाव अथवा विलंब दर्शाते हैं।"
        },
        {
            "id": "career",
            "title_hi": "आजीविका, पदोन्नति एवं व्यापार (Career & Profession)",
            "icon": "💼",
            "primary_cusp": 10,
            "favorable_houses": [2, 6, 10, 11],
            "detrimental_houses": [5, 9],
            "description": "दशम भाव का कस्प उप-स्वामी जब 2 (धन), 6 (सेवा/प्रतियोगिता), 10 (कर्म/प्रतिष्ठा) व 11 (लाभ) भावों का कार्येश बनता है, तब करियर में स्थिरता व उच्च पद का पक्का प्रॉमिस बनता है। 5 व 9 भाव पदमुक्ति या बदलाव दर्शाते हैं।"
        },
        {
            "id": "wealth",
            "title_hi": "धन संचय, समृद्धि एवं वित्तीय स्थिति (Wealth & Finance)",
            "icon": "💰",
            "primary_cusp": 2,
            "favorable_houses": [2, 6, 11],
            "detrimental_houses": [5, 8, 12],
            "description": "द्वितीय (संचित धन) एवं एकादश (लाभ) भावों के उप-स्वामी 2, 6, 11 भावों से जुड़ें तो अखंड धन योग का प्रॉमिस होता है। 5, 8, 12 भाव अनावश्यक व्यय एवं सट्टेबाजी में हानि कराते हैं।"
        },
        {
            "id": "progeny",
            "title_hi": "संतान सुख एवं संतति प्राप्ति (Progeny & Children)",
            "icon": "👶",
            "primary_cusp": 5,
            "favorable_houses": [2, 5, 11],
            "detrimental_houses": [1, 4, 10],
            "description": "पंचम कस्प उप-स्वामी यदि 2 (कुटुम्ब), 5 (गर्भ/संतान) और 11 (इच्छा पूर्ति) से संबंधित हो, तो निर्विघ्न संतान सुख का प्रॉमिस होता है। 1, 4, 10 भाव संतान प्राप्ति में विलंब या चिकित्सा उपचार की आवश्यकता बताते हैं।"
        },
        {
            "id": "education",
            "title_hi": "उच्च विद्या, अनुसंधान एवं बौद्धिक सिद्धि (Education & Academics)",
            "icon": "🎓",
            "primary_cusp": 4,
            "favorable_houses": [4, 9, 11],
            "detrimental_houses": [3, 8],
            "description": "चतुर्थ (मूल शिक्षा) एवं नवम (उच्च डिग्री/अनुसंधान) के उप-स्वामी जब 4, 9, 11 भावों के कार्येश होते हैं तो विशिष्ट शैक्षणिक योग्यता का प्रॉमिस बनता है। 3 व 8 भाव शिक्षा में व्यवधान या दिशा-परिवर्तन देते हैं।"
        },
        {
            "id": "foreign_travel",
            "title_hi": "विदेश गमन, सुदूर प्रवास एवं विदेश वास (Foreign Travel & Settlement)",
            "icon": "✈️",
            "primary_cusp": 12,
            "favorable_houses": [3, 9, 12],
            "detrimental_houses": [4, 11],
            "description": "द्वादश एवं नवम भाव के कस्प उप-स्वामी 3 (गृह त्याग/लघु यात्रा), 9 (सुदूर महाद्वीपीय यात्रा) और 12 (विदेशी भूमि पर निवास) से संबंध बनाएं तो स्थायी विदेश वास का मजबूत प्रॉमिस होता है।"
        },
        {
            "id": "health",
            "title_hi": "स्वास्थ्य, रोग मुक्ति एवं दीर्घायु (Health & Vitality)",
            "icon": "🌿",
            "primary_cusp": 1,
            "favorable_houses": [1, 5, 11],
            "detrimental_houses": [6, 8, 12],
            "description": "लग्न कस्प उप-स्वामी 1 (आरोग्य), 5 (रोग नाश) और 11 (स्वास्थ्य लाभ) का संबंध रखे तो दीर्घायु व रोगमुक्त जीवन का प्रॉमिस होता है। 6, 8, 12 भावों से जुड़ने पर समय-समय पर चिकित्सीय परामर्श आवश्यक रहता है।"
        },
        {
            "id": "property_vehicle",
            "title_hi": "भूमि, भवन, अचल सम्पत्ति व वाहन सुख (Property & Vehicles)",
            "icon": "🏠",
            "primary_cusp": 4,
            "favorable_houses": [4, 11, 12],
            "detrimental_houses": [3, 10],
            "description": "चतुर्थ भाव का उप-स्वामी 4 (भवन/वाहन) व 11 (सम्पत्ति लाभ) तथा 12 (निवेश) का कार्येश हो तो स्वयं के मकान व वाहन क्रय का पूर्ण प्रॉमिस होता है। 3 व 10 भाव सम्पत्ति विक्रय या विलंब दर्शाते हैं।"
        },
        {
            "id": "litigation",
            "title_hi": "मुकदमा, शत्रु दमन एवं प्रतियोगी विजय (Litigation & Competition)",
            "icon": "⚖️",
            "primary_cusp": 6,
            "favorable_houses": [6, 11],
            "detrimental_houses": [5, 12],
            "description": "षष्ठ भाव का उप-स्वामी जब 6 (शत्रु पराजय) और 11 (अंतिम विजय) भावों को सिग्निफाई करे, तो जातक प्रतियोगी परीक्षाओं व मुकदमों में सदैव विजयी रहता है। 5 व 12 भाव समझौते या व्यय को दर्शाते हैं।"
        }
    ]
    
    results = []
    for ev in events:
        c_obj = cusp_map[ev["primary_cusp"]]
        sl = c_obj.sub_lord
        sl_hi = constants.PLANETS_HI.get(sl, sl)
        
        sig_data = planet_significators.get(sl, {})
        signified = sig_data.get("all_signified", [])
        nl_of_sl = sig_data.get("star_lord", "")
        nl_sig = planet_significators.get(nl_of_sl, {}).get("all_signified", [])
        
        total_houses = sorted(list(set(signified + nl_sig)))
        
        fav_present = [h for h in ev["favorable_houses"] if h in total_houses]
        det_present = [h for h in ev["detrimental_houses"] if h in total_houses]
        
        fav_count = len(fav_present)
        det_count = len(det_present)
        
        if fav_count >= 2 and det_count <= 1:
            status = "PROMISED"
            status_hi = "पूर्ण प्रॉमिस (Full Promise)"
            status_color = "#22c55e"
            verdict_text = f"कुण्डली में {ev['title_hi']} का **पूर्ण एवं सशक्त प्रॉमिस** विद्यमान है। कस्प उप-स्वामी {sl_hi} अनुकूल भाव {fav_present} को सक्रिय रूप से सिग्निफाई कर रहा है, जिससे दशा-गोचर अनुकूल होते ही अभीष्ट फल की सहज प्राप्ति होगी।"
        elif fav_count >= 1:
            status = "MODERATE_DELAY"
            status_hi = "मध्यम प्रॉमिस / विलंब से सिद्धि (Moderate / Delayed)"
            status_color = "#eab308"
            verdict_text = f"कुण्डली में {ev['title_hi']} का **मध्यम प्रॉमिस** है। कस्प उप-स्वामी {sl_hi} अनुकूल भाव {fav_present} के साथ-साथ विरोधी भाव {det_present} से भी सम्बद्ध है, जिससे प्रयास अधिक करने होंगे अथवा कुछ विलंब के पश्चात सफलता प्राप्त होगी।"
        else:
            status = "RESTRICTED"
            status_hi = "बाधा / प्रॉमिस में न्यूनता (Challenging / Restricted)"
            status_color = "#ef4444"
            verdict_text = f"कुण्डली में {ev['title_hi']} के लिए कस्प उप-स्वामी {sl_hi} प्राथमिक अनुकूल भावों को सीधे सिग्निफाई नहीं कर रहा है तथा विरोधी भाव {det_present} सक्रिय हैं। इसके लिए विशेष उपाय, अनुष्ठान एवं सतर्कता आवश्यक है।"
            
        results.append({
            "id": ev["id"],
            "title_hi": ev["title_hi"],
            "icon": ev["icon"],
            "primary_cusp": ev["primary_cusp"],
            "sub_lord": sl,
            "sub_lord_hi": sl_hi,
            "star_lord": nl_of_sl,
            "star_lord_hi": constants.PLANETS_HI.get(nl_of_sl, nl_of_sl),
            "signified_houses": total_houses,
            "favorable_houses": ev["favorable_houses"],
            "favorable_active": fav_present,
            "detrimental_houses": ev["detrimental_houses"],
            "detrimental_active": det_present,
            "status": status,
            "status_hi": status_hi,
            "status_color": status_color,
            "description": ev["description"],
            "verdict_text": verdict_text
        })
        
    return results


def evaluate_active_houses_by_dasha(cur_dasha: dict, planet_significators: dict, cusps: Optional[List[KPCusp]] = None) -> dict:
    """
    Evaluates House Activation by Dasha (कब कौनसा भाव एक्टिव हो रहा है):
    Determines currently activated houses based on Mahadasha, Antardasha, Pratyantardasha, and Sookshma Dasha lords.
    """
    md = cur_dasha.get("mahadasha", "Jupiter")
    ad = cur_dasha.get("antardasha", "Saturn")
    pd = cur_dasha.get("pratyantardasha", "Mercury")
    sd = cur_dasha.get("sookshma_dasha", "")
    
    md_sig = planet_significators.get(md, {}).get("all_signified", [])
    ad_sig = planet_significators.get(ad, {}).get("all_signified", [])
    pd_sig = planet_significators.get(pd, {}).get("all_signified", [])
    sd_sig = planet_significators.get(sd, {}).get("all_signified", []) if sd else []
    
    co_active = sorted(list(set(md_sig).intersection(set(ad_sig))))
    all_active = sorted(list(set(md_sig + ad_sig + pd_sig + sd_sig)))
    
    domain_map = {
        1: ("तनु भाव (आरोग्य व व्यक्तित्व)", "स्वास्थ्य, आत्मबल, ऊर्जा एवं निजी निर्णय"),
        2: ("धन भाव (आर्थिक संचय व परिवार)", "धन की आवक, बचत, पारिवारिक सुख एवं वाणी"),
        3: ("सहज भाव (पराक्रम व यात्रा)", "लघु यात्राएं, संचार, अनुबंध, छोटे भाई-बहन एवं नया उद्यम"),
        4: ("सुख भाव (माता, भूमि व वाहन)", "गृह निर्माण, वाहन क्रय, माता का स्वास्थ्य एवं घरेलू शांति"),
        5: ("सुत भाव (संतान, बुद्धि व प्रेम)", "संतान सुख, रचनात्मक सफलता, उच्च परामर्श एवं शेयर/सट्टा"),
        6: ("रिपु भाव (नौकरी, रोग व ऋण)", "प्रतियोगी परीक्षा, नौकरी में दायित्व, स्वास्थ्य सतर्कता व ऋण मुक्ति"),
        7: ("जाया भाव (दाम्पत्य व साझेदारी)", "विवाह, व्यापारिक साझेदारी, जनसंपर्क एवं सामाजिक पद"),
        8: ("आयु भाव (गूढ़ विद्या व अचानक घटनाएं)", "अचानक लाभ/हानि, पैतृक सम्पत्ति, अनुसंधान व मानसिक दबाव"),
        9: ("भाग्य भाव (धर्म, उच्च शिक्षा व तीर्थ)", "भाग्योदय, धार्मिक कार्य, उच्च शिक्षा एवं सुदूर विदेश यात्रा"),
        10: ("कर्म भाव (आजीविका, पद व प्रतिष्ठा)", "नौकरी/व्यापार में प्रतिष्ठा, पदोन्नति, शासन से लाभ व सामाजिक दायित्व"),
        11: ("लाभ भाव (आय, मित्र व इच्छा पूर्ति)", "आर्थिक लाभ, बड़े भाई-बहन, मित्रों का सहयोग व मनोरथ सिद्धि"),
        12: ("व्यय भाव (विदेश, निवेश व मोक्ष)", "विदेश वास, बड़ा वित्तीय निवेश, धर्मार्थ व्यय एवं निद्रा सुख")
    }
    
    active_details = []
    for h in all_active:
        intensity = "अत्यंत तीव्र (Peak Active)" if h in co_active else "सक्रिय (Active)"
        color = "#22c55e" if h in co_active else "#38bdf8"
        title, meaning = domain_map.get(h, (f"भाव {h}", "सामान्य प्रभाव"))
        active_details.append({
            "house": h,
            "title": title,
            "meaning": meaning,
            "intensity": intensity,
            "color": color,
            "is_co_active": h in co_active
        })
        
    triggers = []
    if any(h in co_active for h in [2, 7, 11]) or (set([2, 11]).issubset(set(all_active)) and 7 in all_active):
        triggers.append("💍 **विवाह एवं साझेदारी की सक्रियता:** सप्तम, द्वितीय एवं एकादश भावों की सम्मिलित सक्रियता नए प्रेम प्रसंग, विवाह वार्ता अथवा व्यापारिक साझेदारी के लिए स्वर्णिम योग बना रही है।")
    if any(h in co_active for h in [2, 6, 10, 11]) or (set([10, 11]).issubset(set(all_active))):
        triggers.append("💼 **करियर एवं धन लाभ की सक्रियता:** कर्म भाव (10), सेवा (6) एवं लाभ (11) सक्रिय हैं। यह समय पदोन्नति, नई नौकरी, वेतन वृद्धि अथवा व्यापार विस्तार के लिए सर्वाधिक फलदायी है।")
    if any(h in co_active for h in [3, 9, 12]) or (set([9, 12]).issubset(set(all_active))):
        triggers.append("✈️ **विदेश यात्रा एवं स्थान परिवर्तन:** नवम, द्वादश एवं तृतीय भाव सक्रिय हैं। सुदूर यात्रा, विदेश गमन, पासपोर्ट/वीजा कार्य अथवा शहर परिवर्तन के प्रबल संकेत हैं।")
    if any(h in co_active for h in [4, 11, 12]) or (4 in all_active and 11 in all_active):
        triggers.append("🏠 **सम्पत्ति एवं वाहन क्रय:** चतुर्थ एवं एकादश भावों की सक्रियता नया मकान, फ्लैट, भूमि अथवा वाहन क्रय करने के लिए अनुकूल परिस्थितियां बना रही है।")
    if any(h in co_active for h in [6, 8, 12]) or (set([6, 8]).issubset(set(all_active))):
        triggers.append("⚠️ **स्वास्थ्य एवं अनावश्यक व्यय के प्रति सतर्कता:** 6, 8 अथवा 12 भाव सक्रिय होने के कारण मौसमी रोग, अनावश्यक कानूनी वाद-विवाद अथवा व्यर्थ के खर्चों से बचाव अपेक्षित है। खान-पान व वाहन चलाने में सावधानी रखें।")
    if not triggers:
        triggers.append("⚖️ **संतुलित दिनचर्या एवं स्थिर प्रगति:** वर्तमान दशाएं मिश्रित भावों को सक्रिय कर रही हैं। यह समय धैर्यपूर्वक पूर्व-निर्धारित कार्यों को आगे बढ़ाने एवं योजनाबद्ध कर्म का है।")

    return {
        "mahadasha_lord": md,
        "mahadasha_lord_hi": constants.PLANETS_HI.get(md, md),
        "antardasha_lord": ad,
        "antardasha_lord_hi": constants.PLANETS_HI.get(ad, ad),
        "pratyantardasha_lord": pd,
        "pratyantardasha_lord_hi": constants.PLANETS_HI.get(pd, pd),
        "sookshma_lord": sd,
        "sookshma_lord_hi": constants.PLANETS_HI.get(sd, sd) if sd else "",
        "co_active_houses": co_active,
        "all_active_houses": all_active,
        "active_details": active_details,
        "event_triggers": triggers
    }
