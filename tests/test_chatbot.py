"""Tests for VyasChatbotEngine multi-turn conversational intelligence."""
import pytest
import sys
import os

os.environ["VYAS_TEST_OFFLINE"] = "1"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from vyas.chatbot import vyas_chatbot
from vyas.chart import Chart, PlanetState

@pytest.fixture
def sample_chart_and_dasha():
    planets = {
        'Moon': PlanetState('Moon', 220.0, 13.0),
        'Mars': PlanetState('Mars', 280.0, 0.7),
        'Saturn': PlanetState('Saturn', 200.0, 0.1),
        'Jupiter': PlanetState('Jupiter', 90.0, 0.2),
        'Venus': PlanetState('Venus', 250.0, 1.0),
        'Mercury': PlanetState('Mercury', 260.0, 1.2),
        'Sun': PlanetState('Sun', 240.0, 1.0),
        'Rahu': PlanetState('Rahu', 10.0, -0.05),
        'Ketu': PlanetState('Ketu', 190.0, -0.05)
    }
    chart = Chart(0.0, planets)
    cur_dasha = {
        'MD': {'lord': 'Venus', 'start': '2015-01-01', 'end': '2035-01-01'},
        'AD': {'lord': 'Saturn', 'start': '2024-01-01', 'end': '2027-03-01'},
        'PD': {'lord': 'Mars', 'start': '2024-06-01', 'end': '2024-08-01'}
    }
    birth_info = {'name': 'निखिल व्यास'}
    return chart, cur_dasha, birth_info

def test_career_direct_query(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    reply = vyas_chatbot.consult("करियर, नौकरी एवं पदोन्नति के क्या योग हैं?", chart, cur_dasha, birth_info)
    assert "आजीविका" in reply or "करियर" in reply
    assert "दशम भाव" in reply
    assert "शनि" in reply

def test_career_followup_aage_kya(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    chat_history = [
        {"role": "user", "content": "करियर, नौकरी एवं पदोन्नति के क्या योग हैं?"},
        {"role": "assistant", "content": "पूर्व विश्लेषण..."}
    ]
    reply = vyas_chatbot.consult("aage kya", chart, cur_dasha, birth_info, chat_history=chat_history)
    assert "करियर" in reply or "आजीविका" in reply or "कार्यक्षेत्र" in reply
    assert "2027-03-01" in reply
    assert "बुध" in reply
    assert "उपाय" in reply

def test_ai_engine_live(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    # Test live AI call with force_classical=False
    os.environ.pop("VYAS_TEST_OFFLINE", None)
    reply = vyas_chatbot.consult("आचार्य जी प्रणाम", chart, cur_dasha, birth_info, force_classical=False)
    assert len(reply) > 50
    os.environ["VYAS_TEST_OFFLINE"] = "1"

def test_aspect_query_zero_hallucination(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    reply = vyas_chatbot.consult("mere guru, mangal aur shani teeno lagna ko dekh rahe hai iska kya prabhav padta hai", chart, cur_dasha, birth_info, force_classical=True)
    # Validate exact Parashari lordships
    assert "लग्नेश" in reply or "1H" in reply or "1वें व 8वें" in reply
    assert "मंगल 4वें भाव का नहीं" in reply or "1वें व 8वें भाव का स्वामी" in reply
    assert "शनि 7वें या 12वें भाव के स्वामी नहीं हैं" in reply or "10H" in reply or "कर्मेश" in reply
    assert "गुरु" in reply and "अमृत दृष्टि" in reply
    assert "उपाय" in reply
