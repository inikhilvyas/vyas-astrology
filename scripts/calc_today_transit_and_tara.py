import swisseph as swe
from datetime import datetime

swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Current time: 2026-11-18 17:55 IST -> UTC: 12:25 UTC
jd_now = swe.julday(2026, 11, 18, 12.0 + 25/60.0)

# Calculate Moon position now
moon_pos, _ = swe.calc_ut(jd_now, swe.MOON, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
moon_deg = moon_pos[0]

NAKSHATRAS = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "अश्लेषा",
    "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"
]

transit_nak_idx = int(moon_deg / (13 + 1/3)) % 27
transit_nak_name = NAKSHATRAS[transit_nak_idx]

# Birth Nakshatra for Nikhil Vyas: Anuradha (idx 16)
birth_nak_idx = 16 # Anuradha (0-indexed)

# Navatara Count
tara_count = ((transit_nak_idx - birth_nak_idx) % 27) + 1
tara_rem = ((tara_count - 1) % 9) + 1

TARAS = {
    1: ("जन्म", "Janma", "शारीरिक श्रम, मानसिक सतर्कता"),
    2: ("सम्पत्", "Sampat", "धन, लाभ, आर्थिक अवसर"),
    3: ("विपत्", "Vipat", "अचानक बाधाएं, व्यय, सावधानी"),
    4: ("क्षेम", "Kshema", "कल्याण, पारिवारिक सुख, सफलता"),
    5: ("प्रत्यक्", "Pratyak", "विरोध, कार्य में अड़चनें"),
    6: ("साधक", "Sadhak", "कार्य सिद्धि, शोध, सफलता"),
    7: ("निधन/वध", "Naidhana", "अति सावधानी, विवाद टालें"),
    8: ("मित्र", "Mitra", "मित्र सहयोग, सौहार्द"),
    9: ("परम मित्र", "Param Mitra", "अति शुभ, उच्च सहयोग")
}

tara_info = TARAS[tara_rem]

print(f"Date: 18 Nov 2026")
print(f"Transit Moon Degree: {moon_deg:.4f}°")
print(f"Transit Moon Nakshatra: {transit_nak_name} (#{transit_nak_idx+1})")
print(f"Birth Nakshatra: Anuradha (#{birth_nak_idx+1})")
print(f"Tara Count: {tara_count}, Mod 9: {tara_rem}")
print(f"Authentic Navatara: {tara_info[0]} ({tara_info[1]}) - {tara_info[2]}")

# Check day of week
dt = datetime(2026, 11, 18)
print(f"Day of week: {dt.strftime('%A')} (weekday={dt.weekday()})")
