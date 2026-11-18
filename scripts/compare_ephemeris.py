# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'src')
from vyas import ephem, ashtakavarga, varga
from datetime import datetime

dt = datetime(1984, 11, 23, 16, 51)
dt_utc = ephem.local_to_utc(dt, 5.5)
lat, lon = 25.2418, 73.2389

asc = ephem.ascendant_sidereal(dt_utc, lat, lon)
jd = ephem.julian_day_tt(dt_utc)
ayan = ephem.ayanamsa_deg(jd)
SIGNS = ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya', 'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena']

print('=== EXACT NASA JPL / SWISS EPHEMERIS VALUES ===')
print(f'Lagna: {SIGNS[int(asc//30)]} ({int(asc//30)+1}) {asc%30:.4f} deg')
print(f'Ayanamsa: {ayan:.6f} deg')

positions = ephem.planet_positions(dt_utc)
p_signs = {}
exact_degs = {}
for p, pos in positions.items():
    sid_lon = (pos.longitude - ayan) % 360.0
    s_idx = int(sid_lon // 30)
    deg_in_sign = sid_lon % 30
    p_signs[p] = s_idx
    exact_degs[p] = (s_idx, deg_in_sign)
    d = int(deg_in_sign)
    m = int((deg_in_sign - d) * 60)
    s = int(round(((deg_in_sign - d) * 60 - m) * 60))
    print(f'{p:8s}: {SIGNS[s_idx]:10s} {d:02d}deg {m:02d}m {s:02d}s ({deg_in_sign:.4f} deg)')

av = ashtakavarga.compute_ashtakavarga(p_signs, int(asc//30))
print('\n=== SAMUDAYA ASHTAKAVARGA (SAV) ===')
for i, s in enumerate(SIGNS):
    print(f'  {s:10s} ({i+1}): {av["sav"][i]} bindus')
print('Total SAV points:', sum(av['sav']))

# D-9 Navamsha
print('\n=== D-9 NAVAMSHA CHARTS ===')
asc_v = varga.calculate_vargas_detailed(asc)
print(f'Lagna D9: {asc_v["D9"].sign_name} ({asc_v["D9"].dms_str})')
for p, pos in positions.items():
    sid_lon = (pos.longitude - ayan) % 360.0
    pv = varga.calculate_vargas_detailed(sid_lon)
    print(f'{p:8s} D9: {pv["D9"].sign_name:10s} ({pv["D9"].dms_str})')

# D-10 Dashamsha
print('\n=== D-10 DASHAMSHA CHARTS ===')
print(f'Lagna D10: {asc_v["D10"].sign_name} ({asc_v["D10"].dms_str})')
for p, pos in positions.items():
    sid_lon = (pos.longitude - ayan) % 360.0
    pv = varga.calculate_vargas_detailed(sid_lon)
    print(f'{p:8s} D10: {pv["D10"].sign_name:10s} ({pv["D10"].dms_str})')
