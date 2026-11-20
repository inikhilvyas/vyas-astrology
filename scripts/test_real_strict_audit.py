import swisseph as swe
import math
from datetime import datetime, timezone

# 1. Benchmark: Nikhil Vyas
# 23 Nov 1984, 16:51 IST (11:21 UTC), Pali, Rajasthan (25.7711 N, 73.3234 E)
lat = 25.7711
lon = 73.3234

# Julian Day for 23 Nov 1984, 11:21:00 UTC
jd = swe.julday(1984, 11, 23, 11.0 + 21.0/60.0)
swe.set_sid_mode(swe.SIDM_LAHIRI)
ayan = swe.get_ayanamsa_ut(jd)
print(f"Calculated Lahiri Ayanamsha: {ayan:.6f}° -> {int(ayan)}°{int((ayan%1)*60)}'{int(((ayan%1)*60%1)*60)}\"")

# Calculate Lagna (Ascendant)
# Houses: swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
asc_deg = ascmc[0]
asc_rem = asc_deg % 30
print(f"Calculated Lagna: Rashi {int(asc_deg//30)} (मेष) {int(asc_rem):02d}°{int((asc_rem%1)*60):02d}'{int(((asc_rem%1)*60%1)*60):02d}\" (Exact: {asc_deg:.6f}°)")

# Canonical benchmark degrees from Drik Panchang
benchmark = {
    "Lagna": 23.7000,    # मेष 23°42'
    "Sun": 217.7138,     # वृश्चिक 07°42'50"
    "Moon": 224.6494,    # वृश्चिक 14°38'58"
    "Mars": 282.1561,    # मकर 12°09'22"
    "Mercury": 239.2667, # वृश्चिक 29°16'00"
    "Jupiter": 259.3522, # धनु 19°21'08"
    "Venus": 257.7500,   # धनु 17°45'00"
    "Saturn": 206.8833,  # तुला 26°53'00"
    "Rahu": 33.6167      # वृषभ 03°37'00"
}

planets_sw = {
    "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE
}

print("\n--- MATHEMATICAL VARIANCE AUDIT ---")
max_var_arcsec = 0.0
for p, p_id in planets_sw.items():
    pos, _ = swe.calc_ut(jd, p_id, swe.FLG_SIDEREAL)
    deg = pos[0] % 360
    bench_deg = benchmark[p]
    diff_deg = abs(deg - bench_deg)
    diff_arcsec = diff_deg * 3600.0
    if diff_arcsec > max_var_arcsec:
        max_var_arcsec = diff_arcsec
    print(f"{p:10}: Calc={deg:08.4f}° | Bench={bench_deg:08.4f}° | Variance={diff_arcsec:.2f} arcseconds")

# Lagna variance
lagna_diff_arcsec = abs(asc_deg - benchmark["Lagna"]) * 3600.0
print(f"{'Lagna':10}: Calc={asc_deg:08.4f}° | Bench={benchmark['Lagna']:08.4f}° | Variance={lagna_diff_arcsec:.2f} arcseconds")
print(f"\nMax Planetary Variance: {max_var_arcsec:.2f}\" | Lagna Variance: {lagna_diff_arcsec:.2f}\"")

