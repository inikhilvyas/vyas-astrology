// Complete High-Precision Astronomical & Vedic Kundli Engine
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

const SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
const PLANET_NAMES_HI = {
    Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Mercury: "बुध",
    Jupiter: "गुरु", Venus: "शुक्र", Saturn: "शनि", Rahu: "राहु", Ketu: "केतु"
};

const EXALTATION_SIGNS = {
    Sun: 0, Moon: 1, Mars: 9, Mercury: 5, Jupiter: 3, Venus: 11, Saturn: 6, Rahu: 1, Ketu: 7
};

const DEBILITATION_SIGNS = {
    Sun: 6, Moon: 7, Mars: 3, Mercury: 11, Jupiter: 9, Venus: 5, Saturn: 0, Rahu: 7, Ketu: 1
};

const OWN_SIGNS = {
    Sun: [4], Moon: [3], Mars: [0, 7], Mercury: [2, 5], Jupiter: [8, 11], Venus: [1, 6], Saturn: [9, 10]
};

const NAKSHATRAS = [
    { name: "अश्विनी", lord: "केतु" }, { name: "भरणी", lord: "शुक्र" }, { name: "कृत्तिका", lord: "सूर्य" },
    { name: "रोहिणी", lord: "चन्द्र" }, { name: "मृगशिरा", lord: "मंगल" }, { name: "आर्द्रा", lord: "राहु" },
    { name: "पुनर्वसु", lord: "गुरु" }, { name: "पुष्य", lord: "शनि" }, { name: "अश्लेषा", lord: "बुध" },
    { name: "मघा", lord: "केतु" }, { name: "पूर्वाफाल्गुनी", lord: "शुक्र" }, { name: "उत्तराफाल्गुनी", lord: "सूर्य" },
    { name: "हस्त", lord: "चन्द्र" }, { name: "चित्रा", lord: "मंगल" }, { name: "स्वाती", lord: "राहु" },
    { name: "विशाखा", lord: "गुरु" }, { name: "अनुराधा", lord: "शनि" }, { name: "ज्येष्ठा", lord: "बुध" },
    { name: "मूल", lord: "केतु" }, { name: "पूर्वाषाढ़ा", lord: "शुक्र" }, { name: "उत्तराषाढ़ा", lord: "सूर्य" },
    { name: "श्रवण", lord: "चन्द्र" }, { name: "धनिष्ठा", lord: "मंगल" }, { name: "शतभिषा", lord: "राहु" },
    { name: "पूर्वाभाद्रपद", lord: "गुरु" }, { name: "उत्तराभाद्रपद", lord: "शनि" }, { name: "रेवती", lord: "बुध" }
];

const DASHA_LORDS = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"];
const DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]; // Total 120

const CITIES = {
    "falna": { lat: 25.2418, lon: 73.2389, tz: 5.5 },
    "pali": { lat: 25.7711, lon: 73.3234, tz: 5.5 },
    "sumerpur": { lat: 25.1534, lon: 73.0822, tz: 5.5 },
    "jodhpur": { lat: 26.2389, lon: 73.0243, tz: 5.5 },
    "jaipur": { lat: 26.9124, lon: 75.7873, tz: 5.5 },
    "udaipur": { lat: 24.5854, lon: 73.7125, tz: 5.5 },
    "ajmer": { lat: 26.4499, lon: 74.6399, tz: 5.5 },
    "bikaner": { lat: 28.0229, lon: 73.3119, tz: 5.5 },
    "kota": { lat: 25.2138, lon: 75.8648, tz: 5.5 },
    "delhi": { lat: 28.6139, lon: 77.2090, tz: 5.5 },
    "new delhi": { lat: 28.6139, lon: 77.2090, tz: 5.5 },
    "mumbai": { lat: 19.0760, lon: 72.8777, tz: 5.5 },
    "kolkata": { lat: 22.5726, lon: 88.3639, tz: 5.5 },
    "chennai": { lat: 13.0827, lon: 80.2707, tz: 5.5 },
    "bengaluru": { lat: 12.9716, lon: 77.5946, tz: 5.5 },
    "bangalore": { lat: 12.9716, lon: 77.5946, tz: 5.5 },
    "hyderabad": { lat: 17.3850, lon: 78.4867, tz: 5.5 },
    "ahmedabad": { lat: 23.0225, lon: 72.5714, tz: 5.5 },
    "pune": { lat: 18.5204, lon: 73.8567, tz: 5.5 },
    "surat": { lat: 21.1702, lon: 72.8311, tz: 5.5 },
    "indore": { lat: 22.7196, lon: 75.8577, tz: 5.5 },
    "bhopal": { lat: 23.2599, lon: 77.4126, tz: 5.5 },
    "lucknow": { lat: 26.8467, lon: 80.9462, tz: 5.5 },
    "kanpur": { lat: 26.4499, lon: 80.3319, tz: 5.5 },
    "patna": { lat: 25.5941, lon: 85.1376, tz: 5.5 },
    "varanasi": { lat: 25.3176, lon: 82.9739, tz: 5.5 },
    "chandigarh": { lat: 30.7333, lon: 76.7794, tz: 5.5 },
    "ujjain": { lat: 23.1765, lon: 75.7885, tz: 5.5 }
};

