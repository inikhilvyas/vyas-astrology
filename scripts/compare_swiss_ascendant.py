import sys
sys.path.insert(0, "src")
import datetime as dt
import swisseph as swe
from vyas import ephem

swe.set_sid_mode(swe.SIDM_LAHIRI)

test_cases = [
    ("1900-01-01 Delhi", dt.datetime(1900, 1, 1, 6, 0, tzinfo=dt.timezone.utc), 28.6139, 77.2090),
    ("1956-03-21 Ujjain", dt.datetime(1956, 3, 21, 12, 0, tzinfo=dt.timezone.utc), 23.1765, 75.7885),
    ("2000-01-01 Greenwich", dt.datetime(2000, 1, 1, 12, 0, tzinfo=dt.timezone.utc), 51.48, 0.0),
    ("2020-01-01 Mumbai", dt.datetime(2020, 1, 1, 18, 0, tzinfo=dt.timezone.utc), 19.0760, 72.8777),
    ("2026-11-18 Jaipur", dt.datetime(2026, 11, 18, 9, 30, tzinfo=dt.timezone.utc), 26.9124, 75.7873),
]

print(f"{'Case':22s} | {'Swiss Lagna':14s} | {'Current ephem.py':16s} | {'Diff (deg)':14s} | {'Diff (arcmin)':14s}")
print("-" * 90)

for label, dtu, lat, lon in test_cases:
    # Swiss Ephemeris
    y, m, d = dtu.year, dtu.month, dtu.day
    h = dtu.hour + dtu.minute / 60.0 + dtu.second / 3600.0 + dtu.microsecond / 3600e6
    jd = swe.julday(y, m, d, h)
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
    swiss_asc = ascmc[0] % 360.0
    
    # Current ephem.py
    curr_asc = ephem.ascendant_sidereal(dtu, lat, lon)
    diff_deg = ((curr_asc - swiss_asc + 180.0) % 360.0) - 180.0
    diff_min = diff_deg * 60.0
    print(f"{label:22s} | {swiss_asc:14.6f} | {curr_asc:16.6f} | {diff_deg:+14.6f}° | {diff_min:+14.3f}'")

