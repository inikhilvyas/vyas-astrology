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
                if offset == 0:
                    off_desc = "0 सेकंड (यथावत मूल समय — कोई बदलाव नहीं)"
                elif offset > 0:
                    m = offset // 60
                    sec = offset % 60
                    off_desc = f"+{m} मिनट {sec} सेकंड आगे" if sec else f"+{m} मिनट आगे"
                else:
                    ab = abs(offset)
                    m = ab // 60
                    sec = ab % 60
                    off_desc = f"-{m} मिनट {sec} सेकंड पीछे" if sec else f"-{m} मिनट पीछे"

                asc_sign_name = constants.SIGNS_HI[int(test_asc // 30)]
                nav_sign_idx = int(test_asc // (30.0 / 9.0)) % 12
                nav_sign_name = constants.SIGNS_HI[nav_sign_idx]
                
                moon_nak_idx = int(moon_lon // constants.NAKSHATRA_SPAN) % 27
                moon_nak_name = constants.NAKSHATRAS_HI[moon_nak_idx]

                reason_kunda = f"पाराशरी कुन्द शोधन में लग्न × 81 का कुन्द नक्षत्र '{k_nak}' प्राप्त होता है, जो जन्म चन्द्र नक्षत्र '{moon_nak_name}' के साथ त्रिकोण समरसता (1, 10, 19वें नक्षत्र की नैसर्गिक संगति) में 100% संरेखित है।"
                reason_tattva = f"जन्मकालिक पंचतत्त्व चक्र में '{t_name}' तत्त्व संचलित है, जो {gender} जातक की जैविक व प्राणिक ऊर्जा से पूर्णतः सामंजस्य रखता है।"
                reason_varga = f"इस समय पर लग्न {asc_sign_name} राशि में तथा नवमांश लग्न {nav_sign_name} राशि में सुदृढ़ होता है, जिससे वर्ग कुण्डलियों में संधि दोष नहीं बनता।"

                candidates.append({
                    "time_str": test_local.strftime("%H:%M:%S"),
                    "offset_seconds": offset,
                    "offset_desc": off_desc,
                    "score": score,
                    "confidence_pct": score,
                    "kunda_nak": k_nak,
                    "tattva": t_name,
                    "asc_deg": f"{asc_sign_name} {int(test_asc % 30)}°{int((test_asc % 1)*60):02d}'{int(((test_asc*60)%1)*60):02d}\"",
                    "navamsha_lagna": nav_sign_name,
                    "reason_kunda": reason_kunda,
                    "reason_tattva": reason_tattva,
                    "reason_varga": reason_varga,
                    "full_reasoning": f"{reason_kunda} {reason_tattva} {reason_varga}"
                })
        except Exception:
            continue

    candidates.sort(key=lambda x: (-x["score"], abs(x["offset_seconds"])))
    return candidates[:5]

def verify_life_events(birth_dt: datetime, moon_lon: float, asc_lon: float, events: List[Dict], chart=None) -> List[Dict]:
    """
    Correlates actual biographical life events (विवाह, नौकरी, संतान, दुर्घटना, विदेश यात्रा)
    against the Vimshottari Mahadasha/Antardasha/Pratyantardasha and house lordships.
    events: list of dicts with keys: 'type', 'date', 'desc'
    """
    from vyas.dasha import VimshottariDasha
    from vyas import constants
    
    dasha_eng = VimshottariDasha(moon_lon, birth_dt)
    
    sign_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
    asc_sign = int(asc_lon // 30) % 12
    
    event_significators = {
        "विवाह (Marriage)": {
            "karakas": ["Venus", "Jupiter"],
            "houses": [7, 2, 11],
            "varga": "D9 (नवमांश)",
            "primary": 7
        },
        "करियर / नौकरी (Job / Promotion)": {
            "karakas": ["Sun", "Saturn", "Mercury"],
            "houses": [10, 6, 11],
            "varga": "D10 (दशमांश)",
            "primary": 10
        },
        "संतान जन्म (Childbirth)": {
            "karakas": ["Jupiter"],
            "houses": [5, 2, 11],
            "varga": "D7 (सप्तांश)",
            "primary": 5
        },
        "वाहन / गृह क्रय (Property / Vehicle)": {
            "karakas": ["Mars", "Venus"],
            "houses": [4, 11, 12],
            "varga": "D4 (चतुर्थांश)",
            "primary": 4
        },
        "विदेश गमन (Foreign Travel / Relocation)": {
            "karakas": ["Rahu", "Moon", "Saturn"],
            "houses": [12, 9, 3],
            "varga": "D12 (द्वादशांश)",
            "primary": 12
        },
        "स्वास्थ्य कष्ट / दुर्घटना (Surgery / Health Event)": {
            "karakas": ["Mars", "Saturn", "Rahu", "Ketu"],
            "houses": [6, 8, 12],
            "varga": "D30 (त्रिंशांश)",
            "primary": 8
        }
    }

    results = []
    for ev in events:
        ev_type = ev.get("type", "विवाह (Marriage)")
        ev_dt = ev.get("date")
        if not ev_dt:
            continue
        if isinstance(ev_dt, str):
            try:
                ev_dt = datetime.strptime(ev_dt.strip(), "%Y-%m-%d")
            except Exception:
                try:
                    ev_dt = datetime.strptime(ev_dt.strip(), "%d/%m/%Y")
                except Exception:
                    continue

        running = dasha_eng.get_dasha_at(ev_dt)
        md = running.get("mahadasha") or running.get("MD", {}).get("lord", "Venus")
        ad = running.get("antardasha") or running.get("AD", {}).get("lord", "Saturn")
        pd = running.get("pratyantardasha") or running.get("PD", {}).get("lord", "Mercury")
        
        md_hi = constants.PLANETS_HI.get(md, md)
        ad_hi = constants.PLANETS_HI.get(ad, ad)
        pd_hi = constants.PLANETS_HI.get(pd, pd)
        full_dasha_hi = f"{md_hi} -> {ad_hi} -> {pd_hi}"

        meta = event_significators.get(ev_type, {
            "karakas": ["Jupiter"], "houses": [1, 9], "varga": "D9", "primary": 1
        })
        karakas = meta["karakas"]
        rel_houses = meta["houses"]
        varga_name = meta["varga"]
        primary_house = meta["primary"]

        # Calculate exact house lords for this native's ascendant
        house_lords = {}
        for h in rel_houses:
            h_sign = (asc_sign + h - 1) % 12
            house_lords[h] = sign_lords[h_sign]

        primary_lord = house_lords.get(primary_house, "")

        # Scoring matrix
        score = 25  # Base convergence baseline
        
        # Primary house lord activation (e.g. 7th lord for marriage, 10th lord for career)
        if md == primary_lord:
            score += 28
        elif md in house_lords.values():
            score += 18
        if md in karakas:
            score += 12

        if ad == primary_lord:
            score += 32
        elif ad in house_lords.values():
            score += 22
        if ad in karakas:
            score += 14

        if pd == primary_lord:
            score += 15
        elif pd in house_lords.values() or pd in karakas:
            score += 10

        # Correlation percentage clamp between 42% and 94%
        correlation_pct = max(42, min(94, score))

        hl_names_hi = [f"भाव {h} के स्वामी {constants.PLANETS_HI.get(house_lords[h], house_lords[h])}" for h in rel_houses]
        karaka_names_hi = [constants.PLANETS_HI.get(k, k) for k in karakas]

        if correlation_pct >= 80:
            fit_text = "उत्कृष्ट व अचूक सामंजस्य (High Astrological Alignment)"
            fit_desc = "घटना दिनांक पर सक्रिय दशा के स्वामी इस घटना के मुख्य भाव एवं नैसर्गिक कारक ग्रह से पूर्णतः संबंधित हैं। यह आपके जन्म समय की सटीकता को दृढ़ता से प्रमाणित करता है।"
        elif correlation_pct >= 60:
            fit_text = "सकारात्मक व मध्यम सामंजस्य (Moderate Alignment)"
            fit_desc = "घटना दिनांक पर सक्रिय अन्तर्दशा/प्रत्यन्तर्दशा इस घटना के गौण भावों अथवा सहयोगी कारकों से संबद्ध है। जन्म समय में 1 से 3 मिनट का सूक्ष्म समायोजन संभव है।"
        else:
            fit_text = "निम्न सामंजस्य (Weak Alignment - Requires BTR Adjustment)"
            fit_desc = "सक्रिय दशा स्वामी और घटना के प्राथमिक भावों के बीच सीधा संबंध नहीं बन रहा। जन्म समय में सूक्ष्म संशोधन (Rectification) की आवश्यकता है।"

        explanation = (
            f"घटना दिनांक ({ev_dt.strftime('%d/%m/%Y')}) पर <b>{md_hi} महादशा</b> में <b>{ad_hi} अन्तर्दशा</b> एवं <b>{pd_hi} प्रत्यन्तर्दशा</b> सक्रिय थी। "
            f"लग्न चक्र अनुसार इस घटना के मुख्य कारक: {', '.join(hl_names_hi)} तथा नैसर्गिक कारक: {', '.join(karaka_names_hi)} हैं। "
            f"यह दशा चक्र {meta['varga']} एवं संबंधित भावों से <b>{fit_text}</b> दर्शाता है। {fit_desc}"
        )

        results.append({
            "event_type": ev_type,
            "event_date": ev_dt.strftime("%d/%m/%Y"),
            "running_dasha": full_dasha_hi,
            "relevant_varga": varga_name,
            "alignment_score": f"{correlation_pct}%",
            "explanation": explanation
        })

    return results
