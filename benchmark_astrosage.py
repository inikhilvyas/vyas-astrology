"""Benchmark: VYAS vs AstroSage report of Nikhil Vyas (23/11/1984 15:45 IST, Pali)."""
import sys, os
from datetime import datetime, timedelta, timezone
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from vyas import ephem, panchang, gochar

LAT, LON, TZ = 25.7711, 73.3234, 5.5
local = datetime(1984, 11, 23, 15, 45)
utc = (local - timedelta(hours=TZ)).replace(tzinfo=timezone.utc)

# AstroSage values (KP ayanamsa), degrees from the report screenshot
ASTROSAGE = {"Sun": "217.48.44", "Moon": "224.40.17", "Mars": "282.14.44",
             "Mercury": "239.21.22", "Jupiter": "259.28.21", "Venus": "257.50.13",
             "Saturn": "206.59.47", "Rahu": "033.37.57", "Ketu": "213.37.57"}

def to_deg(s):
    d, m, x = (float(v) for v in s.split("."))
    return d + m / 60 + x / 3600

ephem.set_ayanamsa("KP")
pos = ephem.planet_positions(utc)
print(f"{'Planet':8} {'VYAS':>10} {'AstroSage':>10} {'diff(arcsec)':>12}")
worst = 0
for n, ref in ASTROSAGE.items():
    v = pos[n].longitude
    d = ((v - to_deg(ref) + 180) % 360 - 180) * 3600
    worst = max(worst, abs(d))
    print(f"{n:8} {v:10.4f} {to_deg(ref):10.4f} {d:12.1f}")
print(f"Worst difference: {worst:.1f} arcsec")

asc = ephem.ascendant_sidereal(utc, LAT, LON)
print("\nLagna:", round(asc, 4))
p = panchang.compute(local, LAT, LON, TZ, asc)
for k, v in p.as_dict().items():
    print(f"{k:18}: {v}")

print("\n--- Gochar today ---")
now = datetime(2026, 10, 4, 12, 40)
for r in gochar.transits(now, TZ, pos["Moon"].longitude, asc):
    print(r.planet, r.sign, r.degree, "H(Moon)", r.house_from_moon, r.tara, r.verdict,
          ("vedha:" + r.vedha_by) if r.vedha_by else "", "| next:", r.next_ingress)
print(gochar.shani_status(now, TZ, pos["Moon"].longitude))
