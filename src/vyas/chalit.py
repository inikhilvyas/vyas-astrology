"""Sripati Bhava Chalit & Panchadha Maitri Chakra Engine.

Computes:
1. Sripati Bhava Chalit:
   - Bhava Madhya (Mid-point / Peak of each house 1 to 12)
   - Bhava Arambha (Beginning point of each house 1 to 12)
   - Bhava Anta (Ending point of each house 1 to 12)
   - Shifted Planets: Planets whose Bhava Chalit house differs from their D1 Whole Sign house.
2. Panchadha Maitri Chakra:
   - Naisargika (Natural) Friendship
   - Tatkalika (Temporal) Friendship based on 2, 3, 4, 10, 11, 12 positions
   - Compound Panchadha (Adhi-Mitra, Mitra, Sama, Shatru, Adhi-Shatru)
"""
from typing import Dict, List, Tuple, NamedTuple
from vyas import constants

class BhavaCuspDetail(NamedTuple):
    bhava_num: int
    arambha_sign: str
    arambha_dms: str
    arambha_deg: float
    madhya_sign: str
    madhya_dms: str
    madhya_deg: float
    anta_sign: str
    anta_dms: str
    anta_deg: float
    planets_in_bhava: List[str]

def format_dms(deg_val: float) -> str:
    deg = deg_val % 30.0
    d = int(deg)
    rem = (deg - d) * 60.0
    m = int(rem)
    s = int(round((rem - m) * 60.0))
    if s >= 60:
        m += 1
        s = 0
    if m >= 60:
        d += 1
        m = 0
    return f"{d:02d}°{m:02d}'{s:02d}\""

def compute_sripati_chalit(asc_lon: float, mc_lon: float, planet_lons: Dict[str, float]) -> List[BhavaCuspDetail]:
    """
    Computes classical Sripati Bhava Chalit table.
    """
    asc = asc_lon % 360.0
    mc = mc_lon % 360.0
    desc = (asc + 180.0) % 360.0
    ic = (mc + 180.0) % 360.0

    # Sripati Bhava Madhyas:
    # Quadrant 1 (MC to Ascendant): Arc = (Asc - MC) % 360
    arc1 = (asc - mc) % 360.0
    step1 = arc1 / 3.0
    bm_10 = mc
    bm_11 = (mc + step1) % 360.0
    bm_12 = (mc + 2.0 * step1) % 360.0
    bm_1 = asc

    # Quadrant 2 (Ascendant to IC): Arc = (IC - Asc) % 360
    arc2 = (ic - asc) % 360.0
    step2 = arc2 / 3.0
    bm_2 = (asc + step2) % 360.0
    bm_3 = (asc + 2.0 * step2) % 360.0
    bm_4 = ic

    # Quadrant 3 & 4: Opposite points (+180°)
    bm_5 = (bm_11 + 180.0) % 360.0
    bm_6 = (bm_12 + 180.0) % 360.0
    bm_7 = desc
    bm_8 = (bm_2 + 180.0) % 360.0
    bm_9 = (bm_3 + 180.0) % 360.0

    madhyas = [bm_1, bm_2, bm_3, bm_4, bm_5, bm_6, bm_7, bm_8, bm_9, bm_10, bm_11, bm_12]

    # Bhava Arambhas: Midpoints between previous Bhava Madhya and current Bhava Madhya
    # For Bhava i, arambha = midpoint(madhya[i-1], madhya[i])
    arambhas = []
    antas = []
    for i in range(12):
        prev_m = madhyas[(i - 1) % 12]
        curr_m = madhyas[i]
        next_m = madhyas[(i + 1) % 12]

        # Arc from prev to curr
        arc_prev = (curr_m - prev_m) % 360.0
        arambha = (prev_m + arc_prev / 2.0) % 360.0
        arambhas.append(arambha)

        # Arc from curr to next
        arc_next = (next_m - curr_m) % 360.0
        anta = (curr_m + arc_next / 2.0) % 360.0
        antas.append(anta)

    # Distribute planets into Chalit Bhavas
    bhava_planets: Dict[int, List[str]] = {h: [] for h in range(1, 13)}
    for p_name, p_lon in planet_lons.items():
        pl = p_lon % 360.0
        # Check which arambha-anta interval pl falls into
        placed = False
        for i in range(12):
            ar = arambhas[i]
            an = antas[i]
            span = (an - ar) % 360.0
            pos = (pl - ar) % 360.0
            if pos < span:
                bhava_planets[i + 1].append(p_name)
                placed = True
                break
        if not placed:
            bhava_planets[1].append(p_name)

    results = []
    for i in range(12):
        ar = arambhas[i]
        bm = madhyas[i]
        an = antas[i]
        results.append(BhavaCuspDetail(
            bhava_num=i + 1,
            arambha_sign=constants.SIGNS[int(ar // 30.0) % 12],
            arambha_dms=format_dms(ar),
            arambha_deg=ar,
            madhya_sign=constants.SIGNS[int(bm // 30.0) % 12],
            madhya_dms=format_dms(bm),
            madhya_deg=bm,
            anta_sign=constants.SIGNS[int(an // 30.0) % 12],
            anta_dms=format_dms(an),
            anta_deg=an,
            planets_in_bhava=bhava_planets[i + 1]
        ))
    return results

# --- PANCHADHA MAITRI CHAKRA ---
def compute_panchadha_maitri(planet_signs: Dict[str, int]) -> Dict[str, Dict[str, str]]:
    """
    Computes 5-fold Compound Friendship (Panchadha Maitri) between all 7 classical planets.
    Categories:
    - Adhi-Mitra (Great Friend)
    - Mitra (Friend)
    - Sama (Neutral)
    - Shatru (Enemy)
    - Adhi-Shatru (Bitter Enemy)
    """
    planets_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    matrix: Dict[str, Dict[str, str]] = {p: {} for p in planets_7}

    for p1 in planets_7:
        s1 = planet_signs[p1]
        for p2 in planets_7:
            if p1 == p2:
                matrix[p1][p2] = "Self (स्व)"
                continue

            # 1. Naisargika (Natural) score: Friend (+1), Enemy (-1), Equal (0)
            if p2 in constants.FRIENDS.get(p1, set()):
                n_score = 1
            elif p2 in constants.ENEMIES.get(p1, set()):
                n_score = -1
            else:
                n_score = 0

            # 2. Tatkalika (Temporal) score:
            # Planets in 2, 3, 4, 10, 11, 12 from p1 are temporary friends (+1); others enemies (-1).
            s2 = planet_signs[p2]
            dist_house = (s2 - s1 + 12) % 12 + 1
            t_score = 1 if dist_house in (2, 3, 4, 10, 11, 12) else -1

            # 3. Compound Panchadha Score
            total_score = n_score + t_score # ranges from -2 to +2
            if total_score == 2:
                pancha = "Adhi-Mitra (अतिमित्र)"
            elif total_score == 1:
                pancha = "Mitra (मित्र)"
            elif total_score == 0:
                pancha = "Sama (सम)"
            elif total_score == -1:
                pancha = "Shatru (शत्रु)"
            else:
                pancha = "Adhi-Shatru (अतिशत्रु)"

            matrix[p1][p2] = pancha

    return matrix