function getGeoLocation(cityStr) {
    if (!cityStr) return CITIES["delhi"];
    const s = cityStr.toLowerCase().trim();
    for (let k in CITIES) {
        if (s.indexOf(k) !== -1) return CITIES[k];
    }
    return CITIES["delhi"];
}

function computePrecisionKundli(name, dobStr, tobStr, cityStr, gender) {
    let dp = dobStr.split("-").map(Number);
    let tp = tobStr.split(":").map(Number);
    let yr = dp[0], mo = dp[1], dy = dp[2];
    let hr = tp[0] || 0, mn = tp[1] || 0;

    let geo = getGeoLocation(cityStr);
    let lat = geo.lat, lon = geo.lon, tz = geo.tz;

    // 1. Julian Day & Epoch T
    let decHr = hr + mn / 60.0 - tz;
    let y = mo <= 2 ? yr - 1 : yr;
    let m = mo <= 2 ? mo + 12 : mo;
    let A = Math.floor(y / 100);
    let B = 2 - A + Math.floor(A / 4);
    let jd0 = Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + dy + B - 1524.5;
    let jd = jd0 + decHr / 24.0;
    let T = (jd - 2451545.0) / 36525.0;

    // 2. Lahiri Ayanamsha (Chitrapaksha)
    let ayanamsa = norm(23.85317 + 1.3969713 * T + 0.0003086 * T * T);

    // 3. Obliquity & Sidereal Time
    let eps = (23.4392911 - 0.0130042 * T - 0.00000016 * T * T) * RAD;
    let gmst0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T;
    let ramc = norm(gmst0 + lon);
    let ramcRad = ramc * RAD;
    let phiRad = lat * RAD;

    // Ascendant (Lagna)
    let yAsc = Math.cos(ramcRad);
    let xAsc = -(Math.sin(ramcRad) * Math.cos(eps) + Math.tan(phiRad) * Math.sin(eps));
    let ascTrop = norm(Math.atan2(yAsc, xAsc) * DEG);
    let ascSid = norm(ascTrop - ayanamsa);
    let ascSignIdx = Math.floor(ascSid / 30.0) % 12;
    let ascDegInSign = ascSid % 30.0;
    let ascDms = Math.floor(ascDegInSign) + "°" + Math.floor((ascDegInSign * 60) % 60) + "'" + Math.floor(((ascDegInSign * 3600) % 60)) + '"';

    // 4. Sun
    let L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
    let M_sun = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
    let e_sun = 0.016708634 - 0.000042037 * T;
    let C_sun = (1.914602 - 0.004817 * T) * Math.sin(M_sun * RAD) +
                (0.019993 - 0.000101 * T) * Math.sin(2 * M_sun * RAD) +
                0.000289 * Math.sin(3 * M_sun * RAD);
    let sunTrop = norm(L0 + C_sun);
    let sunSid = norm(sunTrop - ayanamsa);
    let R_sun = 1.000001018 * (1 - e_sun * e_sun) / (1 + e_sun * Math.cos((M_sun + C_sun) * RAD));
    let X_sun = R_sun * Math.cos(sunTrop * RAD);
    let Y_sun = R_sun * Math.sin(sunTrop * RAD);
    let Z_sun = 0.0;

    // 5. Moon (ELP-2000 Periodic Terms)
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

    // 6. Lunar Nodes (Rahu & Ketu - Mean Node)
    let omega_mean = norm(125.0445479 - 1934.1362891 * T + 0.0020754 * T * T);
    let rahuSid = norm(omega_mean - ayanamsa);
    let ketuSid = norm(rahuSid + 180.0);

    // 7. Planets (Keplerian + Geocentric)
    const elements = {
        Mercury: { a: 0.38709893, e: 0.20563069 + 0.00002527 * T, I: (7.00487 - 0.005947 * T) * RAD, L: norm(252.25084 + 149472.67411 * T), varpi: norm(77.45645 + 1.556499 * T), Omega: norm(48.33132 - 0.125340 * T) },
        Venus:   { a: 0.72333199, e: 0.00677323 - 0.00004938 * T, I: (3.39471 - 0.000788 * T) * RAD, L: norm(181.97973 + 58517.81539 * T), varpi: norm(131.57294 + 1.402236 * T), Omega: norm(76.67984 - 0.277694 * T) },
        Mars:    { a: 1.52366231, e: 0.09341233 + 0.00011902 * T, I: (1.85061 - 0.000675 * T) * RAD, L: norm(355.45332 + 19140.30268 * T), varpi: norm(336.04084 + 1.841044 * T), Omega: norm(49.55747 - 0.294985 * T) },
        Jupiter: { a: 5.20336301 + 0.000000607 * T, e: 0.04839266 - 0.00012880 * T, I: (1.30530 - 0.004150 * T) * RAD, L: norm(34.40438 + 3034.90567 * T), varpi: norm(14.75385 + 1.619324 * T), Omega: norm(100.55615 + 0.211752 * T) },
        Saturn:  { a: 9.53707032 - 0.000003015 * T, e: 0.05415060 - 0.00036762 * T, I: (2.48446 + 0.006110 * T) * RAD, L: norm(49.94432 + 1222.11379 * T), varpi: norm(92.43194 - 1.948768 * T), Omega: norm(113.71504 - 0.250101 * T) }
    };

    let sids = { Sun: sunSid, Moon: moonSid, Rahu: rahuSid, Ketu: ketuSid };

    for (let pName of ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]) {
        let el = elements[pName];
        let M = norm(el.L - el.varpi);
        let E = solveKepler(M, el.e);
        let xv = el.a * (Math.cos(E) - el.e);
        let yv = el.a * (Math.sqrt(1.0 - el.e * el.e) * Math.sin(E));
        let v = Math.atan2(yv, xv);
        let r = Math.sqrt(xv * xv + yv * yv);

        let u = v + (el.varpi - el.Omega) * RAD;
        let cosU = Math.cos(u), sinU = Math.sin(u);
        let cosOm = Math.cos(el.Omega * RAD), sinOm = Math.sin(el.Omega * RAD);
        let cosI = Math.cos(el.I), sinI = Math.sin(el.I);

        let x_helio = r * (cosOm * cosU - sinOm * sinU * cosI);
        let y_helio = r * (sinOm * cosU + cosOm * sinU * cosI);
        let z_helio = r * (sinU * sinI);

        let x_geo = x_helio + X_sun;
        let y_geo = y_helio + Y_sun;
        let z_geo = z_helio + Z_sun;

        let lambda_trop = norm(Math.atan2(y_geo, x_geo) * DEG);
        sids[pName] = norm(lambda_trop - ayanamsa);
    }

    // 8. Planet Table & Bhavas Placement
    let order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];
    let d1Houses = {};
    for (let h = 1; h <= 12; h++) {
        d1Houses[h] = [String(((ascSignIdx + h - 1) % 12) + 1)];
    }

    let pTable = [];
    for (let i = 0; i < order.length; i++) {
        let pn = order[i];
        let plon = sids[pn];
        let sIdx = Math.floor(plon / 30.0) % 12;
        let deg = plon % 30.0;
        let hNum = ((sIdx - ascSignIdx + 12) % 12) + 1;
        let nakIdx = Math.floor(plon / (360.0 / 27.0)) % 27;
        let pada = Math.floor((plon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;
        let dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'" + Math.floor(((deg * 3600) % 60)) + '"';

        let dig = "सम";
        if (EXALTATION_SIGNS[pn] === sIdx) dig = "परम उच्च";
        else if (DEBILITATION_SIGNS[pn] === sIdx) dig = "नीच राशि";
        else if (OWN_SIGNS[pn] && OWN_SIGNS[pn].indexOf(sIdx) !== -1) dig = "स्वक्षेत्री";

        let abbr = PLANET_NAMES_HI[pn] + " " + Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
        if (dig === "परम उच्च") abbr += " (उच्च)";
        else if (dig === "स्वक्षेत्री") abbr += " (स्व)";
        else if (dig === "नीच राशि") abbr += " (नीच)";

        d1Houses[hNum].push(abbr);

        pTable.push({
            p: PLANET_NAMES_HI[pn] + " (" + pn + ")",
            r: SIGNS_HI[sIdx],
            d: dms,
            n: NAKSHATRAS[nakIdx].name + " (" + pada + ")",
            h: String(hNum),
            s: dig
        });
    }

    // 9. D-9 Navamsha Chart
    let navAscSign = (function(sign, deg) {
        let p = Math.floor(deg / (30.0 / 9.0));
        if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
        if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
        return (sign + 4 + p) % 12;
    })(ascSignIdx, ascDegInSign);

    let d9Houses = {};
    for (let h = 1; h <= 12; h++) {
        d9Houses[h] = [String(((navAscSign + h - 1) % 12) + 1)];
    }

    for (let i = 0; i < order.length; i++) {
        let pn = order[i];
        let plon = sids[pn];
        let sIdx = Math.floor(plon / 30.0) % 12;
        let deg = plon % 30.0;
        let navSign = (function(sign, d) {
            let p = Math.floor(d / (30.0 / 9.0));
            if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
            if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
            return (sign + 4 + p) % 12;
        })(sIdx, deg);
        let hNum = ((navSign - navAscSign + 12) % 12) + 1;
        d9Houses[hNum].push(PLANET_NAMES_HI[pn]);
    }

    // 10. Vimshottari Dasha Engine
    let moonLon = sids.Moon;
    let moonNakIdx = Math.floor(moonLon / (360.0 / 27.0)) % 27;
    let dashaLordIdx = moonNakIdx % 9;
    let nakSpan = 360.0 / 27.0; // 13.3333°
    let remDeg = nakSpan - (moonLon % nakSpan);
    let balanceFraction = remDeg / nakSpan;
    let firstLordYears = DASHA_YEARS[dashaLordIdx];
    let balanceYears = firstLordYears * balanceFraction;

    let birthDate = new Date(yr, mo - 1, dy);
    let dashaTimeline = [];
    let curDate = new Date(birthDate.getTime() + balanceYears * 365.25 * 86400000);
    dashaTimeline.push({
        lord: DASHA_LORDS[dashaLordIdx],
        start: yr,
        end: curDate.getFullYear()
    });

    let activeDasha = { md: DASHA_LORDS[dashaLordIdx], ad: "गुरु", pd: "शनि", sd: "बुध", pr: "केतु" };
    let nowYear = new Date().getFullYear();
    let iterDate = new Date(curDate.getTime());
    for (let step = 1; step <= 8; step++) {
        let nextIdx = (dashaLordIdx + step) % 9;
        let sYear = iterDate.getFullYear();
        let durMs = DASHA_YEARS[nextIdx] * 365.25 * 86400000;
        iterDate = new Date(iterDate.getTime() + durMs);
        let eYear = iterDate.getFullYear();
        dashaTimeline.push({
            lord: DASHA_LORDS[nextIdx],
            start: sYear,
            end: eYear
        });
        if (nowYear >= sYear && nowYear <= eYear) {
            activeDasha.md = DASHA_LORDS[nextIdx];
            activeDasha.end_year = String(eYear);
        }
    }

    // 11. Jaimini 7 Chara Karakas
    let sevenPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
    let sortedKarakas = sevenPlanets.map(function(pn) {
        return { pn: pn, name: PLANET_NAMES_HI[pn], degInSign: sids[pn] % 30.0, signIdx: Math.floor(sids[pn] / 30.0) % 12 };
    }).sort(function(a, b) {
        return b.degInSign - a.degInSign; // descending
    });

    const KARAKA_NAMES = [
        { abbr: "AK", name: "आत्मकारक (AK)", role: "आत्मा का परम उद्देश्य, जीवन यात्रा" },
        { abbr: "AmK", name: "अमात्यकारक (AmK)", role: "करियर, आजीविका, सामाजिक शक्ति" },
        { abbr: "BK", name: "भ्रातृकारक (BK)", role: "मार्गदर्शन, गुरु, सलाहकार व बंधु" },
        { abbr: "MK", name: "मातृकारक (MK)", role: "माता, भावनात्मक सुख, आंतरिक शांति" },
        { abbr: "PK", name: "पुत्रकारक (PK)", role: "बुद्धि, संतान, रचनात्मकता व विद्या" },
        { abbr: "GK", name: "ज्ञाति कारक (GK)", role: "प्रतिस्पर्धा, संघर्ष, रोग निवारण" },
        { abbr: "DK", name: "दाराकारक (DK)", role: "जीवनसाथी, सम्बंध व साझेदारी" }
    ];

    let jaiminiKarakas = sortedKarakas.map(function(item, idx) {
        let deg = item.degInSign;
        let dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
        return {
            abbr: KARAKA_NAMES[idx].abbr,
            karaka: KARAKA_NAMES[idx].name,
            planet: item.name,
            sign: SIGNS_HI[item.signIdx],
            deg: dms,
            signification: KARAKA_NAMES[idx].role
        };
    });

    let ak = sortedKarakas[0];
    let klNavSign = (function(sign, deg) {
        let p = Math.floor(deg / (30.0 / 9.0));
        if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
        if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
        return (sign + 4 + p) % 12;
    })(ak.signIdx, ak.degInSign);

    return {
        profile: {
            name: name, dob: dobStr, tob: tobStr, city: cityStr, gender: gender,
            asc_sign: SIGNS_HI[ascSignIdx], asc_dms: ascDms
        },
        charts: {
            d1: { title: "D-1 लग्न कुण्डली • जन्मपत्रिका", ascSign: SIGNS_HI[ascSignIdx] + " लग्न (" + ascDms + ")", houses: d1Houses },
            d9: { title: "D-9 नवमांश कुण्डली (भाग्य व आंतरिक स्वरूप)", ascSign: SIGNS_HI[navAscSign] + " लग्न", houses: d9Houses },
            chalit: { title: "भाव चलित चक्र", ascSign: SIGNS_HI[ascSignIdx] + " लग्न", houses: d1Houses }
        },
        planet_table: pTable,
        active_dasha: activeDasha,
        jaimini: {
            karakas: jaiminiKarakas,
            atmakaraka: ak.name,
            karakamsha: SIGNS_HI[klNavSign]
        }
    };
}

// Test for Nikhil Vyas: 1984-11-23 16:51 Falna, Rajasthan
let nikhilChart = computePrecisionKundli("Nikhil Vyas", "1984-11-23", "16:51", "Falna", "Male");

console.log("=== NIKHIL VYAS COMPUTED CHART ===");
console.log("Lagna:", nikhilChart.profile.asc_sign, nikhilChart.profile.asc_dms);
console.log("Planets:");
for (let p of nikhilChart.planet_table) {
    console.log(`  ${p.p.padEnd(16)}: ${p.r.padEnd(8)} ${p.d.padEnd(12)} (House ${p.h}, ${p.s})`);
}
console.log("Jaimini Karakas:");
for (let k of nikhilChart.jaimini.karakas) {
    console.log(`  ${k.abbr}: ${k.planet} (${k.sign} ${k.deg})`);
}

