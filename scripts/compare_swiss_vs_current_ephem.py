import sys
sys.path.insert(0, "src")
import swisseph as swe
from vyas import ephem

swe.set_sid_mode(swe.SIDM_LAHIRI)

dates = [
    ("1900-01-01", 1900, 1, 1, 0.0),
    ("1956-03-21", 1956, 3, 21, 0.0),
    ("2000-01-01", 2000, 1, 1, 12.0),
    ("2020-01-01", 2020, 1, 1, 0.0),
    ("2050-01-01", 2050, 1, 1, 0.0),
    ("2100-01-01", 2100, 1, 1, 0.0),
]

print(f"{'Date':12s} | {'Swiss Ayanamsa':16s} | {'Current ephem.py':16s} | {'Diff (arcsec)':14s}")
print("-" * 65)

for label, y, m, d, h in dates:
    jd = swe.julday(y, m, d, h)
    swiss_ay = swe.get_ayanamsa_ut(jd)
    current_ay = ephem.ayanamsa_deg(jd, "Lahiri")
    diff_arcsec = (current_ay - swiss_ay) * 3600.0
    print(f"{label:12s} | {swiss_ay:16.8f} | {current_ay:16.8f} | {diff_arcsec:+14.3f}\"")
