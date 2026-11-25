import math

def norm360(d): return d % 360.0

def solve_placidus(asc_nir, lat, ayanamsa, jd):
    asc_trop = norm360(asc_nir + ayanamsa)
    T = (jd - 2451545.0) / 36525.0
    eps_deg = 23.43929111 - (46.8150 * T) / 3600.0
    eps = math.radians(eps_deg)
    phi = math.radians(max(min(lat, 66.0), -66.0))
    lam1 = math.radians(asc_trop)
    
    alpha1 = math.degrees(math.atan2(math.sin(lam1) * math.cos(eps), math.cos(lam1)))
    sin_decl1 = math.sin(eps) * math.sin(lam1)
    tan_decl1 = sin_decl1 / math.sqrt(max(1e-12, 1.0 - sin_decl1**2))
    ad1 = math.degrees(math.asin(max(-0.999999, min(0.999999, math.tan(phi) * tan_decl1))))
    oa1 = norm360(alpha1 - ad1)
    ramc_deg = norm360(oa1 - 90.0)
    ramc = math.radians(ramc_deg)
    mc_deg = norm360(math.degrees(math.atan2(math.sin(ramc), math.cos(ramc) * math.cos(eps))))
    
    def placidus_cusp(offset_deg, factor, diurnal):
        ra0 = norm360(ramc_deg + offset_deg)
        ra_curr = ra0
        for _ in range(35):
            ra_rad = math.radians(ra_curr)
            lam = math.atan2(math.sin(ra_rad), math.cos(ra_rad) * math.cos(eps))
            sin_decl = math.sin(eps) * math.sin(lam)
            tan_decl = sin_decl / math.sqrt(max(1e-12, 1.0 - sin_decl**2))
            ad_deg = math.degrees(math.asin(max(-0.999999, min(0.999999, math.tan(phi) * tan_decl))))
            ra_next = norm360(ra0 + factor * ad_deg) if diurnal else norm360(ra0 - factor * ad_deg)
            if abs((ra_next - ra_curr + 180) % 360 - 180) < 1e-7:
                ra_curr = ra_next
                break
            ra_curr = ra_next
        ra_fin = math.radians(ra_curr)
        return norm360(math.degrees(math.atan2(math.sin(ra_fin), math.cos(ra_fin) * math.cos(eps))))
    
    c11 = placidus_cusp(30.0, 1.0/3.0, True)
    c12 = placidus_cusp(60.0, 2.0/3.0, True)
    c2 = placidus_cusp(120.0, 2.0/3.0, False)
    c3 = placidus_cusp(150.0, 1.0/3.0, False)
    
    trop = {
        1: asc_trop, 2: c2, 3: c3, 4: norm360(mc_deg + 180.0),
        5: norm360(c11 + 180.0), 6: norm360(c12 + 180.0),
        7: norm360(asc_trop + 180.0), 8: norm360(c2 + 180.0), 9: norm360(c3 + 180.0),
        10: mc_deg, 11: c11, 12: c12
    }
    
    signs = ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya', 'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena']
    print('--- AUTHENTIC PLACIDUS CUSPS (SIDEREAL) ---')
    for h in range(1, 13):
        nir = norm360(trop[h] - ayanamsa)
        s_idx = int(nir / 30.0) % 12
        deg_in = nir % 30.0
        d = int(deg_in)
        m = int((deg_in - d) * 60)
        s = int(round(((deg_in - d) * 60 - m) * 60))
        print(f'Cusp {h:2d}: {signs[s_idx]:12s} {d:02d} deg {m:02d} min {s:02d} sec ({nir:8.4f})')

if __name__ == '__main__':
    solve_placidus(12.15, 25.77, 23.64, 2461370.0)
