/**
 * VYAS ASTRA — MASTER ASTROLOGICAL CHART RENDERERS (v4.0)
 * ═════════════════════════════════════════════════════════════════════════
 * Provides 6 specialized classical visual chart renderers:
 * 1. KP Bhava Chalit Chart (Placidus cusps + Sub-Lord badges)
 * 2. Jaimini Karakamsha & Swamsha Chart (AK Navamsha Lagna + Karaka badges)
 * 3. Ashtakavarga SAV 337 Diamond Chart (House-wise SAV bindus + 11 vs 12 balance)
 * 4. Bhrigu Nandi Nadi (BNN) Directional 4-Element Wheel (East/South/West/North 1-5-9 trines)
 * 5. Tajika Varshphal Chart (Solar Return + Muntha [मुंथा] badge + Varshesha)
 * 6. Panchang Tatkalik Akasha Chart (Live celestial Gochar + current Lagna)
 *
 * All renderers are 100% vector SVG, theme-aware (dark/light), mobile-responsive,
 * and completely free of emojis, utilizing sacred geometric vector iconography.
 * ═════════════════════════════════════════════════════════════════════════
 */

(function(global) {
    'use strict';

    var SIGNS_HI = ["", "मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
    var SIGNS_EN = ["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];

    var VyasChartRenderers = {

        /**
         * 1. KP BHAVA CHALIT CHART
         * Renders Placidus unequal house cusps with exact degree spans and residing planets.
         */
        renderKPChalitChart: function(housesData, placidusCusps, size, isLight) {
            var s = size || 460;
            var h = s / 2.0;
            var q = s / 4.0;
            var bgGrad = isLight ?
                '<linearGradient id="kpBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FCFAF6"/><stop offset="100%" stop-color="#EFECE4"/></linearGradient>' :
                '<linearGradient id="kpBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#0a1020"/><stop offset="50%" stop-color="#050a16"/><stop offset="100%" stop-color="#020409"/></linearGradient>';
            var strokeLine = isLight ? '#243A59' : '#38bdf8';
            var strokeBorder = isLight ? '#B58A45' : '#0284c7';
            var textPrimary = isLight ? '#1B2E4B' : '#f0f9ff';
            var textMuted = isLight ? '#64748B' : '#94a3b8';
            var goldAccent = isLight ? '#B45309' : '#38bdf8';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-kp-chalit-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="kpShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.8"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#kpBg)" stroke="' + strokeBorder + '" stroke-width="2.2" rx="10"/>');
            parts.push('<rect x="5" y="5" width="' + (s - 10) + '" height="' + (s - 10) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="4,3" rx="8"/>');

            // Diamond lines
            var lines = [
                [0, 0, s, s], [0, s, s, 0],
                [h, 0, s, h], [s, h, h, s],
                [h, s, 0, h], [0, h, h, 0]
            ];
            for (var i = 0; i < lines.length; i++) {
                var ln = lines[i];
                parts.push('<line x1="' + ln[0] + '" y1="' + ln[1] + '" x2="' + ln[2] + '" y2="' + ln[3] + '" stroke="' + strokeLine + '" stroke-width="1.6"/>');
            }

            // 12 House Centers
            var positions = {
                1: [h, q - 8],
                2: [q, q / 2 + 2],
                3: [q / 2 + 10, q + 6],
                4: [q + 4, h],
                5: [q / 2 + 10, s - q - 6],
                6: [q, s - q / 2 - 2],
                7: [h, s - q + 14],
                8: [s - q, s - q / 2 - 2],
                9: [s - q / 2 - 10, s - q - 6],
                10: [s - q - 4, h],
                11: [s - q / 2 - 10, q + 6],
                12: [s - q, q / 2 + 2]
            };

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];

                // Cusp info
                var cusp = (placidusCusps && placidusCusps[house]) ? placidusCusps[house] : null;
                var cuspDegStr = cusp ? (cusp.deg || cusp.d || '') : '';
                var cuspSign = cusp ? (cusp.sign || cusp.r || '') : '';
                var cuspSubLord = cusp ? (cusp.subLord || cusp.sl || '') : '';

                // Bhava Badge
                parts.push('<circle cx="' + x + '" cy="' + (y - 30) + '" r="12" fill="' + (isLight ? '#E0F2FE' : '#082f49') + '" stroke="' + goldAccent + '" stroke-width="1.2"/>');
                parts.push('<text x="' + x + '" y="' + (y - 25) + '" font-family="Cinzel, serif" font-size="12" font-weight="900" fill="' + goldAccent + '" text-anchor="middle">भाव ' + house + '</text>');

                // Cusp degree
                if (cuspDegStr || cuspSign) {
                    var cLabel = (cuspSign ? cuspSign.substring(0, 3) + ' ' : '') + cuspDegStr;
                    parts.push('<text x="' + x + '" y="' + (y - 12) + '" font-family="monospace" font-size="9" font-weight="700" fill="' + textMuted + '" text-anchor="middle">' + cLabel + '</text>');
                }

                // Planets in this Bhava Chalit
                var pList = (housesData && housesData[house]) ? housesData[house] : [];
                var cleanPlanets = [];
                for (var pi = 0; pi < pList.length; pi++) {
                    var p = pList[pi];
                    var pName = (typeof p === 'object' && p !== null) ? (p.p || p.planet || '') : String(p);
                    pName = pName.replace(/\s*D[0-9]+/gi, '').trim();
                    if (pName && cleanPlanets.indexOf(pName) === -1) cleanPlanets.push(pName);
                }

                var py = y + 4;
                for (var k = 0; k < cleanPlanets.length; k++) {
                    var plName = cleanPlanets[k];
                    var isRetro = plName.indexOf('(R)') !== -1 || plName.indexOf('(व)') !== -1;
                    var pColor = isRetro ? '#f97316' : textPrimary;
                    parts.push('<text x="' + x + '" y="' + (py + (k * 13)) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="11" font-weight="800" fill="' + pColor + '" text-anchor="middle" filter="url(#kpShd)">' + plName + '</text>');
                }

                // Sub-Lord tag at bottom of house
                if (cuspSubLord) {
                    parts.push('<text x="' + x + '" y="' + (y + 36) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="8.5" font-weight="600" fill="' + goldAccent + '" text-anchor="middle">SL: ' + cuspSubLord + '</text>');
                }
            }

            // Center watermark
            parts.push('<text x="' + h + '" y="' + (h - 6) + '" font-family="Cinzel, serif" font-size="13" font-weight="800" fill="' + goldAccent + '" text-anchor="middle" letter-spacing="1">KP BHAVA CHALIT</text>');
            parts.push('<text x="' + h + '" y="' + (h + 10) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9" font-weight="600" fill="' + textMuted + '" text-anchor="middle">भाव चलित • कस्पल सब-लॉर्ड</text>');

            parts.push('</svg>');
            return parts.join('\n');
        },


        /**
         * 2. JAIMINI KARAKAMSHA & SWAMSHA CHART
         * Renders the Navamsha sign of Atmakaraka (AK) as House 1 (Lagna) with 7 Chara Karaka tags.
         */
        renderJaiminiKarakamsaChart: function(karakamsaLagnaSignNum, housesData, karakas, size, isLight, chartTypeTitle) {
            var s = size || 460;
            var h = s / 2.0;
            var q = s / 4.0;
            var bgGrad = isLight ?
                '<linearGradient id="jBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FDFBF7"/><stop offset="100%" stop-color="#F3ECE0"/></linearGradient>' :
                '<linearGradient id="jBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#180b24"/><stop offset="50%" stop-color="#0f051a"/><stop offset="100%" stop-color="#05020a"/></linearGradient>';
            var strokeLine = isLight ? '#7C3AED' : '#c084fc';
            var strokeBorder = isLight ? '#B58A45' : '#a855f7';
            var textPrimary = isLight ? '#2E1065' : '#f5f3ff';
            var textMuted = isLight ? '#6B7280' : '#c4b5fd';
            var akGold = '#fbbf24';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-jaimini-karakamsa-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="jShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.85"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#jBg)" stroke="' + strokeBorder + '" stroke-width="2.4" rx="12"/>');
            parts.push('<rect x="6" y="6" width="' + (s - 12) + '" height="' + (s - 12) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="5,3" rx="8"/>');

            // Diamond lines
            var lines = [
                [0, 0, s, s], [0, s, s, 0],
                [h, 0, s, h], [s, h, h, s],
                [h, s, 0, h], [0, h, h, 0]
            ];
            for (var i = 0; i < lines.length; i++) {
                var ln = lines[i];
                parts.push('<line x1="' + ln[0] + '" y1="' + ln[1] + '" x2="' + ln[2] + '" y2="' + ln[3] + '" stroke="' + strokeLine + '" stroke-width="1.6"/>');
            }

            var positions = {
                1: [h, q - 8],
                2: [q, q / 2 + 2],
                3: [q / 2 + 10, q + 6],
                4: [q + 4, h],
                5: [q / 2 + 10, s - q - 6],
                6: [q, s - q / 2 - 2],
                7: [h, s - q + 14],
                8: [s - q, s - q / 2 - 2],
                9: [s - q / 2 - 10, s - q - 6],
                10: [s - q - 4, h],
                11: [s - q / 2 - 10, q + 6],
                12: [s - q, q / 2 + 2]
            };

            var signsList = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var lagnaSign = parseInt(karakamsaLagnaSignNum) || 1;
            var isSvamsa = (chartTypeTitle === 'स्वांश' || chartTypeTitle === 'Svamsa' || chartTypeTitle === 'Svamsha');
            var chartHeaderLabel = isSvamsa ? 'स्वांश लग्न (D-9)' : 'कारकांश लग्न (D-1)';

            // Build properly rotated houses based on the true sign of each planet
            var rotatedHouses = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] };

            if (Array.isArray(housesData)) {
                housesData.forEach(function (p) {
                    var sName = p.sign || p.r || '';
                    var sIdx = signsList.indexOf(sName);
                    if (sIdx !== -1) {
                        var hNum = ((sIdx + 1 - lagnaSign + 12) % 12) + 1;
                        rotatedHouses[hNum].push(p);
                    }
                });
            } else if (housesData && typeof housesData === 'object') {
                var hasSignMap = false;
                for (var hKey = 1; hKey <= 12; hKey++) {
                    var list = housesData[hKey] || [];
                    for (var pi = 0; pi < list.length; pi++) {
                        var it = list[pi];
                        if (typeof it === 'object' && it !== null && (it.sign || it.r)) {
                            hasSignMap = true;
                            break;
                        }
                    }
                }

                if (hasSignMap) {
                    for (var hKey = 1; hKey <= 12; hKey++) {
                        var list = housesData[hKey] || [];
                        for (var pi = 0; pi < list.length; pi++) {
                            var it = list[pi];
                            if (typeof it === 'object' && it !== null && (it.sign || it.r)) {
                                var sIdx = signsList.indexOf(it.sign || it.r);
                                if (sIdx !== -1) {
                                    var hNum = ((sIdx + 1 - lagnaSign + 12) % 12) + 1;
                                    rotatedHouses[hNum].push(it);
                                }
                            }
                        }
                    }
                } else {
                    rotatedHouses = housesData;
                }
            }

            // Map karakas for fast tag lookup
            var karakaTagMap = {};
            if (karakas) {
                var kKeys = ['AK', 'AmK', 'BK', 'MK', 'PK', 'GK', 'DK'];
                for (var ki = 0; ki < kKeys.length; ki++) {
                    var kObj = karakas[kKeys[ki]];
                    if (kObj && kObj.planet) {
                        var baseP = kObj.planet.replace(/\s*\(.*\)/, '').trim();
                        karakaTagMap[baseP] = kKeys[ki];
                    }
                }
            }

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];

                // Sign in this house (Karakamsha/Svamsha Sign as House 1)
                var signNum = ((lagnaSign - 1 + house - 1) % 12) + 1;

                // Sign Badge
                parts.push('<circle cx="' + x + '" cy="' + (y - 30) + '" r="12" fill="' + (isLight ? '#F3E8FF' : '#3b0764') + '" stroke="' + strokeBorder + '" stroke-width="1.2"/>');
                parts.push('<text x="' + x + '" y="' + (y - 25) + '" font-family="Cinzel, serif" font-size="12" font-weight="900" fill="' + (isLight ? '#6B21A8' : '#e9d5ff') + '" text-anchor="middle">' + signNum + '</text>');

                // House 1 Label: कारकांश / स्वांश लग्न
                if (house === 1) {
                    parts.push('<text x="' + x + '" y="' + (y - 12) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9" font-weight="800" fill="' + akGold + '" text-anchor="middle">' + chartHeaderLabel + '</text>');
                } else if (house === 12) {
                    parts.push('<text x="' + x + '" y="' + (y - 12) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="8.5" font-weight="600" fill="' + textMuted + '" text-anchor="middle">मोक्ष / इष्ट भाव</text>');
                }

                // Correct rotated planets in this house
                var pList = rotatedHouses[house] || [];
                var py = y + 2;
                for (var pi = 0; pi < pList.length; pi++) {
                    var rawP = pList[pi];
                    var pName = (typeof rawP === 'object' && rawP !== null) ? (rawP.p || rawP.planet || '') : String(rawP);
                    pName = pName.replace(/\s*D[0-9]+/gi, '').trim();
                    if (!pName) continue;

                    var baseName = pName.replace(/\s*\(.*\)/, '').trim();
                    var kTag = karakaTagMap[baseName] || '';
                    var isAK = kTag === 'AK';
                    var fillCol = isAK ? akGold : textPrimary;
                    var label = pName + (kTag ? (' [' + kTag + ']') : '');

                    parts.push('<text x="' + x + '" y="' + (py + (pi * 13)) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="' + (isAK ? 11.5 : 10.5) + '" font-weight="' + (isAK ? 900 : 700) + '" fill="' + fillCol + '" text-anchor="middle" filter="url(#jShd)">' + label + '</text>');
                }
            }

            // Center watermark
            parts.push('<text x="' + h + '" y="' + (h - 10) + '" font-family="Cinzel, serif" font-size="11" font-weight="800" fill="' + textMuted + '" fill-opacity="0.3" text-anchor="middle" letter-spacing="1">JAIMINI SUTRAM</text>');
            parts.push('<text x="' + h + '" y="' + (h + 8) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="11.5" font-weight="800" fill="' + akGold + '" fill-opacity="0.5" text-anchor="middle">' + (isSvamsa ? 'स्वांश कुण्डली (D-9)' : 'कारकांश कुण्डली (D-1)') + '</text>');

            parts.push('</svg>');
            return parts.join('\n');
        },


        /**
         * 3. ASHTAKAVARGA 337 SAV DIAMOND CHART
         * Traditional diamond chart prominently displaying the SAV bindus (22-38) in each of the 12 houses.
         * Houses >= 30: Balavan (Emerald/Green), 28-29: Medium (Gold), < 28: Low (Red/Amber).
         */
        renderAshtakavargaChart: function(savPointsArray, lagnaSignNum, size, isLight) {
            var s = size || 460;
            var h = s / 2.0;
            var q = s / 4.0;
            var bgGrad = isLight ?
                '<linearGradient id="avBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FCFAF6"/><stop offset="100%" stop-color="#F2EFE8"/></linearGradient>' :
                '<linearGradient id="avBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#06120b"/><stop offset="50%" stop-color="#030b06"/><stop offset="100%" stop-color="#010502"/></linearGradient>';
            var strokeLine = isLight ? '#047857' : '#10b981';
            var strokeBorder = isLight ? '#B58A45' : '#059669';
            var textMuted = isLight ? '#64748B' : '#94a3b8';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-ashtakavarga-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="avShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.85"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#avBg)" stroke="' + strokeBorder + '" stroke-width="2.4" rx="12"/>');
            parts.push('<rect x="6" y="6" width="' + (s - 12) + '" height="' + (s - 12) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="5,3" rx="8"/>');

            // Diamond lines
            var lines = [
                [0, 0, s, s], [0, s, s, 0],
                [h, 0, s, h], [s, h, h, s],
                [h, s, 0, h], [0, h, h, 0]
            ];
            for (var i = 0; i < lines.length; i++) {
                var ln = lines[i];
                parts.push('<line x1="' + ln[0] + '" y1="' + ln[1] + '" x2="' + ln[2] + '" y2="' + ln[3] + '" stroke="' + strokeLine + '" stroke-width="1.6"/>');
            }

            var positions = {
                1: [h, q - 6],
                2: [q, q / 2 + 2],
                3: [q / 2 + 10, q + 6],
                4: [q + 4, h],
                5: [q / 2 + 10, s - q - 6],
                6: [q, s - q / 2 - 2],
                7: [h, s - q + 14],
                8: [s - q, s - q / 2 - 2],
                9: [s - q / 2 - 10, s - q - 6],
                10: [s - q - 4, h],
                11: [s - q / 2 - 10, q + 6],
                12: [s - q, q / 2 + 2]
            };

            var lagnaSign = parseInt(lagnaSignNum) || 1;
            var sav = Array.isArray(savPointsArray) ? savPointsArray : [30, 28, 32, 29, 27, 31, 33, 25, 28, 32, 34, 28];

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];

                // Sign in this house
                var signNum = ((lagnaSign - 1 + house - 1) % 12) + 1;
                // SAV bindu for this sign/house
                var bindus = sav[signNum - 1] || sav[house - 1] || 28;

                // Color coding for bindus
                var bColor = '#10b981'; // Green (>= 30)
                var bBg = 'rgba(16,185,129,0.15)';
                var bStatus = 'सबल';
                if (bindus < 28) {
                    bColor = '#ef4444'; // Red (< 28)
                    bBg = 'rgba(239,68,68,0.15)';
                    bStatus = 'अल्प';
                } else if (bindus <= 29) {
                    bColor = '#f59e0b'; // Amber (28-29)
                    bBg = 'rgba(245,158,11,0.15)';
                    bStatus = 'मध्यम';
                }

                // Sign badge
                parts.push('<circle cx="' + x + '" cy="' + (y - 30) + '" r="11" fill="' + (isLight ? '#ECFDF5' : '#064e3b') + '" stroke="' + strokeBorder + '" stroke-width="1.1"/>');
                parts.push('<text x="' + x + '" y="' + (y - 26) + '" font-family="Cinzel, serif" font-size="11" font-weight="900" fill="' + (isLight ? '#065F46' : '#a7f3d0') + '" text-anchor="middle">' + signNum + '</text>');

                // House label
                parts.push('<text x="' + x + '" y="' + (y - 12) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="8.5" font-weight="600" fill="' + textMuted + '" text-anchor="middle">भाव ' + house + '</text>');

                // Prominent SAV Bindus
                parts.push('<circle cx="' + x + '" cy="' + (y + 10) + '" r="18" fill="' + bBg + '" stroke="' + bColor + '" stroke-width="1.4"/>');
                parts.push('<text x="' + x + '" y="' + (y + 17) + '" font-family="Cinzel, serif" font-size="19" font-weight="900" fill="' + bColor + '" text-anchor="middle" filter="url(#avShd)">' + bindus + '</text>');

                // Strength pill
                parts.push('<text x="' + x + '" y="' + (y + 36) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="8" font-weight="700" fill="' + bColor + '" text-anchor="middle">' + bStatus + '</text>');
            }

            // Center watermark
            var h11Bindus = sav[10] || 33;
            var h12Bindus = sav[11] || 27;
            var incomeStatus = h11Bindus > h12Bindus ? 'आय > व्यय (शुभ)' : 'व्यय > आय (संयम)';
            parts.push('<text x="' + h + '" y="' + (h - 8) + '" font-family="Cinzel, serif" font-size="13" font-weight="800" fill="#10b981" text-anchor="middle" letter-spacing="1">SARVASHTAKAVARGA</text>');
            parts.push('<text x="' + h + '" y="' + (h + 8) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9.5" font-weight="700" fill="#fcd34d" text-anchor="middle">कुल: 337 बिन्दु • ' + incomeStatus + '</text>');

            parts.push('</svg>');
            return parts.join('\n');
        },


        /**
         * 4. BHRIGU NANDI NADI (BNN) DIRECTIONAL 4-ELEMENT CHART
         * Displays the 4 Cardinal Directions with their 1-5-9 element trines:
         * - East: Agni (1-5-9)
         * - South: Prithvi (2-6-10)
         * - West: Vayu (3-7-11)
         * - North: Jala (4-8-12)
         */
        renderNadiDirectionalChart: function(planetTable, size, isLight) {
            var s = size || 460;
            var h = s / 2.0;
            var bgGrad = isLight ?
                '<linearGradient id="nadiBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FCFAF6"/><stop offset="100%" stop-color="#F2EFE8"/></linearGradient>' :
                '<linearGradient id="nadiBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#110902"/><stop offset="50%" stop-color="#0a0501"/><stop offset="100%" stop-color="#030200"/></linearGradient>';
            var strokeBorder = isLight ? '#B58A45' : '#ea580c';
            var textPrimary = isLight ? '#1B2E4B' : '#ffedd5';
            var textMuted = isLight ? '#64748B' : '#fdba74';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-nadi-directional-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="nadiShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.85"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#nadiBg)" stroke="' + strokeBorder + '" stroke-width="2.4" rx="14"/>');
            parts.push('<rect x="6" y="6" width="' + (s - 10) + '" height="' + (s - 10) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="5,3" rx="10"/>');

            // 4 Quadrant Grid Dividers
            parts.push('<line x1="' + h + '" y1="10" x2="' + h + '" y2="' + (s - 10) + '" stroke="' + strokeBorder + '" stroke-width="1.4" stroke-dasharray="4,4"/>');
            parts.push('<line x1="10" y1="' + h + '" x2="' + (s - 10) + '" y2="' + h + '" stroke="' + strokeBorder + '" stroke-width="1.4" stroke-dasharray="4,4"/>');

            // Group planets by Nadi Element Direction
            var EAST_SIGNS = ['मेष', 'सिंह', 'धनु', 'Aries', 'Leo', 'Sagittarius', 1, 5, 9];
            var SOUTH_SIGNS = ['वृषभ', 'कन्या', 'मकर', 'Taurus', 'Virgo', 'Capricorn', 2, 6, 10];
            var WEST_SIGNS = ['मिथुन', 'तुला', 'कुंभ', 'Gemini', 'Libra', 'Aquarius', 3, 7, 11];
            var NORTH_SIGNS = ['कर्क', 'वृश्चिक', 'मीन', 'Cancer', 'Scorpio', 'Pisces', 4, 8, 12];

            var dirPlanets = { east: [], south: [], west: [], north: [] };

            if (Array.isArray(planetTable)) {
                for (var pi = 0; pi < planetTable.length; pi++) {
                    var pl = planetTable[pi];
                    var pName = (pl.p || pl.planet || '').replace(/\s*\(.*\)/, '').trim();
                    var pSign = pl.r || pl.sign || pl.signNum || '';
                    if (!pName) continue;

                    var item = pName + (pl.d ? (' ' + pl.d) : '');
                    if (EAST_SIGNS.indexOf(pSign) !== -1) dirPlanets.east.push(item);
                    else if (SOUTH_SIGNS.indexOf(pSign) !== -1) dirPlanets.south.push(item);
                    else if (WEST_SIGNS.indexOf(pSign) !== -1) dirPlanets.west.push(item);
                    else if (NORTH_SIGNS.indexOf(pSign) !== -1) dirPlanets.north.push(item);
                }
            }

            // 4 Direction Panels Configuration
            var panels = [
                {
                    key: 'east',
                    title: 'पूर्व (East) • अग्नि तत्त्व',
                    sub: 'मेष • सिंह • धनु (1-5-9 धर्म)',
                    color: '#ef4444',
                    bg: isLight ? 'rgba(239,68,68,0.06)' : 'rgba(239,68,68,0.12)',
                    x: 14, y: 14, w: h - 20, h: h - 20,
                    planets: dirPlanets.east
                },
                {
                    key: 'south',
                    title: 'दक्षिण (South) • पृथ्वी तत्त्व',
                    sub: 'वृषभ • कन्या • मकर (2-6-10 अर्थ)',
                    color: '#10b981',
                    bg: isLight ? 'rgba(16,185,129,0.06)' : 'rgba(16,185,129,0.12)',
                    x: h + 6, y: 14, w: h - 20, h: h - 20,
                    planets: dirPlanets.south
                },
                {
                    key: 'west',
                    title: 'पश्चिम (West) • वायु तत्त्व',
                    sub: 'मिथुन • तुला • कुंभ (3-7-11 काम)',
                    color: '#38bdf8',
                    bg: isLight ? 'rgba(56,189,248,0.06)' : 'rgba(56,189,248,0.12)',
                    x: 14, y: h + 6, w: h - 20, h: h - 20,
                    planets: dirPlanets.west
                },
                {
                    key: 'north',
                    title: 'उत्तर (North) • जल तत्त्व',
                    sub: 'कर्क • वृश्चिक • मीन (4-8-12 मोक्ष)',
                    color: '#a855f7',
                    bg: isLight ? 'rgba(168,85,247,0.06)' : 'rgba(168,85,247,0.12)',
                    x: h + 6, y: h + 6, w: h - 20, h: h - 20,
                    planets: dirPlanets.north
                }
            ];

            for (var k = 0; k < panels.length; k++) {
                var pnl = panels[k];
                parts.push('<rect x="' + pnl.x + '" y="' + pnl.y + '" width="' + pnl.w + '" height="' + pnl.h + '" fill="' + pnl.bg + '" stroke="' + pnl.color + '" stroke-width="1.2" rx="8"/>');
                // Title
                parts.push('<text x="' + (pnl.x + pnl.w / 2) + '" y="' + (pnl.y + 20) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="12" font-weight="800" fill="' + pnl.color + '" text-anchor="middle">' + pnl.title + '</text>');
                // Subtitle
                parts.push('<text x="' + (pnl.x + pnl.w / 2) + '" y="' + (pnl.y + 34) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="8.5" font-weight="600" fill="' + textMuted + '" text-anchor="middle">' + pnl.sub + '</text>');

                // Planets in this direction
                var pArr = pnl.planets;
                if (!pArr || pArr.length === 0) {
                    parts.push('<text x="' + (pnl.x + pnl.w / 2) + '" y="' + (pnl.y + pnl.h / 2 + 10) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="10" font-weight="600" fill="' + textMuted + '" text-anchor="middle" font-style="italic">ग्रह रहित (निरीह)</text>');
                } else {
                    var startY = pnl.y + 54;
                    for (var pi = 0; pi < pArr.length; pi++) {
                        parts.push('<text x="' + (pnl.x + pnl.w / 2) + '" y="' + (startY + (pi * 16)) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="11" font-weight="700" fill="' + textPrimary + '" text-anchor="middle" filter="url(#nadiShd)">• ' + pArr[pi] + '</text>');
                    }
                }
            }

            // Center Compass Rose / Emblem
            parts.push('<circle cx="' + h + '" cy="' + h + '" r="28" fill="' + (isLight ? '#FEF3C7' : '#1e1103') + '" stroke="' + strokeBorder + '" stroke-width="1.6"/>');
            parts.push('<text x="' + h + '" y="' + (h - 4) + '" font-family="Cinzel, serif" font-size="9" font-weight="900" fill="#d4af37" text-anchor="middle">BNN NADI</text>');
            parts.push('<text x="' + h + '" y="' + (h + 8) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="7.5" font-weight="800" fill="#ea580c" text-anchor="middle">1-5-9 त्रिकोण</text>');

            parts.push('</svg>');
            return parts.join('\n');
        },


        /**
         * 5. TAJIKA VARSHPHAL CHART (Solar Return Chart + Muntha Badge)
         * Solar return chart with Muntha badge [🚩 मुंथा] and Varshesha badge.
         */
        renderVarshphalChart: function(housesData, munthaSignNum, varsheshaPlanet, varshAge, size, isLight) {
            var s = size || 460;
            var h = s / 2.0;
            var q = s / 4.0;
            var bgGrad = isLight ?
                '<linearGradient id="vBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FFFDF7"/><stop offset="100%" stop-color="#F5EFE0"/></linearGradient>' :
                '<linearGradient id="vBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#1a1402"/><stop offset="50%" stop-color="#0f0c01"/><stop offset="100%" stop-color="#050400"/></linearGradient>';
            var strokeLine = isLight ? '#B45309' : '#f59e0b';
            var strokeBorder = isLight ? '#92400E' : '#d97706';
            var textPrimary = isLight ? '#1B2E4B' : '#fef3c7';
            var textMuted = isLight ? '#64748B' : '#fde68a';
            var munthaGold = '#eab308';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-varshphal-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="vShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.85"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#vBg)" stroke="' + strokeBorder + '" stroke-width="2.4" rx="12"/>');
            parts.push('<rect x="6" y="6" width="' + (s - 12) + '" height="' + (s - 12) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="5,3" rx="8"/>');

            // Diamond lines
            var lines = [
                [0, 0, s, s], [0, s, s, 0],
                [h, 0, s, h], [s, h, h, s],
                [h, s, 0, h], [0, h, h, 0]
            ];
            for (var i = 0; i < lines.length; i++) {
                var ln = lines[i];
                parts.push('<line x1="' + ln[0] + '" y1="' + ln[1] + '" x2="' + ln[2] + '" y2="' + ln[3] + '" stroke="' + strokeLine + '" stroke-width="1.6"/>');
            }

            var positions = {
                1: [h, q - 8],
                2: [q, q / 2 + 2],
                3: [q / 2 + 10, q + 6],
                4: [q + 4, h],
                5: [q / 2 + 10, s - q - 6],
                6: [q, s - q / 2 - 2],
                7: [h, s - q + 14],
                8: [s - q, s - q / 2 - 2],
                9: [s - q / 2 - 10, s - q - 6],
                10: [s - q - 4, h],
                11: [s - q / 2 - 10, q + 6],
                12: [s - q, q / 2 + 2]
            };

            // Varsha Lagna Sign
            var lagnaSignNum = 1;
            if (housesData && housesData[1]) {
                var d1Val = housesData[1][0];
                lagnaSignNum = parseInt(typeof d1Val === 'object' && d1Val !== null ? d1Val.sign : d1Val) || 1;
            }

            var munthaSign = parseInt(munthaSignNum) || 1;
            var vLord = (varsheshaPlanet || '').replace(/\s*\(.*\)/, '').trim();

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];

                var signNum = ((lagnaSignNum - 1 + house - 1) % 12) + 1;
                var isMunthaHere = (signNum === munthaSign);

                // Sign Badge
                parts.push('<circle cx="' + x + '" cy="' + (y - 30) + '" r="12" fill="' + (isLight ? '#FEF3C7' : '#451a03') + '" stroke="' + strokeBorder + '" stroke-width="1.2"/>');
                parts.push('<text x="' + x + '" y="' + (y - 25) + '" font-family="Cinzel, serif" font-size="12" font-weight="900" fill="' + (isLight ? '#92400E' : '#fde68a') + '" text-anchor="middle">' + signNum + '</text>');

                // Muntha Badge in the relevant house
                if (isMunthaHere) {
                    parts.push('<rect x="' + (x - 30) + '" y="' + (y - 14) + '" width="60" height="15" fill="#f59e0b" rx="4"/>');
                    parts.push('<text x="' + x + '" y="' + (y - 3) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9" font-weight="900" fill="#000" text-anchor="middle">मुंथा (Muntha)</text>');
                }

                // Planets in this house
                var pList = (housesData && housesData[house]) ? housesData[house] : [];
                var py = y + (isMunthaHere ? 10 : 0);
                for (var pi = 0; pi < pList.length; pi++) {
                    var rawP = pList[pi];
                    var pName = (typeof rawP === 'object' && rawP !== null) ? (rawP.p || rawP.planet || '') : String(rawP);
                    pName = pName.replace(/\s*D[0-9]+/gi, '').trim();
                    if (!pName) continue;

                    var isVarshesha = vLord && pName.indexOf(vLord) !== -1;
                    var tag = isVarshesha ? ' [वर्षेश]' : '';
                    var fillCol = isVarshesha ? '#fbbf24' : textPrimary;

                    parts.push('<text x="' + x + '" y="' + (py + (pi * 13)) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="11" font-weight="' + (isVarshesha ? 900 : 700) + '" fill="' + fillCol + '" text-anchor="middle" filter="url(#vShd)">' + pName + tag + '</text>');
                }
            }

            // Center watermark
            parts.push('<text x="' + h + '" y="' + (h - 7) + '" font-family="Cinzel, serif" font-size="13" font-weight="800" fill="' + munthaGold + '" text-anchor="middle" letter-spacing="1">TAJIKA VARSHPHAL</text>');
            parts.push('<text x="' + h + '" y="' + (h + 9) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9.5" font-weight="700" fill="' + textMuted + '" text-anchor="middle">वर्ष ' + (varshAge ? (varshAge + 'वां वर्ष') : '') + ' • वर्षेश: ' + (vLord || 'गुरु') + '</text>');

            parts.push('</svg>');
            return parts.join('\n');
        },


        /**
         * 6. PANCHANG TATKALIK AKASHA CHART
         * Real-time celestial North Indian chart cast for current city and timestamp.
         */
        renderTatkalikPanchangChart: function(housesData, currentCityName, istTimeStr, size, isLight) {
            var s = size || 460;
            var h = s / 2.0;
            var q = s / 4.0;
            var bgGrad = isLight ?
                '<linearGradient id="pBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FCFAF6"/><stop offset="100%" stop-color="#EDE9FE"/></linearGradient>' :
                '<linearGradient id="pBg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#090514"/><stop offset="50%" stop-color="#04020a"/><stop offset="100%" stop-color="#010003"/></linearGradient>';
            var strokeLine = isLight ? '#4338CA' : '#818cf8';
            var strokeBorder = isLight ? '#3730A3' : '#6366f1';
            var textPrimary = isLight ? '#1E1B4B' : '#e0e7ff';
            var textMuted = isLight ? '#64748B' : '#a5b4fc';

            var parts = [];
            parts.push('<svg width="' + s + '" height="' + s + '" viewBox="0 0 ' + s + ' ' + s + '" xmlns="http://www.w3.org/2000/svg" class="vyas-tatkalik-panchang-chart" style="max-width:100%; height:auto;">');
            parts.push('<defs>' + bgGrad + '<filter id="pShd"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity="0.85"/></filter></defs>');

            // Outer frame
            parts.push('<rect x="0" y="0" width="' + s + '" height="' + s + '" fill="url(#pBg)" stroke="' + strokeBorder + '" stroke-width="2.4" rx="12"/>');
            parts.push('<rect x="6" y="6" width="' + (s - 12) + '" height="' + (s - 12) + '" fill="none" stroke="' + strokeBorder + '" stroke-width="0.8" stroke-dasharray="5,3" rx="8"/>');

            // Diamond lines
            var lines = [
                [0, 0, s, s], [0, s, s, 0],
                [h, 0, s, h], [s, h, h, s],
                [h, s, 0, h], [0, h, h, 0]
            ];
            for (var i = 0; i < lines.length; i++) {
                var ln = lines[i];
                parts.push('<line x1="' + ln[0] + '" y1="' + ln[1] + '" x2="' + ln[2] + '" y2="' + ln[3] + '" stroke="' + strokeLine + '" stroke-width="1.6"/>');
            }

            var positions = {
                1: [h, q - 8],
                2: [q, q / 2 + 2],
                3: [q / 2 + 10, q + 6],
                4: [q + 4, h],
                5: [q / 2 + 10, s - q - 6],
                6: [q, s - q / 2 - 2],
                7: [h, s - q + 14],
                8: [s - q, s - q / 2 - 2],
                9: [s - q / 2 - 10, s - q - 6],
                10: [s - q - 4, h],
                11: [s - q / 2 - 10, q + 6],
                12: [s - q, q / 2 + 2]
            };

            var lagnaSignNum = 1;
            if (housesData && housesData[1]) {
                var d1Val = housesData[1][0];
                lagnaSignNum = parseInt(typeof d1Val === 'object' && d1Val !== null ? d1Val.sign : d1Val) || 1;
            }

            for (var house = 1; house <= 12; house++) {
                var pos = positions[house];
                var x = pos[0];
                var y = pos[1];

                var signNum = ((lagnaSignNum - 1 + house - 1) % 12) + 1;

                // Sign Badge
                parts.push('<circle cx="' + x + '" cy="' + (y - 30) + '" r="12" fill="' + (isLight ? '#EEF2FF' : '#1e1b4b') + '" stroke="' + strokeBorder + '" stroke-width="1.2"/>');
                parts.push('<text x="' + x + '" y="' + (y - 25) + '" font-family="Cinzel, serif" font-size="12" font-weight="900" fill="' + (isLight ? '#3730A3' : '#c7d2fe') + '" text-anchor="middle">' + signNum + '</text>');

                if (house === 1) {
                    parts.push('<text x="' + x + '" y="' + (y - 12) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9" font-weight="800" fill="#a5b4fc" text-anchor="middle">तात्कालिक लग्न</text>');
                }

                // Real-time planets
                var pList = (housesData && housesData[house]) ? housesData[house] : [];
                var py = y + 2;
                for (var pi = 0; pi < pList.length; pi++) {
                    var rawP = pList[pi];
                    var pName = (typeof rawP === 'object' && rawP !== null) ? (rawP.p || rawP.planet || '') : String(rawP);
                    pName = pName.replace(/\s*D[0-9]+/gi, '').trim();
                    if (!pName) continue;

                    parts.push('<text x="' + x + '" y="' + (py + (pi * 13)) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="11" font-weight="700" fill="' + textPrimary + '" text-anchor="middle" filter="url(#pShd)">' + pName + '</text>');
                }
            }

            // Center watermark
            parts.push('<text x="' + h + '" y="' + (h - 7) + '" font-family="Cinzel, serif" font-size="13" font-weight="800" fill="#818cf8" text-anchor="middle" letter-spacing="1">TATKALIK GOCHAR</text>');
            parts.push('<text x="' + h + '" y="' + (h + 9) + '" font-family="Noto Sans Devanagari, sans-serif" font-size="9" font-weight="700" fill="' + textMuted + '" text-anchor="middle">' + (currentCityName || 'अयोध्या') + ' • ' + (istTimeStr || 'वर्तमान वेध') + '</text>');

            parts.push('</svg>');
            return parts.join('\n');
        }
    };

    // Attach to global / window
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = VyasChartRenderers;
    }
    global.VyasChartRenderers = VyasChartRenderers;

})(typeof window !== 'undefined' ? window : global);

