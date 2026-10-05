"""Fixed reference data for the VYAS engine (Parashari / Vimshottari conventions)."""
from __future__ import annotations

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला",
            "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]

PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
PLANETS_HI = {"Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
              "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि",
              "Rahu": "राहु", "Ketu": "केतु"}

# Nakshatra order from Ashwini; lords repeat in Vimshottari order.
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana",
    "Dhanishta", "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati",
]
NAKSHATRAS_HI = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु",
    "पुष्य", "आश्लेषा", "मघा", "पूर्वा फाल्गुनी", "उत्तरा फाल्गुनी", "हस्त",
    "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा",
    "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्व भाद्रपद",
    "उत्तर भाद्रपद", "रेवती",
]

VIMSHOTTARI_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
                     "Jupiter", "Saturn", "Mercury"]
VIMSHOTTARI_YEARS = {"Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
                     "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17}
assert sum(VIMSHOTTARI_YEARS.values()) == 120

NAKSHATRA_SPAN = 360.0 / 27          # 13°20'
PADA_SPAN = NAKSHATRA_SPAN / 4       # 3°20'

SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus",
             "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

# (exaltation sign index, exact degree), debilitation is the opposite sign.
EXALTATION = {"Sun": (0, 10), "Moon": (1, 3), "Mars": (9, 28), "Mercury": (5, 15),
              "Jupiter": (3, 5), "Venus": (11, 27), "Saturn": (6, 20)}
OWN_SIGNS = {"Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
             "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10]}
# Moolatrikona: (sign index, from degree, to degree)
MOOLATRIKONA = {"Sun": (4, 0, 20), "Moon": (1, 3, 30), "Mars": (0, 0, 12),
                "Mercury": (5, 15, 20), "Jupiter": (8, 0, 10),
                "Venus": (6, 0, 15), "Saturn": (10, 0, 20)}

# Naisargika (natural) friendship - Parashara.
FRIENDS = {"Sun": {"Moon", "Mars", "Jupiter"}, "Moon": {"Sun", "Mercury"},
           "Mars": {"Sun", "Moon", "Jupiter"}, "Mercury": {"Sun", "Venus"},
           "Jupiter": {"Sun", "Moon", "Mars"}, "Venus": {"Mercury", "Saturn"},
           "Saturn": {"Mercury", "Venus"}}
ENEMIES = {"Sun": {"Venus", "Saturn"}, "Moon": set(),
           "Mars": {"Mercury"}, "Mercury": {"Moon"},
           "Jupiter": {"Mercury", "Venus"}, "Venus": {"Sun", "Moon"},
           "Saturn": {"Sun", "Moon", "Mars"}}

# Combustion orbs in degrees: (direct, retrograde). Moon/Mars/Merc/Jup/Ven/Sat.
COMBUST_ORB = {"Moon": (12, 12), "Mars": (17, 17), "Mercury": (14, 12),
               "Jupiter": (11, 11), "Venus": (10, 8), "Saturn": (15, 15)}

# Graha (sign) aspects, as house offsets counted from the planet (1 = same sign).
ASPECTS = {"Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7],
           "Mars": [4, 7, 8], "Jupiter": [5, 7, 9], "Saturn": [3, 7, 10],
           "Rahu": [5, 7, 9], "Ketu": [5, 7, 9]}

YEAR_DAYS = 365.25   # Vimshottari year convention (documented, fixed)
