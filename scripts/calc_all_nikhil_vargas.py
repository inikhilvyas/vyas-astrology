import swisseph as swe

# Pali coordinates
LAT = 25.7700
LON = 73.3200

# 23 Nov 1984, 16:51 IST -> 11:21 UTC
# JD calculation
swe.set_ephe_path('')
jd_utc = swe.julday(1984, 11, 23, 11.0 + 21.0/60.0)

# Lahiri Ayanamsha
swe.set_sid_mode(swe.SIDM_LAHIRI)
ayan = swe.get_ayanamsa_ut(jd_utc)

# Lagna
res, ascmc = swe.houses_ex(jd_utc, LAT, LON, b'P', swe.FLG_SIDEREAL)
asc_deg = ascmc[0]

planets = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mars': swe.MARS,
    'Mercury': swe.MERCURY,
    'Jupiter': swe.JUPITER,
    'Venus': swe.VENUS,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE
}

p_lons = {}
for name, pid in planets.items():
    xx, r = swe.calc_ut(jd_utc, pid, swe.FLG_SIDEREAL)
    p_lons[name] = xx[0]

p_lons['Ketu'] = (p_lons['Rahu'] + 180.0) % 360.0

SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"]
PLANET_HI = {
    'Sun': 'सूर्य', 'Moon': 'चन्द्र', 'Mars': 'मंगल', 'Mercury': 'बुध',
    'Jupiter': 'गुरु', 'Venus': 'शुक्र', 'Saturn': 'शनि', 'Rahu': 'राहु', 'Ketu': 'केतु'
}

