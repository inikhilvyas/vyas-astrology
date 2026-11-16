import math

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
RASHI_LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
NAK_LORDS = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"] * 3
DASHA_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
TOTAL_YEARS = 120

def get_kp_sublord(longitude):
    # longitude: 0 to 360
    lon = longitude % 360.0
    nak_span = 360.0 / 27.0 # 13.3333 degrees = 13°20'
    nak_idx = int(lon / nak_span)
    nak_lord = NAK_LORDS[nak_idx]
    
    # offset inside nakshatra (0 to 13.3333)
    offset_in_nak = lon - (nak_idx * nak_span)
    
    # sublord order starts with the nakshatra lord
    sub_order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    start_idx = sub_order.index(nak_lord)
    
    accum = 0.0
    for i in range(9):
        curr_sub = sub_order[(start_idx + i) % 9]
        span = (DASHA_YEARS[curr_sub] / 120.0) * nak_span
        accum += span
        if offset_in_nak <= accum or i == 8:
            return curr_sub
    return "Mercury"

print("Test get_kp_sublord at 0.0:", get_kp_sublord(0.0))
print("Test get_kp_sublord at 23.45 (Aries):", get_kp_sublord(23.45))
print("Test get_kp_sublord at 230.5 (Scorpio):", get_kp_sublord(230.5))
