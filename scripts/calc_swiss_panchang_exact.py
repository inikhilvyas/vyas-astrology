import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
# 1984-11-23 16:51 IST = 11:21:00 UTC
jd_ut = swe.julday(1984, 11, 23, 11 + 21.0/60.0)
ayan = swe.get_ayanamsa_ut(jd_ut)
print(f"Lahiri Ayanamsha: {ayan:.6f}°")

lat = 25.77
lon = 73.32

cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P', swe.FLG_SIDEREAL)
lagna = ascmc[0]
rashi_names = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन']

def fmt(deg):
    r_idx = int(deg // 30) % 12
    rem = deg % 30
    d = int(rem)
    m = int((rem - d) * 60)
    s = int(round(((rem - d) * 60 - m) * 60))
    if s >= 60:
        s = 0
        m += 1
    if m >= 60:
        m = 0
        d += 1
    return f"{rashi_names[r_idx]} {d:02d}°{m:02d}'{s:02d}\" ({deg:.4f}°)"

print(f"Lagna:   {fmt(lagna)}")

planets = [
    ('सूर्य', swe.SUN),
    ('चन्द्र', swe.MOON),
    ('मंगल', swe.MARS),
    ('बुध', swe.MERCURY),
    ('गुरु', swe.JUPITER),
    ('शुक्र', swe.VENUS),
    ('शनि', swe.SATURN),
    ('राहु', swe.TRUE_NODE)
]

for p_name, p_id in planets:
    res, flg = swe.calc_ut(jd_ut, p_id, swe.FLG_SIDEREAL | swe.FLG_SPEED)
    lon_p = res[0]
    print(f"{p_name:6s}: {fmt(lon_p)}")
    if p_id == swe.TRUE_NODE:
        ketu_lon = (lon_p + 180.0) % 360.0
        print(f"{'केतु':6s}: {fmt(ketu_lon)}")

# Also calculate Mean Node (औसत राहु)
res_mean, _ = swe.calc_ut(jd_ut, swe.MEAN_NODE, swe.FLG_SIDEREAL)
print(f"{'राहु(औसत)':6s}: {fmt(res_mean[0])}")
