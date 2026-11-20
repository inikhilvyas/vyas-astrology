import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
# 1984-11-23 16:51 IST = 11:21:00 UTC
jd_ut = swe.julday(1984, 11, 23, 11 + 21.0/60.0)

lat = 25.77
lon = 73.32

for hsys in [b'P', b'W', b'A', b'E', b'V', b'B', b'O', b'M']:
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys, swe.FLG_SIDEREAL)
    asc = ascmc[0]
    rem = asc % 30
    d = int(rem)
    m = int((rem - d) * 60)
    s = int(round(((rem - d) * 60 - m) * 60))
    print(f"Hsys {chr(hsys[0])}: Asc = {d:02d}°{m:02d}'{s:02d}\" ({asc:.4f}°)")

# Also test without FLG_SIDEREAL and subtracting ayanamsa
cusps_trop, ascmc_trop = swe.houses_ex(jd_ut, lat, lon, b'P', 0)
ayan = swe.get_ayanamsa_ut(jd_ut)
asc_sid = (ascmc_trop[0] - ayan) % 360
rem = asc_sid % 30
d = int(rem)
m = int((rem - d) * 60)
s = int(round(((rem - d) * 60 - m) * 60))
print(f"Tropical Asc - Ayanamsa: {d:02d}°{m:02d}'{s:02d}\" ({asc_sid:.4f}°)")

