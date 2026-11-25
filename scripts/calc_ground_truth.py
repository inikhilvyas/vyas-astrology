try:
    import swisseph as swe
    has_swe = True
except ImportError:
    has_swe = False

print('Has swisseph:', has_swe)

if has_swe:
    # 1984-11-23 16:45:00 at Pali (25.7711 N, 73.3234 E, TZ 5.5)
    # UTC = 16.75 - 5.5 = 11.25 -> 11:15:00
    jd = swe.julday(1984, 11, 23, 11.25)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ay = swe.get_ayanamsa_ut(jd)
    print(f'Julian Day: {jd:.6f}, Lahiri Ayanamsa: {ay:.6f}°')

    signs = ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya', 'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena']

    planets = [
        ('Surya (Sun)', swe.SUN),
        ('Chandra (Moon)', swe.MOON),
        ('Mangala (Mars)', swe.MARS),
        ('Budha (Mercury)', swe.MERCURY),
        ('Guru (Jupiter)', swe.JUPITER),
        ('Shukra (Venus)', swe.VENUS),
        ('Shani (Saturn)', swe.SATURN),
        ('Rahu (Mean)', swe.MEAN_NODE),
        ('Rahu (True)', swe.TRUE_NODE)
    ]

    for name, p in planets:
        res, flags = swe.calc_ut(jd, p, swe.FLG_SIDEREAL | swe.FLG_SWIEPH)
        deg = res[0] % 360.0
        r_idx = int(deg // 30)
        in_s = deg % 30
        d = int(in_s)
        m = int((in_s - d) * 60)
        s = int(round(((in_s - d) * 60 - m) * 60))
        print(f'{name:15}: {deg:8.4f}° | {signs[r_idx]:10} {d:02d}° {m:02d}\' {s:02d}\"')

    # Lagna
    cusps, ascmc = swe.houses_ex(jd, 25.7711, 73.3234, b'P', swe.FLG_SIDEREAL)
    lagna_deg = ascmc[0] % 360.0
    r_idx = int(lagna_deg // 30)
    in_s = lagna_deg % 30
    d = int(in_s)
    m = int((in_s - d) * 60)
    s = int(round(((in_s - d) * 60 - m) * 60))
    print(f'{"Lagna (Asc)":15}: {lagna_deg:8.4f}° | {signs[r_idx]:10} {d:02d}° {m:02d}\' {s:02d}\"')

# Also test ephemeris_shodashvarga_engine.py
from ephemeris_shodashvarga_engine import compute_ephemeris_and_shodashvarga
res = compute_ephemeris_and_shodashvarga('1984-11-23T16:45:00', 25.7711, 73.3234, 5.5)
print('\n--- ephemeris_shodashvarga_engine.py results ---')
for k, v in res['planets'].items():
    print(f'{k:10}: {v["longitude"]:.4f}° | {v["sign"]} {v["deg"]}° {v["min"]}\' {v["sec"]}\"')
print(f'Lagna: {res["ascendant_deg"]:.4f}°')

