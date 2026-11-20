import sys
sys.path.insert(0, 'src')
from datetime import datetime, timezone, timedelta
from vyas.ephem import planet_positions, ascendant_sidereal, set_ayanamsa
from vyas.dasha import VimshottariDasha

set_ayanamsa('Lahiri')
dt = datetime(1984, 11, 23, 16, 45, 0, tzinfo=timezone(timedelta(hours=5.5)))
planets = planet_positions(dt)
asc_lon = ascendant_sidereal(dt, 25.5835, 73.3837)
SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

def dms(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = int(round(((deg - d) * 60 - m) * 60))
    return f"{d} deg {m:02d}' {s:02d}\""

asc_sign = SIGNS[int(asc_lon // 30) % 12]
print(f"Ascendant (16:45, Pali): {asc_sign} at {dms(asc_lon % 30)} (Full: {asc_lon:.6f})")

dt2 = datetime(1984, 11, 23, 16, 51, 0, tzinfo=timezone(timedelta(hours=5.5)))
asc_lon2 = ascendant_sidereal(dt2, 25.53, 73.38)
asc_sign2 = SIGNS[int(asc_lon2 // 30) % 12]
print(f"Ascendant (16:51, Pali): {asc_sign2} at {dms(asc_lon2 % 30)} (Full: {asc_lon2:.6f})")

for p, raw in planets.items():
    sign = SIGNS[int(raw.longitude // 30) % 12]
    print(f"{p:8s}: {sign:12s} at {dms(raw.longitude % 30)} (Full: {raw.longitude:.6f})")

moon_lon = planets['Moon'].longitude
vd = VimshottariDasha(moon_lon, dt)
now_dt = datetime(2026, 11, 18, 15, 30, 0, tzinfo=timezone(timedelta(hours=5.5)))
chain = vd.get_running_dasha(now_dt)
print("\nCurrent active dasha chain on 18 Nov 2026 (for 16:45 birth):")
print("chain:", chain)

print("\nAll Mahadashas from birth:")
for md in vd.calculate_mahadashas():
    print(f"  MD {md.lord}: {md.start_date} to {md.end_date}")
