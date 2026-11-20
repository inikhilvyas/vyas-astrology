"""Tests for EvidenceLedger and Predictive Synthesis (Phase D & E)."""
import datetime as dt
from datetime import timezone
import pytest

from vyas.chart import Chart, PlanetState
from vyas.dasha import VimshottariDasha
from vyas.kp import calculate_placidus_cusps_sidereal
from vyas.evidence_ledger import EvidenceLedger, DomainJudgment
from vyas.predictive_engine import synthesize_prediction


def test_evidence_ledger_deduplication():
    ledger = EvidenceLedger("Career Testing")
    # Add two rules depending on the same underlying factor 'Mars_Exalted'
    ledger.add_evidence(
        source_system="Parashari",
        subject="Mars",
        raw_fact="Mars in Capricorn 12°",
        interpretation="Ruchaka Yoga in 10H",
        polarity="Support",
        weight=1.5,
        dependency_group="Mars_Exalted",
        rule_id="RUCHAKA_YOGA"
    )
    ledger.add_evidence(
        source_system="KP",
        subject="Mars",
        raw_fact="Mars star lord of 10H",
        interpretation="Signifies 10H",
        polarity="Support",
        weight=1.0,
        dependency_group="Mars_Exalted",
        rule_id="KP_MARS_10H"
    )

    # Evaluate convergence
    judg = ledger.evaluate_convergence(
        is_natal_promised=True,
        dasha_aligned=True,
        varga_confirmed=True,
        transit_triggered=True
    )
    # Total positive score should be capped at max weight (1.5), NOT 1.5 + 1.0 = 2.5!
    assert judg.evidence_score == 1.5
    assert judg.tier == "C3"


def test_evidence_ledger_contradiction_downgrade():
    ledger = EvidenceLedger("Career Obstruction")
    ledger.add_evidence(
        source_system="Parashari",
        subject="10th Lord",
        raw_fact="10th Lord Debilitated in 6H",
        interpretation="Weak career foundation",
        polarity="Obstruction",
        weight=1.8,
        dependency_group="10th_Lord_Affliction",
        rule_id="DEB_10H_LORD"
    )
    judg = ledger.evaluate_convergence(
        is_natal_promised=False,
        dasha_aligned=True,
        varga_confirmed=False,
        transit_triggered=True
    )
    # Because natal promise is false and strong obstruction exists, C3 must be DENIED!
    assert judg.tier != "C3"
    assert judg.tier == "C1"
    assert len(judg.contradictions) > 0


def test_synthesize_prediction_full_flow():
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
    chart_data = {
        "asc_lon": 23.14,
        "planets": planets
    }
    birth_utc = dt.datetime(1990, 5, 15, 9, 5, tzinfo=timezone.utc)
    dasha_eng = VimshottariDasha(planets["Moon"].longitude, birth_utc)
    cusps = calculate_placidus_cusps_sidereal(birth_utc, 26.9124, 75.7873)

    target_dt = dt.datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
    result = synthesize_prediction(chart_data, cusps, dasha_eng, target_dt, 5.5)

    assert "predictions" in result
    assert len(result["predictions"]) >= 3
    # Check that predictions have valid C1/C2/C3 confidence badges
    for pred in result["predictions"]:
        assert any(c in pred.confidence for c in ("[C1]", "[C2]", "[C3]"))
        assert len(pred.detailed_analysis) > 30
        assert len(pred.key_factors) > 0

