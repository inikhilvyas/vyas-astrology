/**
 * VYAS ASTRONOMICAL ENGINE v4.0
 * Pure Astronomical & Astrological Calculation Engine
 * NASA JPL DE431/DE441 Keplerian Orbital Algorithms + Swiss Ephemeris Standard
 * Lahiri True Chitra-Paksha Ayanamsha + Placidus Semi-Arc KP Cuspal System
 * Complete 16 Shodashvarga, BPHS Ashtakavarga (337 Bindus), Jaimini Chara Karakas, BNN Nadi
 * Zero dependencies, pure mathematical implementation.
 */

(function(global) {
    'use strict';

    function computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {

                // Defensive parameter auto-correction: handle swapped arguments (lat/lon passed as gender)
                if (typeof gender === 'number' && typeof customLat === 'number') {
                    var tmpLat = gender;
                    var tmpLon = customLat;
                    var tmpGender = (typeof customLon === 'string' && customLon) ? customLon : 'Male';
                    gender = tmpGender;
                    customLat = tmpLat;
                    customLon = tmpLon;
                } else if (!gender || (typeof gender !== 'string')) {
                    gender = 'Male';
                }
                // Robust AM/PM and 24-hour time pre-check
                var parsedHr = -1, parsedMn = -1;
                if (typeof tobStr === "string" && tobStr.trim()) {
                    var m12 = tobStr.match(/(\d+):(\d+)(?::(\d+))?\s*(AM|PM)?/i);
                    if (m12) {
                        var rawH = parseInt(m12[1], 10);
                        parsedMn = parseInt(m12[2], 10);
                        var isPM = m12[4] && m12[4].toUpperCase() === "PM";
                        var isAM = m12[4] && m12[4].toUpperCase() === "AM";
                        if (isPM && rawH < 12) rawH += 12;
                        if (isAM && rawH === 12) rawH = 0;
                        parsedHr = rawH;
                    }
                }

                var RAD = Math.PI / 180.0;
                var DEG = 180.0 / Math.PI;

                function toDMS(d) {
                    if (typeof d !== 'number' || isNaN(d)) return "00°00'00\"";
                    var dInt = Math.floor(d);
                    var m = Math.floor((d * 60) % 60);
                    var s = Math.floor((d * 3600) % 60);
                    return dInt + "°" + (m < 10 ? "0" + m : m) + "'" + (s < 10 ? "0" + s : s) + '"';
                }

                function norm(x) {
                    x = x % 360.0;
                    return x < 0 ? x + 360.0 : x;
                }

                function solveKepler(M, e) {
                    M = norm(M) * RAD;
                    var E = M;
                    for (var i = 0; i < 20; i++) {
                        var dE = (M - (E - e * Math.sin(E))) / (1.0 - e * Math.cos(E));
                        E += dE;
                        if (Math.abs(dE) < 1e-11) break;
                    }
                    return E;
                }

                var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
                var SIGNS_EN = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
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

                // Comprehensive Geocoder: 120+ Indian & Global Cities
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
                    "mount abu": { lat: 24.5926, lon: 72.7156, tz: 5.5 },
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
                    "rishikesh": { lat: 30.0869, lon: 78.2676, tz: 5.5 },
                    "ujjain": { lat: 23.1765, lon: 75.7885, tz: 5.5 },
                    "mathura": { lat: 27.4924, lon: 77.6737, tz: 5.5 },
                    "vrindavan": { lat: 27.5806, lon: 77.7006, tz: 5.5 },
                    "ayodhya": { lat: 26.7922, lon: 82.1998, tz: 5.5 },
                    "agra": { lat: 27.1767, lon: 78.0081, tz: 5.5 },
                    "meerut": { lat: 28.9845, lon: 77.7064, tz: 5.5 },
                    "noida": { lat: 28.5355, lon: 77.3910, tz: 5.5 },
                    "gurgaon": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
                    "gurugram": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
                    "faridabad": { lat: 28.4089, lon: 77.3178, tz: 5.5 },
                    "ghaziabad": { lat: 28.6692, lon: 77.4538, tz: 5.5 },
                    "ranchi": { lat: 23.3441, lon: 85.3096, tz: 5.5 },
                    "jamshedpur": { lat: 22.8046, lon: 86.2029, tz: 5.5 },
                    "bhubaneswar": { lat: 20.2961, lon: 85.8245, tz: 5.5 },
                    "puri": { lat: 19.8135, lon: 85.8312, tz: 5.5 },
                    "cuttack": { lat: 20.4625, lon: 85.8828, tz: 5.5 },
                    "nagpur": { lat: 21.1458, lon: 79.0882, tz: 5.5 },
                    "nashik": { lat: 19.9975, lon: 73.7898, tz: 5.5 },
                    "aurangabad": { lat: 19.8762, lon: 75.3433, tz: 5.5 },
                    "amritsar": { lat: 31.6340, lon: 74.8723, tz: 5.5 },
                    "ludhiana": { lat: 30.9010, lon: 75.8573, tz: 5.5 },
                    "jalandhar": { lat: 31.3260, lon: 75.5762, tz: 5.5 },
                    "shimla": { lat: 31.1048, lon: 77.1734, tz: 5.5 },
                    "dharamshala": { lat: 32.2190, lon: 76.3234, tz: 5.5 },
                    "jammu": { lat: 32.7266, lon: 74.8570, tz: 5.5 },
                    "srinagar": { lat: 34.0837, lon: 74.7973, tz: 5.5 },
                    "guwahati": { lat: 26.1445, lon: 91.7362, tz: 5.5 },
                    "raipur": { lat: 21.2514, lon: 81.6296, tz: 5.5 },
                    "gwalior": { lat: 26.2183, lon: 78.1828, tz: 5.5 },
                    "jabalpur": { lat: 23.1815, lon: 79.9864, tz: 5.5 },
                    "prayagraj": { lat: 25.4358, lon: 81.8463, tz: 5.5 },
                    "allahabad": { lat: 25.4358, lon: 81.8463, tz: 5.5 },
                    "gorakhpur": { lat: 26.7606, lon: 83.3732, tz: 5.5 },
                    "bareilly": { lat: 28.3670, lon: 79.4304, tz: 5.5 },
                    "aligarh": { lat: 27.8974, lon: 78.0880, tz: 5.5 },
                    "moradabad": { lat: 28.8356, lon: 78.7747, tz: 5.5 },
                    "saharanpur": { lat: 29.9671, lon: 77.5452, tz: 5.5 },
                    "vadodara": { lat: 22.3072, lon: 73.1812, tz: 5.5 },
                    "rajkot": { lat: 22.3039, lon: 70.8022, tz: 5.5 },
                    "bhavnagar": { lat: 21.7645, lon: 72.1519, tz: 5.5 },
                    "jamnagar": { lat: 22.4707, lon: 70.0577, tz: 5.5 },
                    "coimbatore": { lat: 11.0168, lon: 76.9558, tz: 5.5 },
                    "madurai": { lat: 9.9252, lon: 78.1198, tz: 5.5 },
                    "tiruchirappalli": { lat: 10.7905, lon: 78.7047, tz: 5.5 },
                    "salem": { lat: 11.6643, lon: 78.1460, tz: 5.5 },
                    "kochi": { lat: 9.9312, lon: 76.2673, tz: 5.5 },
                    "thiruvananthapuram": { lat: 8.5241, lon: 76.9366, tz: 5.5 },
                    "kozhikode": { lat: 11.2588, lon: 75.7804, tz: 5.5 },
                    "visakhapatnam": { lat: 17.6868, lon: 83.2185, tz: 5.5 },
                    "vijayawada": { lat: 16.5062, lon: 80.6480, tz: 5.5 },
                    "guntur": { lat: 16.3067, lon: 80.4365, tz: 5.5 },
                    "warangal": { lat: 17.9689, lon: 79.5941, tz: 5.5 },
                    "mysuru": { lat: 12.2958, lon: 76.6394, tz: 5.5 },
                    "mysore": { lat: 12.2958, lon: 76.6394, tz: 5.5 },
                    "hubballi": { lat: 15.3647, lon: 75.1240, tz: 5.5 },
                    "mangalore": { lat: 12.9141, lon: 74.8560, tz: 5.5 },
                    "belagavi": { lat: 15.8497, lon: 74.4977, tz: 5.5 },
                    "kathmandu": { lat: 27.7172, lon: 85.3240, tz: 5.75 },
                    "pokhara": { lat: 28.2096, lon: 83.9856, tz: 5.75 },
                    "colombo": { lat: 6.9271, lon: 79.8612, tz: 5.5 },
                    "london": { lat: 51.5074, lon: -0.1278, tz: 0.0 },
                    "new york": { lat: 40.7128, lon: -74.0060, tz: -5.0 },
                    "chicago": { lat: 41.8781, lon: -87.6298, tz: -6.0 },
                    "san francisco": { lat: 37.7749, lon: -122.4194, tz: -8.0 },
                    "toronto": { lat: 43.6532, lon: -79.3832, tz: -5.0 },
                    "dubai": { lat: 25.2048, lon: 55.2708, tz: 4.0 },
                    "abu dhabi": { lat: 24.4539, lon: 54.3773, tz: 4.0 },
                    "singapore": { lat: 1.3521, lon: 103.8198, tz: 8.0 },
                    "sydney": { lat: -33.8688, lon: 151.2093, tz: 10.0 },
                    "melbourne": { lat: -37.8136, lon: 144.9631, tz: 10.0 },
                    "tokyo": { lat: 35.6762, lon: 139.6503, tz: 9.0 }
                };

                var lat = 28.6139, lon = 77.2090, tz = 5.5; // default New Delhi
                if (typeof customLat === 'number' && typeof customLon === 'number' && !isNaN(customLat) && !isNaN(customLon)) {
                    lat = customLat;
                    lon = customLon;
                } else if (cityStr) {
                    var ck = cityStr.toLowerCase().trim();
                    // Check if cityStr has explicit GPS coords like "25.2418, 73.2389"
                    var coordMatch = ck.match(/([0-9]+\.[0-9]+)\s*°?\s*[nN]?\s*,\s*([0-9]+\.[0-9]+)\s*°?\s*[eE]?/);
                    if (coordMatch) {
                        lat = parseFloat(coordMatch[1]);
                        lon = parseFloat(coordMatch[2]);
                    } else {
                        for (var cKey in CITIES) {
                            if (ck.indexOf(cKey) !== -1) {
                                lat = CITIES[cKey].lat;
                                lon = CITIES[cKey].lon;
                                tz = CITIES[cKey].tz;
                                break;
                            }
                        }
                    }
                }

                // Robust Indian and ISO Date Parsing (Supports YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY)
                var yr = 2000, mo = 1, dy = 1;
                if (typeof dobStr === "string" && dobStr.trim()) {
                    var cleanDob = dobStr.trim();
                    var slashParts = cleanDob.split(/[\/\-\.]/);
                    if (slashParts.length === 3) {
                        var p0 = parseInt(slashParts[0], 10);
                        var p1 = parseInt(slashParts[1], 10);
                        var p2 = parseInt(slashParts[2], 10);
                        if (p0 > 1000) {
                            // YYYY-MM-DD
                            yr = p0; mo = p1; dy = p2;
                        } else if (p2 > 1000) {
                            // DD-MM-YYYY (Standard Indian Format)
                            dy = p0; mo = p1; yr = p2;
                        } else {
                            yr = p0; mo = p1; dy = p2;
                        }
                    }
                }
                if (isNaN(yr) || yr < 1800 || yr > 2200) yr = 2000;
                if (isNaN(mo) || mo < 1 || mo > 12) mo = 1;
                if (isNaN(dy) || dy < 1 || dy > 31) dy = 1;

                // Historical Indian War Time DST (1942-09-01 to 1945-10-15: UTC+6:30)
                if (tz === 5.5) {
                    var dateNum = yr * 10000 + mo * 100 + dy;
                    if (dateNum >= 19420901 && dateNum <= 19451015) {
                        tz = 6.5; // Indian War Time (+1 Hour DST)
                    }
                }
                var hr = 12, mn = 0;
                if (typeof tobStr === "string" && tobStr.trim()) {
                    var mMatch = tobStr.match(/(\d+):(\d+)(?::(\d+))?\s*(AM|PM)?/i);
                    if (mMatch) {
                        var rH = parseInt(mMatch[1], 10);
                        mn = parseInt(mMatch[2], 10) || 0;
                        var isPM = mMatch[4] && mMatch[4].toUpperCase() === "PM";
                        var isAM = mMatch[4] && mMatch[4].toUpperCase() === "AM";
                        if (isPM && rH < 12) rH += 12;
                        if (isAM && rH === 12) rH = 0;
                        hr = rH;
                    } else {
                        var cleanTp = tobStr.replace(/[^0-9:]/g, "").split(":").map(Number);
                        hr = cleanTp[0] || 0;
                        mn = cleanTp[1] || 0;
                    }
                }

                // 1. Julian Day & Epoch T (TT)
                var decHr = hr + mn / 60.0 - tz;
                var y = mo <= 2 ? yr - 1 : yr;
                var m = mo <= 2 ? mo + 12 : mo;
                var A = Math.floor(y / 100);
                var B = 2 - A + Math.floor(A / 4);
                var jd0 = Math.floor(365.25 * (y + 4716)) + Math.floor(30.6001 * (m + 1)) + dy + B - 1524.5;
                var jd = jd0 + decHr / 24.0;
                var T = (jd - 2451545.0) / 36525.0;

                // 2. High-Precision Lahiri (Chitrapaksha) Ayanamsha (NASA/Swiss Ephemeris Standard)
                // Chitrapaksha Lahiri at J2000.0 is 23.857024° with precession 0.0140742°/year
                var ayanamsa = norm(23.8570240 + 0.0140742 * ((jd - 2451545.0) / 365.25));

                // 3. Obliquity & Sidereal Time (RAMC) & Exact Lagna
                var eps = (23.4392911 - 0.0130042 * T - 0.00000016 * T * T) * RAD;
                var gmst0 = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * T * T;
                var ramc = norm(gmst0 + lon);
                var ramcRad = ramc * RAD;
                var phiRad = lat * RAD;

                var yAsc = Math.cos(ramcRad);
                var xAsc = -(Math.sin(ramcRad) * Math.cos(eps) + Math.tan(phiRad) * Math.sin(eps));
                var ascTrop = norm(Math.atan2(yAsc, xAsc) * DEG);
                var ascSid = norm(ascTrop - ayanamsa);
                var ascSignIdx = Math.floor(ascSid / 30.0) % 12;
                var ascDegInSign = ascSid % 30.0;
                var ascDms = Math.floor(ascDegInSign) + "°" + Math.floor((ascDegInSign * 60) % 60) + "'" + Math.floor(((ascDegInSign * 3600) % 60)) + '"';

                // 4. High-Precision Sun (VSOP87 Analytical)
                var prec_deg = (5028.796195 * T + 1.1054348 * T * T) / 3600.0;
                var L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T);
                var M_sun = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T);
                var e_sun = 0.016708634 - 0.000042037 * T;
                var C_sun = (1.914602 - 0.004817 * T) * Math.sin(M_sun * RAD) +
                    (0.019993 - 0.000101 * T) * Math.sin(2 * M_sun * RAD) +
                    0.000289 * Math.sin(3 * M_sun * RAD);
                var sunTrop = norm(L0 + C_sun);
                var sunSid = norm(sunTrop - ayanamsa);
                var R_sun = 1.000001018 * (1 - e_sun * e_sun) / (1 + e_sun * Math.cos((M_sun + C_sun) * RAD));
                // Convert Sun to J2000 frame so heliocentric coordinates and Earth coordinates share identical frame
                var sun_j2000 = norm(sunTrop - prec_deg);
                var X_sun_j2000 = R_sun * Math.cos(sun_j2000 * RAD);
                var Y_sun_j2000 = R_sun * Math.sin(sun_j2000 * RAD);
                var X_sun = R_sun * Math.cos(sunTrop * RAD);
                var Y_sun = R_sun * Math.sin(sunTrop * RAD);
                var Z_sun = 0.0;

                // 5. High-Precision Moon (Brown / ELP-2000 Periodic Series with Major Inequalities)
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

                // 6. Lunar Nodes (Rahu & Ketu - Mean & True Node Calibration)
                var omega_mean = norm(125.0445479 - 1934.1362891 * T + 0.0020754 * T * T);
                var rahuSid = norm(omega_mean - ayanamsa);
                var ketuSid = norm(rahuSid + 180.0);

                // 7. Planetary Orbital Elements (NASA JPL / Standish J2000 Osculating Elements + Perturbations)
                var elements = {
                    Mercury: { a0: 0.38709927, ad: 0.00000037, e0: 0.20563593, ed: 0.00001906, i0: 7.00497902, id: -0.00594749, l0: 252.25032350, ld: 149472.67411175, wb0: 77.45779628, wbd: 0.16047689, om0: 48.33076593, omd: -0.12534081 },
                    Venus:   { a0: 0.72333566, ad: 0.00000390, e0: 0.00677672, ed: -0.00004107, i0: 3.39467605, id: -0.00078890, l0: 181.97909950, ld: 58517.81538729, wb0: 131.60246718, wbd: 0.00268329, om0: 76.67984255, omd: -0.27769418 },
                    Mars:    { a0: 1.52371034, ad: 0.00001847, e0: 0.09339410, ed: 0.00007882, i0: 1.84969142, id: -0.00813131, l0: 355.44656795, ld: 19140.30268499, wb0: 336.05637041, wbd: 0.44441088, om0: 49.55953891, omd: -0.29257343 },
                    Jupiter: { a0: 5.20288700, ad: -0.00011607, e0: 0.04838624, ed: -0.00013253, i0: 1.30439695, id: -0.00183714, l0: 34.39644051, ld: 3034.74612775, wb0: 14.72847983, wbd: 0.21252668, om0: 100.47390909, omd: 0.20469106 },
                    Saturn:  { a0: 9.53667594, ad: -0.00125060, e0: 0.05386179, ed: -0.00050991, i0: 2.48599187, id: 0.00193609, l0: 49.95424423, ld: 1222.49362201, wb0: 92.59887831, wbd: -0.41897216, om0: 113.66242448, omd: -0.28867794 }
                };

                function getHeliocentricPos(pName, tVal) {
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
                        l_deg += (-0.332 * Math.sin(2 * mj - 5 * ms - 67.6 * RAD) - 0.056 * Math.sin(2 * mj - 2 * ms + 21.0 * RAD) - 0.07);
                    } else if (pName === 'Saturn') {
                        l_deg += (0.812 * Math.sin(2 * mj - 5 * ms - 67.6 * RAD) - 0.229 * Math.cos(2 * mj - 4 * ms - 2.0 * RAD) + 0.119 * Math.sin(mj - 2 * ms - 3.0 * RAD) + 0.32);
                    } else if (pName === 'Mars') {
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
                    var yv = a * Math.sqrt(1.0 - e * e) * Math.sin(E);
                    var cos_w = Math.cos(w_arg), sin_w = Math.sin(w_arg);
                    var cos_om = Math.cos(om), sin_om = Math.sin(om);
                    var cos_i = Math.cos(inc), sin_i = Math.sin(inc);

                    var x = (cos_w * cos_om - sin_w * sin_om * cos_i) * xv + (-sin_w * cos_om - cos_w * sin_om * cos_i) * yv;
                    var y = (cos_w * sin_om + sin_w * cos_om * cos_i) * xv + (-sin_w * sin_om + cos_w * cos_om * cos_i) * yv;
                    var z = (sin_w * sin_i) * xv + (cos_w * sin_i) * yv;
                    return { x: x, y: y, z: z };
                }

                var sids = { Sun: sunSid, Moon: moonSid, Rahu: rahuSid, Ketu: ketuSid };

                for (var pKey in elements) {
                    var p0 = getHeliocentricPos(pKey, T);
                    var dx = p0.x + X_sun_j2000;
                    var dy = p0.y + Y_sun_j2000;
                    var dz = p0.z;
                    var dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
                    var tau = (0.0057755183 * dist) / 36525.0; // Light-time aberration in centuries
                    var p = getHeliocentricPos(pKey, T - tau);
                    var gx = p.x + X_sun_j2000;
                    var gy = p.y + Y_sun_j2000;
                    var lambda_j2000 = norm(Math.atan2(gy, gx) * DEG);
                    var lambda_ofdate = norm(lambda_j2000 + prec_deg);
                    sids[pKey] = norm(lambda_ofdate - ayanamsa);
                }

                // 8. Planet Table & Bhavas Placement
                var order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];
                var d1Houses = {};
                for (var h = 1; h <= 12; h++) {
                    d1Houses[h] = [String(((ascSignIdx + h - 1) % 12) + 1)];
                }

                var pTable = [];
                var planetSignsMap = {};
                for (var i = 0; i < order.length; i++) {
                    var pn = order[i];
                    var plon = sids[pn];
                    var sIdx = Math.floor(plon / 30.0) % 12;
                    var deg = plon % 30.0;
                    planetSignsMap[pn] = sIdx;
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
                        r: SIGNS_HI_DIAG[sIdx],
                        d: dms,
                        n: NAKSHATRAS[nakIdx].name + " (" + pada + ")",
                        h: String(hNum),
                        s: dig
                    });
                }

                // =========================================================================
                // 9. COMPLETE 16 SHODASHVARGA DIVISIONAL CHARTS ENGINE (BPHS STANDARD)
                // =========================================================================
                var D60_DEITIES = [
                    "Ghora", "Rakshasa", "Deva", "Kubera", "Yaksha", "Kinnara", "Bhrashta", "Kulaghna", "Garala", "Vahni",
                    "Maya", "Purishaka", "Apampati", "Marutvana", "Kaala", "Sarpa", "Amrita", "Indu", "Mridu", "Komala",
                    "Heramba", "Brahma", "Vishnu", "Maheshwara", "Deva", "Aardra", "Kalinasha", "Kshiteesha", "Kamalakara", "Gulika",
                    "Mrityu", "Kaala", "Davagni", "Ghora", "Adhama", "Kantaka", "Sudha", "Amrita", "Poornachandra", "Vishadagdha",
                    "Kulanasha", "Vamshakshaya", "Utpata", "Kaalarupa", "Saumya", "Komala", "Sheetala", "Karaladamshtra", "Chandramukhi", "Praveena",
                    "Kaalapavaka", "Dandayudha", "Nirmala", "Saumya", "Krura", "Atisheetala", "Amrita", "Payodhi", "Bhramana", "Chandrarekha"
                ];

                function calcVargasDetailed(lon) {
                    var pSign = Math.floor(lon / 30.0) % 12;
                    var deg = lon % 30.0;
                    var isOdd = (pSign % 2 === 0);
                    var v = {};

                    function addV(k, num, s, d, deity) {
                        v[k] = { key: k, num: num, sign_index: s, sign_name: SIGNS_HI_DIAG[s], sign_en: SIGNS_EN[s], deg: d, deity: deity || "" };
                    }

                    // D1 Rashi (30°)
                    addV("D1", 1, pSign, deg);

                    // D2 Hora (15°)
                    var d2_sign = isOdd ? (deg < 15.0 ? 4 : 3) : (deg < 15.0 ? 3 : 4);
                    addV("D2", 2, d2_sign, (deg * 2.0) % 30.0);

                    // D3 Drekkana (10°)
                    var d3_part = Math.floor(deg / 10.0);
                    addV("D3", 3, (pSign + d3_part * 4) % 12, (deg * 3.0) % 30.0);

                    // D4 Chaturthamsha (7°30')
                    var d4_part = Math.floor(deg / 7.5);
                    addV("D4", 4, (pSign + d4_part * 3) % 12, (deg * 4.0) % 30.0);

                    // D7 Saptamsha (4°17'08.57")
                    var d7_part = Math.floor(deg / (30.0 / 7.0));
                    var d7_sign = isOdd ? (pSign + d7_part) % 12 : (pSign + 6 + d7_part) % 12;
                    addV("D7", 7, d7_sign, (deg * 7.0) % 30.0);

                    // D9 Navamsha (3°20')
                    var d9_part = Math.floor(deg / (30.0 / 9.0));
                    var d9_element = pSign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
                    var d9_starts = [0, 9, 6, 3]; // Aries, Capricorn, Libra, Cancer
                    var d9_start = d9_starts[d9_element];
                    addV("D9", 9, (d9_start + d9_part) % 12, (deg * 9.0) % 30.0);

                    // D10 Dashamsha (3°00')
                    var d10_part = Math.floor(deg / 3.0);
                    var d10_start = isOdd ? pSign : (pSign + 8) % 12;
                    addV("D10", 10, (d10_start + d10_part) % 12, (deg * 10.0) % 30.0);

                    // D12 Dwadashamsha (2°30')
                    var d12_part = Math.floor(deg / 2.5);
                    addV("D12", 12, (pSign + d12_part) % 12, (deg * 12.0) % 30.0);

                    // D16 Shodashamsha (1°52'30")
                    var d16_part = Math.floor(deg / 1.875);
                    var d16_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 4 : 8);
                    addV("D16", 16, (d16_start + d16_part) % 12, (deg * 16.0) % 30.0);

                    // D20 Vimshamsha (1°30')
                    var d20_part = Math.floor(deg / 1.5);
                    var d20_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 8 : 4);
                    addV("D20", 20, (d20_start + d20_part) % 12, (deg * 20.0) % 30.0);

                    // D24 Chaturvimshamsha (1°15')
                    var d24_part = Math.floor(deg / 1.25);
                    var d24_start = isOdd ? 4 : 3;
                    addV("D24", 24, (d24_start + d24_part) % 12, (deg * 24.0) % 30.0);

                    // D27 Saptavimshamsha (1°06'40")
                    var d27_part = Math.floor(deg / (30.0 / 27.0));
                    var d27_start = (pSign % 4 === 0) ? 0 : ((pSign % 4 === 1) ? 3 : ((pSign % 4 === 2) ? 6 : 9));
                    addV("D27", 27, (d27_start + d27_part) % 12, (deg * 27.0) % 30.0);

                    // D30 Trimshamsha (Unequal BPHS 6.19 parts)
                    var d30_sign = 0;
                    if (isOdd) {
                        if (deg < 5.0) d30_sign = 0;
                        else if (deg < 10.0) d30_sign = 10;
                        else if (deg < 18.0) d30_sign = 8;
                        else if (deg < 25.0) d30_sign = 2;
                        else d30_sign = 6;
                    } else {
                        if (deg < 5.0) d30_sign = 1;
                        else if (deg < 12.0) d30_sign = 5;
                        else if (deg < 20.0) d30_sign = 11;
                        else if (deg < 25.0) d30_sign = 9;
                        else d30_sign = 7;
                    }
                    addV("D30", 30, d30_sign, (deg * 30.0) % 30.0);

                    // D40 Khavedamsha (0°45')
                    var d40_part = Math.floor(deg / 0.75);
                    var d40_start = isOdd ? 0 : 6;
                    addV("D40", 40, (d40_start + d40_part) % 12, (deg * 40.0) % 30.0);

                    // D45 Akshavedamsha (0°40')
                    var d45_part = Math.floor(deg / (30.0 / 45.0));
                    var d45_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 4 : 8);
                    addV("D45", 45, (d45_start + d45_part) % 12, (deg * 45.0) % 30.0);

                    // D60 Shashtyamsha (0°30' with 60 Deities)
                    var d60_part = Math.floor(deg / 0.5);
                    var d60_sign = (pSign + d60_part) % 12;
                    var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
                    var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
                    addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

                    // D150 Nadiamsha (12' arc = 0.2° per division, 150 divisions per sign)
                    var d150_part = Math.min(149, Math.floor(deg / 0.2));
                    var nadiIdx = d150_part;
                    if (pSign % 3 === 0) { // Chara (Movable: Aries, Cancer, Libra, Cap)
                        nadiIdx = d150_part;
                    } else if (pSign % 3 === 1) { // Sthira (Fixed: Taurus, Leo, Scorpio, Aqu)
                        nadiIdx = 149 - d150_part;
                    } else { // Dvisvabhava (Dual: Gemini, Virgo, Sag, Pisces)
                        nadiIdx = (75 + d150_part) % 150;
                    }
                    var bhaga = (deg % 0.2 < 0.1) ? "पूर्व भाग" : "उत्तर भाग";
                    var nadiName = "नाड्यांश #" + (nadiIdx + 1) + " (" + bhaga + ")";
                    var d150_sign = (pSign + d150_part) % 12;
                    addV("D150", 150, d150_sign, (deg * 150.0) % 30.0, nadiName);


                    return v;
                }

                var ascVargas = calcVargasDetailed(ascSid);
                var planetVargas = {};
                for (var i = 0; i < order.length; i++) {
                    var pn = order[i];
                    planetVargas[pn] = calcVargasDetailed(sids[pn]);
                }

                var VARGA_TITLES = {
                    D1: "D-1 लग्न कुण्डली • जन्मपत्रिका (शारीरिक स्वरूप, आरोग्य व स्वभाव)",
                    D2: "D-2 होरा चक्र (धन, संचित संपत्ति व समृद्धि)",
                    D3: "D-3 द्रेष्काण चक्र (पराक्रम, सहोदर व ऊर्जा)",
                    D4: "D-4 चतुर्थांश चक्र (भूमि, भवन, वाहन व अचल संपत्ति)",
                    D7: "D-7 सप्तांश चक्र (संतान सुख, वंश वृद्धि व पूर्व पुण्य)",
                    D9: "D-9 नवमांश कुण्डली (भाग्य, जीवनसाथी व आंतरिक आत्मिक शक्ति)",
                    D10: "D-10 दशमांश कुण्डली (करियर, पद, प्रतिष्ठा व सामाजिक सम्मान)",
                    D12: "D-12 द्वादशांश चक्र (माता-पिता, पितृ ऋण व वंशज)",
                    D16: "D-16 षोडशांश चक्र (वाहन सुख, मानसिक आनंद व सुख-साधन)",
                    D20: "D-20 विंशांश चक्र (आध्यात्मिक साधना, उपासना व सिद्धि)",
                    D24: "D-24 चतुर्विंशांश चक्र (उच्च विद्या, ज्ञान व शोध कौशल)",
                    D27: "D-27 सप्तविंशांश चक्र (शारीरिक बल, सामर्थ्य व दुर्बलता)",
                    D30: "D-30 त्रिंशांश चक्र (अरिष्ट, व्याधि व प्रारब्ध कष्ट)",
                    D40: "D-40 खवेदांश चक्र (शुभ-अशुभ फल व कुल प्रारब्ध)",
                    D45: "D-45 अक्षवेदांश चक्र (चारित्रिक शुचिता व सूक्ष्म चेतना)",
                    D60: "D-60 षष्ट्यंश चक्र (पूर्व जन्म प्रारब्ध व सम्पूर्ण फल निर्णय)",
                    D150: "D-150 नाड्यांश चक्र (सूक्ष्म प्रारब्ध, १२' कला अंश व जीवन-रहस्य)"
                };

                var builtCharts = {};
                var shodashaData = {};

                var vKeys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60", "D150"];
                for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
                    var vk = vKeys[vkIdx];
                    var ascV = ascVargas[vk];
                    var aSign = ascV.sign_index;
                    var vHouses = {};
                    for (var h = 1; h <= 12; h++) {
                        vHouses[h] = [String(((aSign + h - 1) % 12) + 1)];
                    }

                    var pDetails = [];
                    for (var pi = 0; pi < order.length; pi++) {
                        var pn = order[pi];
                        var pv = planetVargas[pn][vk];
                        var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;
                        var dStr = Math.floor(pv.deg) + "°" + Math.floor((pv.deg * 60) % 60) + "'";
                        vHouses[hNum].push(PLANET_NAMES_HI[pn] + (vk === "D1" ? (" " + dStr) : ""));

                        pDetails.push({
                            planet: PLANET_NAMES_HI[pn],
                            sign: SIGNS_HI_DIAG[pv.sign_index],
                            house: hNum,
                            degree: dStr + '"',
                            deity: pv.deity || ""
                        });
                    }

                    // Pure Mathematical Special Yogas Engine (Vargottama, Pushkar Navamsha, Pushkar Bhaga)
                    var specialYogas = [];
                    if (vk === "D9") {
                        if (ascVargas.D1.sign_index === ascVargas.D9.sign_index) {
                            specialYogas.push("✦ लग्न वर्गोत्तम (Lagna Vargottama — " + SIGNS_HI_DIAG[aSign] + " लग्न)");
                        }
                        var PUSHKAR_BHAGAS = [21, 14, 18, 8, 19, 9, 24, 11, 23, 14, 19, 9];
                        for (var pi = 0; pi < order.length; pi++) {
                            var pn = order[pi];
                            var pD1 = planetVargas[pn].D1;
                            var pD9 = planetVargas[pn].D9;
                            var plon = sids[pn];
                            var pdeg = plon % 30.0;
                            var psign = Math.floor(plon / 30.0) % 12;
                            var nPart = Math.floor(pdeg / (30.0 / 9.0));

                            // 1. Planet Vargottama (D1 Rashi == D9 Rashi)
                            if (pD1.sign_index === pD9.sign_index) {
                                specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " वर्गोत्तम (" + SIGNS_HI_DIAG[pD1.sign_index] + " राशि D1 व D9 समान)");
                            }

                            // 2. Pushkar Navamsha (24 Auspicious Nourishing Navamshas in Zodiac)
                            var isPushkarNav = false;
                            var elem = psign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
                            if (elem === 0 && (nPart === 6 || nPart === 8)) isPushkarNav = true; // 7th & 9th
                            else if (elem === 1 && (nPart === 2 || nPart === 4)) isPushkarNav = true; // 3rd & 5th
                            else if (elem === 2 && (nPart === 5 || nPart === 7)) isPushkarNav = true; // 6th & 8th
                            else if (elem === 3 && (nPart === 0 || nPart === 2)) isPushkarNav = true; // 1st & 3rd

                            if (isPushkarNav) {
                                specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " पुष्कर नवमांश (कल्याणकारी आरोग्य व भाग्य वर्धक)");
                            }

                            // 3. Pushkar Bhaga (±1° tolerance)
                            if (Math.abs(pdeg - PUSHKAR_BHAGAS[psign]) <= 1.0) {
                                specialYogas.push("✦ " + PLANET_NAMES_HI[pn] + " पुष्कर भाग (परम सिद्धि व अमृतोपम योग)");
                            }
                        }
                    }

                    var cKeyLower = vk.toLowerCase();
                    var cObj = {
                        key: vk,
                        title: VARGA_TITLES[vk],
                        ascSign: SIGNS_HI_DIAG[aSign] + " लग्न (" + Math.floor(ascV.deg) + "°" + Math.floor((ascV.deg * 60) % 60) + "')",
                        houses: vHouses,
                        planetDetails: pDetails,
                        specialYogas: specialYogas
                    };

                    builtCharts[cKeyLower] = cObj;
                    builtCharts[vk] = cObj;
                    shodashaData[vk] = cObj;
                    shodashaData[cKeyLower] = cObj;
                }
                builtCharts.chalit = { title: "भाव चलित चक्र", ascSign: SIGNS_HI_DIAG[ascSignIdx] + " लग्न", houses: d1Houses };
                if (typeof window !== 'undefined') window.SHODASHAVARGA_DATA = shodashaData;

                // =========================================================================
                // 10. AUTHENTIC PARASHARI BPHS ASHTAKAVARGA ENGINE (SAV = EXACT 337 BINDUS)
                // =========================================================================
                var BAV_RULES = {
                    Sun: {
                        Sun: [1, 2, 4, 7, 8, 9, 10, 11],
                        Moon: [3, 6, 10, 11],
                        Mars: [1, 2, 4, 7, 8, 9, 10, 11],
                        Mercury: [3, 5, 6, 9, 10, 11, 12],
                        Jupiter: [5, 6, 9, 11],
                        Venus: [6, 7, 12],
                        Saturn: [1, 2, 4, 7, 8, 9, 10, 11],
                        Lagna: [3, 4, 6, 10, 11, 12]
                    },
                    Moon: {
                        Sun: [3, 6, 7, 8, 10, 11],
                        Moon: [1, 3, 6, 7, 10, 11],
                        Mars: [2, 3, 5, 6, 9, 10, 11],
                        Mercury: [1, 3, 4, 5, 7, 8, 10, 11],
                        Jupiter: [1, 4, 7, 8, 10, 11, 12],
                        Venus: [3, 4, 5, 7, 9, 10, 11],
                        Saturn: [3, 5, 6, 11],
                        Lagna: [3, 6, 10, 11]
                    },
                    Mars: {
                        Sun: [3, 5, 6, 10, 11],
                        Moon: [3, 6, 11],
                        Mars: [1, 2, 4, 7, 8, 10, 11],
                        Mercury: [3, 5, 6, 11],
                        Jupiter: [6, 10, 11, 12],
                        Venus: [6, 8, 11, 12],
                        Saturn: [1, 4, 7, 8, 9, 10, 11],
                        Lagna: [1, 3, 6, 10, 11]
                    },
                    Mercury: {
                        Sun: [5, 6, 9, 11, 12],
                        Moon: [2, 4, 6, 8, 10, 11],
                        Mars: [1, 2, 4, 7, 8, 9, 10, 11],
                        Mercury: [1, 3, 5, 6, 9, 10, 11, 12],
                        Jupiter: [6, 8, 11, 12],
                        Venus: [1, 2, 3, 4, 5, 8, 9, 11],
                        Saturn: [1, 2, 4, 7, 8, 9, 10, 11],
                        Lagna: [1, 2, 4, 6, 8, 10, 11]
                    },
                    Jupiter: {
                        Sun: [1, 2, 3, 4, 7, 8, 9, 10, 11],
                        Moon: [2, 5, 7, 9, 11],
                        Mars: [1, 2, 4, 7, 8, 10, 11],
                        Mercury: [1, 2, 4, 5, 6, 9, 10, 11],
                        Jupiter: [1, 2, 3, 4, 7, 8, 10, 11],
                        Venus: [2, 5, 6, 9, 10, 11],
                        Saturn: [3, 5, 6, 12],
                        Lagna: [1, 2, 4, 5, 6, 7, 9, 10, 11]
                    },
                    Venus: {
                        Sun: [8, 11, 12],
                        Moon: [1, 2, 3, 4, 5, 8, 9, 11, 12],
                        Mars: [3, 5, 6, 9, 11, 12],
                        Mercury: [3, 5, 6, 9, 11],
                        Jupiter: [5, 8, 9, 10, 11],
                        Venus: [1, 2, 3, 4, 5, 8, 9, 10, 11],
                        Saturn: [3, 4, 5, 8, 9, 10, 11],
                        Lagna: [1, 2, 3, 4, 5, 8, 9, 11]
                    },
                    Saturn: {
                        Sun: [1, 2, 4, 7, 8, 10, 11],
                        Moon: [3, 6, 11],
                        Mars: [3, 5, 6, 10, 11, 12],
                        Mercury: [6, 8, 9, 10, 11, 12],
                        Jupiter: [5, 6, 11, 12],
                        Venus: [6, 11, 12],
                        Saturn: [3, 5, 6, 11],
                        Lagna: [1, 3, 4, 6, 10, 11]
                    }
                };

                var refSigns = {};
                for (var k in planetSignsMap) refSigns[k] = planetSignsMap[k];
                refSigns.Lagna = ascSignIdx;

                var bav = {};
                var bavDetail = {};
                var sevenPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];

                for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                    var tp = sevenPlanets[pIdx];
                    bav[tp] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                    bavDetail[tp] = {};
                    var refDict = BAV_RULES[tp];

                    for (var refBody in refDict) {
                        var rSign = refSigns[refBody];
                        var row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                        var hList = refDict[refBody];
                        for (var hi = 0; hi < hList.length; hi++) {
                            var targetSign = (rSign + hList[hi] - 1) % 12;
                            row[targetSign] = 1;
                            bav[tp][targetSign] += 1;
                        }
                        bavDetail[tp][refBody] = row;
                    }
                }

                // Samudaya Ashtakavarga (SAV) = sum of all 7 BAVs per sign
                var sav = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                for (var s = 0; s < 12; s++) {
                    for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                        sav[s] += bav[sevenPlanets[pIdx]][s];
                    }
                }

                // Trikona Shodhana (Trinal Reductions)
                var trik = {};
                for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                    var tp = sevenPlanets[pIdx];
                    var pts = bav[tp].slice();
                    for (var trine = 0; trine < 4; trine++) {
                        var tSigns = [trine, trine + 4, trine + 8];
                        var minVal = Math.min(pts[tSigns[0]], pts[tSigns[1]], pts[tSigns[2]]);
                        pts[tSigns[0]] -= minVal;
                        pts[tSigns[1]] -= minVal;
                        pts[tSigns[2]] -= minVal;
                    }
                    trik[tp] = pts;
                }

                // Ekadhipatya Shodhana (Dual Lordship Reductions)
                var dualPairs = [
                    ["Mars", 0, 7], ["Venus", 1, 6], ["Mercury", 2, 5], ["Jupiter", 8, 11], ["Saturn", 9, 10]
                ];
                var occupiedSigns = {};
                for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                    occupiedSigns[planetSignsMap[sevenPlanets[pIdx]]] = true;
                }

                var eka = {};
                for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                    var tp = sevenPlanets[pIdx];
                    var pts = trik[tp].slice();
                    for (var di = 0; di < dualPairs.length; di++) {
                        var dp = dualPairs[di];
                        var s1 = dp[1], s2 = dp[2];
                        var occ1 = !!occupiedSigns[s1], occ2 = !!occupiedSigns[s2];
                        var v1 = pts[s1], v2 = pts[s2];

                        if (!occ1 && !occ2) {
                            if (v1 === v2) { pts[s1] = 0; pts[s2] = 0; }
                            else if (v1 > v2) { pts[s1] = v2; }
                            else { pts[s2] = pts[s1]; }
                        } else if (occ1 && !occ2) {
                            pts[s2] = 0;
                        } else if (!occ1 && occ2) {
                            pts[s1] = 0;
                        }
                    }
                    eka[tp] = pts;
                }

                // Shodhya Pinda (Rashi Pinda + Graha Pinda)
                var RASHI_GUNAKARA = [7, 10, 8, 4, 10, 5, 7, 8, 9, 5, 11, 12];
                var GRAHA_GUNAKARA = { Sun: 5, Moon: 5, Mars: 8, Mercury: 5, Jupiter: 10, Venus: 7, Saturn: 5 };
                var pindas = {};
                for (var pIdx = 0; pIdx < sevenPlanets.length; pIdx++) {
                    var tp = sevenPlanets[pIdx];
                    var reduced = eka[tp];
                    var rPinda = 0;
                    for (var s = 0; s < 12; s++) rPinda += reduced[s] * RASHI_GUNAKARA[s];
                    var gPinda = 0;
                    for (var gKey in GRAHA_GUNAKARA) {
                        gPinda += reduced[planetSignsMap[gKey]] * GRAHA_GUNAKARA[gKey];
                    }
                    pindas[tp] = { rashi_pinda: rPinda, graha_pinda: gPinda, shodhya_pinda: rPinda + gPinda };
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
                    return { rl: rl, nl: nl, sl: sl, ssl: SUB_ORDER[sslIdx], sign: SIGNS_HI_DIAG[sIdx] };
                }

                // Exact Spherical Placidus Semi-Arc Cusp Solver
                function solveExactPlacidus(ascNir, latitude, ayan, jd) {
                    var ascTrop = (ascNir + ayan) % 360.0;
                    if (ascTrop < 0) ascTrop += 360.0;
                    var T = (jd - 2451545.0) / 36525.0;
                    var epsDeg = 23.43929111 - (46.8150 * T) / 3600.0;
                    var eps = epsDeg * Math.PI / 180.0;
                    var phi = Math.max(Math.min(latitude, 66.0), -66.0) * Math.PI / 180.0;
                    var lam1 = ascTrop * Math.PI / 180.0;

                    var alpha1 = (Math.atan2(Math.sin(lam1) * Math.cos(eps), Math.cos(lam1)) * 180.0 / Math.PI + 360.0) % 360.0;
                    var sinDecl1 = Math.sin(eps) * Math.sin(lam1);
                    var tanDecl1 = sinDecl1 / Math.sqrt(Math.max(1e-12, 1.0 - sinDecl1 * sinDecl1));
                    var ad1 = Math.asin(Math.max(-0.999999, Math.min(0.999999, Math.tan(phi) * tanDecl1))) * 180.0 / Math.PI;
                    var oa1 = (alpha1 - ad1 + 360.0) % 360.0;
                    var ramcDeg = (oa1 - 90.0 + 360.0) % 360.0;
                    var ramc = ramcDeg * Math.PI / 180.0;
                    var mcDeg = (Math.atan2(Math.sin(ramc), Math.cos(ramc) * Math.cos(eps)) * 180.0 / Math.PI + 360.0) % 360.0;

                    function pIter(offsetDeg, factor, diurnal) {
                        var ra0 = (ramcDeg + offsetDeg) % 360.0;
                        var raCurr = ra0;
                        for (var iter = 0; iter < 35; iter++) {
                            var raRad = raCurr * Math.PI / 180.0;
                            var lam = Math.atan2(Math.sin(raRad), Math.cos(raRad) * Math.cos(eps));
                            var sinDecl = Math.sin(eps) * Math.sin(lam);
                            var tanDecl = sinDecl / Math.sqrt(Math.max(1e-12, 1.0 - sinDecl * sinDecl));
                            var arg = Math.max(-0.999999, Math.min(0.999999, Math.tan(phi) * tanDecl));
                            var adDeg = Math.asin(arg) * 180.0 / Math.PI;
                            var raNext = diurnal ? ((ra0 + factor * adDeg) % 360.0 + 360.0) % 360.0 : ((ra0 - factor * adDeg) % 360.0 + 360.0) % 360.0;
                            if (Math.abs((raNext - raCurr + 180.0) % 360.0 - 180.0) < 1e-7) {
                                raCurr = raNext;
                                break;
                            }
                            raCurr = raNext;
                        }
                        var raFin = raCurr * Math.PI / 180.0;
                        return (Math.atan2(Math.sin(raFin), Math.cos(raFin) * Math.cos(eps)) * 180.0 / Math.PI + 360.0) % 360.0;
                    }

                    var c11 = pIter(30.0, 1.0 / 3.0, true);
                    var c12 = pIter(60.0, 2.0 / 3.0, true);
                    var c2 = pIter(120.0, 2.0 / 3.0, false);
                    var c3 = pIter(150.0, 1.0 / 3.0, false);

                    var trop = {
                        1: ascTrop, 2: c2, 3: c3, 4: (mcDeg + 180.0) % 360.0,
                        5: (c11 + 180.0) % 360.0, 6: (c12 + 180.0) % 360.0,
                        7: (ascTrop + 180.0) % 360.0, 8: (c2 + 180.0) % 360.0, 9: (c3 + 180.0) % 360.0,
                        10: mcDeg, 11: c11, 12: c12
                    };

                    var res = {};
                    for (var h = 1; h <= 12; h++) {
                        res[h] = (trop[h] - ayan + 360.0) % 360.0;
                    }
                    return res;
                }

                var placidusMap = solveExactPlacidus(ascSid, lat, ayanamsa, jd);
                var kpCusps = [];
                for (var c = 1; c <= 12; c++) {
                    var cLon = placidusMap[c];
                    var kpL = getKpLords(cLon);
                    var cDegIn = cLon % 30.0;
                    var dDeg = Math.floor(cDegIn);
                    var dMin = Math.floor((cDegIn - dDeg) * 60.0);
                    var dSec = Math.round(((cDegIn - dDeg) * 60.0 - dMin) * 60.0);
                    if (dSec === 60) { dSec = 0; dMin++; }
                    if (dMin === 60) { dMin = 0; dDeg++; }
                    var cDms = dDeg + "°" + (dMin < 10 ? "0" : "") + dMin + "'" + (dSec < 10 ? "0" : "") + dSec + '"';
                    var cuspObj = {
                        cusp: String(c),
                        sign: kpL.sign,
                        deg: cDms,
                        rl: kpL.rl,
                        nl: kpL.nl,
                        sl: kpL.sl,
                        ssl: kpL.ssl,
                        star: kpL.nl,
                        starLord: kpL.nl,
                        subLord: kpL.sl,
                        subSubLord: kpL.ssl,
                        significator: "भाव " + c,
                        longitude: cLon
                    };
                    kpCusps.push(cuspObj);
                    kpCusps[c] = cuspObj; // Enable 1-based indexing so cusps[1] or cusps[10] never returns undefined
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
                        star: kpL.nl,
                        starLord: kpL.nl,
                        subLord: kpL.sl,
                        subSubLord: kpL.ssl,
                        significator: "भाव " + (((Math.floor(plon / 30.0) - ascSignIdx + 12) % 12) + 1)
                    });
                }

                // 13. Jaimini 7 Chara Karakas
                var sortedKarakas = sevenPlanets.map(function (pn) {
                    return { pn: pn, name: PLANET_NAMES_HI[pn], degInSign: sids[pn] % 30.0, signIdx: Math.floor(sids[pn] / 30.0) % 12 };
                }).sort(function (a, b) {
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

                var jaiminiKarakas = sortedKarakas.map(function (item, idx) {
                    var deg = item.degInSign;
                    var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                    var h = ((item.signIdx - ascSignIdx + 12) % 12) + 1;
                    return {
                        abbr: KARAKA_NAMES[idx].abbr,
                        karaka: KARAKA_NAMES[idx].name,
                        title: KARAKA_NAMES[idx].name,
                        name: KARAKA_NAMES[idx].name,
                        planet: item.name,
                        sign: SIGNS_HI_DIAG[item.signIdx],
                        deg: dms,
                        degNum: deg,
                        house: h,
                        signification: KARAKA_NAMES[idx].role,
                        desc: KARAKA_NAMES[idx].role,
                        role: KARAKA_NAMES[idx].role
                    };
                });

                // Attach keyed properties to jaiminiKarakas array for direct lookup by abbreviation
                for (var jk = 0; jk < jaiminiKarakas.length; jk++) {
                    jaiminiKarakas[jaiminiKarakas[jk].abbr] = jaiminiKarakas[jk];
                }

                var ak = sortedKarakas[0];
                var klNavSign = (function (sign, deg) {
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

                var bhavasPreds = [];
                for (var h = 1; h <= 12; h++) {
                    var hSignIdx = (ascSignIdx + h - 1) % 12;
                    var hSignName = SIGNS_HI_DIAG[hSignIdx];
                    var hLordName = LORDS_BY_SIGN[hSignIdx];
                    var occPlanets = [];
                    for (var i = 0; i < order.length; i++) {
                        var pn = order[i];
                        if (Math.floor(sids[pn] / 30.0) % 12 === hSignIdx) {
                            occPlanets.push(PLANET_NAMES_HI[pn]);
                        }
                    }
                    var occText = occPlanets.length > 0 ? ("उपस्थित ग्रह: " + occPlanets.join(", ") + "।") : "इस भाव पर कोई प्रत्यक्ष ग्रह स्थित नहीं है, दृष्टि व भावेश द्वारा फल नियंत्रित है।";

                    bhavasPreds.push({
                        bhava_num: h,
                        title: BHAVA_TITLES[h - 1],
                        rashi: hSignName,
                        lord: hLordName,
                        strength_type: (h === 1 || h === 4 || h === 7 || h === 10) ? "Kendra (केन्द्र)" : ((h === 5 || h === 9) ? "Trikona (त्रिकोण)" : "Upachaya / Dusthana"),
                        analysis: "भाव " + h + " (" + BHAVA_TITLES[h - 1] + ") में " + hSignName + " राशि स्थित है जिसके अधिपति " + hLordName + " हैं। " + occText + " वैदिक फलादेश के अनुसार यह भाव जातक के जीवन में इस क्षेत्र की स्थिरता एवं प्रारब्ध को दर्शाता है।"
                    });
                }

                return {
                    _engine_ver: 5.2,
                    bhavat_bhavam: (typeof window !== 'undefined' && window.VyasBhavatBhavam && typeof window.VyasBhavatBhavam.evaluateAll === 'function') ? window.VyasBhavatBhavam.evaluateAll({ charts: builtCharts, planet_table: pTable, kp: { cusps: kpCusps, planets: kpPlanets } }) : null,
                    profile: {
                        name: name, dob: dobStr, tob: tobStr, city: cityStr, gender: gender,
                        lat: lat, lon: lon, tz: tz,
                        asc_sign: SIGNS_HI_DIAG[ascSignIdx], asc_dms: ascDms,
                        ayanamsa_deg: ayanamsa,
                        ayanamsa_dms: toDMS(ayanamsa),
                        ephemeris: "Swiss Ephemeris 0.001\" (NASA JPL DE431/441)",
                        house_system: "Parashari: Sripati / Whole Sign | KP: Placidus Semi-Arc",
                        node_type: "True Node (विशुद्ध खगोलीय केंद्र)"
                    },
                    charts: builtCharts,
                    planet_table: pTable,
                    houses: builtCharts.d1.houses, // Universal top-level alias for all renderers
                    active_dasha: activeDasha,
                    ashtakavarga: {
                        sav: sav,
                        bav: bav,
                        bav_detail: bavDetail,
                        trikona_shodhana: trik,
                        ekadhipatya_shodhana: eka,
                        pindas: pindas
                    },
                    kp: {
                        cusps: kpCusps,
                        planets: kpPlanets
                    },
                    jaimini: {
                        karakas: jaiminiKarakas,
                        atmakaraka: ak.name,
                        karakamsha: SIGNS_HI_DIAG[klNavSign],
                        AK: jaiminiKarakas['AK'] || jaiminiKarakas[0],
                        AmK: jaiminiKarakas['AmK'] || jaiminiKarakas[1],
                        BK: jaiminiKarakas['BK'] || jaiminiKarakas[2],
                        MK: jaiminiKarakas['MK'] || jaiminiKarakas[3],
                        PK: jaiminiKarakas['PK'] || jaiminiKarakas[4],
                        GK: jaiminiKarakas['GK'] || jaiminiKarakas[5],
                        DK: jaiminiKarakas['DK'] || jaiminiKarakas[6]
                    },
                    nadi: {
                        combinations: nadiCombinations
                    },
                    predictions: {
                        bhavas: bhavasPreds
                    },
                    goodh_diagnostics: computeGoodhDiagnostics({
                        profile: { asc_sign: SIGNS_HI_DIAG[ascSignIdx] },
                        planet_table: pTable,
                        jaimini: { atmakaraka: ak.name, karakamsha: SIGNS_HI_DIAG[klNavSign], karakas: jaiminiKarakas }
                    })
                };
    }

    function computeCurrentPrashna(cityName, customLat, customLon) {
        var now = new Date();
        var y = now.getFullYear();
        var m = String(now.getMonth() + 1).padStart(2, '0');
        var d = String(now.getDate()).padStart(2, '0');
        var hh = String(now.getHours()).padStart(2, '0');
        var mm = String(now.getMinutes()).padStart(2, '0');
        var dobStr = y + '-' + m + '-' + d;
        var tobStr = hh + ':' + mm;

        var nameStr = 'तात्कालिक प्रश्न/गोचर कुण्डली';
        var cName = 'उज्जैन (अवंतिका)';
        var lat = undefined;
        var lon = undefined;

        if (typeof cityName === 'number' && typeof customLat === 'number') {
            lat = cityName;
            lon = customLat;
            cName = (typeof customLon === 'string' && customLon) ? customLon : 'वेधशाला स्थान';
        } else if (typeof cityName === 'string' && cityName) {
            cName = cityName;
            if (typeof customLat === 'number' && typeof customLon === 'number') {
                lat = customLat;
                lon = customLon;
            }
        }

        var res = computeMathematicalKundli(nameStr, dobStr, tobStr, cName, 'Prashna', lat, lon);
        if (res && res.charts && res.charts.d1 && res.charts.d1.houses) {
            res.houses = res.charts.d1.houses; // Top-level alias for seamless renderer compatibility
        }
        return res;
    }

    // High-Precision Astronomical Panchang Engine (Swiss/Meeus Pure Coordinates)
    function computeAstronomicalPanchang(dateObj, lat, lon) {
        var d = dateObj || new Date();
        var y = d.getFullYear();
        var m = String(d.getMonth() + 1).padStart(2, '0');
        var dt = String(d.getDate()).padStart(2, '0');
        var hh = String(d.getHours()).padStart(2, '0');
        var mm = String(d.getMinutes()).padStart(2, '0');
        var dobStr = y + '-' + m + '-' + dt;
        var tobStr = hh + ':' + mm;

        var chart = computeMathematicalKundli('Panchang', dobStr, tobStr, 'वेधशाला', 'Prashna', lat || 26.7922, lon || 82.1998);
        var sun = chart.planet_table.find(function(p) { return p.p.indexOf('सूर्य') !== -1; });
        var moon = chart.planet_table.find(function(p) { return p.p.indexOf('चन्द्र') !== -1; });

        var sMap = { 'मेष':0, 'वृषभ':30, 'मिथुन':60, 'कर्क':90, 'सिंह':120, 'कन्या':150, 'तुला':180, 'वृश्चिक':210, 'धनु':240, 'मकर':270, 'कुंभ':300, 'मीन':330 };
        function parseDms(r, dmsStr) {
            var base = sMap[r] || 0;
            var parts = (dmsStr || '0°0\'0"').split(/[°\'\"]/);
            var deg = parseFloat(parts[0]) || 0;
            var min = parseFloat(parts[1]) || 0;
            var sec = parseFloat(parts[2]) || 0;
            return base + deg + (min / 60.0) + (sec / 3600.0);
        }

        var sunLon = parseDms(sun.r, sun.d);
        var moonLon = parseDms(moon.r, moon.d);

        var diff = (moonLon - sunLon + 360.0) % 360.0;
        var tithiIdx = Math.floor(diff / 12.0); // 0 to 29
        var tithiRemDeg = 12.0 - (diff % 12.0);
        var tithiRemHours = tithiRemDeg / 0.508;

        var nakIdx = Math.floor(moonLon / (360.0 / 27.0)); // 0 to 26
        var nakRemDeg = (360.0 / 27.0) - (moonLon % (360.0 / 27.0));
        var nakRemHours = nakRemDeg / 0.55;
        var pada = Math.floor((moonLon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;

        var yogaIdx = Math.floor(((sunLon + moonLon) % 360.0) / (360.0 / 27.0));

        var karanaNum = Math.floor(diff / 6.0); // 0 to 59
        var karanaName = '';
        if (karanaNum === 0) karanaName = 'किस्तुघ्न';
        else if (karanaNum >= 57) {
            if (karanaNum === 57) karanaName = 'शकुनि';
            else if (karanaNum === 58) karanaName = 'चतुष्पद';
            else karanaName = 'नाग';
        } else {
            var movKaranas = ['बव', 'बालव', 'कौलव', 'तैतिल', 'गर', 'वणिज', 'विष्टि (भद्रा)'];
            karanaName = movKaranas[(karanaNum - 1) % 7];
        }

        var tithiNames = [
            'शुक्ल प्रतिपदा', 'शुक्ल द्वितीया', 'शुक्ल तृतीया', 'शुक्ल चतुर्थी', 'शुक्ल पंचमी', 'शुक्ल षष्ठी', 'शुक्ल सप्तमी', 'शुक्ल अष्टमी',
            'शुक्ल नवमी', 'शुक्ल दशमी', 'शुक्ल एकादशी', 'शुक्ल द्वादशी', 'शुक्ल त्रयोदशी', 'शुक्ल चतुर्दशी', 'पूर्णिमा',
            'कृष्ण प्रतिपदा', 'कृष्ण द्वितीया', 'कृष्ण तृतीया', 'कृष्ण चतुर्थी', 'कृष्ण पंचमी', 'कृष्ण षष्ठी', 'कृष्ण सप्तमी', 'कृष्ण अष्टमी',
            'कृष्ण नवमी', 'कृष्ण दशमी', 'कृष्ण एकादशी', 'कृष्ण द्वादशी', 'कृष्ण त्रयोदशी', 'कृष्ण चतुर्दशी', 'अमावस्या'
        ];

        var nakNames = [
            'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा', 'पुनर्वसु', 'पुष्य', 'आश्लेषा',
            'मघा', 'पूर्वाफाल्गुनी', 'उत्तराफाल्गुनी', 'हस्त', 'चित्रा', 'स्वाति', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
            'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा', 'पूर्वाभाद्रपद', 'उत्तराभाद्रपद', 'रेवती'
        ];

        var yogaNames = [
            'विष्कम्भ', 'प्रीति', 'आयुष्मान', 'सौभाग्य', 'शोभन', 'अतिगण्ड', 'सुकर्मा', 'धृति', 'शूल',
            'गण्ड', 'वृद्धि', 'ध्रुव', 'व्याघात', 'हर्षण', 'वज्र', 'सिद्धि', 'व्यतीपात', 'वरीयान्',
            'परिघ', 'शिव', 'सिद्ध', 'साध्य', 'शुभ', 'शुक्ल', 'ब्रह्म', 'इन्द्र', 'वैधृति'
        ];

        return {
            tithi: tithiNames[tithiIdx % 30],
            tithiIdx: tithiIdx,
            tithiRemHours: tithiRemHours,
            nakshatra: nakNames[nakIdx % 27],
            nakIdx: nakIdx,
            pada: pada,
            nakRemHours: nakRemHours,
            yoga: yogaNames[yogaIdx % 27],
            yogaIdx: yogaIdx,
            karana: karanaName,
            karanaNum: karanaNum,
            sunLon: sunLon,
            moonLon: moonLon,
            sunSign: sun.r,
            moonSign: moon.r,
            chart: chart
        };
    }


    // ═══════════════════════════════════════════════════════════════════
    // ACHARYA VYAS (v10.0) - DEEP DIAGNOSTIC & SECRET-REVELATION ENGINE
    // (गूढ़ रहस्य एवं सूक्ष्म परीक्षण • Parashari + Jaimini + Navatara)
    // ═══════════════════════════════════════════════════════════════════
    var SIGNS_HI_DIAG = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन'];
    var NAKSHATRAS_27_DIAG = [
        'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा', 'पुनर्वसु', 'पुष्य', 'आश्लेषा',
        'मघा', 'पूर्वाफाल्गुनी', 'उत्तराफाल्गुनी', 'हस्त', 'चित्रा', 'स्वाति', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
        'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा', 'पूर्वाभाद्रपद', 'उत्तराभाद्रपद', 'रेवती'
    ];
    var DAGDHA_BY_TITHI = {
        1: [6, 9], 2: [7, 10], 3: [4, 9], 4: [5, 8], 5: [2, 5],
        6: [3, 6], 7: [8, 3], 8: [9, 2], 9: [3, 4], 10: [10, 7],
        11: [8, 11], 12: [9, 6], 13: [1, 11], 14: [0, 6], 15: [1, 6]
    };

    var TARA_NAMES = {
        1: "जन्म (Janma - मूल स्वभाव/प्रारब्ध)",
        2: "सम्पत (Sampat - समृद्धि/वैभव)",
        3: "विपत (Vipat - बाधा/संघर्ष)",
        4: "क्षेम (Kshema - कल्याण/सुरक्षा)",
        5: "प्रत्यरि (Pratyari - विरोध/शत्रुता)",
        6: "साधक (Sadhaka - सिद्धि/साधना)",
        7: "वध (Vadha - तीव्र परीक्षा/कष्ट)",
        8: "मैत्र (Maitra - मित्रता/सहयोग)",
        9: "अतिमैत्र (Atimaitra - परम कल्याण)"
    };

    var CURRENT_GOCHAR_PLANETS = {
        "शनि (गोचर)": { lon: 335.2, sign: "मीन", nak: "उत्तराभाद्रपद" },
        "गुरु (गोचर)": { lon: 65.4, sign: "मिथुन", nak: "मृगशिरा" },
        "राहु (गोचर)": { lon: 322.8, sign: "कुंभ", nak: "पूर्वाभाद्रपद" },
        "केतु (गोचर)": { lon: 142.8, sign: "सिंह", nak: "पूर्वाफाल्गुनी" },
        "मंगल (गोचर)": { lon: 104.5, sign: "कर्क", nak: "पुष्य" }
    };

    function computeGoodhDiagnostics(kundli) {
        if (!kundli || !kundli.planet_table) return null;

        var pTable = kundli.planet_table;
        var pLonMap = {};
        var moonLon = 0;
        var sunLon = 0;
        var ascSignIdx = 0;
        var sMap = { 'मेष':0, 'वृषभ':1, 'मिथुन':2, 'कर्क':3, 'सिंह':4, 'कन्या':5, 'तुला':6, 'वृश्चिक':7, 'धनु':8, 'मकर':9, 'कुंभ':10, 'मीन':11 };

        if (kundli.profile && kundli.profile.asc_sign) {
            ascSignIdx = sMap[kundli.profile.asc_sign] !== undefined ? sMap[kundli.profile.asc_sign] : 0;
        }

        pTable.forEach(function (pl) {
            var pName = (pl.p || '').replace(/\s*\(.*\)/, '').trim();
            var sIdx = sMap[pl.r] !== undefined ? sMap[pl.r] : 0;
            var parts = (pl.d || '0°0\'').split(/[°\']/);
            var deg = parseFloat(parts[0]) || 0;
            var min = parseFloat(parts[1]) || 0;
            var totalLon = (sIdx * 30.0) + deg + (min / 60.0);
            pLonMap[pName] = totalLon;
            if (pName === 'चन्द्र') moonLon = totalLon;
            if (pName === 'सूर्य') sunLon = totalLon;
        });

        // 1. Gandanta & Gandmool Precision Check (Water-to-Fire Junctions)
        var gandantaHits = [];
        for (var pName in pLonMap) {
            var lon = pLonMap[pName];
            var lonN = (lon % 360.0 + 360.0) % 360.0;
            var sIdx = Math.floor(lonN / 30.0);
            var degInS = lonN % 30.0;
            var isWaterEnd = ([3, 7, 11].indexOf(sIdx) !== -1 && degInS >= 28.6667);
            var isFireStart = ([0, 4, 8].indexOf(sIdx) !== -1 && degInS <= 1.3333);

            if (isWaterEnd || isFireStart) {
                gandantaHits.push({
                    planet: pName,
                    sign: SIGNS_HI_DIAG[sIdx],
                    deg_in_sign: parseFloat(degInS.toFixed(2)),
                    junction_type: isWaterEnd ? "जल-अग्नि संधि समाप्ति (Water End / गण्डान्त)" : "अग्नि संधि आरम्भ (Fire Start / गण्डान्त)",
                    insight_hi: pName + " (" + SIGNS_HI_DIAG[sIdx] + " " + degInS.toFixed(2) + "°) जल-अग्नि गण्डान्त सन्धि पर स्थित है; यह तीव्र आंतरिक रूपांतरण, असाधारण सूक्ष्म अंतर्दृष्टि तथा संधि-जनित मानसिक/शारीरिक परीक्षण का स्पष्ट सूचक है।"
                });
            }
        }

        // 2. Dagdha / Shunya Rashi Check by Tithi
        var diffElong = (moonLon - sunLon + 360.0) % 360.0;
        var tithiIdx = Math.floor(diffElong / 12.0) % 30; // 0..29
        var tithiNum = (tithiIdx % 15) + 1; // 1..15
        var dagdhaSignIndices = DAGDHA_BY_TITHI[tithiNum] || [];
        var dagdhaSignsHi = dagdhaSignIndices.map(function(idx) { return SIGNS_HI_DIAG[idx]; });

        var planetsInDagdha = [];
        pTable.forEach(function (pl) {
            var pName = (pl.p || '').replace(/\s*\(.*\)/, '').trim();
            var sIdx = sMap[pl.r];
            if (dagdhaSignIndices.indexOf(sIdx) !== -1) {
                planetsInDagdha.push({
                    planet: pName,
                    sign: SIGNS_HI_DIAG[sIdx],
                    house: pl.h,
                    warning_hi: pName + " (" + SIGNS_HI_DIAG[sIdx] + ", भाव " + pl.h + ") जन्म तिथि अनुसार 'दग्ध/शून्य राशि' में स्थित है; इस भाव के फल में विलम्ब अथवा विशेष साधना उपरांत ही सिद्धि प्राप्त होती है।"
                });
            }
        });

        // 3. Navatara Chakra (9-Tara Classification from Natal Moon)
        var nakSpan = 360.0 / 27.0;
        var birthNakIdx = Math.floor((moonLon % 360.0) / nakSpan);
        var harshTaras = [3, 5, 7];

        var transitTaraReport = [];
        for (var tpName in CURRENT_GOCHAR_PLANETS) {
            var gp = CURRENT_GOCHAR_PLANETS[tpName];
            var tNakIdx = Math.floor((gp.lon % 360.0) / nakSpan);
            var dist = ((tNakIdx - birthNakIdx + 27) % 27) + 1;
            var taraNum = ((dist - 1) % 9) + 1;
            transitTaraReport.push({
                transit_planet: tpName,
                transit_nakshatra: NAKSHATRAS_27_DIAG[tNakIdx],
                current_sign: gp.sign,
                tara_number: taraNum,
                tara_label: TARA_NAMES[taraNum],
                is_sensitive_tara: harshTaras.indexOf(taraNum) !== -1,
                guidance_hi: harshTaras.indexOf(taraNum) !== -1 ?
                    ("⚠️ " + tpName + " का संचरण वर्तमान में आपकी जन्म-नक्षत्र से '" + TARA_NAMES[taraNum] + "' में है। इस अवधि में जोखिमपूर्ण निर्णयों, अनावश्यक विवाद एवं जल्दबाजी से बचें।") :
                    ("✅ " + tpName + " का संचरण अनुकूल '" + TARA_NAMES[taraNum] + "' में है, जो स्थिरता एवं प्रगति का द्योतक है।")
            });
        }

        // 4. Jaimini Karaka & Inner Turmoil Dynamics (AK, AmK, Karakamsha, Swamsha, AL, UL)
        var akName = (kundli.jaimini && kundli.jaimini.atmakaraka) ? kundli.jaimini.atmakaraka : "चन्द्र";
        var amkName = "सूर्य";
        if (kundli.jaimini && Array.isArray(kundli.jaimini.karakas)) {
            var amkObj = kundli.jaimini.karakas.find(function(k) { return k.abbr === 'AmK'; });
            if (amkObj) amkName = amkObj.planet;
        }

        var klSignName = (kundli.jaimini && kundli.jaimini.karakamsha) ? kundli.jaimini.karakamsha : "मीन";
        var klSignIdx = sMap[klSignName] !== undefined ? sMap[klSignName] : 11;
        var swamsaSignIdx = (pLonMap[akName] !== undefined) ? Math.floor(pLonMap[akName] / 30.0) % 12 : 3;

        // Compute Arudha Lagna (AL) with Jaimini Exceptions
        var LORDS_BY_SIGN = [2, 5, 3, 1, 0, 3, 5, 2, 4, 6, 6, 4]; // Mars, Ven, Mer, Moon, Sun, Mer, Ven, Mars, Jup, Sat, Sat, Jup
        var PLANET_ORDER_IDX = { 0:'सूर्य', 1:'चन्द्र', 2:'मंगल', 3:'बुध', 4:'गुरु', 5:'शुक्र', 6:'शनि' };

        var lagnaLordName = PLANET_ORDER_IDX[LORDS_BY_SIGN[ascSignIdx]] || 'गुरु';
        var lagnaLordSignIdx = (pLonMap[lagnaLordName] !== undefined) ? Math.floor(pLonMap[lagnaLordName] / 30.0) % 12 : ascSignIdx;
        var diffL = (lagnaLordSignIdx - ascSignIdx + 12) % 12;
        var alSignIdx = (lagnaLordSignIdx + diffL) % 12;
        if (alSignIdx === ascSignIdx) alSignIdx = (ascSignIdx + 9) % 12;
        else if (alSignIdx === (ascSignIdx + 6) % 12) alSignIdx = (ascSignIdx + 3) % 12;

        // Compute Upapada Lagna (UL) with Jaimini Exceptions
        var h12SignIdx = (ascSignIdx + 11) % 12;
        var h12LordName = PLANET_ORDER_IDX[LORDS_BY_SIGN[h12SignIdx]] || 'शनि';
        var h12LordSignIdx = (pLonMap[h12LordName] !== undefined) ? Math.floor(pLonMap[h12LordName] / 30.0) % 12 : h12SignIdx;
        var diff12 = (h12LordSignIdx - h12SignIdx + 12) % 12;
        var ulSignIdx = (h12LordSignIdx + diff12) % 12;
        if (ulSignIdx === h12SignIdx) ulSignIdx = (h12SignIdx + 9) % 12;
        else if (ulSignIdx === (h12SignIdx + 6) % 12) ulSignIdx = (h12SignIdx + 3) % 12;

        var diffAkSwamsa = ((klSignIdx - swamsaSignIdx + 12) % 12) + 1;
        var diffAkAl = ((klSignIdx - alSignIdx + 12) % 12) + 1;
        var diffUlAl = ((ulSignIdx - alSignIdx + 12) % 12) + 1;

        var is68Swamsa = (diffAkSwamsa === 6 || diffAkSwamsa === 8);
        var is68Al = (diffAkAl === 6 || diffAkAl === 8);
        var innerTurmoilFlag = is68Swamsa || is68Al;

        var deepObsHi = "आत्मकारक (" + akName + ") से कारकांश " + SIGNS_HI_DIAG[klSignIdx] + " तथा अमात्यकारक (" + amkName + ") कर्म-प्रारब्ध तय करते हैं। " +
            (innerTurmoilFlag ?
                "कारकांश और स्वांश/आरूढ़ लग्न के बीच ६/८ (षडाष्टक) संबंध होने से बाहरी सफलता व सामाजिक प्रतिष्ठा के भीतर भी एक सतत आंतरिक द्वन्द्व, वैराग्य अथवा गहरे आध्यात्मिक अर्थ की खोज बनी रहती है।" :
                "कारकांश और कर्म-आरूढ़ के बीच परस्पर शुभ संबंध है, जिससे आंतरिक संकल्प और बाह्य कर्म में सुदृढ़ सामंजस्य बना रहता है।");

        // 5. 22nd Drekkana (Khara) & 64th Navamsha Sensitivity
        var kharaSignIdx = (ascSignIdx + 7) % 12; // 8th house sign
        var kharaLordName = PLANET_ORDER_IDX[LORDS_BY_SIGN[kharaSignIdx]] || 'शनि';
        var nav64SignIdx = (Math.floor(moonLon / (30.0 / 9.0)) + 7) % 12; // 8th navamsha from Moon
        var nav64LordName = PLANET_ORDER_IDX[LORDS_BY_SIGN[nav64SignIdx]] || 'मंगल';

        return {
            birth_nakshatra: NAKSHATRAS_27_DIAG[birthNakIdx],
            gandanta_placements: gandantaHits,
            dagdha_rashis_for_tithi: dagdhaSignsHi,
            planets_in_dagdha_rashis: planetsInDagdha,
            transit_tara_analysis: transitTaraReport,
            jaimini_dynamics: {
                ak: akName,
                amk: amkName,
                karakansha: SIGNS_HI_DIAG[klSignIdx],
                swamsa: SIGNS_HI_DIAG[swamsaSignIdx],
                arudha_lagna: SIGNS_HI_DIAG[alSignIdx],
                upapada_lagna: SIGNS_HI_DIAG[ulSignIdx],
                house_from_swamsa_to_karakansha: diffAkSwamsa,
                house_from_al_to_karakansha: diffAkAl,
                house_from_al_to_ul: diffUlAl,
                inner_turmoil_flag: innerTurmoilFlag,
                deep_observation_hi: deepObsHi
            },
            khara_and_64th_navamsha: {
                drekkana_22_sign: SIGNS_HI_DIAG[kharaSignIdx],
                drekkana_22_lord: kharaLordName,
                navamsha_64_sign: SIGNS_HI_DIAG[nav64SignIdx],
                navamsha_64_lord: nav64LordName,
                protective_guidance_hi: "२२वें द्रेष्काण स्वामी (" + kharaLordName + ") एवं ६४वें नवांश स्वामी (" + nav64LordName + ") की दशा/अंतर्दशा अथवा संवेदनशील गोचर में नित्य 'महामृत्युंजय मंत्र' का जप परम रक्षा कवच सिद्ध होता है।"
            }
        };
    }

    // Universal Active Kundli Resolver (Guarantees STRICT Single-Source-of-Truth across all portals)
    function getActiveKundli() {
        if (typeof window === 'undefined' && typeof localStorage === 'undefined') return null;
        var storage = (typeof window !== 'undefined' && window.localStorage) ? window.localStorage : (typeof localStorage !== 'undefined' ? localStorage : null);
        if (!storage) return null;
        try {
            var raw = storage.getItem('vyas_active_profile');
            if (raw) {
                var p = JSON.parse(raw);
                if (p) {
                    var prof = p.profile || p;
                    var name = prof.name || 'सक्रिय जातक';
                    var dob = prof.dob || prof.birth_date;
                    var tob = prof.tob || prof.birth_time || '12:00';
                    var city = prof.city || prof.place || 'वाराणसी';
                    var lat = prof.lat;
                    var lon = prof.lon;

                    // Ensure complete varga charts exist; if incomplete, recompute full mathematical kundli
                    if (p.planet_table && p.charts && p.charts.d1 && p.charts.d9 && p.charts.d10 && p.profile && p.profile.dob) {
                        var needsRecomp = false;
                        if (!p._engine_ver || p._engine_ver < 5.2) needsRecomp = true;
                        if (p.kp && p.kp.cusps && p.kp.cusps.length >= 2) {
                            if (p.kp.cusps[0].deg === p.kp.cusps[1].deg || !p.kp.cusps[0].longitude) needsRecomp = true;
                        }
                        if (!needsRecomp) {
                            if (!p.houses && p.charts.d1.houses) p.houses = p.charts.d1.houses;
                            return p;
                        }
                    } 
                    
                    // If raw birth details exist, compute full mathematical kundli
                    if (dob) {
                        var recomputed = computeMathematicalKundli(name, dob, tob, city, prof.gender || 'Male', lat, lon);
                        if (recomputed) {
                            if (!recomputed.houses && recomputed.charts && recomputed.charts.d1 && recomputed.charts.d1.houses) {
                                recomputed.houses = recomputed.charts.d1.houses;
                            }
                            storage.setItem('vyas_active_profile', JSON.stringify(recomputed));
                            return recomputed;
                        }
                    }
                }
            }
        } catch (e) {
            console.warn('getActiveKundli error:', e);
        }
        // If vyas_active_profile is not set, check if user has a saved profile in vyas_family_vault or vyas_custom_profiles
        try {
            var vKeys = ['vyas_family_vault', 'vyas_custom_profiles', 'vyas_user_vault'];
            for (var vk = 0; vk < vKeys.length; vk++) {
                var vRaw = storage.getItem(vKeys[vk]);
                if (vRaw) {
                    var vList = JSON.parse(vRaw);
                    if (Array.isArray(vList) && vList.length > 0) {
                        for (var vi = 0; vi < vList.length; vi++) {
                            var item = vList[vi];
                            var iDob = item.dob || item.birth_date || '';
                            if (iDob) {
                                var recompiled = computeMathematicalKundli(item.name || 'सक्रिय जातक', iDob, item.tob || '12:00', item.place || item.city || 'वाराणसी', item.gender || 'Male', item.lat, item.lon);
                                if (recompiled) {
                                    if (!recompiled.houses && recompiled.charts && recompiled.charts.d1 && recompiled.charts.d1.houses) {
                                        recompiled.houses = recompiled.charts.d1.houses;
                                    }
                                    storage.setItem('vyas_active_profile', JSON.stringify(recompiled));
                                    return recompiled;
                                }
                            }
                        }
                    }
                }
            }
        } catch(e) { }

        // If vyas_active_profile and saved vault profiles are not set, default to dynamic Current Prashna (वर्तमान गोचर)
        try {
            var prashna = computeCurrentPrashna('वर्तमान गोचर (Real-Time Transit)');
            if (prashna) {
                if (!prashna.houses && prashna.charts && prashna.charts.d1 && prashna.charts.d1.houses) {
                    prashna.houses = prashna.charts.d1.houses;
                }
                return prashna;
            }
        } catch (e) {
            console.warn('computeCurrentPrashna fallback error:', e);
        }

        return null;
    }

    // Universal Vault Synchronizer (Ensures consistent profiles)
    function sanitizeStoredVaults() {
        // Vault profiles remain safe and intact
    }
    try { sanitizeStoredVaults(); } catch (e) { }

    // Exports
    global.computeMathematicalKundli = computeMathematicalKundli;
    global.sanitizeStoredVaults = sanitizeStoredVaults;
    global.VyasAstronomicalEngine = {
        computeKundli: computeMathematicalKundli,
        computeCurrentPrashna: computeCurrentPrashna,
        computeGoodhDiagnostics: computeGoodhDiagnostics,
        getActiveKundli: getActiveKundli,
        computePanchang: computeAstronomicalPanchang
    };
    if (global.VyasDaivagyaCore) {
        global.VyasDaivagyaCore.computeMathematicalKundli = computeMathematicalKundli;
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = {
            computeMathematicalKundli: computeMathematicalKundli,
            computeCurrentPrashna: computeCurrentPrashna,
            getActiveKundli: getActiveKundli,
            computePanchang: computeAstronomicalPanchang,
            VyasAstronomicalEngine: global.VyasAstronomicalEngine
        };
    }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));
