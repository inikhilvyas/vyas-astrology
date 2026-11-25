function test(y, m, d, hr, mn, sc, tz, lat, lon) {
    const RAD = Math.PI / 180.0;
    const DEG = 180.0 / Math.PI;
    function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }

    var ut = hr + mn / 60.0 + sc / 3600.0 - tz;
    var a = Math.floor((14 - m) / 12);
    var y1 = y + 4800 - a;
    var m1 = m + 12 * a - 3;
    var jdn = d + Math.floor((153 * m1 + 2) / 5) + 365 * y1 + Math.floor(y1 / 4) - Math.floor(y1 / 100) + Math.floor(y1 / 400) - 32045;
    var jd_ut = jdn + (ut - 12.0) / 24.0;
    var deltaT = (y - 2000) * 0.5 + 64.0;
    var jd_tt = jd_ut + deltaT / 86400.0;
    var T = (jd_tt - 2451545.0) / 36525.0;

    var prec_deg = (5028.796195 * T + 1.1054348 * (T * T)) / 3600.0;
    var ayanamsa = 23.857088 + 1.3969713 * T + 0.0003086 * T * T;

    var L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
    var M_sun = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
    var e_sun = 0.016708634 - 0.000042037 * T;
    var C_sun = (1.914602 - 0.004817 * T) * Math.sin(M_sun * RAD) +
        (0.019993 - 0.000101 * T) * Math.sin(2 * M_sun * RAD) +
        0.000289 * Math.sin(3 * M_sun * RAD);
    var sunTrop = norm(L0 + C_sun);
    var sun_j2000 = norm(sunTrop - prec_deg);
    var R_sun = 1.000001018 * (1 - e_sun * e_sun) / (1 + e_sun * Math.cos((M_sun + C_sun) * RAD));
    var X_sun_j2000 = R_sun * Math.cos(sun_j2000 * RAD);
    var Y_sun_j2000 = R_sun * Math.sin(sun_j2000 * RAD);

    var elements = {
        Mercury: { a0: 0.38709927, ad: 0.00000037, e0: 0.20563593, ed: 0.00001906, i0: 7.00497902, id: -0.00594749, l0: 252.25032350, ld: 149472.67411175, wb0: 77.45779628, wbd: 0.16047689, om0: 48.33076593, omd: -0.12534081 },
        Venus:   { a0: 0.72333566, ad: 0.00000390, e0: 0.00677672, ed: -0.00004107, i0: 3.39467605, id: -0.00078890, l0: 181.97909950, ld: 58517.81538729, wb0: 131.60246718, wbd: 0.00268329, om0: 76.67984255, omd: -0.27769418 },
        Mars:    { a0: 1.52371034, ad: 0.00001847, e0: 0.09339410, ed: 0.00007882, i0: 1.84969142, id: -0.00813131, l0: 355.44656795, ld: 19140.30268499, wb0: 336.05637041, wbd: 0.44441088, om0: 49.55953891, omd: -0.29257343 },
        Jupiter: { a0: 5.20288700, ad: -0.00011607, e0: 0.04838624, ed: -0.00013253, i0: 1.30439695, id: -0.00183714, l0: 34.39644051, ld: 3034.74612775, wb0: 14.72847983, wbd: 0.21252668, om0: 100.47390909, omd: 0.20469106 },
        Saturn:  { a0: 9.53667594, ad: -0.00125060, e0: 0.05386179, ed: -0.00050991, i0: 2.48599187, id: 0.00193609, l0: 49.95424423, ld: 1222.49362201, wb0: 92.59887831, wbd: -0.41897216, om0: 113.66242448, omd: -0.28867794 }
    };

    function getHeliocentric(pName, tVal) {
        var el = elements[pName];
        var a = el.a0 + el.ad * tVal;
        var e = el.e0 + el.ed * tVal;
        var inc = (el.i0 + el.id * tVal) * RAD;
        var l_deg = el.l0 + el.ld * tVal;
        var wb_deg = el.wb0 + el.wbd * tVal;
        var om_deg = el.om0 + el.omd * tVal;

        var mj = norm(34.39644 + 3034.74613 * tVal - 14.72848) * RAD;
        var ms = norm(49.95424 + 1222.49362 * tVal - 92.59888) * RAD;

        if (pName === 'Jupiter') {
            l_deg += (-0.332 * Math.sin(2*mj - 5*ms - 67.6*RAD) - 0.056 * Math.sin(2*mj - 2*ms + 21*RAD) + 0.042 * Math.sin(3*mj - 5*ms + 21*RAD));
        } else if (pName === 'Saturn') {
            l_deg += (0.812 * Math.sin(2*mj - 5*ms - 67.6*RAD) - 0.229 * Math.cos(2*mj - 4*ms - 2*RAD) + 0.119 * Math.sin(mj - 2*ms - 3*RAD) + 0.32);
        } else if (pName === 'Mars') {
            var mm = norm(355.44657 + 19140.30268 * tVal - 336.05637) * RAD;
            l_deg += (-0.02);
        }

        var w_arg = (wb_deg - om_deg) * RAD;
        var om = om_deg * RAD;
        var m_anom = norm(l_deg - wb_deg) * RAD;

        var E = m_anom;
        for (var k = 0; k < 15; k++) {
            var dE = (m_anom - (E - e * Math.sin(E))) / (1.0 - e * Math.cos(E));
            E += dE;
            if (Math.abs(dE) < 1e-11) break;
        }

        var xv = a * (Math.cos(E) - e);
        var yv = a * Math.sqrt(1 - e * e) * Math.sin(E);
        var cos_w = Math.cos(w_arg), sin_w = Math.sin(w_arg);
        var cos_om = Math.cos(om), sin_om = Math.sin(om);
        var cos_i = Math.cos(inc), sin_i = Math.sin(inc);

        var x = (cos_w * cos_om - sin_w * sin_om * cos_i) * xv + (-sin_w * cos_om - cos_w * sin_om * cos_i) * yv;
        var y = (cos_w * sin_om + sin_w * cos_om * cos_i) * xv + (-sin_w * sin_om + cos_w * cos_om * cos_i) * yv;
        var z = (sin_w * sin_i) * xv + (cos_w * sin_i) * yv;
        return { x: x, y: y, z: z };
    }

    var result = {};
    result['Sun'] = norm(sunTrop - ayanamsa);

    for (var pName in elements) {
        var p0 = getHeliocentric(pName, T);
        var dx = p0.x + X_sun_j2000;
        var dy = p0.y + Y_sun_j2000;
        var dz = p0.z;
        var dist = Math.sqrt(dx*dx + dy*dy + dz*dz);
        var tau = (0.0057755183 * dist) / 36525.0; // in centuries
        var p = getHeliocentric(pName, T - tau);
        var gx = p.x + X_sun_j2000;
        var gy = p.y + Y_sun_j2000;
        var lambda_j2000 = norm(Math.atan2(gy, gx) * DEG);
        var lambda_ofdate = norm(lambda_j2000 + prec_deg);
        result[pName] = norm(lambda_ofdate - ayanamsa);
    }
    return result;
}

var res = test(1984, 11, 23, 16, 45, 0, 5.5, 25.7711, 73.3234);
for (var k in res) {
    var deg = res[k];
    var in_s = deg % 30;
    var d = Math.floor(in_s);
    var m = Math.floor((in_s - d) * 60);
    var s = Math.round(((in_s - d) * 60 - m) * 60);
    console.log(k.padEnd(10), deg.toFixed(4) + '°', '->', d + '° ' + m + '\' ' + s + '\"');
}
