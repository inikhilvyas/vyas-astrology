"""Golden-reference regression tests for the VYAS calculation engine.

Every number here is an *external* reference (Swiss Ephemeris / published
almanac values), not a snapshot of our own output: these tests fail when the
engine drifts away from what a world-class astrologer's software prints.

Run:  .venv311/Scripts/python.exe -m pytest tests/test_engine_golden.py -q
"""
import datetime as dt
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vyas import ephem, ashtakavarga, dasha, varga, kp  # noqa: E402
from vyas.chart import Chart, PlanetState  # noqa: E402
from vyas import constants  # noqa: E402

UTC = dt.timezone.utc


# --------------------------------------------------------------------------
# Ayanamsa -- Swiss Ephemeris SE_SIDM_LAHIRI (swetest -sid1)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("jd,expected_deg", [
    (2451545.0, 23.8531709167),   # J2000.0   : 23°51'11.4153"
    (2435553.5, 23.2455251667),   # 1956-03-21: 23°14'43.8906"
])
def test_lahiri_ayanamsa_matches_swiss_ephemeris(jd, expected_deg):
    got = ephem.ayanamsa_deg(jd)
    assert abs(got - expected_deg) * 3600 < 1.0, (
        f"ayanamsa off by {(got - expected_deg) * 3600:.2f}\" at JD {jd}")


def test_ayanamsa_is_monotonic_and_slow():
    """Ayanamsa must grow ~50.3"/yr and never jump."""
    a = ephem.ayanamsa_deg(2451545.0)
    b = ephem.ayanamsa_deg(2451545.0 + 36525.0)
    assert 1.38 < (b - a) < 1.42


# --------------------------------------------------------------------------
# Time handling -- a naive datetime must never be silently reinterpreted
# --------------------------------------------------------------------------
def test_naive_datetime_rejected():
    with pytest.raises(ephem.NaiveDatetimeError):
        ephem.planet_positions(dt.datetime(2000, 1, 1, 12))


def test_local_to_utc_ist():
    assert ephem.local_to_utc(dt.datetime(1990, 5, 15, 14, 35), 5.5) == \
        dt.datetime(1990, 5, 15, 9, 5, tzinfo=UTC)


def test_local_to_utc_west_of_greenwich():
    assert ephem.local_to_utc(dt.datetime(1990, 5, 15, 14, 35), -5.0) == \
        dt.datetime(1990, 5, 15, 19, 35, tzinfo=UTC)


# --------------------------------------------------------------------------
# Planetary positions -- J2000 12:00 UT, Lahiri sidereal
# --------------------------------------------------------------------------
def test_planet_positions_j2000():
    pos = ephem.planet_positions(dt.datetime(2000, 1, 1, 12, tzinfo=UTC))
    # Sun sidereal ≈ 256.51° (tropical 280.36 - ayanamsa 23.85)
    assert abs(pos["Sun"].longitude - 256.516) < 0.05
    assert abs(pos["Moon"].longitude - 199.470) < 0.30
    # Ketu must be exactly opposite Rahu
    assert abs(((pos["Ketu"].longitude - pos["Rahu"].longitude) % 360) - 180) < 1e-9


# --------------------------------------------------------------------------
# Ashtakavarga -- BPHS totals: 48/49/39/54/56/52/39 and SAV = 337
# --------------------------------------------------------------------------
def test_ashtakavarga_totals():
    expected = {"Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
                "Jupiter": 56, "Venus": 52, "Saturn": 39}
    for planet, rules in ashtakavarga.BAV_RULES.items():
        assert sum(len(v) for v in rules.values()) == expected[planet], planet
    assert sum(expected.values()) == 337


def test_sav_sums_to_337():
    signs = {p: (i * 4) % 12 for i, p in enumerate(constants.PLANETS)}
    res = ashtakavarga.compute_ashtakavarga(signs, 0)
    assert sum(res["sav"]) == 337


# --------------------------------------------------------------------------
# Varga -- D30 boundaries (BPHS 6.19) and D60 deity order (BPHS 6.33)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("abs_lon,expected_sign", [
    (2.0, 0),    # Aries 0-5      -> Aries
    (7.0, 10),   # Aries 5-10     -> Aquarius
    (12.0, 8),   # Aries 10-18    -> Sagittarius
    (20.0, 2),   # Aries 18-25    -> Gemini
    (27.0, 6),   # Aries 25-30    -> Libra
    (32.0, 1),   # Taurus 0-5     -> Taurus
    (38.0, 5),   # Taurus 5-12    -> Virgo
    (45.0, 11),  # Taurus 12-20   -> Pisces
    (52.0, 9),   # Taurus 20-25   -> Capricorn
    (57.0, 7),   # Taurus 25-30   -> Scorpio
])
def test_d30_trishamsha(abs_lon, expected_sign):
    assert varga.calculate_vargas_detailed(abs_lon)["D30"].sign_index == expected_sign


