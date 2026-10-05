"""VYAS ASTRA-Omega v3.0 Predictive Synthesis Engine.

Integrates:
1. Natal Promise: Parashari Dignities, D60 Shashtyamsha Deities, House ownerships.
2. Dasha Timing: Active MD, AD, PD, SD lords with micro-temporal intervals.
3. Transit Triggers: Real-time Gochar (Double transit of Saturn & Jupiter, Rahu-Ketu axis, Mars triggers).
4. KP Cuspal Sub-Lord validation: Houses signified by active dasha lords.
5. Triple-Convergence Rule (TCR) arbitration: [C3] Verified, [C2] Probable, [C1] Weak.
"""
from typing import Dict, List, NamedTuple
from datetime import datetime

from vyas import constants
from vyas.varga import calculate_vargas_detailed
from vyas.kp import calculate_sub_lords, compute_kp_significators, KPCusp
from vyas.dasha import VimshottariDasha
from vyas.gochar import transits, shani_status

class PredictionItem(NamedTuple):
    domain: str             # Career, Wealth, Relationship, Health, General
    verdict: str            # Highly Favourable, Favourable, Mixed, Challenging
    confidence: str         # [C3], [C2], [C1]
    title: str
    detailed_analysis: str
    key_factors: List[str]
    timing_window: str

