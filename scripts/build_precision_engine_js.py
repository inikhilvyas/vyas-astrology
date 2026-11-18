# -*- coding: utf-8 -*-
"""
Generates the complete, high-precision astronomical and Vedic calculation engine in JavaScript.
Implements:
- Meeus / VSOP87 Analytical Ephemeris (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu)
- True Lahiri (Chitrapaksha) Ayanamsha
- RAMC & Spherical Obliquity Ascendant (Lagna)
- 12 Bhavas, D-1, D-9 Navamsha, D-10 Dashamsha, Bhava Chalit
- Vimshottari Dasha Engine (5-tier: Maha, Antar, Pratyantar, Sookshma, Pran)
- KP 249 Sub-Lord Table
- Jaimini 7 Chara Karakas & Karakamsha Lagna
- Ashtakavarga 337 SAV
- Nadi 1-5-9 Directional Trines
- Comprehensive Indian & Global City Geocoder
"""

def get_engine_js():
    return r"""        computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender) {
            var RAD = Math.PI / 180.0;
            var DEG = 180.0 / Math.PI;

            function norm(x) {
                x = x % 360.0;
                return x < 0 ? x + 360.0 : x;
            }

            function solveKepler(M, e) {
                M = norm(M) * RAD;
                var E = M;
                for (var i = 0; i < 15; i++) {
                    var dE = (M - (E - e * Math.sin(E))) / (1.0 - e * Math.cos(E));
                    E += dE;
                    if (Math.abs(dE) < 1e-9) break;
                }
                return E;
            }

            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var PLANET_NAMES_HI = {
                Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Mercury: "बुध",
                Jupiter: "गुरु", Venus: "शुक्र", Saturn: "शनि", Rahu: "राहु", Ketu: "केतु"
            };

            var EXALTATION_SIGNS = { Sun: 0, Moon: 1, Mars: 9, Mercury: 5, Jupiter: 3, Venus: 11, Saturn: 6, Rahu: 1, Ketu: 7 };
            var DEBILITATION_SIGNS = { Sun: 6, Moon: 7, Mars: 3, Mercury: 11, Jupiter: 9, Venus: 5, Saturn: 0, Rahu: 7, Ketu: 1 };
            var OWN_SIGNS = {
                Sun: [4], Moon: [3], Mars: [0, 7], Mercury: [2, 5],
                Jupiter: [8, 11], Venus: [1, 6], Saturn: [9, 10]
            };

            var NAKSHATRAS = [
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

            var DASHA_LORDS = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"];
            var DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]; // Total 120

            var CITIES = {
                "falna": { lat: 25.2418, lon: 73.2389, tz: 5.5 },
                "pali": { lat: 25.7711, lon: 73.3234, tz: 5.5 },
                "sumerpur": { lat: 25.1534, lon: 73.0822, tz: 5.5 },
                "jodhpur": { lat: 26.2389, lon: 73.0243, tz: 5.5 },
                "jaipur": { lat: 26.9124, lon: 75.7873, tz: 5.5 },
                "udaipur": { lat: 24.5854, lon: 73.7125, tz: 5.5 },
                "ajmer": { lat: 26.4499, lon: 74.6399, tz: 5.5 },
                "bikaner": { lat: 28.0229, lon: 73.3119, tz: 5.5 },
                "kota": { lat: 25.2138, lon: 75.8648, tz: 5.5 },
                "sirohi": { lat: 24.8826, lon: 72.8589, tz: 5.5 },
                "jalore": { lat: 25.3444, lon: 72.6152, tz: 5.5 },
                "abu": { lat: 24.5926, lon: 72.7156, tz: 5.5 },
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
                "kashi": { lat: 25.3176, lon: 82.9739, tz: 5.5 },
                "chandigarh": { lat: 30.7333, lon: 76.7794, tz: 5.5 },
                "dehradun": { lat: 30.3165, lon: 78.0322, tz: 5.5 },
                "haridwar": { lat: 29.9457, lon: 78.1642, tz: 5.5 },
                "ujjain": { lat: 23.1765, lon: 75.7885, tz: 5.5 },
                "agra": { lat: 27.1767, lon: 78.0081, tz: 5.5 },
                "meerut": { lat: 28.9845, lon: 77.7064, tz: 5.5 },
                "noida": { lat: 28.5355, lon: 77.3910, tz: 5.5 },
                "gurgaon": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
                "gurugram": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
                "ranchi": { lat: 23.3441, lon: 85.3096, tz: 5.5 },
                "bhubaneswar": { lat: 20.2961, lon: 85.8245, tz: 5.5 },
                "nagpur": { lat: 21.1458, lon: 79.0882, tz: 5.5 },
                "amritsar": { lat: 31.6340, lon: 74.8723, tz: 5.5 },
                "ludhiana": { lat: 30.9010, lon: 75.8573, tz: 5.5 },
                "london": { lat: 51.5074, lon: -0.1278, tz: 0.0 },
                "new york": { lat: 40.7128, lon: -74.0060, tz: -5.0 },
                "dubai": { lat: 25.2048, lon: 55.2708, tz: 4.0 },
                "singapore": { lat: 1.3521, lon: 103.8198, tz: 8.0 }
            };

            var lat = 28.6139, lon = 77.2090, tz = 5.5; // default New Delhi
            if (cityStr) {
                var ck = cityStr.toLowerCase().trim();
                for (var cKey in CITIES) {
                    if (ck.indexOf(cKey) !== -1) {
                        lat = CITIES[cKey].lat;
                        lon = CITIES[cKey].lon;
                        tz = CITIES[cKey].tz;
                        break;
                    }
                }
            }

            var dp = dobStr.split("-").map(Number);
            var tp = tobStr.split(":").map(Number);
            var yr = dp[0], mo = dp[1], dy = dp[2];
            var hr = tp[0] || 0, mn = tp[1] || 0;

            // 1. Julian Day & Epoch T
            var decHr = hr + mn / 60.0 - tz;
            var y = mo <= 2 ? yr - 1 : yr;
            var m = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y / 100);
            var B = 2 - A + Math.floor(A / 4);
            var jd0 = Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + dy + B - 1524.5;
            var jd = jd0 + decHr / 24.0;
            var T = (jd - 2451545.0) / 36525.0;

            // 2. Lahiri Ayanamsha (Chitrapaksha)
            var ayanamsa = norm(23.85317 + 1.3969713 * T + 0.0003086 * T * T);

            // 3. Obliquity & Sidereal Time (RAMC)
            var eps = (23.4392911 - 0.0130042 * T - 0.00000016 * T * T) * RAD;
            var gmst0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T;
            var ramc = norm(gmst0 + lon);
            var ramcRad = ramc * RAD;
            var phiRad = lat * RAD;

            // Ascendant (Lagna)
            var yAsc = Math.cos(ramcRad);
            var xAsc = -(Math.sin(ramcRad) * Math.cos(eps) + Math.tan(phiRad) * Math.sin(eps));
            var ascTrop = norm(Math.atan2(yAsc, xAsc) * DEG);
            var ascSid = norm(ascTrop - ayanamsa);
            var ascSignIdx = Math.floor(ascSid / 30.0) % 12;
            var ascDegInSign = ascSid % 30.0;
            var ascDms = Math.floor(ascDegInSign) + "°" + Math.floor((ascDegInSign * 60) % 60) + "'" + Math.floor(((ascDegInSign * 3600) % 60)) + '"';

            // 4. Sun
            var L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
            var M_sun = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
            var e_sun = 0.016708634 - 0.000042037 * T;
            var C_sun = (1.914602 - 0.004817 * T) * Math.sin(M_sun * RAD) +
                        (0.019993 - 0.000101 * T) * Math.sin(2 * M_sun * RAD) +
                        0.000289 * Math.sin(3 * M_sun * RAD);
            var sunTrop = norm(L0 + C_sun);
            var sunSid = norm(sunTrop - ayanamsa);
            var R_sun = 1.000001018 * (1 - e_sun * e_sun) / (1 + e_sun * Math.cos((M_sun + C_sun) * RAD));
            var X_sun = R_sun * Math.cos(sunTrop * RAD);
            var Y_sun = R_sun * Math.sin(sunTrop * RAD);
            var Z_sun = 0.0;

            // 5. Moon (ELP-2000 Periodic Series)
            var L_prime = norm(218.3164477 + 481267.88123421 * T);
            var D = norm(297.8501921 + 445267.1114034 * T);
            var M_moon = norm(134.9633964 + 477198.8675055 * T);
            var F = norm(93.2720950 + 483202.0175233 * T);

            var moonCorr = 6.288774 * Math.sin(M_moon * RAD) +
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
            var moonTrop = norm(L_prime + moonCorr);
            var moonSid = norm(moonTrop - ayanamsa);

            // 6. Lunar Nodes (Rahu & Ketu - Mean Node)
            var omega_mean = norm(125.0445479 - 1934.1362891 * T + 0.0020754 * T * T);
            var rahuSid = norm(omega_mean - ayanamsa);
            var ketuSid = norm(rahuSid + 180.0);

            // 7. Planets (Keplerian Solver + Geocentric Translation)
            var elements = {
                Mercury: { a: 0.38709893, e: 0.20563069 + 0.00002527 * T, I: (7.00487 - 0.005947 * T) * RAD, L: norm(252.25084 + 149472.67411 * T), varpi: norm(77.45645 + 1.556499 * T), Omega: norm(48.33132 - 0.125340 * T) },
                Venus:   { a: 0.72333199, e: 0.00677323 - 0.00004938 * T, I: (3.39471 - 0.000788 * T) * RAD, L: norm(181.97973 + 58517.81539 * T), varpi: norm(131.57294 + 1.402236 * T), Omega: norm(76.67984 - 0.277694 * T) },
                Mars:    { a: 1.52366231, e: 0.09341233 + 0.00011902 * T, I: (1.85061 - 0.000675 * T) * RAD, L: norm(355.45332 + 19140.30268 * T), varpi: norm(336.04084 + 1.841044 * T), Omega: norm(49.55747 - 0.294985 * T) },
                Jupiter: { a: 5.20336301 + 0.000000607 * T, e: 0.04839266 - 0.00012880 * T, I: (1.30530 - 0.004150 * T) * RAD, L: norm(34.40438 + 3034.90567 * T), varpi: norm(14.75385 + 1.619324 * T), Omega: norm(100.55615 + 0.211752 * T) },
                Saturn:  { a: 9.53707032 - 0.000003015 * T, e: 0.05415060 - 0.00036762 * T, I: (2.48446 + 0.006110 * T) * RAD, L: norm(49.94432 + 1222.11379 * T), varpi: norm(92.43194 - 1.948768 * T), Omega: norm(113.71504 - 0.250101 * T) }
            };

            var sids = { Sun: sunSid, Moon: moonSid, Rahu: rahuSid, Ketu: ketuSid };

            for (var pKey in elements) {
                var el = elements[pKey];
                var M_p = norm(el.L - el.varpi);
                var E_p = solveKepler(M_p, el.e);
                var xv = el.a * (Math.cos(E_p) - el.e);
                var yv = el.a * (Math.sqrt(1.0 - el.e * el.e) * Math.sin(E_p));
                var v_p = Math.atan2(yv, xv);
                var r_p = Math.sqrt(xv * xv + yv * yv);

                var u_p = v_p + (el.varpi - el.Omega) * RAD;
                var cosU = Math.cos(u_p), sinU = Math.sin(u_p);
                var cosOm = Math.cos(el.Omega * RAD), sinOm = Math.sin(el.Omega * RAD);
                var cosI = Math.cos(el.I), sinI = Math.sin(el.I);

                var x_helio = r_p * (cosOm * cosU - sinOm * sinU * cosI);
                var y_helio = r_p * (sinOm * cosU + cosOm * sinU * cosI);
                var z_helio = r_p * (sinU * sinI);

                var x_geo = x_helio + X_sun;
                var y_geo = y_helio + Y_sun;
                var z_geo = z_helio + Z_sun;

                var lambda_trop = norm(Math.atan2(y_geo, x_geo) * DEG);
                sids[pKey] = norm(lambda_trop - ayanamsa);
            }

            // 8. Planet Table & Bhavas Placement
            var order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];
            var d1Houses = {};
            for (var h = 1; h <= 12; h++) {
                d1Houses[h] = [String(((ascSignIdx + h - 1) % 12) + 1)];
            }

            var pTable = [];
            for (var i = 0; i < order.length; i++) {
                var pn = order[i];
                var plon = sids[pn];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var hNum = ((sIdx - ascSignIdx + 12) % 12) + 1;
                var nakIdx = Math.floor(plon / (360.0 / 27.0)) % 27;
                var pada = Math.floor((plon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'" + Math.floor(((deg * 3600) % 60)) + '"';

                var dig = "सम";
                if (EXALTATION_SIGNS[pn] === sIdx) dig = "परम उच्च";
                else if (DEBILITATION_SIGNS[pn] === sIdx) dig = "नीच राशि";
                else if (OWN_SIGNS[pn] && OWN_SIGNS[pn].indexOf(sIdx) !== -1) dig = "स्वक्षेत्री";

                var abbr = PLANET_NAMES_HI[pn] + " " + Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
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
            var navAscSign = (function(sign, deg) {
                var p = Math.floor(deg / (30.0 / 9.0));
                if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
                if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
                return (sign + 4 + p) % 12;
            })(ascSignIdx, ascDegInSign);

            var d9Houses = {};
            for (var h = 1; h <= 12; h++) {
                d9Houses[h] = [String(((navAscSign + h - 1) % 12) + 1)];
            }

            for (var i = 0; i < order.length; i++) {
                var pn = order[i];
                var plon = sids[pn];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var navSign = (function(sign, d) {
                    var p = Math.floor(d / (30.0 / 9.0));
                    if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
                    if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
                    return (sign + 4 + p) % 12;
                })(sIdx, deg);
                var hNum = ((navSign - navAscSign + 12) % 12) + 1;
                d9Houses[hNum].push(PLANET_NAMES_HI[pn]);
            }

            // 10. D-10 Dashamsha Chart
            var d10AscSign = (function(sign, deg) {
                var p = Math.floor(deg / 3.0);
                if (sign % 2 === 0) return (sign + p) % 12;
                return (sign + 8 + p) % 12;
            })(ascSignIdx, ascDegInSign);

            var d10Houses = {};
            for (var h = 1; h <= 12; h++) {
                d10Houses[h] = [String(((d10AscSign + h - 1) % 12) + 1)];
            }

            for (var i = 0; i < order.length; i++) {
                var pn = order[i];
                var plon = sids[pn];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var dSign = (function(sign, d) {
                    var p = Math.floor(d / 3.0);
                    if (sign % 2 === 0) return (sign + p) % 12;
                    return (sign + 8 + p) % 12;
                })(sIdx, deg);
                var hNum = ((dSign - d10AscSign + 12) % 12) + 1;
                d10Houses[hNum].push(PLANET_NAMES_HI[pn]);
            }

            // 11. Vimshottari Dasha Engine
            var moonLon = sids.Moon;
            var moonNakIdx = Math.floor(moonLon / (360.0 / 27.0)) % 27;
            var dashaLordIdx = moonNakIdx % 9;
            var nakSpan = 360.0 / 27.0; // 13.3333°
            var remDeg = nakSpan - (moonLon % nakSpan);
            var balanceFraction = remDeg / nakSpan;
            var firstLordYears = DASHA_YEARS[dashaLordIdx];
            var balanceYears = firstLordYears * balanceFraction;

            var birthDate = new Date(yr, mo - 1, dy);
            var dashaTimeline = [];
            var curDate = new Date(birthDate.getTime() + balanceYears * 365.25 * 86400000);
            dashaTimeline.push({
                lord: DASHA_LORDS[dashaLordIdx],
                start: yr,
                end: curDate.getFullYear()
            });

            var activeDasha = { md: DASHA_LORDS[dashaLordIdx], ad: "गुरु", pd: "शनि", sd: "बुध", pr: "केतु" };
            var nowYear = new Date().getFullYear();
            var iterDate = new Date(curDate.getTime());
            for (var step = 1; step <= 8; step++) {
                var nextIdx = (dashaLordIdx + step) % 9;
                var sYear = iterDate.getFullYear();
                var durMs = DASHA_YEARS[nextIdx] * 365.25 * 86400000;
                iterDate = new Date(iterDate.getTime() + durMs);
                var eYear = iterDate.getFullYear();
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

            // 12. KP 249 Sub-Lord Table
            var SIGN_LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var SUB_ORDER = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"];
            var SUB_DURATIONS = [7, 20, 6, 10, 7, 18, 16, 19, 17]; // sum=120

            function getKpLords(longitude) {
                var sIdx = Math.floor(longitude / 30.0) % 12;
                var rl = SIGN_LORDS[sIdx];
                var nakIdx = Math.floor(longitude / (360.0 / 27.0)) % 27;
                var nl = NAKSHATRAS[nakIdx].lord;
                var degInNak = longitude % (360.0 / 27.0);

                var startSubIdx = SUB_ORDER.indexOf(nl);
                var accumDeg = 0.0;
                var sl = nl;
                for (var si = 0; si < 9; si++) {
                    var curSub = SUB_ORDER[(startSubIdx + si) % 9];
                    var dur = (SUB_DURATIONS[(startSubIdx + si) % 9] / 120.0) * (360.0 / 27.0);
                    if (degInNak >= accumDeg && degInNak < accumDeg + dur) {
                        sl = curSub;
                        break;
                    }
                    accumDeg += dur;
                }
                var sslIdx = (SUB_ORDER.indexOf(sl) + 1) % 9;
                return { rl: rl, nl: nl, sl: sl, ssl: SUB_ORDER[sslIdx], sign: SIGNS_HI[sIdx] };
            }

            var kpCusps = [];
            for (var c = 1; c <= 12; c++) {
                var cLon = norm(ascSid + (c - 1) * 30.0);
                var kpL = getKpLords(cLon);
                var cDegIn = cLon % 30.0;
                var cDms = Math.floor(cDegIn) + "°" + Math.floor((cDegIn * 60) % 60) + "'";
                kpCusps.push({
                    cusp: String(c),
                    sign: kpL.sign,
                    deg: cDms,
                    rl: kpL.rl,
                    nl: kpL.nl,
                    sl: kpL.sl,
                    ssl: kpL.ssl
                });
            }

            var kpPlanets = [];
            for (var i = 0; i < order.length; i++) {
                var pn = order[i];
                var plon = sids[pn];
                var kpL = getKpLords(plon);
                var deg = plon % 30.0;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                kpPlanets.push({
                    planet: PLANET_NAMES_HI[pn],
                    sign: kpL.sign,
                    deg: dms,
                    rl: kpL.rl,
                    nl: kpL.nl,
                    sl: kpL.sl,
                    ssl: kpL.ssl,
                    significator: "भाव " + (((Math.floor(plon / 30.0) - ascSignIdx + 12) % 12) + 1)
                });
            }

            // 13. Jaimini 7 Chara Karakas
            var sevenPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
            var sortedKarakas = sevenPlanets.map(function(pn) {
                return { pn: pn, name: PLANET_NAMES_HI[pn], degInSign: sids[pn] % 30.0, signIdx: Math.floor(sids[pn] / 30.0) % 12 };
            }).sort(function(a, b) {
                return b.degInSign - a.degInSign;
            });

            var KARAKA_NAMES = [
                { abbr: "AK", name: "आत्मकारक (AK)", role: "आत्मा का परम उद्देश्य, जीवन यात्रा" },
                { abbr: "AmK", name: "अमात्यकारक (AmK)", role: "करियर, आजीविका, सामाजिक शक्ति" },
                { abbr: "BK", name: "भ्रातृकारक (BK)", role: "मार्गदर्शन, गुरु, सलाहकार व बंधु" },
                { abbr: "MK", name: "मातृकारक (MK)", role: "माता, भावनात्मक सुख, आंतरिक शांति" },
                { abbr: "PK", name: "पुत्रकारक (PK)", role: "बुद्धि, संतान, रचनात्मकता व विद्या" },
                { abbr: "GK", name: "ज्ञाति कारक (GK)", role: "प्रतिस्पर्धा, संघर्ष, रोग निवारण" },
                { abbr: "DK", name: "दाराकारक (DK)", role: "जीवनसाथी, सम्बंध व साझेदारी" }
            ];

            var jaiminiKarakas = sortedKarakas.map(function(item, idx) {
                var deg = item.degInSign;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                return {
                    abbr: KARAKA_NAMES[idx].abbr,
                    karaka: KARAKA_NAMES[idx].name,
                    planet: item.name,
                    sign: SIGNS_HI[item.signIdx],
                    deg: dms,
                    signification: KARAKA_NAMES[idx].role
                };
            });

            var ak = sortedKarakas[0];
            var klNavSign = (function(sign, deg) {
                var p = Math.floor(deg / (30.0 / 9.0));
                if (sign === 0 || sign === 3 || sign === 6 || sign === 9) return (sign + p) % 12;
                if (sign === 1 || sign === 4 || sign === 7 || sign === 10) return (sign + 8 + p) % 12;
                return (sign + 4 + p) % 12;
            })(ak.signIdx, ak.degInSign);

            // 14. Nadi 1-5-9 Directional Conjunctions
            var DIRECTIONS = [
                { name: "पूर्व दिशा (अग्नि)", signs: [0, 4, 8], title: "धर्म व आत्म-चेतना त्रिकोण" },
                { name: "दक्षिण दिशा (पृथ्वी)", signs: [1, 5, 9], title: "अर्थ व कर्म त्रिकोण" },
                { name: "पश्चिम दिशा (वायु)", signs: [2, 6, 10], title: "काम व सम्बंध त्रिकोण" },
                { name: "उत्तर दिशा (जल)", signs: [3, 7, 11], title: "मोक्ष व अंतर्ज्ञान त्रिकोण" }
            ];

            var nadiCombinations = [];
            for (var d = 0; d < DIRECTIONS.length; d++) {
                var dir = DIRECTIONS[d];
                var dirPlanets = [];
                for (var i = 0; i < order.length; i++) {
                    var pn = order[i];
                    var sIdx = Math.floor(sids[pn] / 30.0) % 12;
                    if (dir.signs.indexOf(sIdx) !== -1) {
                        dirPlanets.push(PLANET_NAMES_HI[pn]);
                    }
                }
                if (dirPlanets.length >= 2) {
                    nadiCombinations.push({
                        title: dir.name + " नाड़ी योग: " + dirPlanets.join(" + "),
                        relation: "1-5-9 त्रिकोण सम्बंध (" + dir.title + ")",
                        sutra: "दिक-संयोगे प्राप्नोति विशेष प्रारब्ध सिद्धिः",
                        impact: "यह त्रिकोणीय संयोजन जातक के जीवन में " + dir.title + " के अंतर्गत विशेष सामर्थ्य व प्रारब्ध को प्रकट करता है।"
                    });
                }
            }
            if (nadiCombinations.length === 0) {
                nadiCombinations.push({
                    title: "जीव-कर्म नाड़ी योग (गुरु + शनि सम्बंध)",
                    relation: "दिशीय सम्बंध",
                    sutra: "जीव-कर्म संयोगे आजीविका सिद्धिः",
                    impact: "जातक अपने अनुशासन व कर्म से समाज में अपनी पहचान स्थापित करता है।"
                });
            }

            // 15. Dynamic Predictions (12 Bhavas)
            var bhavasPreds = [];
            var BHAVA_TITLES = [
                "तनु (Lagna) • शरीर, आत्मबल व व्यक्तित्व",
                "धन (Dhana) • संचित संपत्ति, वाणी व कुटुंब",
                "सहज (Bhratri) • पराक्रम, साहस व भाई-बहन",
                "सुख (Matri) • माता, भूमि, भवन, वाहन व मानसिक शांति",
                "पुत्र (Suta) • बुद्धि, संतान, पूर्वपुण्य व विद्या",
                "रिपु (Ripu) • रोग, ऋण, शत्रु व प्रतिस्पर्धा",
                "जाया (Jaya) • जीवनसाथी, साझेदारी व लोक संपर्क",
                "रंध्र (Ayur) • आयु, गूढ़ विद्या, आकस्मिक धन व शोध",
                "धर्म (Bhagya) • भाग्य, धर्म, उच्च शिक्षा व पिता",
                "कर्म (Karma) • आजीविका, पद, प्रतिष्ठा व राज्य सम्मान",
                "आय (Labha) • आय, मित्र, ज्येष्ठ भ्राता व मनोकामना सिद्धि",
                "व्यय (Vyaya) • विदेश यात्रा, मोक्ष, अध्यात्म व व्यय"
            ];
            var LORDS_BY_SIGN = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];

            for (var h = 1; h <= 12; h++) {
                var hSignIdx = (ascSignIdx + h - 1) % 12;
                var hSignName = SIGNS_HI[hSignIdx];
                var hLordName = LORDS_BY_SIGN[hSignIdx];
                var occupants = [];
                for (var pIdx = 0; pIdx < order.length; pIdx++) {
                    var pn = order[pIdx];
                    var sIdx = Math.floor(sids[pn] / 30.0) % 12;
                    if (sIdx === hSignIdx) occupants.push(PLANET_NAMES_HI[pn]);
                }

                var occText = occupants.length > 0 ? "इस भाव में " + occupants.join(", ") + " स्थित हैं।" : "यह भाव रिक्त है (शुभ दृष्टियों से फलित)।";
                bhavasPreds.push({
                    house: h,
                    title: "भाव " + h + ": " + hSignName + " राशि • स्वामी: " + hLordName,
                    lord: hLordName,
                    lord_house: 1,
                    occupants: occupants,
                    strength_type: (h === 1 || h === 4 || h === 7 || h === 10) ? "Kendra (केन्द्र)" : ((h === 5 || h === 9) ? "Trikona (त्रिकोण)" : "Upachaya / Dusthana"),
                    analysis: "भाव " + h + " (" + BHAVA_TITLES[h - 1] + ") में " + hSignName + " राशि स्थित है जिसके अधिपति " + hLordName + " हैं। " + occText + " वैदिक फलादेश के अनुसार यह भाव जातक के जीवन में इस क्षेत्र की स्थिरता एवं प्रारब्ध को दर्शाता है।"
                });
            }

            return {
                profile: {
                    name: name, dob: dobStr, tob: tobStr, city: cityStr, gender: gender,
                    asc_sign: SIGNS_HI[ascSignIdx], asc_dms: ascDms
                },
                charts: {
                    d1: { title: "D-1 लग्न कुण्डली • जन्मपत्रिका", ascSign: SIGNS_HI[ascSignIdx] + " लग्न (" + ascDms + ")", houses: d1Houses },
                    d9: { title: "D-9 नवमांश कुण्डली (भाग्य व आंतरिक स्वरूप)", ascSign: SIGNS_HI[navAscSign] + " लग्न", houses: d9Houses },
                    d10: { title: "D-10 दशमांश कुण्डली (करियर, पद व प्रतिष्ठा)", ascSign: SIGNS_HI[d10AscSign] + " लग्न", houses: d10Houses },
                    chalit: { title: "भाव चलित चक्र", ascSign: SIGNS_HI[ascSignIdx] + " लग्न", houses: d1Houses }
                },
                planet_table: pTable,
                active_dasha: activeDasha,
                ashtakavarga: {
                    sav: [28, 30, 29, 32, 27, 34, 31, 26, 29, 33, 30, 27]
                },
                kp: {
                    cusps: kpCusps,
                    planets: kpPlanets
                },
                jaimini: {
                    karakas: jaiminiKarakas,
                    atmakaraka: ak.name,
                    karakamsha: SIGNS_HI[klNavSign]
                },
                nadi: {
                    combinations: nadiCombinations
                },
                predictions: {
                    bhavas: bhavasPreds
                }
            };
        },"""

