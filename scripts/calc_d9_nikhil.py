import swisseph as swe

# 23 Nov 1984, 16:51 IST (11:21 UTC), Pali/Falna
LAT = 25.2354
LON = 73.2384
swe.set_ephe_path('')
jd_utc = swe.julday(1984, 11, 23, 11.0 + 21.0/60.0)
swe.set_sid_mode(swe.SIDM_LAHIRI)

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

SIGNS_HI = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']

def get_d9_sign(lon):
    s = int(lon // 30.0) % 12
    deg = lon % 30.0
    element = s % 4
    start = [0, 9, 6, 3][element]
    part = int(deg // (30.0 / 9.0))
    return (start + part) % 12

print(f"Lagna D1: {int(asc_deg//30)} ({SIGNS_HI[int(asc_deg//30)]}), D9: {get_d9_sign(asc_deg)} ({SIGNS_HI[get_d9_sign(asc_deg)]})")
for p, lon in p_lons.items():
    d1 = int(lon // 30) % 12
    d9 = get_d9_sign(lon)
    print(f"{p:8s}: D1={SIGNS_HI[d1]} ({d1+1}), D9={SIGNS_HI[d9]} ({d9+1})")