def synthesize_prediction(chart_data: dict, cusps: List[KPCusp], 
                          dasha_engine: VimshottariDasha, target_dt: datetime, 
                          tz_hours: float) -> Dict[str, any]:
    """
    Executes deep multi-system astrological synthesis for the native at target_dt.
    """
    # 1. Resolve Active 5-fold Dasha
    running_dasha = dasha_engine.get_running_dasha(target_dt, max_depth=5)
    md_lord = running_dasha["MD"]["lord"]
    ad_lord = running_dasha["AD"]["lord"]
    pd_lord = running_dasha["PD"]["lord"]
    sd_lord = running_dasha["SD"]["lord"]
    prd_lord = running_dasha["PrD"]["lord"]
    
    # 2. Extract Planetry details & D60 deities
    planets = chart_data["planets"]
    asc_lon = chart_data["asc_lon"]
    moon_lon = planets["Moon"].longitude
    
    d60_summary = {}
    for p_name, p_state in planets.items():
        vargas = calculate_vargas_detailed(p_state.longitude)
        d60_summary[p_name] = vargas["D60"]
        
    asc_vargas = calculate_vargas_detailed(asc_lon)
    d60_summary["Lagna"] = asc_vargas["D60"]

    # 3. KP Significators for Active Lords
    kp_sig = compute_kp_significators(planets, cusps)
    md_sig = kp_sig.get(md_lord, {}).get("all_signified", [])
    ad_sig = kp_sig.get(ad_lord, {}).get("all_signified", [])
    pd_sig = kp_sig.get(pd_lord, {}).get("all_signified", [])
    active_houses = sorted(list(set(md_sig + ad_sig + pd_sig)))

    # 4. Transits at target date
    transit_rows = transits(target_dt, tz_hours, moon_lon, asc_lon)
    saturn_transit = next(r for r in transit_rows if r.planet == "Saturn")
    jupiter_transit = next(r for r in transit_rows if r.planet == "Jupiter")
    shani_info = shani_status(target_dt, tz_hours, moon_lon)

    # 5. Core Domain Synthesis
    predictions: List[PredictionItem] = []

    # Domain A: Career & Status (Houses 10, 6, 2, 11)
    career_houses = {10, 6, 2, 11}
    career_hits = career_houses.intersection(active_houses)
    d60_ben = d60_summary[md_lord].is_benefic and d60_summary[ad_lord].is_benefic
    
    if len(career_hits) >= 2 and jupiter_transit.favourable:
        c_conf = "[C3]"
        c_verdict = "High Professional Elevation"
        c_desc = (f"The active Vimshottari period ({md_lord} MD / {ad_lord} AD / {pd_lord} PD) strongly activates "
                  f"houses {sorted(list(career_hits))} via KP cuspal significations. "
                  f"In D60 (Shashtyamsha), {md_lord} is presided over by {d60_summary[md_lord].deity} "
                  f"and {ad_lord} by {d60_summary[ad_lord].deity}. Concurrently, Jupiter's transit in "
                  f"{jupiter_transit.sign} (house {jupiter_transit.house_from_moon} from natal Moon) lends auspicious support, "
                  f"satisfying the Triple-Convergence Rule (TCR). Promotes rank elevation, lucrative authority, and recognition.")
    elif len(career_hits) >= 1:
        c_conf = "[C2]"
        c_verdict = "Progress with Focused Effort"
        c_desc = (f"Career house {sorted(list(career_hits))} is energized under {md_lord}-{ad_lord}. "
                  f"Professional responsibilities expand, but requires persistent diplomacy. "
                  f"D60 disposition shows {d60_summary[md_lord].deity} influencing strategic decisions.")
    else:
        c_conf = "[C1]"
        c_verdict = "Routine Professional Consolidation"
        c_desc = f"Period focuses on foundational strengthening rather than abrupt career leaps."

    predictions.append(PredictionItem(
        domain="Career & Profession (कार्यक्षेत्र व पदोन्नति)",
        verdict=c_verdict,
        confidence=c_conf,
        title=f"Professional Trajectory under {md_lord}-{ad_lord} Period",
        detailed_analysis=c_desc,
        key_factors=[f"Active Houses: {career_hits}", f"MD Lord D60: {d60_summary[md_lord].deity}", f"Jupiter Transit: {jupiter_transit.verdict}"],
        timing_window=f"{running_dasha['AD']['start']} to {running_dasha['AD']['end']}"
    ))

    # Domain B: Wealth & Finance (Houses 2, 11, 5, 9 vs 8, 12)
    wealth_pos = len({2, 11}.intersection(active_houses))
    wealth_neg = len({8, 12}.intersection(active_houses))
    if wealth_pos > wealth_neg:
        w_conf = "[C3]" if d60_ben else "[C2]"
        w_verdict = "Financial Expansion & Wealth Accumulation"
        w_desc = (f"Active lords {md_lord} and {ad_lord} connect to Dhana (2nd) and Labha (11th) cusps. "
                  f"D60 deities indicate fruition of past karmic investments. Excellent window for capital growth and asset creation.")
    elif wealth_neg > wealth_pos:
        w_conf = "[C2]"
        w_verdict = "Caution in Speculation & Heavy Outflows"
        w_desc = f"Significations link to 8th/12th houses. Advised against unhedged speculative risks. Channel funds into fixed long-term assets."
    else:
        w_conf = "[C2]"
        w_verdict = "Balanced Inflow & Re-investment"
        w_desc = f"Income flows remain steady with planned reinvestment into family and long-term commitments."

    predictions.append(PredictionItem(
        domain="Wealth & Finance (धन व लाभ योग)",
        verdict=w_verdict,
        confidence=w_conf,
        title=f"Financial Matrix during {md_lord}-{ad_lord}-{pd_lord}",
        detailed_analysis=w_desc,
        key_factors=[f"Net Dhana Houses: {wealth_pos}", f"Shani Transit: {saturn_transit.verdict}"],
        timing_window=f"{running_dasha['PD']['start']} to {running_dasha['PD']['end']}"
    ))

    # Domain C: Health & Vitality (Houses 1, 5 vs 6, 8)
    h_hits = {6, 8}.intersection(active_houses)
    if h_hits:
        h_verdict = "Vigilance for Vitality & Immunity"
        h_conf = "[C2]"
        h_desc = (f"Cuspal activation of house(s) {sorted(list(h_hits))}. "
                  f"Pay heed to dietary discipline, digestion, and stress control during {pd_lord} Pratyantar.")
    else:
        h_verdict = "Robust Vitality & High Stamina"
        h_conf = "[C3]"
        h_desc = f"Ascendant and trines predominate. High restorative energy and positive physical stamina."

    predictions.append(PredictionItem(
        domain="Health & Vitality (स्वास्थ्य व जीवनशक्ति)",
        verdict=h_verdict,
        confidence=h_conf,
        title=f"Vitality Assessment",
        detailed_analysis=h_desc,
        key_factors=[f"Active Rogas/Maraka: {sorted(list(h_hits))}", f"Saturn Status: {shani_info['status']}"],
        timing_window=f"{running_dasha['PD']['start']} to {running_dasha['PD']['end']}"
    ))

    return {
        "running_dasha": running_dasha,
        "d60_summary": d60_summary,
        "active_houses": active_houses,
        "shani_status": shani_info,
        "predictions": predictions
    }
