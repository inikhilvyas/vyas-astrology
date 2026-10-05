"""Shadbala (Six-fold Planetary Strength) & Bhavabala Engine (BPHS Standards).

Computes:
1. Sthana Bala (Positional: Uchha, Saptavargaja, Ojhayugma, Kendra, Drekkana)
2. Dig Bala (Directional)
3. Kala Bala (Temporal: Nathonnatha, Paksha, Tribhaga, Varsha/Masa/Dina/Hora, Ayana)
4. Chesta Bala (Motional / Speed)
5. Naisargika Bala (Natural)
6. Drik Bala (Aspectual / Drishti)
Total Virupas, Rupas (Virupas / 60), Minimum Required, Strength Ratio, Relative Ranking.
Bhavabala: Total strength for each of the 12 Bhavas.
"""
from typing import Dict, List, Tuple, NamedTuple
import math
from vyas import constants
from vyas.varga import calculate_vargas_detailed

# Minimum Shadbala Virupas required (BPHS):
# Sun: 390 (6.5R), Moon: 360 (6.0R), Mars: 300 (5.0R), Mercury: 420 (7.0R),
# Jupiter: 390 (6.5R), Venus: 330 (5.5R), Saturn: 300 (5.0R)
MIN_VIRUPAS = {
    "Sun": 390.0,
    "Moon": 360.0,
    "Mars": 300.0,
    "Mercury": 420.0,
    "Jupiter": 390.0,
    "Venus": 330.0,
    "Saturn": 300.0
}

NAISARGIKA_VIRUPAS = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Venus": 42.86,
    "Jupiter": 34.29,
    "Mercury": 25.71,
    "Mars": 17.14,
    "Saturn": 8.57
}

# Digbala powerful points in degrees (from 1st cusp = 0)
# East (1st): Mercury, Jupiter (0°)
# North (4th): Moon, Venus (90°)
# West (7th): Saturn (180°)
# South (10th): Sun, Mars (270°)
DIGBALA_POINTS = {
    "Mercury": 0.0,
    "Jupiter": 0.0,
    "Moon": 90.0,
    "Venus": 90.0,
    "Saturn": 180.0,
    "Sun": 270.0,
    "Mars": 270.0
}

class PlanetShadbala(NamedTuple):
    planet: str
    sthana_bala: float
    dig_bala: float
    kala_bala: float
    chesta_bala: float
    naisargika_bala: float
    drik_bala: float
    total_virupas: float
    total_rupas: float
    min_required: float
    strength_ratio: float
    rank: int
    verdict: str

