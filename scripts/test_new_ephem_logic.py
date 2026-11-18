import datetime as dt
import swisseph as swe

# Let's test all functions we plan to put in ephem.py
AYANAMSAS = {
    "Lahiri": swe.SIDM_LAHIRI,
    "KP": swe.SIDM_KRISHNAMURTI,
    "Raman": swe.SIDM_RAMAN
}

_BODIES = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN
}

def to_jd(dt_utc: dt.datetime) -> float:
    y, m, d = dt_utc.year, dt_utc.month, dt_utc.day
    h = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3600e6
    return swe.julday(y, m, d, h)

now = dt.datetime.now(dt.timezone.utc)
jd = to_jd(now)
swe.set_sid_mode(swe.SIDM_LAHIRI)
ay = swe.get_ayanamsa_ut(jd)
print("Now JD:", jd, "Lahiri ayanamsa:", ay)

for p, pid in _BODIES.items():
    res, _ = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
    print(f"  {p:8s}: lon={res[0]:9.4f}°, speed={res[3]:8.4f}°/d")

# Nodes
res_t, _ = swe.calc_ut(jd, swe.TRUE_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
print(f"  {'Rahu (True)':12s}: lon={res_t[0]:9.4f}°, speed={res_t[3]:8.4f}°/d")
res_m, _ = swe.calc_ut(jd, swe.MEAN_NODE, swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED)
print(f"  {'Rahu (Mean)':12s}: lon={res_m[0]:9.4f}°, speed={res_m[3]:8.4f}°/d")

# Houses
cusps, ascmc = swe.houses_ex(jd, 26.9124, 75.7873, b'P', swe.FLG_SIDEREAL)
print(f"  Lagna (Jaipur): {ascmc[0]:9.4f}°, MC: {ascmc[1]:9.4f}°")
print("All Swiss calls executed with 100% success!")

