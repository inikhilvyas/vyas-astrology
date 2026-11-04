"""Shodashvarga (16 Divisional Charts) Engine with Micro-Degree Precision & D60 Deities.

Implements BPHS (Brihat Parashara Hora Shastra) algorithms for all 16 divisional charts.
For every chart D_N, computes:
1. Sign Index (0-11, Aries to Pisces)
2. Exact Degree, Minute, Second inside that divisional sign: (deg_in_sign * N) % 30.0
3. For D60 (Shashtyamsha): Calculates the exact Shashtyamsha number (1 to 60), 
   the classical ruling Deity according to Parashara, and nature (Shubha/Ashubha).
"""
from typing import Dict, Tuple, NamedTuple
import math

class VargaPosition(NamedTuple):
    varga_name: str
    varga_num: int
    sign_index: int       # 0 to 11
    sign_name: str
    degree_in_sign: float # 0.0 to 30.0
    dms_str: str          # e.g. "14°28'12\""
    deity: str = ""       # For D60 or specific vargas
    is_benefic: bool = True

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला",
            "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]

# Parashara BPHS 60 Shashtyamsha Deities (in order 1 to 60 for Odd Signs)
# Even signs count in reverse order (60 down to 1).
D60_DEITIES = [
    ("Ghora", False),          # 1
    ("Rakshasa", False),       # 2
    ("Deva", True),            # 3
    ("Kubera", True),          # 4
    ("Yaksha", True),          # 5
    ("Kinnara", True),         # 6
    ("Bhrashta", False),       # 7
    ("Kulaghna", False),       # 8
    ("Garala", False),         # 9
    ("Vahni", False),          # 10
    ("Maya", False),           # 11
    ("Purishaka", False),      # 12
    ("Apampati", True),        # 13 (Varuna)
    ("Marutvana", True),       # 14 (Vayu)
    ("Kaala", False),          # 15
    ("Sarpa", False),          # 16
    ("Amrita", True),          # 17
    ("Indu", True),            # 18 (Chandra)
    ("Mridu", True),           # 19
    ("Komala", True),          # 20
    ("Heramba", True),         # 21 (Ganesha)
    ("Brahma", True),          # 22
    ("Vishnu", True),          # 23
    ("Maheshwara", True),      # 24 (Shiva)
    ("Deva", True),            # 25
    ("Aardra", True),          # 26
    ("Kalinasha", True),       # 27
    ("Kshiteesha", True),      # 28
    ("Kamalakara", True),      # 29
    ("Gulika", False),         # 30 (Mandatmaja)
    ("Mrityu", False),         # 31
    ("Kaala", False),          # 32
    ("Davagni", False),        # 33
    ("Ghora", False),          # 34
    ("Adhama", False),         # 35
    ("Kantaka", False),        # 36
    ("Sudha", True),           # 37
    ("Amrita", True),          # 38
    ("Poornachandra", True),   # 39
    ("Vishadagdha", False),    # 40
    ("Kulanasha", False),      # 41
    ("Vamshakshaya", False),   # 42
    ("Utpata", False),         # 43
    ("Kaalarupa", False),      # 44
    ("Saumya", True),          # 45
    ("Komala", True),          # 46
    ("Sheetala", True),        # 47
    ("Karaladamshtra", False), # 48
    ("Chandramukhi", True),    # 49
    ("Praveena", True),        # 50
    ("Kaalapavaka", False),    # 51
    ("Dandayudha", False),     # 52
    ("Nirmala", True),         # 53
    ("Saumya", True),          # 54
    ("Krura", False),          # 55
    ("Atisheetala", True),     # 56
    ("Amrita", True),          # 57
    ("Payodhi", True),         # 58
    ("Bhramana", False),       # 59
    ("Chandrarekha", True),    # 60
]

def format_dms(deg_val: float) -> str:
    """Formats float degree to DD°MM'SS\"."""
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

def get_sign(index: int) -> int:
    return int(index) % 12

