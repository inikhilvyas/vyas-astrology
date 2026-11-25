import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ephemeris_shodashvarga_engine import _planet_geocentric_tropical, compute_chitrapaksha_ayanamsa

jd = 2446027.968750
ay = compute_chitrapaksha_ayanamsa(jd)
mars_trop = _planet_geocentric_tropical('Mars', jd)
mars_sid = (mars_trop - ay) % 360.0
in_sign = mars_sid % 30.0
d = int(in_sign)
m = int((in_sign - d) * 60)
s = int(round(((in_sign - d) * 60 - m) * 60))
print(f"Mars Sidereal: {mars_sid:.4f}° -> {d}° {m}' {s}\"")

sat_trop = _planet_geocentric_tropical('Saturn', jd)
sat_sid = (sat_trop - ay) % 360.0
sin_s = sat_sid % 30.0
sd = int(sin_s)
sm = int((sin_s - sd) * 60)
ss = int(round(((sin_s - sd) * 60 - sm) * 60))
print(f"Saturn Sidereal: {sat_sid:.4f}° -> {sd}° {sm}' {ss}\"")
