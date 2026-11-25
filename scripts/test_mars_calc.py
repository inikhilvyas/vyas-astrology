import math

RAD = math.pi / 180.0
DEG = 180.0 / math.pi
def norm(d): return (d % 360.0 + 360.0) % 360.0

# User birth: 1990-11-24 12:00 IST = 06:30 UTC
# JD = 2448220.7708333335
jd = 2448220.7708333335
d = jd - 2451545.0
T = d / 36525.0

elements = {
    'Mercury': dict(a0=0.38709927, ad=0.00000037, e0=0.20563593, ed=0.00001906, i0=7.00497902, id=-0.00594749, l0=252.25032350, ld=149472.67411175, wb0=77.45779628, wbd=0.16047689, om0=48.33076593, omd=-0.12534081),
    'Venus':   dict(a0=0.72333566, ad=0.00000390, e0=0.00677672, ed=-0.00004107, i0=3.39467605, id=-0.00078890, l0=181.97909950, ld=58517.81538729, wb0=131.60246718, wbd=0.00268329, om0=76.67984255, omd=-0.27769418),
    'Mars':    dict(a0=1.52371034, ad=0.00001847, e0=0.09339410, ed=0.00007882, i0=1.84969142, id=-0.00813131, l0=355.44656795, ld=19140.30268499, wb0=336.05637041, wbd=0.44441088, om0=49.55953891, omd=-0.29257343),
    'Jupiter': dict(a0=5.20288700, ad=-0.00011607, e0=0.04838624, ed=-0.00013253, i0=1.30439695, id=-0.00183714, l0=34.39644051, ld=3034.74612775, wb0=14.72847983, wbd=0.21252668, om0=100.47390909, omd=0.20469106),
    'Saturn':  dict(a0=9.53667594, ad=-0.00125060, e0=0.05386179, ed=-0.00050991, i0=2.48599187, id=0.00193609, l0=49.95424423, ld=1222.49362201, wb0=92.59887831, wbd=-0.41897216, om0=113.66242448, omd=-0.28867794)
}

prec_deg = (5028.796195 * T + 1.1054348 * T * T) / 3600.0
# Earth/Sun
L0 = norm(280.4664567 + 36000.76982779 * T)
M_sun = norm(357.5291092 + 35999.0502909 * T) * RAD
C_sun = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(M_sun) + (0.019993 - 0.000101 * T) * math.sin(2 * M_sun) + 0.000289 * math.sin(3 * M_sun)
sun_app_lon = norm(L0 + C_sun - 0.00569 - 0.00478 * math.sin((125.04 - 1934.136 * T) * RAD))
e_sun = 0.016708634 - 0.000042037 * T
v_sun = M_sun + C_sun * RAD
R_sun = (1.000001018 * (1.0 - e_sun * e_sun)) / (1.0 + e_sun * math.cos(v_sun))
earth_helio_lon_j2000 = norm(sun_app_lon + 180.0 - prec_deg) * RAD
X_sun_j2000 = R_sun * math.cos(earth_helio_lon_j2000)
Y_sun_j2000 = R_sun * math.sin(earth_helio_lon_j2000)

def getH(pName, tVal):
    el = elements[pName]
    a = el['a0'] + el['ad'] * tVal
    e = el['e0'] + el['ed'] * tVal
    inc = (el['i0'] + el['id'] * tVal) * RAD
    l_deg = el['l0'] + el['ld'] * tVal
    wb_deg = el['wb0'] + el['wbd'] * tVal
    om_deg = el['om0'] + el['omd'] * tVal
    mj = norm(34.39644 + 3034.74613 * tVal - 14.72848) * RAD
    ms = norm(49.95424 + 1222.49362 * tVal - 92.59888) * RAD
    if pName == 'Jupiter':
        l_deg += (-0.332 * math.sin(2 * mj - 5 * ms - 67.6 * RAD) - 0.056 * math.sin(2 * mj - 2 * ms + 21.0 * RAD) - 0.07)
    elif pName == 'Saturn':
        l_deg += (0.812 * math.sin(2 * mj - 5 * ms - 67.6 * RAD) - 0.229 * math.cos(2 * mj - 4 * ms - 2.0 * RAD) + 0.119 * math.sin(mj - 2 * ms - 3.0 * RAD) + 0.32)
    elif pName == 'Mars':
        l_deg += (-0.02)
    w_arg = (wb_deg - om_deg) * RAD
    om = om_deg * RAD
    m_anom = norm(l_deg - wb_deg) * RAD
    E = m_anom
    for _ in range(15):
        dE = (m_anom - (E - e * math.sin(E))) / (1.0 - e * math.cos(E))
        E += dE
        if abs(dE) < 1e-11: break
    xv = a * (math.cos(E) - e)
    yv = a * math.sqrt(1.0 - e * e) * math.sin(E)
    cos_w, sin_w = math.cos(w_arg), math.sin(w_arg)
    cos_om, sin_om = math.cos(om), math.sin(om)
    cos_i, sin_i = math.cos(inc), math.sin(inc)
    x = (cos_w * cos_om - sin_w * sin_om * cos_i) * xv + (-sin_w * cos_om - cos_w * sin_om * cos_i) * yv
    y = (cos_w * sin_om + sin_w * cos_om * cos_i) * xv + (-sin_w * sin_om + cos_w * cos_om * cos_i) * yv
    z = (sin_w * sin_i) * xv + (cos_w * sin_i) * yv
    return x, y, z

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
lambda_ofdate = norm(lambda_j2000 + prec_deg)
ayanamsa = 23.738805
sid_mars = norm(lambda_ofdate - ayanamsa)
deg_in_sign = sid_mars % 30.0
sign_idx = int(sid_mars / 30.0)
signs = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"]
print(f"Mars Sidereal: {sid_mars:.6f} deg, Sign: {signs[sign_idx]}, Deg in sign: {int(deg_in_sign)} deg {int((deg_in_sign%1)*60)} min {int(((deg_in_sign*60)%1)*60)} sec ({deg_in_sign:.2f})")
