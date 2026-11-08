"""Unit tests for Daivagya Master Astrology Engine (daivagya_engine.py)."""
import pytest
from datetime import datetime
from vyas import ephem
from vyas.chart import Chart, PlanetState
from vyas.daivagya_engine import (
    generate_kundli_data_lock,
    compute_triple_convergence_predictions,
    generate_daivagya_remedy,
    compute_sudarshana_tri_layer
)


def create_sample_chart():
    # Pali, 1984-11-23 16:51:00
    birth = {
        "name": "Nikhil Vyas",
        "city": "Pali, Rajasthan",
        "local": datetime(1984, 11, 23, 16, 51, 0),
        "lat": 25.58,
        "lon": 73.38,
        "tz": 5.5
    }
    utc = ephem.local_to_utc(birth["local"], birth["tz"])
    pos = ephem.planet_positions(utc)
    asc = ephem.ascendant_sidereal(utc, birth["lat"], birth["lon"])
    chart = Chart(asc, {n: PlanetState(n, p.longitude, p.speed) for n, p in pos.items()})
    return chart, birth


def test_kundli_data_lock():
    chart, birth = create_sample_chart()
    kdlt = generate_kundli_data_lock(chart, birth, dasha_info="Jupiter-Saturn")
    assert kdlt.native_name == "Nikhil Vyas"
    assert "°" in kdlt.lagna_dms
    assert len(kdlt.rows) >= 9
    for row in kdlt.rows:
        assert row.planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        assert "°" in row.degree_dms
        assert 1 <= row.bhava <= 12


def test_triple_convergence_predictions():
    chart, birth = create_sample_chart()
    forecasts = compute_triple_convergence_predictions(chart, "Jupiter-Saturn")
    assert len(forecasts) >= 5
    for f in forecasts:
        assert f.convergence_tier in ["C3", "C2", "C1", "CN"]
        assert len(f.primary_houses) > 0
        assert "BTR" in f.falsification_trigger or "शोधन" in f.falsification_trigger


def test_daivagya_remedies_all_planets():
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        rem = generate_daivagya_remedy(p)
        assert rem.planet == p
        assert len(rem.beej_mantra) > 0
        assert rem.mantra_count > 0
        assert len(rem.tier1_cognitive_shift_hi) > 0
        assert len(rem.tier2_tantra_behavior_hi) > 0
        assert len(rem.yantra_name_hi) > 0
        assert len(rem.daan_items_hi) > 0


def test_sudarshana_tri_layer():
    chart, birth = create_sample_chart()
    sl = compute_sudarshana_tri_layer(chart, target_house=1)
    assert sl.house_num == 1
    assert "लग्न से भाव 1" in sl.deha_lagna_status_hi
    assert "चन्द्र लग्न से भाव 1" in sl.mana_chandra_status_hi
    assert "सूर्य लग्न से भाव 1" in sl.atma_surya_status_hi
