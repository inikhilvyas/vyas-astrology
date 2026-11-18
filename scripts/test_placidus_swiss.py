import swisseph as swe
import datetime as dt

swe.set_sid_mode(swe.SIDM_LAHIRI)
d = dt.datetime(2000, 1, 1, 12, tzinfo=dt.timezone.utc)
jd = swe.julday(d.year, d.month, d.day, d.hour + d.minute/60.0)

for lat in [0.0, 13.0, 28.6, 45.0, 60.0]:
    cusps, ascmc = swe.houses_ex(jd, lat, 0.0, b'P', swe.FLG_SIDEREAL)
    print(f"Lat: {lat:4.1f} | Asc: {ascmc[0]:6.2f}° | H1: {cusps[0]:6.2f}° | H10 (MC): {cusps[9]:6.2f}° | H11: {cusps[10]:6.2f}°")