def calc_varga_sign(lon, divisor):
    s = int(lon // 30)
    deg = lon % 30.0
    is_odd = (s % 2 == 0)
    
    if divisor == 1:
        return s
    elif divisor == 2: # Hora
        return 4 if (deg < 15.0 if is_odd else deg >= 15.0) else 3
    elif divisor == 3: # Drekkana
        part = int(deg // 10.0)
        return (s + part * 4) % 12
    elif divisor == 4: # Chaturthamsha
        part = int(deg // 7.5)
        return (s + part * 3) % 12
    elif divisor == 7: # Saptamsha
        part = int(deg // (30.0 / 7.0))
        return (s + part) % 12 if is_odd else (s + 6 + part) % 12
    elif divisor == 9: # Navamsha
        part = int(deg // (30.0 / 9.0))
        # Fiery: Aries (0), Earthy: Capricorn (9), Airy: Libra (6), Watery: Cancer (3)
        element = s % 4
        start = [0, 9, 6, 3][element]
        return (start + part) % 12
    elif divisor == 10: # Dashamsha
        part = int(deg // 3.0)
        start = s if is_odd else (s + 8) % 12
        return (start + part) % 12
    elif divisor == 12: # Dwadashamsha
        part = int(deg // 2.5)
        return (s + part) % 12
    elif divisor == 16: # Shodashamsha
        part = int(deg // 1.875)
        # Movable: Aries(0), Fixed: Leo(4), Dual: Sagittarius(8)
        mfd = s % 3
        start = [0, 4, 8][mfd]
        return (start + part) % 12
    elif divisor == 20: # Vimshamsha
        part = int(deg // 1.5)
        mfd = s % 3
        start = [0, 8, 4][mfd]
        return (start + part) % 12
    elif divisor == 24: # Chaturvimshamsha
        part = int(deg // 1.25)
        start = 4 if is_odd else 3
        return (start + part) % 12
    elif divisor == 27: # Saptavimshamsha / Bhamsha
        part = int(deg // (30.0 / 27.0))
        element = s % 4
        start = [0, 3, 6, 9][element]
        return (start + part) % 12
    elif divisor == 30: # Trimshamsha
        # Odd: Mars(0-5:Aries), Sat(5-10:Aquarius), Jup(10-18:Sagittarius), Mer(18-25:Gemini), Ven(25-30:Libra)
        # Even: Ven(0-5:Taurus), Mer(5-12:Virgo), Jup(12-20:Pisces), Sat(20-25:Capricorn), Mars(25-30:Scorpio)
        if is_odd:
            if deg < 5: return 0
            elif deg < 10: return 10
            elif deg < 18: return 8
            elif deg < 25: return 2
            else: return 6
        else:
            if deg < 5: return 1
            elif deg < 12: return 5
            elif deg < 20: return 11
            elif deg < 25: return 9
            else: return 7
    elif divisor == 40: # Khavedamsha
        part = int(deg // 0.75)
        start = 0 if is_odd else 6
        return (start + part) % 12
    elif divisor == 45: # Akshavedamsha
        part = int(deg // (30.0 / 45.0))
        mfd = s % 3
        start = [0, 4, 8][mfd]
        return (start + part) % 12
    elif divisor == 60: # Shashtiamsha
        part = int(deg // 0.5)
        return (s + part) % 12
    return s

vargas = {
    'D1': 1, 'D2': 2, 'D3': 3, 'D4': 4, 'D7': 7, 'D9': 9, 'D10': 10,
    'D12': 12, 'D16': 16, 'D20': 20, 'D24': 24, 'D27': 27, 'D30': 30,
    'D40': 40, 'D45': 45, 'D60': 60
}

TITLES = {
    'D1': "D-1 लग्न कुण्डली • जन्मपत्रिका (शारीरिक स्वरूप, आरोग्य व स्वभाव)",
    'D2': "D-2 होरा चक्र (धन, संचित संपत्ति व समृद्धि)",
    'D3': "D-3 द्रेष्काण चक्र (पराक्रम, सहोदर व ऊर्जा)",
    'D4': "D-4 चतुर्थांश चक्र (भूमि, भवन, वाहन व अचल संपत्ति)",
    'D7': "D-7 सप्तांश चक्र (संतान सुख, वंश वृद्धि व पूर्व पुण्य)",
    'D9': "D-9 नवमांश कुण्डली (धर्म, जीवनसाथी व आंतरिक आत्मिक शक्ति)",
    'D10': "D-10 दशमांश कुण्डली (करियर, पद, प्रतिष्ठा व सामाजिक सम्मान)",
    'D12': "D-12 द्वादशांश चक्र (माता-पिता, पितृ ऋण व वंशज)",
    'D16': "D-16 षोडशांश चक्र (वाहन सुख, मानसिक आनंद व सुख-साधन)",
    'D20': "D-20 विंशांश चक्र (आध्यात्मिक साधना, उपासना व सिद्धि)",
    'D24': "D-24 चतुर्विंशांश चक्र (उच्च विद्या, ज्ञान व शोध कौशल)",
    'D27': "D-27 सप्तविंशांश चक्र (शारीरिक बल, सामर्थ्य व दुर्बलता)",
    'D30': "D-30 त्रिंशांश चक्र (अरिष्ट, व्याधि व प्रारब्ध कष्ट)",
    'D40': "D-40 खवेदांश चक्र (शुभ-अशुभ फल व कुल प्रारब्ध)",
    'D45': "D-45 अक्षवेदांश चक्र (चारित्रिक शुचिता व सूक्ष्म चेतना)",
    'D60': "D-60 षष्ट्यंश चक्र (पूर्व जन्म प्रारब्ध व सर्वातिशायी फल)"
}

out_data = {}

for vk, div in vargas.items():
    asc_v_sign = calc_varga_sign(asc_deg, div)
    houses = {str(h): [str(((asc_v_sign + h - 1) % 12) + 1)] for h in range(1, 13)}
    planet_details = []
    
    for p_name, p_lon in p_lons.items():
        p_v_sign = calc_varga_sign(p_lon, div)
        h_num = ((p_v_sign - asc_v_sign + 12) % 12) + 1
        d_in_v = (p_lon * div) % 30.0
        d_str = f"{int(d_in_v):02d}°{int((d_in_v % 1)*60):02d}'"
        
        houses[str(h_num)].append(f"{PLANET_HI[p_name]} {d_str}")
        planet_details.append({
            'planet': PLANET_HI[p_name],
            'sign': SIGNS_HI[p_v_sign],
            'house': h_num,
            'degree': d_str + '"',
            'deity': ""
        })
        
    out_data[vk] = {
        'key': vk,
        'title': TITLES[vk],
        'ascSign': f"{SIGNS_HI[asc_v_sign]} ({asc_v_sign + 1})",
        'houses': houses,
        'planetDetails': planet_details
    }

print("Calculated all 16 Varga Charts for Nikhil Vyas successfully!")
for vk, d in out_data.items():
    print(f"{vk}: Lagna={d['ascSign']}, House 1={d['houses']['1']}")

import json
with open('data/nikhil_vargas_canonical.json', 'w', encoding='utf-8') as f:
    json.dump(out_data, f, ensure_ascii=False, indent=2)

