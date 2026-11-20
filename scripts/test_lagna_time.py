import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
lat = 25.77
lon = 73.32

for sec in range(0, 180, 10):
    t_min = 51 + sec / 60.0
    jd_ut = swe.julday(1984, 11, 23, 11 + t_min / 60.0)
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P', swe.FLG_SIDEREAL)
    lagna = ascmc[0]
    rem = lagna % 30
    d = int(rem)
    m = int((rem - d) * 60)
    s = int(round(((rem - d) * 60 - m) * 60))
    print(f"Time 16:{51 + sec//60}:{sec%60:02d} -> Lagna: {d:02d}°{m:02d}'{s:02d}\" ({lagna:.4f}°)")

