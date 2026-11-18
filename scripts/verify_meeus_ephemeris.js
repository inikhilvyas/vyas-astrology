// High-precision Meeus Analytical Ephemeris in JavaScript
const RAD = Math.PI / 180.0;
const DEG = 180.0 / Math.PI;

function norm(x) {
    x = x % 360.0;
    return x < 0 ? x + 360.0 : x;
}

function solveKepler(M, e) {
    M = norm(M) * RAD;
    let E = M;
    for (let i = 0; i < 15; i++) {
        let dE = (M - (E - e * Math.sin(E))) / (1.0 - e * Math.cos(E));
        E += dE;
        if (Math.abs(dE) < 1e-9) break;
    }
    return E;
}

function calculateHighPrecisionPlanets(year, month, day, hour, minute, lat, lon, tz) {
    // 1. Julian Day
    let decHr = hour + minute / 60.0 - tz;
    let y = month <= 2 ? year - 1 : year;
    let m = month <= 2 ? month + 12 : month;
    let A = Math.floor(y / 100);
    let B = 2 - A + Math.floor(A / 4);
    let jd0 = Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + day + B - 1524.5;
    let jd = jd0 + decHr / 24.0;
    let T = (jd - 2451545.0) / 36525.0;

    // 2. Lahiri Ayanamsha (Chitrapaksha)
    // Swiss Ephemeris Lahiri: 23.85317 at J2000.0, speed 50.27"/year
    let ayanamsa = norm(23.85317 + 1.3969713 * T + 0.0003086 * T * T);

    // 3. Obliquity of Ecliptic
    let eps = (23.4392911 - 0.0130042 * T - 0.00000016 * T * T) * RAD;

    // 4. Sidereal Time & Ascendant
    let gmst0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T;
    let ramc = norm(gmst0 + lon);
    let ramcRad = ramc * RAD;
    let phiRad = lat * RAD;
    let yAsc = Math.cos(ramcRad);
    let xAsc = -(Math.sin(ramcRad) * Math.cos(eps) + Math.tan(phiRad) * Math.sin(eps));
    let ascTrop = norm(Math.atan2(yAsc, xAsc) * DEG);
    let ascSid = norm(ascTrop - ayanamsa);

    // 5. Sun Heliocentric / Geocentric Coordinates
    let L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
    let M_sun = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
    let e_sun = 0.016708634 - 0.000042037 * T;
    let C_sun = (1.914602 - 0.004817 * T) * Math.sin(M_sun * RAD) +
                (0.019993 - 0.000101 * T) * Math.sin(2 * M_sun * RAD) +
                0.000289 * Math.sin(3 * M_sun * RAD);
    let sunTrop = norm(L0 + C_sun);
    let sunSid = norm(sunTrop - ayanamsa);
    let R_sun = 1.000001018 * (1 - e_sun * e_sun) / (1 + e_sun * Math.cos((M_sun + C_sun) * RAD));

    // Sun geocentric rectangular (ecliptic)
    let X_sun = R_sun * Math.cos(sunTrop * RAD);
    let Y_sun = R_sun * Math.sin(sunTrop * RAD);
    let Z_sun = 0.0;

    // 6. Moon Geocentric (ELP-2000 Truncated Periodic Series)
    let L_prime = norm(218.3164477 + 481267.88123421 * T);
    let D = norm(297.8501921 + 445267.1114034 * T);
    let M_moon = norm(134.9633964 + 477198.8675055 * T);
    let F = norm(93.2720950 + 483202.0175233 * T);

    let moonCorr = 6.288774 * Math.sin(M_moon * RAD) +
                   1.274027 * Math.sin((2 * D - M_moon) * RAD) +
                   0.658314 * Math.sin(2 * D * RAD) +
                   0.213618 * Math.sin(2 * M_moon * RAD) -
                   0.185116 * Math.sin(M_sun * RAD) -
                   0.114332 * Math.sin(2 * F * RAD) +
                   0.058793 * Math.sin((2 * D - M_sun - M_moon) * RAD) +
                   0.057066 * Math.sin((2 * D - 2 * M_moon) * RAD) +
                   0.053322 * Math.sin((2 * D + M_moon) * RAD) +
                   0.046038 * Math.sin((2 * D - M_sun) * RAD) +
                   0.041024 * Math.sin((M_moon - M_sun) * RAD) -
                   0.034720 * Math.sin(D * RAD) -
                   0.030647 * Math.sin((M_moon + M_sun) * RAD);

    let moonTrop = norm(L_prime + moonCorr);
    let moonSid = norm(moonTrop - ayanamsa);

    // 7. Lunar Nodes (Rahu & Ketu - Mean & True)
    let omega_mean = norm(125.04452 - 1934.136261 * T + 0.0020708 * T * T);
    let rahuCorr = -1.4979 * Math.sin(2 * (D - F) * RAD) -
                   0.4416 * Math.sin(2 * D * RAD) -
                   0.1498 * Math.sin(M_sun * RAD) +
                   0.1255 * Math.sin(2 * (D - M_moon) * RAD);
    let rahuTrop = norm(omega_mean + rahuCorr);
    let rahuSid = norm(rahuTrop - ayanamsa);
    let ketuSid = norm(rahuSid + 180.0);

    // 8. Planets Heliocentric Orbital Elements (VSOP87 / Standish / Meeus Table 31.A & 31.B)
    const elements = {
        Mercury: {
            a: 0.38709893,
            e: 0.20563069 + 0.00002527 * T,
            I: (7.00487 - 0.005947 * T) * RAD,
            L: norm(252.25084 + 149472.67411 * T),
            varpi: norm(77.45645 + 1.556499 * T),
            Omega: norm(48.33132 - 0.125340 * T)
        },
        Venus: {
            a: 0.72333199,
            e: 0.00677323 - 0.00004938 * T,
            I: (3.39471 - 0.000788 * T) * RAD,
            L: norm(181.97973 + 58517.81539 * T),
            varpi: norm(131.57294 + 1.402236 * T),
            Omega: norm(76.67984 - 0.277694 * T)
        },
        Mars: {
            a: 1.52366231,
            e: 0.09341233 + 0.00011902 * T,
            I: (1.85061 - 0.000675 * T) * RAD,
            L: norm(355.45332 + 19140.30268 * T),
            varpi: norm(336.04084 + 1.841044 * T),
            Omega: norm(49.55747 - 0.294985 * T)
        },
        Jupiter: {
            a: 5.20336301 + 0.000000607 * T,
            e: 0.04839266 - 0.00012880 * T,
            I: (1.30530 - 0.004150 * T) * RAD,
            L: norm(34.40438 + 3034.90567 * T),
            varpi: norm(14.75385 + 1.619324 * T),
            Omega: norm(100.55615 + 0.211752 * T)
        },
        Saturn: {
            a: 9.53707032 - 0.000003015 * T,
            e: 0.05415060 - 0.00036762 * T,
            I: (2.48446 + 0.006110 * T) * RAD,
            L: norm(49.94432 + 1222.11379 * T),
            varpi: norm(92.43194 - 1.948768 * T),
            Omega: norm(113.71504 - 0.250101 * T)
        }
    };

    let planetSid = {};
    planetSid.Sun = sunSid;
    planetSid.Moon = moonSid;
    planetSid.Rahu = rahuSid;
    planetSid.Ketu = ketuSid;

    for (let pName of ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]) {
        let el = elements[pName];
        let M = norm(el.L - el.varpi);
        let E = solveKepler(M, el.e);

        // True anomaly v and radius r
        let xv = el.a * (Math.cos(E) - el.e);
        let yv = el.a * (Math.sqrt(1.0 - el.e * el.e) * Math.sin(E));
        let v = Math.atan2(yv, xv); // in radians
        let r = Math.sqrt(xv * xv + yv * yv);

        // Heliocentric coordinates in ecliptic frame
        let u = v + (el.varpi - el.Omega) * RAD;
        let cosU = Math.cos(u), sinU = Math.sin(u);
        let cosOm = Math.cos(el.Omega * RAD), sinOm = Math.sin(el.Omega * RAD);
        let cosI = Math.cos(el.I), sinI = Math.sin(el.I);

        let x_helio = r * (cosOm * cosU - sinOm * sinU * cosI);
        let y_helio = r * (sinOm * cosU + cosOm * sinU * cosI);
        let z_helio = r * (sinU * sinI);

        // Geocentric coordinates: add Sun's geocentric vector
        let x_geo = x_helio + X_sun;
        let y_geo = y_helio + Y_sun;
        let z_geo = z_helio + Z_sun;

        let lambda_trop = norm(Math.atan2(y_geo, x_geo) * DEG);
        planetSid[pName] = norm(lambda_trop - ayanamsa);
    }

    return {
        ascSid: ascSid,
        ayanamsa: ayanamsa,
        planets: planetSid
    };
}

// Compare against Skyfield Baseline for 1990-05-15 10:30 at Jaipur (lat 26.9124, lon 75.7873, tz 5.5)
const calc = calculateHighPrecisionPlanets(1990, 5, 15, 10, 30, 26.9124, 75.7873, 5.5);

const skyfield = {
    Ascendant: 98.00,
    Sun: 30.39,
    Moon: 269.84,
    Mars: 324.39,
    Mercury: 14.33,
    Jupiter: 75.76,
    Venus: 348.76,
    Saturn: 271.53,
    Rahu: 287.63,
    Ketu: 107.63
};

console.log("=== HIGH-PRECISION MEEUS EPHEMERIS ACCURACY TEST ===");
console.log(`Ascendant: Calculated = ${calc.ascSid.toFixed(2)}°, Skyfield = ${skyfield.Ascendant.toFixed(2)}°, Diff = ${(calc.ascSid - skyfield.Ascendant).toFixed(2)}°`);
for (let p of ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]) {
    let diff = (calc.planets[p] - skyfield[p]);
    console.log(`${p.padEnd(8)}: Calculated = ${calc.planets[p].toFixed(2)}°, Skyfield = ${skyfield[p].toFixed(2)}°, Diff = ${diff.toFixed(2)}°`);
}