def calculate_vargas_detailed(longitude: float) -> Dict[str, VargaPosition]:
    """
    Given an absolute sidereal longitude (0.0 to 360.0), calculates all 16 Shodashvargas
    with exact sign index, degree inside the divisional sign, and D60 deity.
    """
    planet_sign = int(longitude // 30.0) % 12
    degree_in_sign = longitude % 30.0
    is_odd_sign = (planet_sign % 2 == 0) # 0=Aries (Odd), 1=Taurus (Even), etc.

    vargas: Dict[str, VargaPosition] = {}

    def add_varga(v_name: str, v_num: int, target_sign: int, internal_deg: float, deity: str = "", is_ben: bool = True):
        dms = format_dms(internal_deg)
        vargas[v_name] = VargaPosition(
            varga_name=v_name,
            varga_num=v_num,
            sign_index=target_sign,
            sign_name=SIGNS[target_sign],
            degree_in_sign=internal_deg,
            dms_str=dms,
            deity=deity,
            is_benefic=is_ben
        )

    # 1. D1 Rashi (Span 30°)
    add_varga("D1", 1, planet_sign, degree_in_sign)

    # 2. D2 Hora (Span 15°)
    # Parashara: Odd signs -> 0-15 Sun (Leo, 4), 15-30 Moon (Cancer, 3)
    # Even signs -> 0-15 Moon (Cancer, 3), 15-30 Sun (Leo, 4)
    hora_deg = (degree_in_sign * 2.0) % 30.0
    if is_odd_sign:
        d2_sign = 4 if degree_in_sign < 15.0 else 3
    else:
        d2_sign = 3 if degree_in_sign < 15.0 else 4
    add_varga("D2", 2, d2_sign, hora_deg)

    # 3. D3 Drekkana (Span 10°)
    d3_part = int(degree_in_sign // 10.0) # 0, 1, 2
    d3_deg = (degree_in_sign * 3.0) % 30.0
    d3_sign = get_sign(planet_sign + d3_part * 4)
    add_varga("D3", 3, d3_sign, d3_deg)

    # 4. D4 Chaturthamsha (Span 7°30')
    d4_part = int(degree_in_sign // 7.5) # 0, 1, 2, 3
    d4_deg = (degree_in_sign * 4.0) % 30.0
    d4_sign = get_sign(planet_sign + d4_part * 3)
    add_varga("D4", 4, d4_sign, d4_deg)

    # 5. D7 Saptamsha (Span 4°17'08.57")
    d7_span = 30.0 / 7.0
    d7_part = int(degree_in_sign // d7_span) # 0 to 6
    d7_deg = (degree_in_sign * 7.0) % 30.0
    d7_sign = get_sign(planet_sign + d7_part) if is_odd_sign else get_sign(planet_sign + 6 + d7_part)
    add_varga("D7", 7, d7_sign, d7_deg)

    # 6. D9 Navamsha (Span 3°20' = 10/3 degrees)
    # Movable signs (0, 3, 6, 9) start from sign itself
    # Fixed signs (1, 4, 7, 10) start from 9th from sign (sign + 8)
    # Dual signs (2, 5, 8, 11) start from 5th from sign (sign + 4)
    nav_span = 30.0 / 9.0  # 3.3333333333333335°
    d9_idx_in_sign = int((degree_in_sign + 1e-10) // nav_span)
    if d9_idx_in_sign > 8:
        d9_idx_in_sign = 8
    sign_type = planet_sign % 3
    if sign_type == 0:    # Chara (Movable)
        start_nav = planet_sign
    elif sign_type == 1:  # Sthira (Fixed)
        start_nav = get_sign(planet_sign + 8)
    else:                 # Dwiswabhava (Dual)
        start_nav = get_sign(planet_sign + 4)
    d9_sign = get_sign(start_nav + d9_idx_in_sign)
    d9_deg = (degree_in_sign * 9.0) % 30.0
    add_varga("D9", 9, d9_sign, d9_deg)

    # 7. D10 Dashamsha (Span 3°00')
    # BPHS 6.11: for an ODD sign the ten parts start from that sign itself;
    # for an EVEN sign they start from the 9th sign from it.  (The old code was
    # right here, but the same rule had been duplicated -- and diverged -- in
    # chart.PlanetState.d10_sign; that duplicate now delegates to this table.)
    d10_part = int(degree_in_sign // 3.0)  # 0 to 9
    d10_deg = (degree_in_sign * 10.0) % 30.0
    start_d10 = planet_sign if is_odd_sign else get_sign(planet_sign + 8)
    d10_sign = get_sign(start_d10 + d10_part)
    add_varga("D10", 10, d10_sign, d10_deg)

    # 8. D12 Dwadashamsha (Span 2°30')
    d12_part = int(degree_in_sign // 2.5) # 0 to 11
    d12_deg = (degree_in_sign * 12.0) % 30.0
    d12_sign = get_sign(planet_sign + d12_part)
    add_varga("D12", 12, d12_sign, d12_deg)

    # 9. D16 Shodashamsha (Span 1°52'30" = 1.875°)
    d16_part = int(degree_in_sign // 1.875)
    d16_deg = (degree_in_sign * 16.0) % 30.0
    # Movable (Aries 0, Cancer 3, Libra 6, Cap 9) -> start from Aries (0)
    # Fixed (Taurus 1, Leo 4, Scorpio 7, Aqua 10) -> start from Leo (4)
    # Dual (Gemini 2, Virgo 5, Sag 8, Pisces 11) -> start from Sag (8)
    if planet_sign % 3 == 0:
        d16_sign = get_sign(0 + d16_part)
    elif planet_sign % 3 == 1:
        d16_sign = get_sign(4 + d16_part)
    else:
        d16_sign = get_sign(8 + d16_part)
    add_varga("D16", 16, d16_sign, d16_deg)

    # 10. D20 Vimshamsha (Span 1°30' = 1.5°)
    d20_part = int(degree_in_sign // 1.5)
    d20_deg = (degree_in_sign * 20.0) % 30.0
    if planet_sign % 3 == 0:
        d20_sign = get_sign(0 + d20_part)
    elif planet_sign % 3 == 1:
        d20_sign = get_sign(8 + d20_part)
    else:
        d20_sign = get_sign(4 + d20_part)
    add_varga("D20", 20, d20_sign, d20_deg)

    # 11. D24 Chaturvimshamsha (Span 1°15' = 1.25°)
    d24_part = int(degree_in_sign // 1.25)
    d24_deg = (degree_in_sign * 24.0) % 30.0
    d24_sign = get_sign(4 + d24_part) if is_odd_sign else get_sign(3 + d24_part)
    add_varga("D24", 24, d24_sign, d24_deg)

    # 12. D27 Saptavimshamsha / Bhamsha (Span 1°06'40" = 30/27)
    d27_span = 30.0 / 27.0
    d27_part = int(degree_in_sign // d27_span)
    d27_deg = (degree_in_sign * 27.0) % 30.0
    element = planet_sign % 4
    start_sign = 0 if element == 0 else (3 if element == 1 else (6 if element == 2 else 9))
    d27_sign = get_sign(start_sign + d27_part)
    add_varga("D27", 27, d27_sign, d27_deg)

    # 13. D30 Trishamsha (BPHS 6.19)
    # Odd sign : 0-5 Mars(Aries), 5-10 Saturn(Aquarius), 10-18 Jupiter(Sagittarius),
    #            18-25 Mercury(Gemini), 25-30 Venus(Libra)
    # Even sign: 0-5 Venus(Taurus), 5-12 Mercury(Virgo), 12-20 Jupiter(Pisces),
    #            20-25 Saturn(Capricorn), 25-30 Mars(Scorpio)
    # The boundaries are NOT uniform 6-degree parts -- a very common bug.
    deg = degree_in_sign
    if is_odd_sign:
        if deg < 5.0: d30_sign = 0      # Aries
        elif deg < 10.0: d30_sign = 10  # Aquarius
        elif deg < 18.0: d30_sign = 8   # Sagittarius
        elif deg < 25.0: d30_sign = 2   # Gemini
        else: d30_sign = 6              # Libra
    else:
        if deg < 5.0: d30_sign = 1      # Taurus
        elif deg < 12.0: d30_sign = 5   # Virgo
        elif deg < 20.0: d30_sign = 11  # Pisces
        elif deg < 25.0: d30_sign = 9   # Capricorn
        else: d30_sign = 7              # Scorpio
    # Internal degree is the proportional position inside the 1/30 of the sign,
    # scaled to the full 30° of the divisional sign.
    _d30_spans_odd = ((0.0, 5.0), (5.0, 10.0), (10.0, 18.0), (18.0, 25.0), (25.0, 30.0))
    _d30_spans_even = ((0.0, 5.0), (5.0, 12.0), (12.0, 20.0), (20.0, 25.0), (25.0, 30.0))
    _spans = _d30_spans_odd if is_odd_sign else _d30_spans_even
    _idx = 0 if deg < 5.0 else 1 if deg < _spans[1][1] else 2 if deg < _spans[2][1] else 3 if deg < 25.0 else 4
    _lo, _hi = _spans[_idx]
    d30_deg = (deg - _lo) / (_hi - _lo) * 30.0
    add_varga("D30", 30, d30_sign, d30_deg)

    # 14. D40 Khavedamsha (Span 0°45' = 0.75°)
    d40_part = int(degree_in_sign // 0.75)
    d40_deg = (degree_in_sign * 40.0) % 30.0
    # BPHS 6.21: odd signs count from Aries (0), even signs from Libra (6).
    d40_sign = get_sign(0 + d40_part) if is_odd_sign else get_sign(6 + d40_part)
    add_varga("D40", 40, d40_sign, d40_deg)

    # 15. D45 Akshavedamsha (Span 0°40' = 30/45)
    d45_span = 30.0 / 45.0
    d45_part = int(degree_in_sign // d45_span)
    d45_deg = (degree_in_sign * 45.0) % 30.0
    if planet_sign % 3 == 0:
        d45_sign = get_sign(0 + d45_part)
    elif planet_sign % 3 == 1:
        d45_sign = get_sign(4 + d45_part)
    else:
        d45_sign = get_sign(8 + d45_part)
    add_varga("D45", 45, d45_sign, d45_deg)

    # 16. D60 Shashtyamsha (Span 0°30' = 0.5°)
    # Parashara: Each sign has 60 parts of 30' each.
    # Sign starts from the sign itself!
    d60_part = int(degree_in_sign // 0.5) # 0 to 59
    d60_deg = (degree_in_sign * 60.0) % 30.0
    d60_sign = get_sign(planet_sign + d60_part)
    
    # Deity lookup (BPHS 6.33):
    # Odd signs run the 60 deities forward (part 0 -> #1 ... part 59 -> #60);
    # even signs run them backward (part 0 -> #60 ... part 59 -> #1).
    deity_idx = d60_part if is_odd_sign else (59 - d60_part)
    deity_name, is_benefic = D60_DEITIES[deity_idx]
    deity_full = f"{deity_name} (#{deity_idx + 1})"
    # Sanity: index 0 must be deity #1 and index 59 deity #60.
    assert D60_DEITIES[0][0] == "Ghora" and D60_DEITIES[59][0] == "Chandrarekha"

    add_varga("D60", 60, d60_sign, d60_deg, deity=deity_full, is_ben=is_benefic)

    return vargas

def calculate_vargas(planet_sign: int, degree_in_sign: float) -> Dict[str, int]:
    """Backward compatibility wrapper returning only sign indices."""
    lon = (planet_sign * 30.0) + degree_in_sign
    v_det = calculate_vargas_detailed(lon)
    return {k: v.sign_index for k, v in v_det.items()}


def get_all_vargas_matrix(chart) -> Dict[str, Dict[str, VargaPosition]]:
    """
    Computes a complete matrix for all 16 Shodashvargas mapped as:
    matrix[varga_key][entity_name] -> VargaPosition
    where varga_key is 'D1', 'D2', ..., 'D60' and entity_name is 'Ascendant', 'Sun', etc.
    """
    keys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"]
    matrix: Dict[str, Dict[str, VargaPosition]] = {k: {} for k in keys}
    
    asc_v = calculate_vargas_detailed(chart.ascendant_longitude)
    for k in keys:
        matrix[k]["Ascendant"] = asc_v[k]
        
    for p_name, p in chart.planets.items():
        p_v = calculate_vargas_detailed(p.longitude)
        for k in keys:
            matrix[k][p_name] = p_v[k]
            
    return matrix