def test_d60_deity_runs_backwards_in_even_signs():
    assert varga.calculate_vargas_detailed(0.1)["D60"].deity.startswith("Ghora")
    assert varga.calculate_vargas_detailed(29.9)["D60"].deity.startswith("Chandrarekha")
    assert varga.calculate_vargas_detailed(30.1)["D60"].deity.startswith("Chandrarekha")
    assert varga.calculate_vargas_detailed(59.9)["D60"].deity.startswith("Ghora")


def test_d10_single_source_of_truth():
    for lon in (15.0, 47.5, 95.0, 200.0, 333.0):
        assert PlanetState("Sun", lon, 1.0).d10_sign() == \
            varga.calculate_vargas_detailed(lon)["D10"].sign_index


# --------------------------------------------------------------------------
# Vimshottari -- balance and boundaries
# --------------------------------------------------------------------------
def test_vimshottari_full_balance_at_nakshatra_start():
    d = dasha.VimshottariDasha(0.0, dt.datetime(1990, 5, 15, tzinfo=UTC))
    assert d.birth_lord == "Ketu" and d.balance_str == "Ketu: 7Y 0M 0D"


def test_vimshottari_first_mahadasha_ends_correctly():
    d = dasha.VimshottariDasha(0.0, dt.datetime(1990, 5, 15, tzinfo=UTC))
    md = d.calculate_mahadashas()
    span = (md[0].end_date - md[0].start_date).days
    assert 2556 <= span <= 2558          # 7 Vimshottari years
    assert md[1].lord == "Venus"


def test_vimshottari_antardasha_sums_to_mahadasha():
    d = dasha.VimshottariDasha(77.0, dt.datetime(1990, 5, 15, tzinfo=UTC))
    md = d.calculate_mahadashas()[0]
    subs = d.expand_sub_dashas(md, target_level=2)
    assert len(subs) == 9
    total = sum((s.end_date - s.start_date).total_seconds() for s in subs)
    assert abs(total - (md.end_date - md.start_date).total_seconds()) < 1.0


# --------------------------------------------------------------------------
# KP Placidus cusps -- structural invariants that must hold at any latitude
# --------------------------------------------------------------------------
@pytest.mark.parametrize("lat", [0.0, 13.0, 28.6, 45.0, 60.0])
def test_placidus_cusp_structure(lat):
    cs = kp.calculate_placidus_cusps_sidereal(dt.datetime(2000, 1, 1, 12, tzinfo=UTC), lat, 0.0)
    longs = [c.longitude for c in cs]
    # Opposite cusps are exactly 180° apart
    for i in range(6):
        assert abs(((longs[i + 6] - longs[i]) % 360) - 180) < 1e-6
    # Cusps advance monotonically through the zodiac
    for i in range(11):
        assert 0 < (longs[i + 1] - longs[i]) % 360 < 90
    # Cusp 1 == Ascendant
    asc = ephem.ascendant_sidereal(dt.datetime(2000, 1, 1, 12, tzinfo=UTC), lat, 0.0)
    assert abs(((longs[0] - asc + 180) % 360) - 180) < 1e-6


# --------------------------------------------------------------------------
# Full chart smoke test -- one published birth data set
# --------------------------------------------------------------------------
def test_end_to_end_chart():
    utc = ephem.local_to_utc(dt.datetime(1990, 5, 15, 14, 35), 5.5)
    pos = ephem.planet_positions(utc)
    asc = ephem.ascendant_sidereal(utc, 26.9124, 75.7873)   # Jaipur
    chart = Chart(asc, {n: PlanetState(n, p.longitude, p.speed) for n, p in pos.items()})
    assert chart.ascendant_sign == 5            # Virgo
    moon = chart.planets["Moon"]
    assert moon.nakshatra_name == "Uttara Ashadha" and moon.pada == 2
    av = ashtakavarga.compute_ashtakavarga(
        {n: p.sign_index for n, p in chart.planets.items()}, chart.ascendant_sign)
    assert sum(av["sav"]) == 337
