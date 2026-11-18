import swisseph as swe

# Test across multiple dates
dates = [
    ("1900-01-01", 1900, 1, 1, 0.0),
    ("1956-03-21", 1956, 3, 21, 0.0),
    ("2000-01-01", 2000, 1, 1, 12.0),
    ("2020-01-01", 2020, 1, 1, 0.0),
    ("2026-11-18", 2026, 11, 18, 12.0),
    ("2050-01-01", 2050, 1, 1, 0.0),
    ("2100-01-01", 2100, 1, 1, 0.0),
]

swe.set_sid_mode(swe.SIDM_LAHIRI)

print(f"{'Date':12s} | {'JD (UT)':12s} | {'Swiss Ayanamsa (deg)':20s} | {'Swiss Ayanamsa (DMS)':24s}")
print("-" * 75)
for label, y, m, d, h in dates:
    jd = swe.julday(y, m, d, h)
    ay = swe.get_ayanamsa_ut(jd)
    deg = int(ay)
    min_ = int((ay - deg) * 60)
    sec = ((ay - deg) * 60 - min_) * 60
    dms = f"{deg}° {min_}' {sec:05.2f}\""
    print(f"{label:12s} | {jd:12.4f} | {ay:20.10f} | {dms:24s}")

