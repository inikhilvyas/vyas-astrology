"""Tests for VyasChatbotEngine multi-turn conversational intelligence."""
import pytest
import sys
import os

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

def test_exam_followup_aage_kya(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    chat_history = [
        {"role": "user", "content": "न्यायिक सेवा (RHJS) परीक्षा में क्या संभावना है?"},
        {"role": "assistant", "content": "पूर्व विश्लेषण..."}
    ]
    reply = vyas_chatbot.consult("आगे क्या", chart, cur_dasha, birth_info, chat_history=chat_history)
    assert "न्यायिक" in reply or "परीक्षा" in reply
    assert "2027-03-01" in reply

def test_standalone_aage_kya(sample_chart_and_dasha):
    chart, cur_dasha, birth_info = sample_chart_and_dasha
    reply = vyas_chatbot.consult("आगे क्या होगा", chart, cur_dasha, birth_info)
    assert "आगामी समय" in reply or "भाग्योदय" in reply
    assert "2027-03-01" in reply
