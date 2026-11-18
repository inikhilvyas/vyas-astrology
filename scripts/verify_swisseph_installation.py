import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
jd = swe.julday(2000, 1, 1, 12.0)
ay = swe.get_ayanamsa_ut(jd)
deg = int(ay)
m = int((ay - deg) * 60)
s = ((ay - deg) * 60 - m) * 60
print(f"Lahiri at J2000: {ay:.6f} deg = {deg} deg {m}' {s:.2f}\"")

# Planets
planets = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu_True": swe.TRUE_NODE,
    "Rahu_Mean": swe.MEAN_NODE
}

for name, pid in planets.items():
    res, flg = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
    print(f"  {name:10s}: lon={res[0]:10.6f} deg, speed={res[3]:9.5f} deg/day")

# Ascendant & Houses
cusps, ascmc = swe.houses_ex(jd, 28.6139, 77.2090, b'P', swe.FLG_SIDEREAL)
print(f"Ascendant (Lagna) sidereal: {ascmc[0]:.6f} deg")
print(f"MC sidereal: {ascmc[1]:.6f} deg")

