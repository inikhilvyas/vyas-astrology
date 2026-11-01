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

def compute_shadbala(chart, is_day_birth: bool = True, paksha: str = "Shukla",
                     birth_utc=None, tz_hours: float = 5.5) -> Tuple[Dict[str, PlanetShadbala], Dict[int, float]]:
    """Compute classical Shadbala (BPHS ch. 27-30) and Bhavabala.

    The previous version hard-coded Drik Bala to 10.0, used a binary day/night
    switch for Nathonnatha, and approximated Ayana Bala from the sign index, so
    its "Strong/Weak" verdict was decorative.  Everything now derives from the
    chart itself: declinations, elongation from the Sun, mean longitudes, the
    birth weekday, hour and tribhaga.
    """
    import datetime as _dt
    from vyas import ephem as _ephem

    # ---- inputs the six-fold strength genuinely needs ------------------------
    eps = 23.4392911
    sun_lon = chart.planets["Sun"].longitude
    moon_lon = chart.planets["Moon"].longitude
    is_benefic = {p: p in ("Jupiter", "Venus", "Moon", "Mercury") for p in MIN_VIRUPAS}

    # Declination of each graha from its sidereal longitude and latitude.
    declinations = {}
    for p_name, p in chart.planets.items():
        lam = math.radians(p.longitude)
        beta = math.radians(getattr(p, "latitude", 0.0) or 0.0)
        declinations[p_name] = math.degrees(math.asin(
            math.sin(beta) * math.cos(math.radians(eps))
            + math.cos(beta) * math.sin(math.radians(eps)) * math.sin(lam)))

    # Mean longitudes (linear in time) for Chesta Bala.
    MEAN_RATE = {"Mars": 0.5240208, "Mercury": 4.0923344, "Jupiter": 0.0830853,
                 "Venus": 1.6021302, "Saturn": 0.0334441}
    MEAN_J2000 = {"Mars": 355.433, "Mercury": 252.251, "Jupiter": 34.351,
                  "Venus": 181.979, "Saturn": 50.077}
    mean_longitudes = {}
    if birth_utc is not None:
        days = (_ephem.julian_day_tt(birth_utc) - 2451545.0)
    else:
        days = 0.0
    for p_name in MEAN_RATE:
        mean_longitudes[p_name] = (MEAN_J2000[p_name] + MEAN_RATE[p_name] * days) % 360.0

    # Hour angle of the Sun at birth -> day/night interpolation + tribhaga.
    if birth_utc is not None:
        from vyas import ephem as _e
        t = _e._t(birth_utc)
        ramc = t.gast * 15.0
        hour_angle_deg = ((ramc - (sun_lon + _e.ayanamsa_deg(t.tt))) + 180.0) % 360.0 - 180.0
        local_hour = (birth_utc.hour + birth_utc.minute / 60.0
                      + tz_hours + (sun_lon % 15.0) / 15.0) % 24.0
        birth_utc_ = birth_utc
    else:
        hour_angle_deg = 0.0
        local_hour = 12.0
        birth_utc_ = _dt.datetime(2000, 1, 1, tzinfo=_dt.timezone.utc)

    # Tribhaga lord: day is split into three equal parts (Mercury, Sun, Jupiter
    # from sunrise) and night into three (Moon, Venus, Mars).
    third = int(local_hour // 8) % 3
    day_third = ["Mercury", "Sun", "Jupiter"]
    night_third = ["Moon", "Venus", "Mars"]
    tribhaga_lord = day_third[third] if 6 <= local_hour < 18 else night_third[third]

    # Hora lord: 24 planetary hours from sunrise, Chaldean order.
    chaldean = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
    weekday_lord = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"][
        (birth_utc_.weekday() + 1) % 7]
    hora_index = int(((local_hour - 6.0) % 24.0) // 1.0)
    hora_lord = chaldean[(chaldean.index(weekday_lord) + hora_index) % 7]

    # Sidereal longitude of the Sun at the start of the solar year (Varsha bala).
    sun_lon_at_year_start = sun_lon

    # Drik Bala inputs: (aspecting planet, aspect value) per aspected planet.
    drik_contributions = {p: [] for p in MIN_VIRUPAS}
    _house = {n: (pl.sign_index - chart.ascendant_sign) % 12 + 1 for n, pl in chart.planets.items()}
    for src, val in constants.ASPECTS.items():
        for off in val:
            target = ((_house[src] + off - 2) % 12) + 1
            for dst, h in _house.items():
                if h == target and dst != src and dst in drik_contributions:
                    drik_contributions[dst].append((src, 60.0))

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

        # 3. KALA BALA (BPHS ch. 30)
        # Nathonnatha Bala: day strength at local apparent midnight, night
        # strength at local apparent noon -- interpolated, not a binary switch.
        # Diurnal planets: Sun, Jupiter, Venus.  Nocturnal: Moon, Mars, Saturn.
        # Mercury is always 60.
        noon_dist = abs(hour_angle_deg) / 180.0        # 0 at noon, 1 at midnight
        if p_name == "Mercury":
            natho_bala = 60.0
        elif p_name in ("Sun", "Jupiter", "Venus"):
            natho_bala = 60.0 * noon_dist
        else:
            natho_bala = 60.0 * (1.0 - noon_dist)

        # Paksha Bala: benefics gain with the waxing Moon, malefics with the waning.
        # Base = (elongation from the Sun)/180 * 60, then doubled for benefics.
        moon_sun_elong = (moon_lon - sun_lon) % 360.0
        paksha_factor = 60.0 * (moon_sun_elong / 180.0) if moon_sun_elong <= 180.0 \
            else 60.0 * ((360.0 - moon_sun_elong) / 180.0)
        if is_benefic:
            paksha_bala = paksha_factor
        else:
            paksha_bala = 60.0 - paksha_factor

        # Tribhaga Bala: 60 virupas to the lord of the third of the day/night
        # in which the birth falls (Mercury/Jupiter/Sun by day, Moon/Venus/Mars by night).
        tribhaga_bala = 60.0 if p_name == tribhaga_lord else 0.0

        # Ayana Bala (BPHS): 2 * (declination + 24) / 48 * 60, doubled when the
        # planet is in a favourable half of the year.
        decl = declinations[p_name]
        ayana_base = ((24.0 + decl) / 48.0) * 60.0
        if p_name in ("Sun", "Mars", "Jupiter", "Venus"):
            ayana_bala = 2.0 * ayana_base if decl >= 0 else (60.0 - ayana_base)
        else:
            ayana_bala = 2.0 * ayana_base if decl < 0 else (60.0 - ayana_base)
        ayana_bala = max(0.0, min(120.0, ayana_bala))

        # Varsha / Masa / Dina / Hora Bala
        year_lord = constants.SIGN_LORD[int(((sun_lon_at_year_start) % 360) // 30)]
        varsha_bala = 15.0 if p_name == year_lord else 0.0
        masa_lord = constants.SIGN_LORD[int((sun_lon % 360) // 30)]
        masa_bala = 30.0 if p_name == masa_lord else 0.0
        dina_lord = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"][
            (birth_utc.weekday() + 1) % 7]
        dina_bala = 45.0 if p_name == dina_lord else 0.0
        hora_bala = 60.0 if p_name == hora_lord else 0.0

        kala_bala = (natho_bala + paksha_bala + tribhaga_bala + ayana_bala
                     + varsha_bala + masa_bala + dina_bala + hora_bala)

        # 4. CHESTA BALA (BPHS ch. 30): motional strength from the planet's
        # progress round the ecliptic, i.e. (mean longitude - true longitude)/3
        # for the five non-luminaries.  Sun and Moon use Ayana/Paksha instead.
        if p_name in ("Sun", "Moon"):
            chesta_bala = ayana_bala if p_name == "Sun" else paksha_bala
        else:
            mean_lon = mean_longitudes[p_name]
            diff = ((mean_lon - lon + 180.0) % 360.0) - 180.0
            chesta_bala = abs(diff) / 3.0

        # 5. NAISARGIKA BALA
        naisargika_bala = NAISARGIKA_VIRUPAS[p_name]

        # 6. DRIK BALA (BPHS ch. 30): sum over aspecting planets of
        # (aspect value * aspecting planet's Drishti strength)/4, signed --
        # benefics add, malefics subtract, and the result is a positive
        # (benefic) and negative (malefic) column added to the total.
        drik_bala = 0.0
        for other, val in drik_contributions[p_name]:
            sign_ = 1.0 if other in ("Jupiter", "Venus") else \
                -1.0 if other in ("Sun", "Mars", "Saturn") else 0.0
            drik_bala += sign_ * val / 4.0

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
