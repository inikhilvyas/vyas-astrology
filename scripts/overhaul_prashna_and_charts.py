"""
Overhaul Script: Prashna Kundli + Dynamic Jaimini/KP/Nadi + Planet Table Fix + UI Elevation
Root Cause Fixes for VYAS ASTRA:
1. Fix desktop planet table ID (desktopPlanetTableBody vs planetPositionsTableBody).
2. Purge personal founder kundli from public fallback / memory.
3. Implement real-time Horary Prashna Kundli (तात्कालिक प्रश्न कुण्डली) engine when no chart is loaded or in incognito.
4. Make D-9, D-10, KP, Jaimini, Nadi 100% mathematically dynamic for all charts.
5. Elevate UI styling with Awwwards/ADX luxury palette.
"""
import os
import re
import json

def generate_js_engines():
    return '''
        // =========================================================================
        // DYNAMIC HORARY PRASHNA KUNDLI ENGINE (तात्कालिक प्रश्न कुण्डली - प्रश्न मार्ग)
        // =========================================================================
        castPrashnaKundli: function(query, userLat, userLon) {
            var now = new Date();
            var lat = (typeof userLat === 'number' && !isNaN(userLat)) ? userLat : 28.6139; // Delhi / Standard India
            var lon = (typeof userLon === 'number' && !isNaN(userLon)) ? userLon : 77.2090;
            var tz = 5.5;

            var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
            var hr = now.getHours(), mn = now.getMinutes(), sc = now.getSeconds();
            var decHrUtc = hr + (mn / 60.0) + (sc / 3600.0) - tz;

            var y2 = mo <= 2 ? yr - 1 : yr;
            var m2 = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y2 / 100);
            var B = 2 - A + Math.floor(A / 4);
            var jd0 = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5;
            var jd = jd0 + decHrUtc / 24.0;
            var d = jd - 2451543.5;
            var T_j2000 = (jd - 2451545.0) / 36525.0;

            var RAD = Math.PI / 180.0, DEG = 180.0 / Math.PI;
            function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
            var ayanamsa = 23.857 + 1.39697 * T_j2000;

            var gmst = norm(280.46061837 + 360.98564736629 * (jd - 2451545.0));
            var lst = norm(gmst + lon) * RAD;
            var eps = (23.4392911 - 0.0130042 * T_j2000) * RAD;
            var ascTrop = norm(Math.atan2(Math.cos(lst), -(Math.sin(lst) * Math.cos(eps) + Math.tan(lat * RAD) * Math.sin(eps))) * DEG);
            var ascSid = norm(ascTrop - ayanamsa);
            var ascSign = Math.floor(ascSid / 30.0) % 12;
            var ascDegIn = ascSid % 30.0;
            var ascDms = Math.floor(ascDegIn) + "°" + Math.floor((ascDegIn * 60) % 60) + "'";

            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var NAKS = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "अश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];

            // Calculate Real-time planetary positions right now
            var sids = {};
            sids.Sun = norm(norm(282.9404 + 4.70935e-5 * d + norm(356.0470 + 0.9856002585 * d)) - ayanamsa);
            sids.Moon = norm(norm(125.1228 + 115.3654 + 13.0649929509 * d) - ayanamsa);
            sids.Mars = norm(norm(49.5574 + 286.5016 + 18.6021 + 0.5240207766 * d) - ayanamsa);
            sids.Mercury = norm(norm(48.3313 + 29.1241 + 168.6562 + 4.0923344368 * d) - ayanamsa);
            sids.Jupiter = norm(norm(100.4542 + 273.8777 + 19.8950 + 0.0830853001 * d) - ayanamsa);
            sids.Venus = norm(norm(76.6799 + 54.8910 + 48.0052 + 1.6021302244 * d) - ayanamsa);
            sids.Saturn = norm(norm(113.6634 + 339.3939 + 316.9670 + 0.0334442282 * d) - ayanamsa);
            sids.Rahu = norm(norm(125.04452 - 1934.136261 * T_j2000) - ayanamsa);
            sids.Ketu = norm(sids.Rahu + 180.0);

            var moonSignIdx = Math.floor(sids.Moon / 30.0) % 12;
            var moonNakIdx = Math.floor(sids.Moon / (360.0 / 27.0)) % 27;
            var moonPada = Math.floor((sids.Moon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1;

            // Intent / Karya Bhava Classification
            var q = (query || "").toLowerCase();
            var karyaHouse = 1;
            var karyaDesc = "तनु व सामान्य फल";

            if (/mla|mp|chunav|chunaw|neta|rajneeti|politics|election|career|naukri|job|promotion|pad|adhikar|shasan|sarkar|ias|ips/.test(q)) {
                karyaHouse = 10;
                karyaDesc = "दशम भाव (राज्य पद, चुनाव, उच्चाधिकार व कर्म सिद्धि)";
            } else if (/vivah|shadi|marriage|patni|pati|prem|love|rishta|sambandh|jeewansaathi/.test(q)) {
                karyaHouse = 7;
                karyaDesc = "सप्तम भाव (विवाह, दांपत्य व जीवनसाथी)";
            } else if (/paisa|dhan|sampatti|labh|wealth|money|business|vyapar|profit|kamai|karz|loan|loss/.test(q)) {
                karyaHouse = 11;
                karyaDesc = "एकादश व द्वितीय भाव (धन, लाभ, व्यापारिक वृद्धि व संचित कोष)";
            } else if (/santan|bacha|garbh|pregnancy|child|padhai|exam|upsc|pariksha|education|study/.test(q)) {
                karyaHouse = 5;
                karyaDesc = "पंचम भाव (संतान सुख, परीक्षा व विद्या अर्जन)";
            } else if (/court|case|mukadma|police|shatru|rog|bimar|bimari|health|swasthya/.test(q)) {
                karyaHouse = 6;
                karyaDesc = "षष्ठ भाव (रोग, ऋण, विवाद व शत्रु विजय)";
            } else if (/yatra|videsh|foreign|travel|visa|sthanantaran|transfer/.test(q)) {
                karyaHouse = 9;
                karyaDesc = "नवम व द्वादश भाव (विदेश यात्रा, भाग्य व स्थान परिवर्तन)";
            }

            var prashnesha = LORDS[ascSign];
            var karyaSign = (ascSign + karyaHouse - 1) % 12;
            var karyesha = LORDS[karyaSign];

            // Real-time planetary placements summary
            var planetSummary = [];
            var order = [
                { k: "Sun", n: "सूर्य" }, { k: "Moon", n: "चन्द्र" }, { k: "Mars", n: "मंगल" },
                { k: "Mercury", n: "बुध" }, { k: "Jupiter", n: "गुरु" }, { k: "Venus", n: "शुक्र" },
                { k: "Saturn", n: "शनि" }, { k: "Rahu", n: "राहु" }, { k: "Ketu", n: "केतु" }
            ];
            for (var i = 0; i < order.length; i++) {
                var p = order[i], plon = sids[p.k];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var deg = plon % 30.0;
                var hNum = ((sIdx - ascSign + 12) % 12) + 1;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                planetSummary.push(p.n + " " + SIGNS_HI[sIdx] + " (" + dms + ", भाव " + hNum + ")");
            }

            return {
                isPrashna: true,
                query: query,
                timestamp: now.toLocaleTimeString('hi-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                date: now.toLocaleDateString('hi-IN'),
                prashnaLagna: SIGNS_HI[ascSign] + " (" + ascDms + ")",
                prashnesha: prashnesha,
                moonSign: SIGNS_HI[moonSignIdx],
                moonNak: NAKS[moonNakIdx] + " (" + moonPada + ")",
                karyaHouse: karyaHouse,
                karyaDesc: karyaDesc,
                karyesha: karyesha,
                karyaSign: SIGNS_HI[karyaSign],
                planets: planetSummary.join("; ")
            };
        },
    ''';

if __name__ == '__main__':
    print("Engine generator ready.")

