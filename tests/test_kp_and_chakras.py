import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from datetime import datetime, timezone, timedelta
import vyas
from vyas.ephem import planet_positions, ascendant_sidereal
from vyas.chart import Chart, PlanetState
from vyas.varga import get_all_vargas_matrix
from vyas import ashtakavarga as vyas_ashtaka
from vyas import forensic_predictor

def test_full_pipeline():
    dt_local = datetime(1995, 10, 15, 14, 30)
    dt_utc = dt_local - timedelta(hours=5.5)
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    
    # 1. Ephemeris & Chart
    raw_pos = planet_positions(dt_utc)
    asc_lon = ascendant_sidereal(dt_utc, 28.6139, 77.2090)
    planets = {n: PlanetState(n, p.longitude, p.speed) for n, p in raw_pos.items()}
    chart = Chart(asc_lon, planets)
    vargas_matrix = get_all_vargas_matrix(chart)
    
    # 2. Forensic Life Chapters (Chapter_num test)
    dignities = forensic_predictor.analyze_all_planetary_dignities(chart, vargas_matrix)
    bhavas = forensic_predictor.analyze_all_12_bhavas(chart, dignities)
    p_signs = {n: p.sign_index for n, p in chart.planets.items()}
    sav = vyas_ashtaka.compute_ashtakavarga(p_signs, chart.ascendant_sign)['sav']
    forecast = forensic_predictor.compute_overall_life_forecast(chart, dignities, bhavas, sav, vargas_matrix)
    assert len(forecast) == 13, f"Expected 13 chapters, got {len(forecast)}"
    for ch in forecast:
        assert 'chapter_num' in ch, f"Missing chapter_num in {ch}"
        assert 'title_hi' in ch, f"Missing title_hi in {ch}"
    print(f"PASS: 13 Forecast Chapters verified with chapter_num and title_hi.")

    # 3. Jaimini compute_chara_dasha flexible calls
    cd1 = vyas.jaimini.compute_chara_dasha(chart.planets, chart.ascendant_sign, dt_local)
    cd2 = vyas.jaimini.compute_chara_dasha(chart.ascendant_sign, dt_local)
    assert len(cd1) > 0 and len(cd2) > 0, "Chara dasha failed"
    print(f"PASS: Jaimini compute_chara_dasha supported both signatures.")

    # 4. KP Placidus Cusps down to SSSSSL
    cusps = vyas.kp.calculate_placidus_cusps_sidereal(dt_utc, 28.6139, 77.2090)
    assert len(cusps) == 12, "Expected 12 cusps"
    for c in cusps:
        assert c.sub_sub_sub_sub_lord != "", f"Cusp {c.cusp_num} missing SSSSL"
        assert c.sub_sub_sub_sub_sub_lord != "", f"Cusp {c.cusp_num} missing SSSSSL"
    print(f"PASS: KP 12 Placidus Cusps calculated down to SSSSL and SSSSSL.")

    # 5. Planetary KP Table down to SSSSSL
    pls = vyas.kp.calculate_planet_kp_lords(chart.planets, cusps)
    assert len(pls) >= 9, f"Expected 9 planets, got {len(pls)}"
    for pl in pls:
        assert pl.sub_sub_sub_sub_lord != "", f"{pl.planet} missing SSSSL"
        assert pl.sub_sub_sub_sub_sub_lord != "", f"{pl.planet} missing SSSSSL"
    print(f"PASS: 9 Planetary KP Lords calculated down to SSSSL and SSSSSL.")

    # 6. KP 4-Fold Significators (A, B, C, D)
    sigs = vyas.kp.compute_kp_4fold_house_significators(chart.planets, cusps)
    assert "house_significators" in sigs and "planet_significators" in sigs
    for h in range(1, 13):
        hs = sigs["house_significators"][h]
        assert "level_a" in hs and "level_b" in hs and "level_c" in hs and "level_d" in hs
    print(f"PASS: KP 4-Fold Significators (Levels A, B, C, D) computed for all 12 houses & planets.")

    # 7. KP House Promises Verification
    promises = vyas.kp.evaluate_kp_house_promises(cusps, sigs['planet_significators'], chart.planets)
    assert len(promises) == 9, f"Expected 9 promises, got {len(promises)}"
    for p in promises:
        assert p["status"] in ("PROMISED", "MODERATE_DELAY", "RESTRICTED")
        assert len(p["verdict_text"]) > 20
    print(f"PASS: KP House Promises evaluated across 9 life categories.")

    # 8. Active Houses by Dasha
    d_act = vyas.kp.evaluate_active_houses_by_dasha({'mahadasha': 'Jupiter', 'antardasha': 'Saturn', 'pratyantardasha': 'Mercury'}, sigs['planet_significators'])
    assert len(d_act['all_active_houses']) > 0
    assert len(d_act['event_triggers']) > 0
    print(f"PASS: Active Houses by Dasha evaluated.")

    # 9. Sudarshan Chakra (Tri-Wheel Analysis)
    sc = vyas.chakras.compute_sudarshan_chakra(chart)
    assert len(sc.houses) == 12
    assert len(sc.sudarshan_verdict_hi) > 20
    print(f"PASS: Sudarshan Chakra evaluated with {len(sc.power_houses)} power centers.")

    # 10. Kota Chakra, Sarvatobhadra Chakra & Navatara Chakra
    pl_lons = {n: p.longitude for n, p in chart.planets.items()}
    kota = vyas.chakras.compute_kota_chakra(chart.planets['Moon'].longitude, chart.ascendant_longitude, pl_lons)
    assert len(kota.segments) == 4
    sbc = vyas.chakras.compute_sbc_special_points(chart.planets['Moon'].longitude, pl_lons)
    assert len(sbc) == 7
    nt = vyas.chakras.compute_navatara_chakra(chart.planets['Moon'].longitude, pl_lons)
    assert len(nt) == 27
    print(f"PASS: Kota, Sarvatobhadra (28-nakshatra), and Navatara Chakras verified.")

    print("\n==========================================")
    print("🌟 ALL 10 ASTROLOGICAL VERIFICATION TESTS PASSED!")
    print("==========================================")

if __name__ == "__main__":
    test_full_pipeline()
