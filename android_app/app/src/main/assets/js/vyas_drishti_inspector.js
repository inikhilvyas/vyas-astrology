/**
 * VYAS ASTRA — Interactive Bhava & Graha Drishti Inspector
 * Tap any House (भाव) or Planet (ग्रह) on the North Indian Diamond Kundli SVG
 * to inspect incoming/outgoing Parashari Drishti arrows, Bhava Lord placement,
 * owned houses (dashed highlight), and 0°-30° Nakshatra Pada ruler.
 */
(function (global) {
    'use strict';

    var BHAVA_META = {
        1:  { name: 'तनु (लग्न)', sig: 'शरीर, व्यक्तित्व, आरोग्य, आत्मबल', tags: ['केंद्र', 'त्रिकोण'] },
        2:  { name: 'धन', sig: 'कुटुम्ब, वाणी, संचित धन, भोजन', tags: ['पणफर', 'मारक'] },
        3:  { name: 'सहज', sig: 'भाई-बहन, साहस, प्रयास, संचार', tags: ['आपोक्लिम', 'उपचय'] },
        4:  { name: 'सुख', sig: 'माता, भूमि, भवन, वाहन, मन', tags: ['केंद्र'] },
        5:  { name: 'पुत्र (विद्या)', sig: 'संतान, बुद्धि, पूर्वपुण्य, मंत्र', tags: ['त्रिकोण', 'पणफर'] },
        6:  { name: 'रिपु (रोग)', sig: 'शत्रु, रोग, ऋण, सेवा, प्रतियोगिता', tags: ['दुस्थान', 'उपचय'] },
        7:  { name: 'कलत्र', sig: 'जीवनसाथी, विवाह, साझेदारी, व्यापार', tags: ['केंद्र', 'मारक'] },
        8:  { name: 'आयु (रन्ध्र)', sig: 'आयु, गुप्त विद्या, शोध, आकस्मिकता', tags: ['दुस्थान', 'पणफर'] },
        9:  { name: 'भाग्य (धर्म)', sig: 'धर्म, भाग्य, पिता, गुरु, तीर्थ', tags: ['त्रिकोण', 'आपोक्लिम'] },
        10: { name: 'कर्म', sig: 'कर्मक्षेत्र, राज्य, पद, प्रतिष्ठा', tags: ['केंद्र', 'उपचय'] },
        11: { name: 'लाभ (आय)', sig: 'आय, बड़े भाई-बहन, सिद्धि, मित्र', tags: ['पणफर', 'उपचय'] },
        12: { name: 'व्यय (मोक्ष)', sig: 'व्यय, विदेश, शयन, मोक्ष, दान', tags: ['दुस्थान', 'आपोक्लिम'] }
    };

    var SIGN_NAMES = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुम्भ', 'मीन'];
    var SIGN_LORDS = ['मंगल', 'शुक्र', 'बुध', 'चन्द्र', 'सूर्य', 'बुध', 'शुक्र', 'मंगल', 'गुरु', 'शनि', 'शनि', 'गुरु'];
    var NAK_NAMES = [
        'अश्विनी', 'भरणी', 'कृत्तिका', 'रोहिणी', 'मृगशिरा', 'आर्द्रा',
        'पुनर्वसु', 'पुष्य', 'आश्लेषा', 'मघा', 'पूर्वाफाल्गुनी', 'उत्तराफाल्गुनी',
        'हस्त', 'चित्रा', 'स्वाती', 'विशाखा', 'अनुराधा', 'ज्येष्ठा',
        'मूल', 'पूर्वाषाढ़ा', 'उत्तराषाढ़ा', 'श्रवण', 'धनिष्ठा', 'शतभिषा',
        'पूर्वाभाद्रपद', 'उत्तराभाद्रपद', 'रेवती'
    ];

    var PLANET_COLORS = {
        'सूर्य': '#f59e0b',
        'चन्द्र': '#38bdf8',
        'मंगल': '#ef4444',
        'बुध': '#10b981',
        'गुरु': '#eab308',
        'बृहस्पति': '#eab308',
        'शुक्र': '#ec4899',
        'शनि': '#6366f1',
        'राहु': '#a855f7',
        'केतु': '#8b5cf6'
    };

    var _state = { containerId: null, mode: 'house', house: 1, planet: null };

    function normPlanetHi(p) {
        if (!p) return '';
        var s = String(p).trim();
        if (/sun|सूर्य/i.test(s)) return 'सूर्य';
        if (/moon|चन्द्र|चंद्र/i.test(s)) return 'चन्द्र';
        if (/mars|मंगल/i.test(s)) return 'मंगल';
        if (/merc|बुध/i.test(s)) return 'बुध';
        if (/jup|गुरु|बृहस्पति/i.test(s)) return 'गुरु';
        if (/ven|शुक्र/i.test(s)) return 'शुक्र';
        if (/sat|शनि/i.test(s)) return 'शनि';
        if (/rah|राहु/i.test(s)) return 'राहु';
        if (/ket|केतु/i.test(s)) return 'केतु';
        return s;
    }

    function getAspectsForPlanet(pHi) {
        if (pHi === 'मंगल') return [4, 7, 8];
        if (pHi === 'गुरु' || pHi === 'बृहस्पति') return [5, 7, 9];
        if (pHi === 'शनि') return [3, 7, 10];
        if (pHi === 'राहु' || pHi === 'केतु') return [5, 7, 9];
        return [7];
    }

    function getActiveChart() {
        if (global.VyasAstronomicalEngine && typeof global.VyasAstronomicalEngine.getActiveKundli === 'function') {
            var c = global.VyasAstronomicalEngine.getActiveKundli();
            if (c) return c;
        }
        if (global.VyasDesktop && global.VyasDesktop.activeChartData) return global.VyasDesktop.activeChartData;
        if (global.VyasMobile && global.VyasMobile.activeChartData) return global.VyasMobile.activeChartData;
        if (global.activeChart) return global.activeChart;
        return null;
    }

    function getChartModel(chart) {
        var houses = {};
        for (var h = 1; h <= 12; h++) houses[h] = { signIdx: (h - 1) % 12, planets: [] };
        if (!chart) return { houses: houses, planets: {} };

        var ascSign = (chart.profile && chart.profile.asc_sign) ? chart.profile.asc_sign : 'मेष';
        var ascIdx = 0;
        for (var i = 0; i < SIGN_NAMES.length; i++) {
            if (ascSign.indexOf(SIGN_NAMES[i]) !== -1) { ascIdx = i; break; }
        }
        for (var h2 = 1; h2 <= 12; h2++) {
            houses[h2].signIdx = (ascIdx + h2 - 1) % 12;
        }

        var planets = {};
        var pt = chart.planet_table || [];
        for (var j = 0; j < pt.length; j++) {
            var row = pt[j];
            var pHi = normPlanetHi(row.name || row.planet || row.p);
            if (!pHi) continue;
            var ph = Number(row.house || row.h || 1);
            if (ph < 1 || ph > 12) ph = 1;
            var sIdx = -1;
            for (var si = 0; si < SIGN_NAMES.length; si++) {
                if (row.sign && row.sign.indexOf(SIGN_NAMES[si]) !== -1) { sIdx = si; break; }
            }
            if (sIdx === -1) sIdx = houses[ph].signIdx;
            var lon = typeof row.longitude === 'number' ? row.longitude : (sIdx * 30 + 15);
            var degInSign = lon % 30;
            var nakIdx = Math.floor(((lon % 360) + 360) % 360 / (360 / 27));
            var pada = Math.floor((lon % (360 / 27)) / (360 / 108)) + 1;

            var aspects = getAspectsForPlanet(pHi).map(function (off) {
                return { offset: off, target: ((ph - 1 + off - 1) % 12) + 1 };
            });

            var owned = [];
            for (var oh = 1; oh <= 12; oh++) {
                if (SIGN_LORDS[houses[oh].signIdx] === pHi) owned.push(oh);
            }

            planets[pHi] = {
                name: pHi,
                house: ph,
                signIdx: sIdx,
                signHi: SIGN_NAMES[sIdx],
                lon: lon,
                degInSign: degInSign,
                degStr: row.degree || row.d || (Math.floor(degInSign) + '°' + Math.floor((degInSign % 1) * 60) + "'"),
                nakHi: row.nakshatra || NAK_NAMES[nakIdx] || '',
                pada: row.pada || pada,
                isRetro: !!(row.isRetro || row.retro || (row.status && String(row.status).indexOf('वक्री') !== -1)),
                aspects: aspects,
                owned: owned
            };
            houses[ph].planets.push(pHi);
        }
        return { houses: houses, planets: planets };
    }

    function getDiamondGeometry(s) {
        var h = s / 2, q = s / 4;
        var polys = {
            1:  [[h,0],[3*q,q],[h,h],[q,q]],
            2:  [[0,0],[h,0],[q,q]],
            3:  [[0,0],[q,q],[0,h]],
            4:  [[q,q],[h,h],[q,3*q],[0,h]],
            5:  [[0,h],[q,3*q],[0,s]],
            6:  [[0,s],[q,3*q],[h,s]],
            7:  [[h,h],[3*q,3*q],[h,s],[q,3*q]],
            8:  [[h,s],[3*q,3*q],[s,s]],
            9:  [[3*q,3*q],[s,h],[s,s]],
            10: [[3*q,q],[s,h],[3*q,3*q],[h,h]],
            11: [[s,0],[s,h],[3*q,q]],
            12: [[h,0],[s,0],[3*q,q]]
        };
        var centers = {
            1: [h, q], 2: [q, q*0.42], 3: [q*0.42, q], 4: [q, h],
            5: [q*0.42, s-q], 6: [q, s-q*0.42], 7: [h, s-q], 8: [s-q, s-q*0.42],
            9: [s-q*0.42, s-q], 10: [s-q, h], 11: [s-q*0.42, q], 12: [s-q, q*0.42]
        };
        return { polys: polys, centers: centers };
    }

    function ptsStr(arr) {
        return arr.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ');
    }

    function curvedArrowPath(p1, p2, s) {
        var cx = (p1[0] + p2[0]) / 2;
        var cy = (p1[1] + p2[1]) / 2;
        var dx = p2[0] - p1[0];
        var dy = p2[1] - p1[1];
        var len = Math.sqrt(dx * dx + dy * dy) || 1;
        // Slight perpendicular curve toward center for clean visual separation
        var bend = Math.min(36, len * 0.18);
        var nx = -dy / len, ny = dx / len;
        var cpx = cx + nx * bend;
        var cpy = cy + ny * bend;
        // Shorten start & end slightly so arrowhead sits cleanly inside target house
        var pad = Math.min(22, len * 0.14);
        var sx = p1[0] + (dx / len) * pad;
        var sy = p1[1] + (dy / len) * pad;
        var ex = p2[0] - (dx / len) * pad;
        var ey = p2[1] - (dy / len) * pad;
        return 'M ' + sx.toFixed(1) + ' ' + sy.toFixed(1) + ' Q ' + cpx.toFixed(1) + ' ' + cpy.toFixed(1) + ' ' + ex.toFixed(1) + ' ' + ey.toFixed(1);
    }

    function renderOverlay(containerId) {
        var container = document.getElementById(containerId);
        if (!container) return;
        var svg = container.querySelector('svg');
        if (!svg) return;
        var vb = (svg.getAttribute('viewBox') || '0 0 380 380').split(/\s+/);
        var s = parseFloat(vb[2]) || 380;
        var geom = getDiamondGeometry(s);
        var chart = getActiveChart();
        var model = getChartModel(chart);
        var isLight = document.documentElement.getAttribute('data-theme') === 'light';

        // Remove previous overlay group
        var oldG = svg.querySelector('#vyasDrishtiOverlayGroup');
        if (oldG) oldG.remove();
        var oldDefs = svg.querySelector('#vyasDrishtiDefs');
        if (oldDefs) oldDefs.remove();

        var ns = 'http://www.w3.org/2000/svg';
        var defs = document.createElementNS(ns, 'defs');
        defs.id = 'vyasDrishtiDefs';
        Object.keys(PLANET_COLORS).forEach(function (pn) {
            var mk = document.createElementNS(ns, 'marker');
            mk.setAttribute('id', 'drishtiArr_' + pn);
            mk.setAttribute('markerWidth', '8');
            mk.setAttribute('markerHeight', '8');
            mk.setAttribute('refX', '6');
            mk.setAttribute('refY', '3');
            mk.setAttribute('orient', 'auto');
            var path = document.createElementNS(ns, 'path');
            path.setAttribute('d', 'M0,0 L7,3 L0,6 Z');
            path.setAttribute('fill', PLANET_COLORS[pn]);
            mk.appendChild(path);
            defs.appendChild(mk);
        });
        svg.insertBefore(defs, svg.firstChild);

        var g = document.createElementNS(ns, 'g');
        g.id = 'vyasDrishtiOverlayGroup';

        var activeHouse = (_state.containerId === containerId && _state.house) ? _state.house : null;
        var activePlanet = (_state.containerId === containerId && _state.mode === 'planet' && _state.planet) ? _state.planet : null;

        // 1. Highlight selected house or planet's house + owned houses
        if (activePlanet && model.planets[activePlanet]) {
            var pObj = model.planets[activePlanet];
            activeHouse = pObj.house;
            pObj.owned.forEach(function (oh) {
                var ownPoly = document.createElementNS(ns, 'polygon');
                ownPoly.setAttribute('points', ptsStr(geom.polys[oh]));
                ownPoly.setAttribute('fill', 'rgba(239,68,68,0.08)');
                ownPoly.setAttribute('stroke', '#ef4444');
                ownPoly.setAttribute('stroke-width', '2');
                ownPoly.setAttribute('stroke-dasharray', '6,4');
                ownPoly.setAttribute('pointer-events', 'none');
                g.appendChild(ownPoly);
            });
        }

        if (activeHouse && geom.polys[activeHouse]) {
            var selPoly = document.createElementNS(ns, 'polygon');
            selPoly.setAttribute('points', ptsStr(geom.polys[activeHouse]));
            selPoly.setAttribute('fill', isLight ? 'rgba(180,134,11,0.14)' : 'rgba(56,189,248,0.14)');
            selPoly.setAttribute('stroke', isLight ? '#92400e' : '#e2e8f0');
            selPoly.setAttribute('stroke-width', '2.5');
            selPoly.setAttribute('pointer-events', 'none');
            g.appendChild(selPoly);
        }

        // 2. Draw Drishti Arrows
        if (activePlanet && model.planets[activePlanet]) {
            var pObj2 = model.planets[activePlanet];
            var pCol = PLANET_COLORS[activePlanet] || '#ef4444';
            pObj2.aspects.forEach(function (asp) {
                if (asp.target === pObj2.house) return;
                var ap = document.createElementNS(ns, 'path');
                ap.setAttribute('d', curvedArrowPath(geom.centers[pObj2.house], geom.centers[asp.target], s));
                ap.setAttribute('fill', 'none');
                ap.setAttribute('stroke', pCol);
                ap.setAttribute('stroke-width', '2.4');
                ap.setAttribute('marker-end', 'url(#drishtiArr_' + activePlanet + ')');
                ap.setAttribute('pointer-events', 'none');
                g.appendChild(ap);
            });
        } else if (activeHouse) {
            // Incoming aspects into activeHouse
            Object.keys(model.planets).forEach(function (pn) {
                var po = model.planets[pn];
                po.aspects.forEach(function (asp) {
                    if (asp.target === activeHouse && po.house !== activeHouse) {
                        var ap = document.createElementNS(ns, 'path');
                        ap.setAttribute('d', curvedArrowPath(geom.centers[po.house], geom.centers[activeHouse], s));
                        ap.setAttribute('fill', 'none');
                        ap.setAttribute('stroke', PLANET_COLORS[pn] || '#f59e0b');
                        ap.setAttribute('stroke-width', '2.3');
                        ap.setAttribute('marker-end', 'url(#drishtiArr_' + pn + ')');
                        ap.setAttribute('pointer-events', 'none');
                        g.appendChild(ap);
                    }
                });
            });
        }

        // 3. Interactive House Hitboxes
        for (var h = 1; h <= 12; h++) {
            (function (houseNum) {
                var hit = document.createElementNS(ns, 'polygon');
                hit.setAttribute('points', ptsStr(geom.polys[houseNum]));
                hit.setAttribute('fill', 'transparent');
                hit.setAttribute('style', 'cursor:pointer;');
                hit.addEventListener('click', function (ev) {
                    ev.stopPropagation();
                    if (_state.containerId === containerId && _state.mode === 'house' && _state.house === houseNum) {
                        _state.containerId = null;
                    } else {
                        _state.containerId = containerId;
                        _state.mode = 'house';
                        _state.house = houseNum;
                        _state.planet = null;
                    }
                    renderOverlay(containerId);
                    renderInspectorBar(containerId);
                });
                g.appendChild(hit);
            })(h);
        }

        svg.appendChild(g);
    }

    function renderInspectorBar(containerId) {
        var container = document.getElementById(containerId);
        if (!container) return;
        var barId = containerId + '_drishtiBar';
        var bar = document.getElementById(barId);
        if (!bar) {
            bar = document.createElement('div');
            bar.id = barId;
            container.parentNode.insertBefore(bar, container);
        }

        var chart = getActiveChart();
        var model = getChartModel(chart);
        if (_state.containerId !== containerId) {
            bar.innerHTML = '<div style="margin-bottom:8px; padding:6px 10px; border-radius:10px; background:rgba(212,175,55,0.08); border:1px dashed var(--border-gold, rgba(212,175,55,0.35)); font-size:0.78rem; color:var(--text-muted); text-align:center;">✦ किसी भी <b>भाव (1–12)</b> पर टैप/क्लिक करें — ग्रहों की दृष्टि (Drishti Arrows) व स्वामित्व देखने के लिए</div>';
            return;
        }

        var hNum = _state.house || 1;
        var hInfo = model.houses[hNum] || { signIdx: 0, planets: [] };
        var bMeta = BHAVA_META[hNum];
        var lordHi = SIGN_LORDS[hInfo.signIdx];
        var lordObj = model.planets[lordHi];

        // Mode Pills: [भाव] + planets in this house (or all planets if planet mode)
        var pillsHtml = '<button type="button" onclick="VyasDrishtiInspector.selectHouse(\'' + containerId + '\',' + hNum + ')" style="padding:5px 12px; border-radius:8px; border:1px solid var(--border-gold, #d4af37); font-weight:800; font-size:0.8rem; cursor:pointer; background:' + (_state.mode === 'house' ? 'var(--gold-gradient, #d4af37)' : 'var(--bg-card-alt, #182442)') + '; color:' + (_state.mode === 'house' ? '#090d16' : 'var(--text-primary, #f8fafc)') + ';">भाव ' + hNum + '</button>';

        var housePlanets = hInfo.planets.length ? hInfo.planets : Object.keys(model.planets);
        housePlanets.slice(0, 5).forEach(function (pn) {
            var isAct = (_state.mode === 'planet' && _state.planet === pn);
            var col = PLANET_COLORS[pn] || '#ef4444';
            pillsHtml += '<button type="button" onclick="VyasDrishtiInspector.selectPlanet(\'' + containerId + '\',\'' + pn + '\')" style="padding:5px 10px; border-radius:8px; border:1px solid ' + (isAct ? col : 'var(--border-subtle, rgba(255,255,255,0.15))') + '; font-weight:700; font-size:0.8rem; cursor:pointer; background:' + (isAct ? 'rgba(239,68,68,0.14)' : 'var(--bg-card-alt, #182442)') + '; color:' + (isAct ? col : 'var(--text-primary, #f8fafc)') + ';">● ' + pn + '</button>';
        });

        var bodyHtml = '';
        if (_state.mode === 'planet' && _state.planet && model.planets[_state.planet]) {
            var po = model.planets[_state.planet];
            var aspStr = po.aspects.map(function (a) { return 'भाव ' + a.target + ' (' + a.offset + 'वीं)'; }).join(', ');
            var ownStr = po.owned.map(function (oh) { return 'भाव ' + oh + ' (' + SIGN_NAMES[model.houses[oh].signIdx] + ')'; }).join(' • ');
            var pct = ((po.degInSign / 30) * 100).toFixed(1);
            bodyHtml =
                '<div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px; font-size:0.82rem; margin-bottom:6px;">' +
                '  <span><b>' + po.lon.toFixed(1) + '°</b> • <b>' + po.signHi + ' ' + po.degStr + '</b></span>' +
                '  <span>नक्षत्र: <b>' + po.nakHi + ' (पाद ' + po.pada + ')</b></span>' +
                '</div>' +
                '<div style="font-size:0.8rem; color:var(--text-secondary); margin-bottom:6px;">' +
                '  <b>स्वामी:</b> ' + (ownStr || 'छाया ग्रह') + ' &nbsp;|&nbsp; <b>दृष्टि:</b> ' + aspStr +
                '</div>' +
                '<div style="position:relative; height:16px; background:rgba(148,163,184,0.18); border-radius:999px; overflow:hidden; border:1px solid rgba(212,175,55,0.28);">' +
                '  <div style="position:absolute; left:' + pct + '%; top:50%; transform:translate(-50%,-50%); width:10px; height:10px; border-radius:50%; background:' + (PLANET_COLORS[po.name] || '#ef4444') + '; box-shadow:0 0 8px ' + (PLANET_COLORS[po.name] || '#ef4444') + ';"></div>' +
                '</div>' +
                '<div style="display:flex; justify-content:space-between; font-size:0.7rem; color:var(--text-muted); margin-top:2px;"><span>0°</span><span>' + po.signHi + '</span><span>30°</span></div>';
        } else {
            var incoming = [];
            Object.keys(model.planets).forEach(function (pn) {
                var po2 = model.planets[pn];
                po2.aspects.forEach(function (a) {
                    if (a.target === hNum && po2.house !== hNum) {
                        incoming.push('<span style="color:' + (PLANET_COLORS[pn] || '#f59e0b') + '; font-weight:700;">' + pn + ' (' + a.offset + 'वीं)</span>');
                    }
                });
            });
            bodyHtml =
                '<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:6px;">' +
                '  <div><b style="font-size:0.96rem; color:var(--primary);">' + hNum + ' • ' + bMeta.name + ' (' + SIGN_NAMES[hInfo.signIdx] + ')</b><div style="font-size:0.78rem; color:var(--text-secondary);">' + bMeta.sig + '</div></div>' +
                '  <div style="display:flex; gap:4px;">' + bMeta.tags.map(function (t) { return '<span style="font-size:0.72rem; padding:2px 7px; border-radius:6px; background:rgba(212,175,55,0.12); border:1px solid rgba(212,175,55,0.3); font-weight:700;">' + t + '</span>'; }).join('') + '</div>' +
                '</div>' +
                '<div style="margin-top:6px; font-size:0.8rem; color:var(--text-secondary);">' +
                '  <b>भाव स्वामी:</b> ' + lordHi + (lordObj ? (' → भाव ' + lordObj.house + ' (' + lordObj.signHi + (lordObj.isRetro ? ' • वक्री' : '') + ')') : '') + '<br>' +
                '  <b>दृष्टि डालने वाले ग्रह:</b> ' + (incoming.length ? incoming.join(', ') : 'कोई बाह्य ग्रह दृष्टि नहीं') +
                '</div>';
        }

        bar.innerHTML =
            '<div style="margin-bottom:10px; padding:10px 12px; border-radius:12px; background:var(--bg-card-alt, rgba(15,23,42,0.88)); border:1px solid var(--border-gold, rgba(212,175,55,0.35));">' +
            '  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:8px;">' +
            '    <div style="display:flex; gap:6px; flex-wrap:wrap;">' + pillsHtml + '</div>' +
            '    <button type="button" onclick="VyasDrishtiInspector.clear(\'' + containerId + '\')" style="background:none; border:none; color:var(--text-muted); font-size:1rem; cursor:pointer; padding:2px 6px;">✕</button>' +
            '  </div>' +
            bodyHtml +
            '</div>';
    }

    function attach(containerId) {
        if (!containerId) return;
        renderOverlay(containerId);
        renderInspectorBar(containerId);
    }

    function selectHouse(cid, h) {
        _state = { containerId: cid, mode: 'house', house: h, planet: null };
        attach(cid);
    }

    function selectPlanet(cid, p) {
        _state = { containerId: cid, mode: 'planet', house: null, planet: p };
        attach(cid);
    }

    function clear(cid) {
        _state = { containerId: null, mode: 'house', house: 1, planet: null };
        attach(cid);
    }

    var TARGET_CONTAINERS = ['desktopKundliSvgWrap', 'mobileKundliSvgBox', 'kpChartWrap', 'chartSvgContainer', 'mChartSvgWrap'];

    function autoAttachAll() {
        TARGET_CONTAINERS.forEach(function (cid) {
            if (document.getElementById(cid)) attach(cid);
        });
    }

    function initDrishtiObserver() {
        autoAttachAll();
        TARGET_CONTAINERS.forEach(function (cid) {
            var el = document.getElementById(cid);
            if (!el || el._vyasDrishtiObserved) return;
            el._vyasDrishtiObserved = true;
            var obs = new MutationObserver(function () {
                if (!el.querySelector('#vyasDrishtiOverlayGroup')) {
                    setTimeout(function () { attach(cid); }, 30);
                }
            });
            obs.observe(el, { childList: true });
        });
    }

    if (typeof MutationObserver !== 'undefined') {
        if (document.readyState === 'loading') {
            window.addEventListener('DOMContentLoaded', initDrishtiObserver);
        } else {
            initDrishtiObserver();
        }
    }

    global.VyasDrishtiInspector = {
        attach: attach,
        selectHouse: selectHouse,
        selectPlanet: selectPlanet,
        clear: clear,
        autoAttachAll: autoAttachAll
    };
})(window);
