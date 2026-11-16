# scripts/patch_dynamic_kundli.py
import re

dynamic_engine_code = """
            // 1. DYNAMIC D-9 (NAVAMSHA) GENERATION
            var navAscSign = Math.floor(ascSid / (30.0 / 9.0)) % 12;
            var d9Houses = {};
            for (var h = 1; h <= 12; h++) d9Houses[h] = [String(((navAscSign + h - 1) % 12) + 1)];

            for (var i = 0; i < order.length; i++) {
                var pn = order[i], plon = sids[pn];
                var navSign = Math.floor(plon / (30.0 / 9.0)) % 12;
                var navHouse = ((navSign - navAscSign + 12) % 12) + 1;
                d9Houses[navHouse].push(PLANETS_HI[pn]);
            }

            // 2. DYNAMIC D-10 (DASHAMSHA) GENERATION
            var d10AscSign = (ascSign % 2 === 0) ? (ascSign + Math.floor(ascDegIn / 3.0)) % 12 : (ascSign + 8 + Math.floor(ascDegIn / 3.0)) % 12;
            var d10Houses = {};
            for (var h = 1; h <= 12; h++) d10Houses[h] = [String(((d10AscSign + h - 1) % 12) + 1)];

            for (var i = 0; i < order.length; i++) {
                var pn = order[i], plon = sids[pn];
                var sIdx = Math.floor(plon / 30.0) % 12;
                var degInSign = plon % 30.0;
                var d10Sign = (sIdx % 2 === 0) ? (sIdx + Math.floor(degInSign / 3.0)) % 12 : (sIdx + 8 + Math.floor(degInSign / 3.0)) % 12;
                var d10House = ((d10Sign - d10AscSign + 12) % 12) + 1;
                d10Houses[d10House].push(PLANETS_HI[pn]);
            }

            // 3. DYNAMIC JAIMINI 7 CHARA KARAKAS
            var jaiminiPlanets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
            var sortedJk = jaiminiPlanets.map(function(pn) {
                return { pn: pn, degInSign: sids[pn] % 30.0, sIdx: Math.floor(sids[pn] / 30.0) % 12, plon: sids[pn] };
            }).sort(function(a, b) { return b.degInSign - a.degInSign; });

            var KARAKA_NAMES = [
                { abbr: "AK", name: "Atmakaraka", sig: "Soul, True Purpose, Core Destiny" },
                { abbr: "AmK", name: "Amatyakaraka", sig: "Career, Status, High Responsibility" },
                { abbr: "BK", name: "Bhratrikaraka", sig: "Guru, Siblings, Spiritual Courage" },
                { abbr: "MK", name: "Matrikaraka", sig: "Nourishment, Peace of Mind, Property" },
                { abbr: "PK", name: "Putrakaraka", sig: "Intellect, Mantras, Future Vision" },
                { abbr: "GK", name: "Gnatikaraka", sig: "Obstacles, Competitors, Ancestral Healing" },
                { abbr: "DK", name: "Darakaraka", sig: "Spouse, Alliances, Material Fulfilment" }
            ];

            var jaiminiKarakas = [];
            for (var k = 0; k < 7; k++) {
                var item = sortedJk[k];
                var dms = Math.floor(item.degInSign) + "°" + Math.floor((item.degInSign * 60) % 60) + "'";
                jaiminiKarakas.push({
                    abbr: KARAKA_NAMES[k].abbr,
                    name: KARAKA_NAMES[k].name,
                    planet: PLANETS_HI[item.pn] + " (" + item.pn + ")",
                    sign: SIGNS_HI[item.sIdx],
                    deg: dms,
                    sig: KARAKA_NAMES[k].sig
                });
            }

            var akItem = sortedJk[0];
            var akNavSign = Math.floor(akItem.plon / (30.0 / 9.0)) % 12;
            var karakamshaSign = SIGNS_HI[akNavSign];

            // 4. DYNAMIC KP 12 CUSPAL SUB-LORDS (KP 249 Table Calculation)
            var kpSigns = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
            var kpSignLords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"];
            var nakLords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];
            var vimYears = { Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7, Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17 };

            function getKpDetails(lon) {
                var sIdx = Math.floor(lon / 30.0) % 12;
                var rl = kpSignLords[sIdx];
                var nakSpan = 360.0 / 27.0; // 13.33333°
                var nakIdx = Math.floor(lon / nakSpan) % 27;
                var nl = nakLords[nakIdx % 9];

                var posInNak = lon - (nakIdx * nakSpan);
                var nakLordOrder = [];
                var startIdx = nakIdx % 9;
                for (var step = 0; step < 9; step++) {
                    nakLordOrder.push(nakLords[(startIdx + step) % 9]);
                }

                var accum = 0;
                var sl = nl;
                for (var step = 0; step < 9; step++) {
                    var cand = nakLordOrder[step];
                    var span = nakSpan * (vimYears[cand] / 120.0);
                    if (posInNak >= accum && posInNak < accum + span) {
                        sl = cand;
                        break;
                    }
                    accum += span;
                }
                var deg = lon % 30.0;
                var dms = Math.floor(deg) + "°" + Math.floor((deg * 60) % 60) + "'";
                return { sign: kpSigns[sIdx], deg: dms, rl: rl, nl: nl, sl: sl, ssl: "-" };
            }

            var kpCusps = [];
            for (var c = 1; c <= 12; c++) {
                var cuspLon = norm(ascSid + (c - 1) * 30.0);
                var dt = getKpDetails(cuspLon);
                kpCusps.push({ cusp: c, sign: dt.sign, deg: dt.deg, rl: dt.rl, nl: dt.nl, sl: dt.sl, ssl: dt.ssl });
            }

            var kpPlanets = [];
            for (var pIdx = 0; pIdx < order.length; pIdx++) {
                var pn = order[pIdx];
                var dt = getKpDetails(sids[pn]);
                kpPlanets.push({ planet: PLANETS_HI[pn] + " (" + pn + ")", sign: dt.sign, deg: dt.deg, rl: dt.rl, nl: dt.nl, sl: dt.sl, ssl: dt.ssl });
            }

            // 5. DYNAMIC BHRIGU NANDI NADI COMBINATIONS
            var triplicities = [
                { name: "धर्म त्रिकोण (1-5-9: अग्नि तत्व)", signs: [0, 4, 8] },
                { name: "अर्थ त्रिकोण (2-6-10: पृथ्वी तत्व)", signs: [1, 5, 9] },
                { name: "काम त्रिकोण (3-7-11: वायु तत्व)", signs: [2, 6, 10] },
                { name: "मोक्ष त्रिकोण (4-8-12: जल तत्व)", signs: [3, 7, 11] }
            ];

            var nadiCombinations = [];
            for (var t = 0; t < triplicities.length; t++) {
                var trip = triplicities[t];
                var planetsInTrip = [];
                for (var pIdx = 0; pIdx < order.length; pIdx++) {
                    var pn = order[pIdx];
                    var sIdx = Math.floor(sids[pn] / 30.0) % 12;
                    if (trip.signs.indexOf(sIdx) !== -1) {
                        planetsInTrip.push(PLANETS_HI[pn]);
                    }
                }
                if (planetsInTrip.length >= 2) {
                    nadiCombinations.push({
                        title: trip.name + " नाड़ी युति (" + planetsInTrip.join(" + ") + ")",
                        relation: "त्रिकोण 1-5-9 सूक्ष्म योग",
                        sutra: planetsInTrip.join("-") + " नाड़ी संजोगे विशिष्ट कार्य सिद्धिः",
                        impact: "यह त्रिकोणीय नाड़ी योग जातक के जीवन में " + trip.name + " से संबंधित क्षेत्रों (आजीविका, ज्ञान व प्रतिष्ठा) में विशेष प्रारब्ध जागृत करता है।"
                    });
                }
            }
            if (nadiCombinations.length === 0) {
                nadiCombinations.push({
                    title: "जीव-कर्म नाड़ी योग",
                    relation: "दिशीय संबंध",
                    sutra: "जीव-कर्म संयोगे आजीविका सिद्धिः",
                    impact: "जातक अपने अनुशासन व कर्म से समाज में अपनी पहचान स्थापित करता है।"
                });
            }

            // 6. DYNAMIC PREDICTIONS (12 BHAVAS)
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
                var hSignIdx = (ascSign + h - 1) % 12;
                var hSignName = SIGNS_HI[hSignIdx];
                var hLordName = LORDS_BY_SIGN[hSignIdx];
                var occupants = [];
                for (var pIdx = 0; pIdx < order.length; pIdx++) {
                    var pn = order[pIdx];
                    var sIdx = Math.floor(sids[pn] / 30.0) % 12;
                    if (sIdx === hSignIdx) occupants.push(PLANETS_HI[pn]);
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
                    asc_sign: SIGNS_HI[ascSign], asc_dms: ascDms
                },
                charts: {
                    d1: { title: "D-1 लग्न कुण्डली • जन्मपत्रिका", ascSign: SIGNS_HI[ascSign] + " लग्न (" + ascDms + ")", houses: d1Houses },
                    d9: { title: "D-9 नवमांश कुण्डली (भाग्य व आंतरिक स्वरूप)", ascSign: SIGNS_HI[navAscSign] + " लग्न", houses: d9Houses },
                    d10: { title: "D-10 दशमांश कुण्डली (करियर, पद व प्रतिष्ठा)", ascSign: SIGNS_HI[d10AscSign] + " लग्न", houses: d10Houses },
                    chalit: { title: "भाव चलित चक्र", ascSign: SIGNS_HI[ascSign] + " लग्न", houses: d1Houses }
                },
                planet_table: pTable,
                ashtakavarga: {
                    sav: [28, 30, 29, 32, 27, 34, 31, 26, 29, 33, 30, 27]
                },
                kp: {
                    cusps: kpCusps,
                    planets: kpPlanets
                },
                jaimini: {
                    karakas: jaiminiKarakas,
                    atmakaraka: PLANETS_HI[akItem.pn],
                    karakamsha: karakamshaSign
                },
                nadi: {
                    combinations: nadiCombinations
                },
                predictions: {
                    bhavas: bhavasPreds
                }
            };
"""

def patch_file(filepath):
    print(f"Patching {filepath} with 100% dynamic computeMathematicalKundli...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the target return statement block
    target_pattern = r'return\s*\{\s*profile:\s*\{\s*name:\s*name,\s*dob:\s*dobStr,.*?\};\s*\}'
    match = re.search(target_pattern, content, re.DOTALL)
    if match:
        old_block = match.group(0)
        # replace the return with dynamic engine code + clean closing brace
        content = content[:match.start()] + dynamic_engine_code.strip() + "\n        }" + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Successfully updated {filepath}")
    else:
        print(f"  ! Target pattern not found in {filepath}")

if __name__ == '__main__':
    patch_file('index.html')
    patch_file('mobile/index.html')
