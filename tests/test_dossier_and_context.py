"""Tests for Normalized Chart Context and Planet & House Dossiers (Phase B & C)."""
import datetime as dt
from datetime import timezone
import pytest

from vyas.chart import Chart, PlanetState
from vyas.dossier import build_normalized_chart_context, PlanetDossier, HouseDossier

@pytest.fixture
def sample_chart_context():
    # Nikhil Vyas Birth Chart Sample
    # Aries Lagna (23°8'), Sun 7°43' Scorpio, Moon 14°38' Scorpio (Debilitated),
    # Mars 12°20' Capricorn (Exalted 10H), Saturn 27°1' Libra (Exalted 7H)
    planets = {
        "Sun": PlanetState("Sun", 217.72, 1.0),
        "Moon": PlanetState("Moon", 224.64, 13.2),
        "Mars": PlanetState("Mars", 282.34, 0.7),
        "Mercury": PlanetState("Mercury", 239.28, 1.3),
        "Jupiter": PlanetState("Jupiter", 259.56, 0.2),
        "Venus": PlanetState("Venus", 257.81, 1.1),
        "Saturn": PlanetState("Saturn", 207.03, 0.05),
        "Rahu": PlanetState("Rahu", 33.54, -0.05),
        "Ketu": PlanetState("Ketu", 213.54, -0.05),
    }
    chart = Chart(ascendant_longitude=23.14, planets=planets)
    birth_utc = dt.datetime(1990, 5, 15, 9, 5, tzinfo=timezone.utc)
    ctx = build_normalized_chart_context(chart, birth_utc, lat=26.9124, lon=75.7873, birth_time_confidence="High")
    return ctx


def test_normalized_chart_context_separation(sample_chart_context):
    ctx = sample_chart_context
    # 1. Whole Sign separation
    assert len(ctx.whole_sign_houses) == 12
    # 2. KP Placidus Cusps separation
    assert len(ctx.kp_cusps) == 12
    # 3. Quality Flags
    assert ctx.quality_flags["calculation_valid"] is True
    assert ctx.quality_flags["engine"].startswith("Swiss Ephemeris")


def test_planet_dossier_dignity_and_strength(sample_chart_context):
    ctx = sample_chart_context
    mars_d = ctx.planet_dossiers["Mars"]
    sat_d = ctx.planet_dossiers["Saturn"]
    moon_d = ctx.planet_dossiers["Moon"]

    # Mars in Capricorn is Exalted
    assert "Exalted" in mars_d.dignity
    assert mars_d.whole_sign_house == 10
    assert mars_d.is_shadbala_strong is True

    # Saturn in Libra is Exalted
    assert "Exalted" in sat_d.dignity
    assert sat_d.whole_sign_house == 7

    # Moon in Scorpio is Debilitated
    assert "Debilitated" in moon_d.dignity
    assert moon_d.whole_sign_house == 8


def test_house_dossier_and_contradiction_detection(sample_chart_context):
    ctx = sample_chart_context
    # 10th House (Career - Capricorn): Ruled by Saturn (Exalted in 7H)
    h10 = ctx.house_dossiers[10]
    assert h10.lord == "Saturn"
    assert "Exalted" in h10.lord_dignity
    assert "Mars" in h10.whole_sign_occupants

    # 8th House: Contains Sun, Moon, Ketu
    h8 = ctx.house_dossiers[8]
    assert "Moon" in h8.whole_sign_occupants
    assert "Sun" in h8.whole_sign_occupants
    assert h8.bhavabala_virupas > 0.0


def test_aspects_cast_and_received(sample_chart_context):
    ctx = sample_chart_context
    mars_d = ctx.planet_dossiers["Mars"]
    # Mars in 10H casts aspect on 1H (4th aspect), 4H (7th aspect), 5H (8th aspect)
    assert 1 in mars_d.aspects_cast_to_houses
    assert 4 in mars_d.aspects_cast_to_houses
    assert 5 in mars_d.aspects_cast_to_houses

