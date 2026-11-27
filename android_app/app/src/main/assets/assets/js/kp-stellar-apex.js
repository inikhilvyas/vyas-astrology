/**
 * VYAS ASTRA — KP Stellar Apex Engine (v1.0)
 * Deterministic Krishnamurti Paddhati & Stellar Astrology Core:
 * - 5-Level KP Chain (RL -> NL -> SL -> SSL -> SSSL)
 * - Classical KSK 4-Level Significators + 4-Step Theory (Sunil Gondhalekar)
 * - S.P. Khullar Cuspal Interlinks (CIL), Nakshatra Nadi, K. Baskaran & A. Devaraj
 * - Pars Fortuna & Live Ruling Planets (RP)
 */
(function (global) {
    'use strict';

    var VIMSHOTTARI_ORDER = [
        { name: 'Ketu', hi: 'केतु', abbr: 'Ke', years: 7 },
        { name: 'Venus', hi: 'शुक्र', abbr: 'Ve', years: 20 },
        { name: 'Sun', hi: 'सूर्य', abbr: 'Su', years: 6 },
        { name: 'Moon', hi: 'चन्द्र', abbr: 'Mo', years: 10 },
        { name: 'Mars', hi: 'मंगल', abbr: 'Ma', years: 7 },
        { name: 'Rahu', hi: 'राहु', abbr: 'Ra', years: 18 },
        { name: 'Jupiter', hi: 'गुरु', abbr: 'Ju', years: 16 },
        { name: 'Saturn', hi: 'शनि', abbr: 'Sa', years: 19 },
        { name: 'Mercury', hi: 'बुध', abbr: 'Me', years: 17 }
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
        marriage: { label: 'विवाह एवं दांपत्य (Marriage)', cusp: 7, supportive: [2, 7, 11], negating: [1, 6, 10] },
        job: { label: 'नौकरी / सेवा प्राप्ति (Job / Service)', cusp: 6, supportive: [2, 6, 10, 11], negating: [1, 5, 8, 9, 12] },
        business: { label: 'स्वतंत्र व्यवसाय (Business)', cusp: 7, supportive: [2, 7, 10, 11], negating: [5, 8, 12] },
        promotion: { label: 'करियर उन्नति / पदोन्नति (Promotion)', cusp: 10, supportive: [2, 6, 10, 11], negating: [5, 8, 9, 12] },
        wealth: { label: 'धन एवं आर्थिक लाभ (Wealth & Gains)', cusp: 11, supportive: [2, 6, 11], negating: [5, 8, 12] },
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
        var m = String(degStr || '').match(/(\d+)[°\s]+(\d+)?/);
        var d = m ? Number(m[1]) : 0;
        var min = (m && m[2]) ? Number(m[2]) : 0;
        if (sIdx >= 0 && d < 30) return sIdx * 30 + d + min / 60;
        return d + min / 60;
    }

    function buildPlanetSignificators(chart) {
        var kp = chart && chart.kp ? chart.kp : null;
        var pt = (chart && chart.planet_table) ? chart.planet_table : [];
        var cusps = (kp && kp.cusps) ? kp.cusps : [];

        var ownedBy = {};
        for (var c = 0; c < cusps.length; c++) {
            var rl = normPlanet(cusps[c].rl);
            if (!rl) continue;
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
            var nl = normPlanet(row.nl || row.nakshatra_lord);
            var sl = normPlanet(row.sl || row.sub_lord);
            var ssl = normPlanet(row.ssl);
            var lon = row.longitude || row.lon || parseSignDegToLon(row.sign, row.deg || row.degree);
            var chain5 = analyzeLongitude(lon);
            planets[pName] = {
                name: pName,
                hi: hiPlanet(pName),
                occ: occ ? [occ] : [],
                owned: ownedBy[pName] || [],
                nl: nl || chain5.star_lord,
                sl: sl || chain5.sub_lord,
                ssl: ssl || chain5.sub_sub_lord,
                sssl: chain5.sub_sub_sub_lord,
                chain5: chain5
            };
            var nlKey = planets[pName].nl;
            if (!starTenants[nlKey]) starTenants[nlKey] = [];
            if (pName !== nlKey) starTenants[nlKey].push(pName);
        }

        Object.keys(planets).forEach(function (pn) {
            var p = planets[pn];
            var isUntenanted = !starTenants[pn] || starTenants[pn].length === 0;
            var isOwnStar = (p.nl === pn);
            p.isPS = isUntenanted || isOwnStar;
            var nlObj = planets[p.nl] || { occ: [], owned: [] };
            var slObj = planets[p.sl] || { occ: [], owned: [] };
            var sslObj = planets[p.ssl] || { occ: [], owned: [] };
            p.step1 = Array.from(new Set(p.occ.concat(p.owned)));
            p.step2 = Array.from(new Set(nlObj.occ.concat(nlObj.owned)));
            p.step3 = Array.from(new Set(slObj.occ.concat(slObj.owned)));
            p.step4 = Array.from(new Set(sslObj.occ.concat(sslObj.owned)));
            p.allHouses = Array.from(new Set(p.step1.concat(p.step2, p.step3, p.step4)));
        });

        return { planets: planets, cusps: cusps };
    }

    function evaluateDomain(chart, domainKey) {
        var dom = KP_DOMAINS[domainKey] || KP_DOMAINS.marriage;
        var built = buildPlanetSignificators(chart);
        var cusps = built.cusps;
        var planets = built.planets;

        var cIdx = dom.cusp - 1;
        var cObj = cusps[cIdx] || { cusp: dom.cusp, sign: '-', deg: '-', rl: '-', nl: '-', sl: '-', ssl: '-' };
        var cLon = parseSignDegToLon(cObj.sign, cObj.deg);
        var c5 = analyzeLongitude(cLon);

        var csl = normPlanet(cObj.sl || c5.sub_lord);
        var cslObj = planets[csl] || { step1: [], step2: [], step3: [], step4: [], allHouses: [], isPS: false };
        var houses = cslObj.allHouses || [];

        var supHits = dom.supportive.filter(function (h) { return houses.indexOf(h) !== -1; });
        var negHits = dom.negating.filter(function (h) { return houses.indexOf(h) !== -1; });

        var khullarSup = [], khullarNeg = [];
        houses.forEach(function (h) {
            var rel = ((h - dom.cusp + 12) % 12) + 1;
            if ([1, 3, 5, 9, 11].indexOf(rel) !== -1) khullarSup.push(h + ' (सापेक्ष ' + rel + ')');
            if ([4, 7, 8, 12].indexOf(rel) !== -1) khullarNeg.push(h + ' (सापेक्ष ' + rel + ')');
        });

        var verdict = 'PROMISED';
        var verdictHi = 'प्रबल योग (PROMISED)';
        var color = '#10b981';
        if (supHits.length === 0 && negHits.length > 0) {
            verdict = 'DENIED'; verdictHi = 'कस्पल अस्वीकृति (DENIED)'; color = '#ef4444';
        } else if (negHits.length > supHits.length) {
            verdict = 'OBSTRUCTED'; verdictHi = 'अवरोध व विलंब (OBSTRUCTED / DELAYED)'; color = '#f59e0b';
        } else if (supHits.length > 0 && negHits.length > 0) {
            verdict = 'DELAYED'; verdictHi = 'संघर्ष के बाद सिद्धि (PROMISED WITH DELAY)'; color = '#eab308';
        }

        return {
            domain: dom,
            cusp5: c5,
            csl: csl,
            cslHi: hiPlanet(csl),
            cslData: cslObj,
            supHits: supHits,
            negHits: negHits,
            khullarSup: khullarSup,
            khullarNeg: khullarNeg,
            verdict: verdict,
            verdictHi: verdictHi,
            color: color,
            planets: planets
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
        var dl = dayLords[now.getDay()];
        return {
            dayLord: hiPlanet(dl),
            moonSignLord: hiPlanet(m5.sign_lord),
            moonStarLord: hiPlanet(m5.star_lord),
            moonSubLord: hiPlanet(m5.sub_lord),
            moonDms: m5.dms_total + ' (' + m5.sign_hi + ')'
        };
    }

    function renderPanel(chart, containerId) {
        var target = document.getElementById(containerId);
        if (!target) return;

        var domSelectId = containerId + '_domain';
        var selectedDomain = (document.getElementById(domSelectId) && document.getElementById(domSelectId).value) || 'marriage';
        var rp = computeLiveRulingPlanets();

        var domainOptions = Object.keys(KP_DOMAINS).map(function (k) {
            return '<option value="' + k + '"' + (k === selectedDomain ? ' selected' : '') + '>' + KP_DOMAINS[k].label + '</option>';
        }).join('');

        var bodyHtml = '';
        if (!chart || !chart.kp) {
            bodyHtml = '<div style="padding:14px; border-radius:10px; background:rgba(212,175,55,0.08); border:1px dashed var(--border-gold); color:var(--text-secondary); font-size:0.88rem;">' +
                '✦ सटीक 4-Step Theory, S.P. Khullar (CIL), Nakshatra Nadi एवं 5-Level Sub-Lord विश्लेषण के लिए पहले कुण्डली लोड या निर्मित करें।' +
                '</div>';
        } else {
            var ev = evaluateDomain(chart, selectedDomain);
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
                    '<td style="font-size:0.8rem;">' + (p.step1.join(',') || '-') + '</td>' +
                    '<td style="font-size:0.8rem;">' + (p.step2.join(',') || '-') + '</td>' +
                    '<td style="font-size:0.8rem;">' + (p.step3.join(',') || '-') + '</td>' +
                    '<td style="font-size:0.8rem;">' + (p.step4.join(',') || '-') + '</td>' +
                    '<td style="font-size:0.76rem; font-family:var(--font-mono);">' + p.chain5.chain_hi + '</td>' +
                    '</tr>';
            }).join('');

            bodyHtml =
                '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; margin-bottom:12px;">' +
                '  <div style="padding:12px; border-radius:12px; background:var(--bg-card-alt); border:1px solid ' + ev.color + ';">' +
                '    <div style="font-size:0.76rem; color:var(--text-muted); font-weight:700;">BLUF KP निर्णय (' + ev.domain.cusp + 'वां कस्प: ' + ev.cslHi + ' SL)</div>' +
                '    <div style="font-size:1.02rem; font-weight:900; color:' + ev.color + '; margin-top:4px;">' + ev.verdictHi + '</div>' +
                '    <div style="font-size:0.82rem; color:var(--text-secondary); margin-top:6px;">समर्थक भाव: <b>' + (ev.supHits.join(', ') || 'कोई नहीं') + '</b> • बाधक: <b>' + (ev.negHits.join(', ') || 'कोई नहीं') + '</b></div>' +
                '  </div>' +
                '  <div style="padding:12px; border-radius:12px; background:var(--bg-card-alt); border:1px solid var(--border-gold);">' +
                '    <div style="font-size:0.76rem; color:var(--text-muted); font-weight:700;">S.P. Khullar (CIL) & 5-Level Chain</div>' +
                '    <div style="font-size:0.84rem; color:var(--text-primary); font-weight:700; margin-top:4px;">' + ev.cusp5.chain_hi + '</div>' +
                '    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:6px;">सापेक्ष शुभ: ' + (ev.khullarSup.slice(0, 3).join(', ') || '-') + '</div>' +
                '  </div>' +
                '  <div style="padding:12px; border-radius:12px; background:var(--bg-card-alt); border:1px solid var(--border-subtle);">' +
                '    <div style="font-size:0.76rem; color:var(--text-muted); font-weight:700;">Pars Fortuna (सहम्) & तात्कालिक RP</div>' +
                '    <div style="font-size:0.84rem; color:var(--primary); font-weight:800; margin-top:4px;">Fortuna: ' + fortuna.sign_hi + ' ' + fortuna.deg_in_sign + ' (' + hiPlanet(fortuna.sub_lord) + ' SL)</div>' +
                '    <div style="font-size:0.8rem; color:var(--text-secondary); margin-top:4px;">RP: दिन-' + rp.dayLord + ' • चन्द्र-' + rp.moonSignLord + '/' + rp.moonStarLord + '/' + rp.moonSubLord + '</div>' +
                '  </div>' +
                '</div>' +
                '<div style="overflow-x:auto;">' +
                '  <table class="astronomy-table m-table" style="width:100%; font-size:0.82rem;">' +
                '    <thead><tr><th>ग्रह (PS)</th><th>Step 1 (स्वयं)</th><th>Step 2 (नक्षत्र)</th><th>Step 3 (Sub)</th><th>Step 4 (Sub-Star)</th><th>5-Level Chain (RL→SSSL)</th></tr></thead>' +
                '    <tbody>' + psRows + '</tbody>' +
                '  </table>' +
                '</div>';
        }

        target.innerHTML =
            '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">' +
            '  <div>' +
            '    <b style="color:var(--primary); font-size:1rem;">⚝ KP Stellar Apex Engine (KSK • 4-Step • Khullar • Nadi • 5-Level)</b>' +
            '    <div style="font-size:0.78rem; color:var(--text-muted);">Zero-Hallucination Deterministic Sub-Lord & Cuspal Interlink Synthesizer</div>' +
            '  </div>' +
            '  <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">' +
            '    <select id="' + domSelectId + '" onchange="VyasKPApex.renderPanel(window._vyasLastKPChart, \'' + containerId + '\')" style="padding:7px 10px; border-radius:8px; border:1px solid var(--border-gold); background:var(--bg-card); color:var(--text-primary); font-size:0.84rem; font-weight:700;">' + domainOptions + '</select>' +
            '  </div>' +
            '</div>' +
            bodyHtml;

        window._vyasLastKPChart = chart;
        if (typeof window.vyasSyncThemeSurfaces === 'function') {
            setTimeout(window.vyasSyncThemeSurfaces, 40);
        }
    }

    global.VyasKPApex = {
        analyzeLongitude: analyzeLongitude,
        evaluateDomain: evaluateDomain,
        computeLiveRulingPlanets: computeLiveRulingPlanets,
        renderPanel: renderPanel
    };
})(window);
