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
    ("2026-11-18", 2026, 11, 18, 12.0),
    ("2050-01-01", 2050, 1, 1, 0.0),
]

print(f"{'Date':12s} | {'Swiss True Node':16s} | {'Current ephem.py':16s} | {'Diff (deg)':14s} | {'Diff (arcmin)':14s}")
print("-" * 80)

for label, y, m, d, h in dates:
    jd = swe.julday(y, m, d, h)
    res, _ = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH)
    swiss_tn = res[0] % 360.0
    current_tn = ephem.true_node_tropical(jd)
    diff_deg = ((current_tn - swiss_tn + 180.0) % 360.0) - 180.0
    diff_min = diff_deg * 60.0
    print(f"{label:12s} | {swiss_tn:16.6f} | {current_tn:16.6f} | {diff_deg:+14.6f}° | {diff_min:+14.3f}'")

