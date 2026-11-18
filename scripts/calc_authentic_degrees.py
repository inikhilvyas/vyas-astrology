import swisseph as swe

# DOB: 1984-11-23 16:51:00 IST -> UTC: 1984-11-23 11:21:00 UTC
year, month, day = 1984, 11, 23
hour_utc = 11 + 21/60.0
lat = 25.2354  # Falna, Pali (25°14'07" N)
lon = 73.2384  # 73°14'18" E

jd_utc = swe.julday(year, month, day, hour_utc)
swe.set_sid_mode(swe.SIDM_LAHIRI)
ayan = swe.get_ayanamsa_ut(jd_utc)

# Houses / Ascendant
houses, ascmc = swe.houses_ex(jd_utc, lat, lon, b'P', swe.FLG_SIDEREAL)
asc = ascmc[0]

planets = [
    ('Sun', swe.SUN),
    ('Moon', swe.MOON),
    ('Mars', swe.MARS),
    ('Mercury', swe.MERCURY),
    ('Jupiter', swe.JUPITER),
    ('Venus', swe.VENUS),
    ('Saturn', swe.SATURN),
    ('Rahu (True)', swe.TRUE_NODE),
    ('Rahu (Mean)', swe.MEAN_NODE),
]

def to_dms(deg):
    sign_idx = int(deg // 30) % 12
    rem = deg % 30
    d = int(rem)
    m = int((rem - d) * 60)
    s = int(round(((rem - d) * 60 - m) * 60))
    if s == 60:
        s = 0
        m += 1
    if m == 60:
        m = 0
        d += 1
    signs = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']
    return f"{signs[sign_idx]} {d}°{m:02d}'{s:02d}\" ({deg:.4f}°)"

print(f"Julian Day UTC: {jd_utc:.6f}")
print(f"Lahiri Ayanamsha: {to_dms(ayan)}")
print(f"Lagna (Ascendant): {to_dms(asc)}")
for name, p_id in planets:
    pos, _ = swe.calc_ut(jd_utc, p_id, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
    print(f"{name:14s}: {to_dms(pos[0])}")
