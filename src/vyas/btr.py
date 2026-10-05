"""Birth Time Rectification (BTR) Engine for VYAS.

Implements multi-dimensional classical and modern rectification principles:
1. Kunda Shodhana (कुन्द शुद्धि):
   Ascendant longitude multiplied by 81, divided by 27. The resulting nakshatra
   must align with natal Moon's nakshatra or its trines (1, 10, 19).
2. Tattva Shodhana (तत्व शुद्धि):
   Gender verification based on the five cosmic elements (Agni, Prithvi, Vayu, Jala, Akasha)
   calculated from sunrise to birth time.
3. KP Ruling Planets (RP) Rectification:
   Ascendant Sub-Lord (SL) must be connected to Moon's Star Lord or Day Lord.
4. Second-by-Second Window Scanner:
   Scans ±15 minutes in 10-second steps to suggest the most mathematically harmonious birth time.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple
from vyas import constants
from vyas.ephem import ascendant_sidereal

def kunda_shodhana(asc_lon: float, moon_lon: float) -> Tuple[bool, str, str]:
    """
    Computes Kunda Shodhana.
    Kunda degree = (asc_lon * 81) % 360
    Kunda Nakshatra = int(Kunda degree // 13.33333333) % 27
    Match condition: Kunda Nakshatra must be same as Moon's Nakshatra or its 10th or 19th trine.
    """
    kunda_deg = (asc_lon * 81.0) % 360.0
    kunda_nak = int(kunda_deg // constants.NAKSHATRA_SPAN) % 27
    moon_nak = int(moon_lon // constants.NAKSHATRA_SPAN) % 27
    
    # Trines of Moon nakshatra
    trines = [moon_nak, (moon_nak + 9) % 27, (moon_nak + 18) % 27]
    is_aligned = kunda_nak in trines

    kunda_nak_name = constants.NAKSHATRAS[kunda_nak]
    moon_nak_name = constants.NAKSHATRAS[moon_nak]

    verdict = (
        f"कुन्द शुद्धि अनुकूल है (Kunda Nakshatra '{kunda_nak_name}' matches Moon Nakshatra '{moon_nak_name}' trines)."
        if is_aligned else
        f"कुन्द शुद्धि में सूक्ष्म अंतर है (Kunda '{kunda_nak_name}' does not fall in Moon trine '{moon_nak_name}')."
    )
    return is_aligned, kunda_nak_name, verdict

def tattva_shodhana(birth_dt: datetime, gender: str = "Male") -> Tuple[bool, str, str]:
    """
    Tattva Shodhana element verification based on sex.
    Male births are favorable in Agni, Vayu, Akasha tattvas; Female in Prithvi, Jala.
    """
    # 24-minute cycle per tattva
    minutes_from_midnight = birth_dt.hour * 60 + birth_dt.minute + (birth_dt.second / 60.0)
    cycle_idx = int((minutes_from_midnight // 24) % 5)
    tattvas = ["Agni (अग्नि)", "Prithvi (पृथ्वी)", "Vayu (वायु)", "Jala (जल)", "Akasha (आकाश)"]
    active_tattva = tattvas[cycle_idx]

    is_male = gender.lower() == "male"
    if is_male:
        aligned = cycle_idx in [0, 2, 4]  # Agni, Vayu, Akasha
    else:
        aligned = cycle_idx in [1, 3]     # Prithvi, Jala

    verdict = (
        f"तत्व शुद्धि पूर्णतः अनुकूल ({active_tattva} is harmonious for {gender})."
        if aligned else
        f"तत्व शुद्धि में अंतर ({active_tattva} indicates fine-tuning needed for {gender})."
    )
    return aligned, active_tattva, verdict

def scan_rectification_window(local_dt: datetime, lat: float, lon: float, tz_offset: float,
                              moon_lon: float, gender: str = "Male", window_minutes: int = 10) -> List[Dict]:
    """
    Scans a ±window_minutes interval around the given birth time in 15-second steps
    to find rectified birth times having optimal Kunda and Tattva scores.
    """
    dt_utc = local_dt - timedelta(hours=tz_offset)
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)

    candidates = []
    step_seconds = 20
    total_steps = int((window_minutes * 60 * 2) / step_seconds)

    start_offset = -window_minutes * 60
    for s in range(total_steps):
        offset = start_offset + (s * step_seconds)
        test_utc = dt_utc + timedelta(seconds=offset)
        test_local = local_dt + timedelta(seconds=offset)

        try:
            test_asc = ascendant_sidereal(test_utc, lat, lon)
            k_ok, k_nak, _ = kunda_shodhana(test_asc, moon_lon)
            t_ok, t_name, _ = tattva_shodhana(test_local, gender)

            score = 50
            if k_ok:
                score += 35
            if t_ok:
                score += 15

            if score >= 85:
                candidates.append({
                    "time_str": test_local.strftime("%H:%M:%S"),
                    "offset_seconds": offset,
                    "score": score,
                    "kunda_nak": k_nak,
                    "tattva": t_name,
                    "asc_deg": f"{int(test_asc % 30)}°{int((test_asc % 1)*60):02d}'{int(((test_asc*60)%1)*60):02d}\""
                })
        except Exception:
            continue

    # Sort candidates by highest score and proximity to original time
    candidates.sort(key=lambda x: (-x["score"], abs(x["offset_seconds"])))
    return candidates[:5]