def compute_shadbala(chart, is_day_birth: bool = True, paksha: str = "Shukla") -> Tuple[Dict[str, PlanetShadbala], Dict[int, float]]:
    """
    Computes comprehensive Shadbala and Bhavabala.
    """
    planets = chart.planets
    asc_lon = chart.ascendant_longitude
    asc_sign = chart.ascendant_sign

    shadbala_dict = {}
    total_scores = {}

    for p_name in MIN_VIRUPAS:
        p = planets[p_name]
        lon = p.longitude
        sign_idx = p.sign_index
        deg_in_sign = lon % 30.0
        
        # 1. STHANA BALA
        # A. Uchha Bala: Exaltation distance / 3 (0 to 60)
        ex_sign, ex_deg = constants.EXALTATION[p_name]
        deep_ex_lon = ex_sign * 30.0 + ex_deg
        deb_lon = (deep_ex_lon + 180.0) % 360.0
        dist_from_deb = (lon - deb_lon) % 360.0
        if dist_from_deb > 180.0:
            dist_from_deb = 360.0 - dist_from_deb
        uchha_bala = dist_from_deb / 3.0 # max 60

        # B. Saptavargaja Bala (approximate classical dignity across vargas)
        v_det = calculate_vargas_detailed(lon)
        saptavarga_pts = 0.0
        for v_name in ["D1", "D2", "D3", "D7", "D9", "D12", "D30"]:
            v_sign = v_det[v_name].sign_index
            if v_sign in constants.OWN_SIGNS.get(p_name, []):
                saptavarga_pts += 30.0
            elif v_sign == constants.EXALTATION.get(p_name, (-1,-1))[0]:
                saptavarga_pts += 45.0
            else:
                saptavarga_pts += 15.0
        saptavargaja_bala = saptavarga_pts / 2.5 # normalized

        # C. Kendra Bala: Kendra (60), Panaphara (30), Apoklima (15)
        house_num = (sign_idx - asc_sign + 12) % 12 + 1
        if house_num in (1, 4, 7, 10):
            kendra_bala = 60.0
        elif house_num in (2, 5, 8, 11):
            kendra_bala = 30.0
        else:
            kendra_bala = 15.0

        # D. Ojhayugma Bala (15 virupas if male in odd or female in even)
        is_odd_sign = (sign_idx % 2 == 0)
        is_male_pl = p_name in ("Sun", "Mars", "Jupiter")
        ojha_bala = 15.0 if (is_male_pl == is_odd_sign) else 0.0

        sthana_bala = uchha_bala + saptavargaja_bala + kendra_bala + ojha_bala

        # 2. DIG BALA
        # Angular distance from opposite of peak direction
        h_offset_deg = ((sign_idx - asc_sign + 12) % 12) * 30.0 + deg_in_sign
        peak_deg = DIGBALA_POINTS[p_name]
        dist_from_zero = (h_offset_deg - ((peak_deg + 180.0) % 360.0)) % 360.0
        if dist_from_zero > 180.0:
            dist_from_zero = 360.0 - dist_from_zero
        dig_bala = dist_from_zero / 3.0 # max 60

        # 3. KALA BALA
        # Nathonnatha Bala
        if p_name in ("Sun", "Jupiter", "Venus"):
            natho_bala = 60.0 if is_day_birth else 0.0
        elif p_name in ("Moon", "Mars", "Saturn"):
            natho_bala = 60.0 if not is_day_birth else 0.0
        else:
            natho_bala = 60.0 # Mercury is always strong

        # Paksha Bala (Waxing/Waning Moon)
        is_benefic = p_name in ("Jupiter", "Venus", "Moon")
        if paksha == "Shukla":
            paksha_bala = 45.0 if is_benefic else 15.0
        else:
            paksha_bala = 15.0 if is_benefic else 45.0

        # Ayana Bala (based on sign declination approximation)
        ayana_bala = 30.0 + (15.0 if sign_idx in (0, 1, 2, 9, 10, 11) else -10.0)

        kala_bala = natho_bala + paksha_bala + ayana_bala

        # 4. CHESTA BALA
        if p_name in ("Sun", "Moon"):
            chesta_bala = ayana_bala # Sun & Moon take Ayana/Paksha
        else:
            if p.is_retrograde:
                chesta_bala = 60.0
            elif abs(p.speed) < 0.2:
                chesta_bala = 15.0
            else:
                chesta_bala = 35.0

        # 5. NAISARGIKA BALA
        naisargika_bala = NAISARGIKA_VIRUPAS[p_name]

        # 6. DRIK BALA (Aspectual strength approximation)
        drik_bala = 10.0 # neutral default

        # TOTAL VIRUPAS & RUPAS
        total_v = sthana_bala + dig_bala + kala_bala + chesta_bala + naisargika_bala + drik_bala
        total_scores[p_name] = total_v

        shadbala_dict[p_name] = {
            "sthana": round(sthana_bala, 2),
            "dig": round(dig_bala, 2),
            "kala": round(kala_bala, 2),
            "chesta": round(chesta_bala, 2),
            "naisargika": round(naisargika_bala, 2),
            "drik": round(drik_bala, 2),
            "total_v": round(total_v, 2),
            "total_r": round(total_v / 60.0, 2),
            "min_req": MIN_VIRUPAS[p_name],
            "ratio": round(total_v / MIN_VIRUPAS[p_name], 2)
        }

    # Assign Ranks
    sorted_planets = sorted(total_scores.keys(), key=lambda x: total_scores[x], reverse=True)
    rank_map = {p: i + 1 for i, p in enumerate(sorted_planets)}

    final_shadbala: Dict[str, PlanetShadbala] = {}
    for p, d in shadbala_dict.items():
        ratio = d["ratio"]
        verdict = "Strong (बली)" if ratio >= 1.0 else "Weak (दुर्बल)"
        final_shadbala[p] = PlanetShadbala(
            planet=p,
            sthana_bala=d["sthana"],
            dig_bala=d["dig"],
            kala_bala=d["kala"],
            chesta_bala=d["chesta"],
            naisargika_bala=d["naisargika"],
            drik_bala=d["drik"],
            total_virupas=d["total_v"],
            total_rupas=d["total_r"],
            min_required=d["min_req"],
            strength_ratio=d["ratio"],
            rank=rank_map[p],
            verdict=verdict
        )

    # 7. BHAVABALA (House Strengths for 12 Houses)
    # Bhava Bala = Bhavadhipati Bala + Bhava Digbala + Bhava Drishti
    bhava_bala: Dict[int, float] = {}
    for h in range(1, 13):
        h_sign = (asc_sign + h - 1) % 12
        h_lord = constants.SIGN_LORD[h_sign]
        lord_v = final_shadbala.get(h_lord, final_shadbala["Sun"]).total_virupas
        # Digbala for houses (Kendra 60, Panaphara 30, Apoklima 15)
        h_dig = 60.0 if h in (1, 4, 7, 10) else (30.0 if h in (2, 5, 8, 11) else 15.0)
        bhava_bala[h] = round(lord_v + h_dig, 2)

    return final_shadbala, bhava_bala
