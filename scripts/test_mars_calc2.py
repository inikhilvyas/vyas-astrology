import math, datetime

RAD = math.pi / 180.0
DEG = 180.0 / math.pi
def norm(d): return (d % 360.0 + 360.0) % 360.0

dt = datetime.datetime(2026, 11, 24, 6, 32, 0, tzinfo=datetime.timezone.utc)
y, m, d = dt.year, dt.month, dt.day
h = dt.hour + dt.minute / 60.0 + dt.second / 3600.0
if m <= 2: y -= 1; m += 12
A = int(y / 100); B = 2 - A + int(A / 4)
jd = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5 + h / 24.0

from test_mars_calc import getH, elements
d = jd - 2451545.0
T = d / 36525.0

L0 = norm(280.4664567 + 36000.76982779 * T)
M_sun = norm(357.5291092 + 35999.0502909 * T) * RAD
C_sun = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(M_sun) + (0.019993 - 0.000101 * T) * math.sin(2 * M_sun) + 0.000289 * math.sin(3 * M_sun)
sun_app_lon = norm(L0 + C_sun - 0.00569 - 0.00478 * math.sin((125.04 - 1934.136 * T) * RAD))
e_sun = 0.016708634 - 0.000042037 * T
v_sun = M_sun + C_sun * RAD
R_sun = (1.000001018 * (1.0 - e_sun * e_sun)) / (1.0 + e_sun * math.cos(v_sun))
prec = (5028.796195 * T + 1.1054348 * T * T) / 3600.0
earth_helio_lon_j2000 = norm(sun_app_lon + 180.0 - prec) * RAD
X_sun_j2000 = R_sun * math.cos(earth_helio_lon_j2000)
Y_sun_j2000 = R_sun * math.sin(earth_helio_lon_j2000)

p0 = getH('Mars', T)
dx = p0[0] + X_sun_j2000
dy = p0[1] + Y_sun_j2000
dz = p0[2]
dist = math.sqrt(dx*dx + dy*dy + dz*dz)
tau = (0.0057755183 * dist) / 36525.0
p = getH('Mars', T - tau)
gx = p[0] + X_sun_j2000
gy = p[1] + Y_sun_j2000
lambda_j2000 = norm(math.atan2(gy, gx) * DEG)
lambda_ofdate = norm(lambda_j2000 + prec)
ayanamsa = 24.2415
sid_mars = norm(lambda_ofdate - ayanamsa)
deg_in_sign = sid_mars % 30.0
sign_idx = int(sid_mars / 30.0)
signs = ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya', 'Tula', 'Vrischika', 'Dhanu', 'Makara', 'Kumbha', 'Meena']
print(f"2026-11-24 Mars: {sid_mars:.6f} deg, Sign: {signs[sign_idx]}, Deg in sign: {int(deg_in_sign)} deg {int((deg_in_sign%1)*60)} min {int(((deg_in_sign*60)%1)*60)} sec ({deg_in_sign:.2f})")
