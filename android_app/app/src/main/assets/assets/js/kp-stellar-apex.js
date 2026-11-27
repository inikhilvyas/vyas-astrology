/**
 * VYAS ASTRA — KP Stellar Apex Suite v3 (Deterministic Multi-School Engine)
 * Covers:
 * 1. Classical KSK (4-Level House Significators L1..L4 + CSL)
 * 2. Four-Step Theory (Sunil Gondhalekar — Untenanted/Self-Star PS)
 * 3. S.P. Khullar (Cuspal Interlinks / CSSL + 12th-from-Cusp Negation)
 * 4. Nakshatra Nadi (Dinesh Mathur — 3-Tier Script & Cusp Degree Hit <= 3°)
 * 5. K. Baskaran Methodology (Star-Lord PS Filtering)
 * 6. A. Devaraj Methodology (CSL ∩ CSSL Micro-Linkage)
 * + 5-Level SubLord Analyzer (RL -> NL -> SL -> SSL -> SSSL)
 * + House Rotation (Bhava Chalit), Pars Fortuna & Live Ruling Planets (RP)
 */
(function (global) {
    'use strict';

    var VIMSHOTTARI_ORDER = [
        { name: 'Ketu', hi: 'केतु', years: 7 },
        { name: 'Venus', hi: 'शुक्र', years: 20 },
        { name: 'Sun', hi: 'सूर्य', years: 6 },
        { name: 'Moon', hi: 'चन्द्र', years: 10 },
        { name: 'Mars', hi: 'मंगल', years: 7 },
        { name: 'Rahu', hi: 'राहु', years: 18 },
        { name: 'Jupiter', hi: 'गुरु', years: 16 },
        { name: 'Saturn', hi: 'शनि', years: 19 },
        { name: 'Mercury', hi: 'बुध', years: 17 }
    ];

    var SIGN_LORDS = ['Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'];
    var SIGN_NAMES_HI = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुम्भ', 'मीन'];
    var NAK_NAMES_HI = [
        'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा',
        'पुनर्वसु', 'पुष्य', 'आश्लेषा', 'मघा', 'पूर्वाफाल्गुनी', 'उत्तराफाल्गुनी',
        'हस्त', 'चित्रा', 'स्वाती', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
        'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा',
        'पूर्वाभाद्रपद', 'उत्तराभाद्रपद', 'रेवती'
    ];
    var NAK_SPAN = 360.0 / 27.0;

    var PLANET_NORM = {
        'सूर्य': 'Sun', 'sun': 'Sun', 'su': 'Sun',
        'चन्द्र': 'Moon', 'चंद्र': 'Moon', 'moon': 'Moon', 'mo': 'Moon',
        'मंगल': 'Mars', 'mars': 'Mars', 'ma': 'Mars',
        'बुध': 'Mercury', 'mercury': 'Mercury', 'me': 'Mercury',
        'गुरु': 'Jupiter', 'बृहस्पति': 'Jupiter', 'jupiter': 'Jupiter', 'ju': 'Jupiter',
        'शुक्र': 'Venus', 'venus': 'Venus', 've': 'Venus',
        'शनि': 'Saturn', 'saturn': 'Saturn', 'sa': 'Saturn',
        'राहु': 'Rahu', 'rahu': 'Rahu', 'ra': 'Rahu',
        'केतु': 'Ketu', 'ketu': 'Ketu', 'ke': 'Ketu'
    };

    var PLANET_HI = {
        Sun: 'सूर्य', Moon: 'चन्द्र', Mars: 'मंगल', Mercury: 'बुध',
        Jupiter: 'गुरु', Venus: 'शुक्र', Saturn: 'शनि', Rahu: 'राहु', Ketu: 'केतु'
    };

    var KP_DOMAINS = {
        job: { label: 'नौकरी / सेवा प्राप्ति (Job / Service)', cusp: 6, supportive: [2, 6, 10, 11], negating: [1, 5, 8, 9, 12] },
        promotion: { label: 'करियर उन्नति / पदोन्नति (Promotion)', cusp: 10, supportive: [2, 6, 10, 11], negating: [5, 8, 9, 12] },
        business: { label: 'स्वतंत्र व्यवसाय (Business)', cusp: 7, supportive: [2, 7, 10, 11], negating: [5, 8, 12] },
        wealth: { label: 'धन एवं आर्थिक लाभ (Wealth & Gains)', cusp: 11, supportive: [2, 6, 11], negating: [5, 8, 12] },
        marriage: { label: 'विवाह एवं दांपत्य (Marriage)', cusp: 7, supportive: [2, 7, 11], negating: [1, 6, 10] },
        childbirth: { label: 'संतान सुख (Progeny / Childbirth)', cusp: 5, supportive: [2, 5, 11], negating: [1, 4, 10] },
        property: { label: 'भूमि, भवन व वाहन (Property / Vehicle)', cusp: 4, supportive: [4, 11, 12], negating: [3, 5, 8] },
        foreign: { label: 'विदेश यात्रा / निवास (Foreign Settlement)', cusp: 12, supportive: [3, 9, 12], negating: [2, 4, 11] },
        education: { label: 'उच्च शिक्षा (Higher Education)', cusp: 9, supportive: [4, 9, 11], negating: [3, 5, 8] },
        litigation: { label: 'मुकदमा / न्याय विजय (Litigation Victory)', cusp: 6, supportive: [1, 6, 11], negating: [5, 7, 12] },
        health: { label: 'रोग निवारण / स्वास्थ्य (Health Recovery)', cusp: 1, supportive: [1, 5, 11], negating: [6, 8, 12] }
    };

    function normPlanet(p) {
        if (!p) return '';
        var k = String(p).trim().toLowerCase();
        return PLANET_NORM[k] || PLANET_NORM[String(p).trim()] || String(p).trim();
    }

    function hiPlanet(p) {
        var np = normPlanet(p);
        return PLANET_HI[np] || p || '-';
    }

    function angularDiff(a, b) {
        var d = Math.abs((a - b) % 360);
        return d > 180 ? 360 - d : d;
    }

    function formatDms(deg) {
        deg = ((deg % 360) + 360) % 360;
        var d = Math.floor(deg);
        var remM = (deg - d) * 60;
        var m = Math.floor(remM);
        var s = Math.round((remM - m) * 60);
        if (s >= 60) { s -= 60; m += 1; }
        if (m >= 60) { m -= 60; d = (d + 1) % 360; }
        return String(d).padStart(2, '0') + '°' + String(m).padStart(2, '0') + "'" + String(s).padStart(2, '0') + '"';
    }

    function rotatedOrder(startName) {
        var idx = 0;
        for (var i = 0; i < VIMSHOTTARI_ORDER.length; i++) {
            if (VIMSHOTTARI_ORDER[i].name === startName) { idx = i; break; }
        }
        return VIMSHOTTARI_ORDER.slice(idx).concat(VIMSHOTTARI_ORDER.slice(0, idx));
    }

    function analyzeLongitude(longitude) {
        var lon = ((Number(longitude) % 360) + 360) % 360;
        var signIdx = Math.floor(lon / 30);
        var degInSign = lon % 30;
        var signLord = SIGN_LORDS[signIdx];

        var nakIdx = Math.floor(lon / NAK_SPAN);
        var degInNak = lon - nakIdx * NAK_SPAN;
        var starLord = VIMSHOTTARI_ORDER[nakIdx % 9].name;
        var pada = Math.floor(degInNak / (NAK_SPAN / 4)) + 1;

        var subSeq = rotatedOrder(starLord);
        var acc = 0, subLord = subSeq[0].name, subStart = 0, subSpan = 0;
        for (var i = 0; i < subSeq.length; i++) {
            var sp = NAK_SPAN * (subSeq[i].years / 120);
            if (degInNak < acc + sp || i === subSeq.length - 1) {
                subLord = subSeq[i].name; subStart = acc; subSpan = sp; break;
            }
            acc += sp;
        }

        var degInSub = Math.max(0, degInNak - subStart);
        var sslSeq = rotatedOrder(subLord);
        var accSsl = 0, sslLord = sslSeq[0].name, sslStart = 0, sslSpan = 0;
        for (var j = 0; j < sslSeq.length; j++) {
            var sp2 = subSpan * (sslSeq[j].years / 120);
            if (degInSub < accSsl + sp2 || j === sslSeq.length - 1) {
                sslLord = sslSeq[j].name; sslStart = accSsl; sslSpan = sp2; break;
            }
            accSsl += sp2;
        }

        var degInSsl = Math.max(0, degInSub - sslStart);
        var ssslSeq = rotatedOrder(sslLord);
        var accSssl = 0, ssslLord = ssslSeq[0].name;
        for (var k = 0; k < ssslSeq.length; k++) {
            var sp3 = sslSpan * (ssslSeq[k].years / 120);
            if (degInSsl < accSssl + sp3 || k === ssslSeq.length - 1) {
                ssslLord = ssslSeq[k].name; break;
            }
            accSssl += sp3;
        }

        return {
            longitude: Number(lon.toFixed(6)),
            dms_total: formatDms(lon),
            sign_hi: SIGN_NAMES_HI[signIdx],
            deg_in_sign: formatDms(degInSign),
            sign_lord: signLord,
            nakshatra_hi: NAK_NAMES_HI[nakIdx],
            pada: pada,
            star_lord: starLord,
            sub_lord: subLord,
            sub_sub_lord: sslLord,
            sub_sub_sub_lord: ssslLord,
            chain_hi: hiPlanet(signLord) + ' → ' + hiPlanet(starLord) + ' → ' + hiPlanet(subLord) + ' → ' + hiPlanet(sslLord) + ' → ' + hiPlanet(ssslLord)
        };
    }

    function parseSignDegToLon(signStr, degStr) {
        if (typeof degStr === 'number') return degStr;
        var sIdx = -1;
        for (var i = 0; i < SIGN_NAMES_HI.length; i++) {
            if (signStr && signStr.indexOf(SIGN_NAMES_HI[i]) !== -1) { sIdx = i; break; }
        }
        var m = String(degStr || '').match(/(\d+)[°\s]+(\d+)?(?:'\s*(\d+))?/);
        var d = m ? Number(m[1]) : 0;
        var min = (m && m[2]) ? Number(m[2]) : 0;
        var sec = (m && m[3]) ? Number(m[3]) : 0;
        if (sIdx >= 0 && d < 30) return sIdx * 30 + d + min / 60 + sec / 3600;
        return d + min / 60 + sec / 3600;
    }

    function buildPlanetSignificators(chart, ayanDeltaDeg) {
        var kp = chart && chart.kp ? chart.kp : null;
        var pt = (chart && chart.planet_table) ? chart.planet_table : [];
        var cusps = (kp && kp.cusps) ? kp.cusps : [];
        var delta = Number(ayanDeltaDeg || 0);

        var ownedBy = {};
        var cuspLons = [];
        for (var c = 0; c < cusps.length; c++) {
            var cLon = ((cusps[c].longitude || parseSignDegToLon(cusps[c].sign, cusps[c].deg)) + delta + 360) % 360;
            cuspLons.push(cLon);
            var c5 = analyzeLongitude(cLon);
            var rl = normPlanet(cusps[c].rl) || c5.sign_lord;
            if (!ownedBy[rl]) ownedBy[rl] = [];
            ownedBy[rl].push(Number(cusps[c].cusp || (c + 1)));
        }

        var planets = {};
        var starTenants = {};
        var srcList = (kp && kp.planets && kp.planets.length) ? kp.planets : pt;
        for (var i = 0; i < srcList.length; i++) {
            var row = srcList[i];
            var pName = normPlanet(row.planet || row.name || row.p);
            if (!pName) continue;
            var occ = Number(row.house || row.h || 0);
            if (!occ && row.significator) {
                var hm = String(row.significator).match(/\d+/);
                if (hm) occ = Number(hm[0]);
            }
            var lon = ((row.longitude || row.lon || parseSignDegToLon(row.sign, row.deg || row.degree)) + delta + 360) % 360;
            var chain5 = analyzeLongitude(lon);
            planets[pName] = {
                name: pName,
                hi: hiPlanet(pName),
                lon: lon,
                occ: occ ? [occ] : [],
                owned: ownedBy[pName] || [],
                nl: delta ? chain5.star_lord : (normPlanet(row.nl || row.nakshatra_lord) || chain5.star_lord),
                sl: delta ? chain5.sub_lord : (normPlanet(row.sl || row.sub_lord) || chain5.sub_lord),
                ssl: delta ? chain5.sub_sub_lord : (normPlanet(row.ssl) || chain5.sub_sub_lord),
                sssl: chain5.sub_sub_sub_lord,
                chain5: chain5,
                isRetro: !!(row.isRetro || row.retro || (row.status && String(row.status).indexOf('वक्री') !== -1))
            };
            var nlKey = planets[pName].nl;
            if (!starTenants[nlKey]) starTenants[nlKey] = [];
            if (pName !== nlKey) starTenants[nlKey].push(pName);
        }

        function getBaseHouses(pn) {
            var p = planets[pn];
            if (!p) return [];
            var hSet = {};
            p.occ.concat(p.owned).forEach(function (h) { if (h) hSet[h] = true; });
            if (pn === 'Rahu' || pn === 'Ketu') {
                Object.keys(planets).forEach(function (other) {
                    if (other !== pn && angularDiff(p.lon, planets[other].lon) <= 3.3333) {
                        planets[other].occ.concat(planets[other].owned).forEach(function (h) { if (h) hSet[h] = true; });
                    }
                });
                if (planets[p.nl]) {
                    planets[p.nl].occ.concat(planets[p.nl].owned).forEach(function (h) { if (h) hSet[h] = true; });
                }
                var sg = p.chain5.sign_lord;
                if (planets[sg]) {
                    planets[sg].occ.concat(planets[sg].owned).forEach(function (h) { if (h) hSet[h] = true; });
                }
            }
            return Object.keys(hSet).map(Number).sort(function (a, b) { return a - b; });
        }

        Object.keys(planets).forEach(function (pn) {
            var p = planets[pn];
            var isUntenanted = !starTenants[pn] || starTenants[pn].length === 0;
            var isOwnStar = (p.nl === pn);
            p.isPS = isUntenanted || isOwnStar;
            var nlObj = planets[p.nl] || { occ: [] };
            var stOfSb = (planets[p.sl] && planets[p.sl].nl) ? planets[p.sl].nl : '';
            p.step1 = getBaseHouses(pn);
            p.step2 = getBaseHouses(p.nl);
            p.step3 = getBaseHouses(p.sl);
            p.step4 = stOfSb ? getBaseHouses(stOfSb) : [];
            p.allHouses = Array.from(new Set(p.step1.concat(p.step2, p.step3, p.step4))).sort(function (a, b) { return a - b; });

            var psH = {};
            if (p.isPS) p.step1.forEach(function (h) { psH[h] = true; });
            if (planets[p.nl] && planets[p.nl].isPS) p.step2.forEach(function (h) { psH[h] = true; });
            else nlObj.occ.forEach(function (h) { psH[h] = true; });
            if (planets[p.sl] && planets[p.sl].isPS) p.step3.forEach(function (h) { psH[h] = true; });
            if (stOfSb && planets[stOfSb] && planets[stOfSb].isPS) getBaseHouses(stOfSb).forEach(function (h) { psH[h] = true; });
            else if (stOfSb && planets[stOfSb]) planets[stOfSb].occ.forEach(function (h) { psH[h] = true; });
            p.psHouses = Object.keys(psH).map(Number).sort(function (a, b) { return a - b; });
        });

        return { planets: planets, cusps: cusps, cuspLons: cuspLons };
    }

    function evaluateDomain(chart, domainKey, ayanMode) {
        var dom = KP_DOMAINS[domainKey] || KP_DOMAINS.job;
        var delta = (ayanMode === 'kp_old') ? (5.5 / 60) : ((ayanMode === 'kp_straight') ? (-2.0 / 60) : 0);
        var built = buildPlanetSignificators(chart, delta);
        var cusps = built.cusps;
        var planets = built.planets;

        var cIdx = dom.cusp - 1;
        var cLon = built.cuspLons[cIdx] || 0;
        var c5 = analyzeLongitude(cLon);

        var csl = normPlanet(c5.sub_lord);
        var cssl = normPlanet(c5.sub_sub_lord);
        var cslObj = planets[csl] || { step1: [], step2: [], step3: [], step4: [], allHouses: [], psHouses: [], isPS: false, nl: '-', sl: '-', isRetro: false };
        var csslObj = planets[cssl] || { allHouses: [], isPS: false };
        var houses = cslObj.allHouses || [];
        var psHouses = cslObj.psHouses || [];
        var csslHouses = csslObj.allHouses || [];

        var supHits = dom.supportive.filter(function (h) { return houses.indexOf(h) !== -1; });
        var negHits = dom.negating.filter(function (h) { return houses.indexOf(h) !== -1; });
        var psSupHits = dom.supportive.filter(function (h) { return psHouses.indexOf(h) !== -1; });
        var csslSupHits = dom.supportive.filter(function (h) { return csslHouses.indexOf(h) !== -1; });

        var twelfthFromCusp = ((dom.cusp - 2 + 12) % 12) + 1;
        var khullarSup = [], khullarNeg = [];
        csslHouses.forEach(function (h) {
            var rel = ((h - dom.cusp + 12) % 12) + 1;
            if ([1, 3, 5, 9, 11].indexOf(rel) !== -1) khullarSup.push(h + ' (सापेक्ष ' + rel + ')');
            if ([4, 7, 8, 12].indexOf(rel) !== -1) khullarNeg.push(h + ' (सापेक्ष ' + rel + ')');
        });

        var supScore = supHits.length * 2 + psSupHits.length * 2 + csslSupHits.length;
        var negScore = negHits.length * 2 + (csslHouses.indexOf(twelfthFromCusp) !== -1 ? 3 : 0);
        var retroFlag = cslObj.isRetro || (planets[cslObj.nl] && planets[cslObj.nl].isRetro);

        var verdictHi = 'प्रबल योग (PROMISED)';
        var color = '#10b981';
        if (supScore >= 4 && supScore > negScore) {
            if (retroFlag) { verdictHi = 'वक्री विलंब के बाद सिद्धि (DELAYED PROMISE)'; color = '#eab308'; }
        } else if (supScore > 0 && supScore >= negScore - 1) {
            verdictHi = 'मिश्रित / सशर्त योग (MIXED / CONDITIONAL)'; color = '#f59e0b';
        } else {
            verdictHi = 'कस्पल अस्वीकृति / प्रबल अवरोध (DENIED)'; color = '#ef4444';
        }

        // Direct cusp degree hits (Nakshatra Nadi Hit Theory <= 3 deg)
        var cuspHits = [];
        Object.keys(planets).forEach(function (pn) {
            var diff = angularDiff(planets[pn].lon, cLon);
            if (diff <= 3.0) cuspHits.push(hiPlanet(pn) + ' (' + diff.toFixed(2) + '°)');
        });

        // K. Baskaran & A. Devaraj checks
        var baskaranStar = planets[cslObj.nl] || { occ: [], owned: [], isPS: false };
        var devarajMicroSup = dom.supportive.filter(function (h) { return houses.indexOf(h) !== -1 && csslHouses.indexOf(h) !== -1; });
        var devarajMicroNeg = dom.negating.filter(function (h) { return houses.indexOf(h) !== -1 || csslHouses.indexOf(h) !== -1; });

        return {
            domain: dom,
            cusp5: c5,
            csl: csl,
            cslHi: hiPlanet(csl),
            csslHi: hiPlanet(cssl),
            cslData: cslObj,
            csslData: csslObj,
            supHits: supHits,
            negHits: negHits,
            supScore: supScore,
            negScore: negScore,
            retroFlag: retroFlag,
            khullarSup: khullarSup,
            khullarNeg: khullarNeg,
            twelfthNegated: csslHouses.indexOf(twelfthFromCusp) !== -1,
            cuspHits: cuspHits,
            baskaran: { starHi: hiPlanet(cslObj.nl), isPS: baskaranStar.isPS, baseHouses: baskaranStar.occ.concat(baskaranStar.owned) },
            devaraj: { microSup: devarajMicroSup, microNeg: devarajMicroNeg },
            verdictHi: verdictHi,
            color: color,
            planets: planets,
            cuspLons: built.cuspLons
        };
    }

    function computeLiveRulingPlanets() {
        var now = new Date();
        var jd = now.getTime() / 86400000 + 2440587.5;
        var t = (jd - 2451545.0) / 36525.0;
        var ayan = 23.85 + 0.01396 * (now.getFullYear() - 2000 + now.getMonth() / 12);
        var moonTrop = (218.3165 + 481267.8813 * t) % 360;
        var moonSid = ((moonTrop - ayan) % 360 + 360) % 360;
        var m5 = analyzeLongitude(moonSid);
        var dayLords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'];
        return {
            dayLord: hiPlanet(dayLords[now.getDay()]),
            moonSignLord: hiPlanet(m5.sign_lord),
            moonStarLord: hiPlanet(m5.star_lord),
            moonSubLord: hiPlanet(m5.sub_lord),
            moonDms: m5.dms_total + ' (' + m5.sign_hi + ')'
        };
    }

    function calcManual5Level(cid) {
        var s = parseInt((document.getElementById(cid + '_s') || {}).value || '0', 10);
        var d = parseFloat((document.getElementById(cid + '_d') || {}).value || '14');
        var m = parseFloat((document.getElementById(cid + '_m') || {}).value || '23');
        var sec = parseFloat((document.getElementById(cid + '_sec') || {}).value || '0');
        var lon = s * 30 + d + m / 60 + sec / 3600;
        var res = analyzeLongitude(lon);
        var out = document.getElementById(cid + '_5res');
        if (out) {
            out.innerHTML =
                '<div style="padding:10px 12px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-gold); font-size:0.86rem;">' +
                '<div><b>स्पष्ट अंश:</b> ' + res.sign_hi + ' ' + res.deg_in_sign + ' • <b>नक्षत्र:</b> ' + res.nakshatra_hi + ' (पाद ' + res.pada + ')</div>' +
                '<div style="margin-top:6px; font-weight:800; color:var(--primary); font-family:var(--font-mono);">5-Level: ' + res.chain_hi + '</div>' +
                '</div>';
        }
    }

    function switchSuiteTab(cid, tab) {
        ['schools', 'five', 'rot'].forEach(function (t) {
            var p = document.getElementById(cid + '_tab_' + t);
            var b = document.getElementById(cid + '_btn_' + t);
            if (p) p.style.display = (t === tab) ? 'block' : 'none';
            if (b) {
                b.style.background = (t === tab) ? 'var(--gold-gradient)' : 'var(--bg-card-alt)';
                b.style.color = (t === tab) ? '#090d16' : 'var(--text-primary)';
            }
        });
    }

    function renderPanel(chart, containerId) {
        var target = document.getElementById(containerId);
        if (!target) return;

        var domSelectId = containerId + '_domain';
        var ayaSelectId = containerId + '_aya';
        var rotSelectId = containerId + '_rot';
        var selectedDomain = (document.getElementById(domSelectId) && document.getElementById(domSelectId).value) || 'job';
        var selectedAya = (document.getElementById(ayaSelectId) && document.getElementById(ayaSelectId).value) || 'kp_new';
        var selectedRot = parseInt((document.getElementById(rotSelectId) && document.getElementById(rotSelectId).value) || '1', 10);
        var rp = computeLiveRulingPlanets();

        var domainOptions = Object.keys(KP_DOMAINS).map(function (k) {
            return '<option value="' + k + '"' + (k === selectedDomain ? ' selected' : '') + '>' + KP_DOMAINS[k].label + '</option>';
        }).join('');

        var rotOptions = '';
        for (var rh = 1; rh <= 12; rh++) {
            rotOptions += '<option value="' + rh + '"' + (rh === selectedRot ? ' selected' : '') + '>भाव ' + rh + ' को लग्न बनाएं</option>';
        }

        var schoolsHtml = '';
        var rotHtml = '';
        if (!chart || !chart.kp) {
            schoolsHtml = '<div style="padding:14px; border-radius:10px; background:rgba(212,175,55,0.08); border:1px dashed var(--border-gold); color:var(--text-secondary); font-size:0.88rem;">' +
                '✦ सटीक 6-School KP Matrix (KSK • 4-Step • Khullar • Nadi • Baskaran • Devaraj) एवं House Rotation के लिए कृपया कुण्डली लोड या निर्मित करें।' +
                '</div>';
            rotHtml = schoolsHtml;
        } else {
            var ev = evaluateDomain(chart, selectedDomain, selectedAya);
            var pt = chart.planet_table || [];
            var asc = parseSignDegToLon(chart.profile ? chart.profile.asc_sign : 'मेष', chart.profile ? chart.profile.asc_dms : '0°00');
            var sunLon = 0, moonLon = 0;
            for (var i = 0; i < pt.length; i++) {
                var nm = normPlanet(pt[i].name || pt[i].p);
                if (nm === 'Sun') sunLon = pt[i].longitude || parseSignDegToLon(pt[i].sign, pt[i].degree || pt[i].d);
                if (nm === 'Moon') moonLon = pt[i].longitude || parseSignDegToLon(pt[i].sign, pt[i].degree || pt[i].d);
            }
            var fortuna = analyzeLongitude((asc + moonLon - sunLon + 360) % 360);

            var psRows = Object.keys(ev.planets).map(function (pk) {
                var p = ev.planets[pk];
                return '<tr>' +
                    '<td><b>' + p.hi + '</b> ' + (p.isPS ? '<span style="font-size:0.7rem; background:rgba(16,185,129,0.16); color:#10b981; padding:1px 6px; border-radius:999px; font-weight:800;">PS</span>' : '') + '</td>' +
                    '<td>' + (p.step1.join(',') || '-') + '</td>' +
                    '<td>' + (p.step2.join(',') || '-') + '</td>' +
                    '<td>' + (p.step3.join(',') || '-') + '</td>' +
                    '<td>' + (p.step4.join(',') || '-') + '</td>' +
                    '<td style="font-size:0.76rem; font-family:var(--font-mono);">' + p.chain5.chain_hi + '</td>' +
                    '</tr>';
            }).join('');

            schoolsHtml =
                '<div style="padding:12px 14px; border-radius:12px; background:var(--bg-card-alt); border:1.5px solid ' + ev.color + '; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">' +
                '  <div>' +
                '    <div style="font-size:0.76rem; color:var(--text-muted); font-weight:700;">BLUF KP 6-School Verdict (' + ev.domain.cusp + 'वां कस्प: ' + ev.cslHi + ' SL / ' + ev.csslHi + ' SSL)</div>' +
                '    <div style="font-size:1.06rem; font-weight:900; color:' + ev.color + '; margin-top:2px;">' + ev.verdictHi + '</div>' +
                '  </div>' +
                '  <div style="font-size:0.84rem; text-align:right;">' +
                '    Promise Score: <b style="color:#10b981;">' + ev.supScore + '</b> • Obstruction: <b style="color:#ef4444;">' + ev.negScore + '</b><br>' +
                '    <span style="font-size:0.78rem; color:var(--text-muted);">RP: दिन-' + rp.dayLord + ' • चन्द्र-' + rp.moonSignLord + '/' + rp.moonStarLord + '/' + rp.moonSubLord + '</span>' +
                '  </div>' +
                '</div>' +
                '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-bottom:12px;">' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">1. KP Default (KSK)</b><br>CSL: <b>' + ev.cslHi + '</b> (NL: ' + hiPlanet(ev.cslData.nl) + ')<br>समर्थक: <b>' + (ev.supHits.join(',') || '-') + '</b> • बाधक: <b>' + (ev.negHits.join(',') || '-') + '</b>' +
                '  </div>' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">2. Four-Step Theory</b><br>PS Status: <b>' + (ev.cslData.isPS ? 'YES (Untenanted/Self)' : 'Tenanted') + '</b><br>PS भाव: <b>' + (ev.cslData.psHouses.join(',') || '-') + '</b>' +
                '  </div>' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">3. S.P. Khullar (CIL)</b><br>CSSL: <b>' + ev.csslHi + '</b> (' + (ev.twelfthNegated ? '<span style="color:#ef4444;">12वां व्यय!</span>' : '<span style="color:#10b981;">12वां मुक्त</span>') + ')<br>शुभ सापेक्ष: <b>' + (ev.khullarSup.slice(0, 3).join(', ') || '-') + '</b>' +
                '  </div>' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">4. Nakshatra Nadi (Hit)</b><br>कस्प Hit (≤3°): <b>' + (ev.cuspHits.join(', ') || 'कोई नहीं') + '</b><br>Fortuna: <b>' + fortuna.sign_hi + ' ' + fortuna.deg_in_sign + ' (' + hiPlanet(fortuna.sub_lord) + ' SL)</b>' +
                '  </div>' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">5. K. Baskaran Check</b><br>CSL Star Lord: <b>' + ev.baskaran.starHi + '</b> (' + (ev.baskaran.isPS ? 'PS' : 'Tenanted') + ')<br>मूल भाव: <b>' + (ev.baskaran.baseHouses.join(',') || '-') + '</b>' +
                '  </div>' +
                '  <div style="padding:10px; border-radius:10px; background:var(--bg-card-alt); border:1px solid var(--border-subtle); font-size:0.82rem;">' +
                '    <b style="color:var(--primary);">6. A. Devaraj Check</b><br>Chain: <b>' + ev.cslHi + ' → ' + ev.csslHi + '</b><br>Micro शुभ: <b>' + (ev.devaraj.microSup.join(',') || '-') + '</b> • अवरोध: <b>' + (ev.devaraj.microNeg.join(',') || '-') + '</b>' +
                '  </div>' +
                '</div>' +
                '<div style="overflow-x:auto;">' +
                '  <table class="astronomy-table m-table kp-table" style="width:100%; font-size:0.82rem;">' +
                '    <thead><tr><th>ग्रह (PS)</th><th>Step 1 (स्वयं)</th><th>Step 2 (नक्षत्र)</th><th>Step 3 (Sub)</th><th>Step 4 (Sub-Star)</th><th>5-Level Chain (RL→SSSL)</th></tr></thead>' +
                '    <tbody>' + psRows + '</tbody>' +
                '  </table>' +
                '</div>';

            // House Rotation Table
            var rotRows = '';
            for (var rIdx = 0; rIdx < 12; rIdx++) {
                var origH = ((selectedRot - 1 + rIdx) % 12) + 1;
                var c5r = analyzeLongitude(ev.cuspLons[origH - 1] || 0);
                rotRows += '<tr><td><b>रोटेटेड ' + (rIdx + 1) + '</b> (मूल ' + origH + ')</td><td>' + c5r.sign_hi + ' ' + c5r.deg_in_sign + '</td><td style="font-family:var(--font-mono); font-size:0.78rem;">' + c5r.chain_hi + '</td></tr>';
            }
            rotHtml = '<div style="margin-bottom:10px;"><label style="font-size:0.82rem; color:var(--text-muted);">किस भाव से कुण्डली घुमाएं (House Rotation):</label> ' +
                '<select id="' + rotSelectId + '" onchange="VyasKPApex.renderPanel(window._vyasLastKPChart, \'' + containerId + '\')" style="padding:6px 10px; border-radius:8px; border:1px solid var(--border-gold); background:var(--bg-card); color:var(--text-primary); font-weight:700;">' + rotOptions + '</select></div>' +
                '<div style="overflow-x:auto;"><table class="astronomy-table m-table kp-table" style="width:100%; font-size:0.82rem;"><thead><tr><th>रोटेटेड भाव</th><th>राशि व अंश</th><th>5-Level Chain</th></tr></thead><tbody>' + rotRows + '</tbody></table></div>';
        }

        var signOpts = SIGN_NAMES_HI.map(function (s, idx) { return '<option value="' + idx + '">' + (idx + 1) + '. ' + s + '</option>'; }).join('');
        var fiveHtml =
            '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(110px, 1fr)); gap:8px; margin-bottom:10px;">' +
            '  <div><label style="font-size:0.75rem; color:var(--text-muted);">राशि</label><select id="' + containerId + '_s" style="width:100%; padding:7px; border-radius:8px;">' + signOpts + '</select></div>' +
            '  <div><label style="font-size:0.75rem; color:var(--text-muted);">अंश (Deg)</label><input id="' + containerId + '_d" type="number" value="14" min="0" max="29" style="width:100%; padding:7px; border-radius:8px;"></div>' +
            '  <div><label style="font-size:0.75rem; color:var(--text-muted);">कला (Min)</label><input id="' + containerId + '_m" type="number" value="23" min="0" max="59" style="width:100%; padding:7px; border-radius:8px;"></div>' +
            '  <div><label style="font-size:0.75rem; color:var(--text-muted);">विकला (Sec)</label><input id="' + containerId + '_sec" type="number" value="0" min="0" max="59" style="width:100%; padding:7px; border-radius:8px;"></div>' +
            '</div>' +
            '<button type="button" onclick="VyasKPApex.calcManual5Level(\'' + containerId + '\')" class="gold-btn btn-action" style="padding:8px 16px; border-radius:8px; font-weight:800; cursor:pointer; margin-bottom:10px;">5-Level Chain निकालें</button>' +
            '<div id="' + containerId + '_5res"></div>';

        target.innerHTML =
            '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">' +
            '  <div>' +
            '    <b style="color:var(--primary); font-size:1.02rem;">⚝ KP Stellar Apex Suite v3 (6-School Multi-Engine)</b>' +
            '    <div style="font-size:0.78rem; color:var(--text-muted);">KSK • 4-Step • Khullar CIL • Nakshatra Nadi • Baskaran • Devaraj</div>' +
            '  </div>' +
            '  <div style="display:flex; gap:6px; align-items:center; flex-wrap:wrap;">' +
            '    <select id="' + domSelectId + '" onchange="VyasKPApex.renderPanel(window._vyasLastKPChart, \'' + containerId + '\')" style="padding:6px 10px; border-radius:8px; border:1px solid var(--border-gold); background:var(--bg-card); color:var(--text-primary); font-size:0.82rem; font-weight:700;">' + domainOptions + '</select>' +
            '    <select id="' + ayaSelectId + '" onchange="VyasKPApex.renderPanel(window._vyasLastKPChart, \'' + containerId + '\')" style="padding:6px 10px; border-radius:8px; border:1px solid var(--border-subtle); background:var(--bg-card); color:var(--text-primary); font-size:0.82rem; font-weight:700;">' +
            '      <option value="kp_new"' + (selectedAya === 'kp_new' ? ' selected' : '') + '>KP New</option>' +
            '      <option value="kp_old"' + (selectedAya === 'kp_old' ? ' selected' : '') + '>KP Old (+5.5\')</option>' +
            '      <option value="kp_straight"' + (selectedAya === 'kp_straight' ? ' selected' : '') + '>KP Straight (-2\')</option>' +
            '    </select>' +
            '  </div>' +
            '</div>' +
            '<div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;">' +
            '  <button type="button" id="' + containerId + '_btn_schools" onclick="VyasKPApex.switchSuiteTab(\'' + containerId + '\', \'schools\')" style="padding:6px 12px; border-radius:8px; border:1px solid var(--border-gold); background:var(--gold-gradient); color:#090d16; font-weight:800; font-size:0.82rem; cursor:pointer;">1. 6-School Matrix</button>' +
            '  <button type="button" id="' + containerId + '_btn_five" onclick="VyasKPApex.switchSuiteTab(\'' + containerId + '\', \'five\')" style="padding:6px 12px; border-radius:8px; border:1px solid var(--border-subtle); background:var(--bg-card-alt); color:var(--text-primary); font-weight:700; font-size:0.82rem; cursor:pointer;">2. SubLord 5-Level</button>' +
            '  <button type="button" id="' + containerId + '_btn_rot" onclick="VyasKPApex.switchSuiteTab(\'' + containerId + '\', \'rot\')" style="padding:6px 12px; border-radius:8px; border:1px solid var(--border-subtle); background:var(--bg-card-alt); color:var(--text-primary); font-weight:700; font-size:0.82rem; cursor:pointer;">3. House Rotation</button>' +
            '</div>' +
            '<div id="' + containerId + '_tab_schools">' + schoolsHtml + '</div>' +
            '<div id="' + containerId + '_tab_five" style="display:none;">' + fiveHtml + '</div>' +
            '<div id="' + containerId + '_tab_rot" style="display:none;">' + rotHtml + '</div>';

        window._vyasLastKPChart = chart;
        if (typeof window.vyasSyncThemeSurfaces === 'function') {
            setTimeout(window.vyasSyncThemeSurfaces, 40);
        }
    }

    global.VyasKPApex = {
        analyzeLongitude: analyzeLongitude,
        evaluateDomain: evaluateDomain,
        computeLiveRulingPlanets: computeLiveRulingPlanets,
        calcManual5Level: calcManual5Level,
        switchSuiteTab: switchSuiteTab,
        renderPanel: renderPanel
    };
})(window);
