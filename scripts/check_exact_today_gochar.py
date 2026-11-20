import swisseph as swe
import datetime

now = datetime.datetime.now()
print("Actual System Datetime:", now)

# UTC time
now_utc = datetime.datetime.utcnow()
dec_hr_utc = now_utc.hour + now_utc.minute / 60.0 + now_utc.second / 3600.0

jd = swe.julday(now_utc.year, now_utc.month, now_utc.day, dec_hr_utc)
swe.set_sid_mode(swe.SIDM_LAHIRI)
ayanamsha = swe.get_ayanamsa_ut(jd)
print(f"Lahiri Ayanamsha: {int(ayanamsha)}°{int((ayanamsha%1)*60)}'{int(((ayanamsha%1)*60%1)*60)}\"")

rashi_names = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
planets = {
    'सूर्य (Sun)': swe.SUN,
    'चन्द्र (Moon)': swe.MOON,
    'मंगल (Mars)': swe.MARS,
    'बुध (Mercury)': swe.MERCURY,
    'गुरु (Jupiter)': swe.JUPITER,
    'शुक्र (Venus)': swe.VENUS,
    'शनि (Saturn)': swe.SATURN,
    'राहु (Rahu)': swe.MEAN_NODE
}

nakshatras = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा",
    "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"
]

print("\n--- EXACT REAL-TIME ASTRONOMICAL SKY ---")
for name, pid in planets.items():
    pos, _ = swe.calc_ut(jd, pid, swe.FLG_SIDEREAL)
    deg = pos[0] % 360
    r_idx = int(deg // 30)
    rem_deg = deg % 30
    d = int(rem_deg)
    m = int((rem_deg - d) * 60)
    s = int(((rem_deg - d) * 60 - m) * 60)
    
    nak_idx = int(deg / (360/27))
    pada = int((deg % (360/27)) / (360/108)) + 1
    
    speed = pos[3]
    state = "वक्री" if speed < 0 else "मार्गी"
    if name.startswith('राहु'):
        state = "वक्री (सदा)"
        
    print(f"{name:15}: {rashi_names[r_idx]} {d:02d}°{m:02d}'{s:02d}\" ({nakshatras[nak_idx]} पद {pada}) [{state}]")

# Ketu
rahu_pos, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SIDEREAL)
ketu_deg = (rahu_pos[0] + 180) % 360
k_r_idx = int(ketu_deg // 30)
k_rem_deg = ketu_deg % 30
k_nak_idx = int(ketu_deg / (360/27))
k_pada = int((ketu_deg % (360/27)) / (360/108)) + 1
print(f"{'केतु (Ketu)':15}: {rashi_names[k_r_idx]} {int(k_rem_deg):02d}°{int((k_rem_deg%1)*60):02d}'{int(((k_rem_deg%1)*60%1)*60):02d}\" ({nakshatras[k_nak_idx]} पद {k_pada}) [वक्री (सदा)]")

# Tithi
sun_pos, _ = swe.calc_ut(jd, swe.SUN, swe.FLG_SIDEREAL)
moon_pos, _ = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)
diff = (moon_pos[0] - sun_pos[0]) % 360
tithi_num = int(diff / 12) + 1
tithi_names = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
    "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा",
    "प्रतिपदा (कृष्ण)", "द्वितीया (कृष्ण)", "तृतीया (कृष्ण)", "चतुर्थी (कृष्ण)", "पंचमी (कृष्ण)", "षष्ठी (कृष्ण)", "सप्तमी (कृष्ण)", "अष्टमी (कृष्ण)", "नवमी (कृष्ण)", "दशमी (कृष्ण)",
    "एकादशी (कृष्ण)", "द्वादशी (कृष्ण)", "त्रयोदशी (कृष्ण)", "चतुर्दशी (कृष्ण)", "अमावस्या"
]
paksha = "शुक्ल पक्ष" if tithi_num <= 15 else "कृष्ण पक्ष"
t_name = tithi_names[tithi_num - 1]
print(f"\nसटीक तिथि: {paksha} {t_name} (Tithi {tithi_num})")

