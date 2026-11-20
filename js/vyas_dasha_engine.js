/**
 * VYAS DASHA ENGINE v1.0
 * Comprehensive 5-Level Vimshottari (Mahadasha, Antardasha, Pratyantar, Sookshma, Pran),
 * Jaimini Chara Dasha (12 Rashi Cycles with Shastric Years), and KP Cuspal Dasha.
 * Pure mathematical algorithms conforming to Brihat Parashara Hora Shastra,
 * Jaimini Upadesha Sutras & K.S. Krishnamurti KP System.
 */

(function(global) {
    'use strict';

    var DASHA_LORDS = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"];
    var DASHA_LORDS_EN = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];
    var DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]; // Total = 120

    var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
    var SIGN_LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];

    function addDays(date, days) {
        var result = new Date(date);
        result.setTime(result.getTime() + days * 86400000);
        return result;
    }

    function formatDate(d) {
        if (!d || isNaN(d.getTime())) return '-';
        var day = String(d.getDate()).padStart(2, '0');
        var m = String(d.getMonth() + 1).padStart(2, '0');
        var y = d.getFullYear();
        return day + '/' + m + '/' + y;
    }

    function toISODate(d) {
        if (!d || isNaN(d.getTime())) return '';
        var day = String(d.getDate()).padStart(2, '0');
        var m = String(d.getMonth() + 1).padStart(2, '0');
        var y = d.getFullYear();
        return y + '-' + m + '-' + day;
    }

    // -------------------------------------------------------------------------
    // 1. 5-LEVEL VIMSHOTTARI DASHA GENERATOR
    // -------------------------------------------------------------------------
    function computeVimshottari5Levels(dobStr, tobStr, moonLongitude) {
        var birthDate = new Date(dobStr + 'T' + (tobStr ? tobStr : '12:00:00'));
        if (isNaN(birthDate.getTime())) birthDate = new Date(dobStr);

        var nakSpan = 360.0 / 27.0; // 13°20' = 13.333333°
        var nakIdx = Math.floor(moonLongitude / nakSpan) % 27;
        var startLordIdx = nakIdx % 9;
        var remDeg = nakSpan - (moonLongitude % nakSpan);
        var balanceFrac = remDeg / nakSpan;

        var firstLordYears = DASHA_YEARS[startLordIdx];
        var balanceDays = firstLordYears * 365.2422 * balanceFrac;

        var currentDate = new Date();
        var mahadashas = [];
        var curDateCursor = new Date(birthDate);

        for (var i = 0; i < 9; i++) {
            var lordIdx = (startLordIdx + i) % 9;
            var lordName = DASHA_LORDS[lordIdx];
            var lordEn = DASHA_LORDS_EN[lordIdx];
            var totalYears = DASHA_YEARS[lordIdx];
            var dashaDays = (i === 0) ? balanceDays : (totalYears * 365.2422);

            var mdStartDate = new Date(curDateCursor);
            var mdEndDate = addDays(mdStartDate, dashaDays);
            curDateCursor = new Date(mdEndDate);

            var isMdActive = (currentDate >= mdStartDate && currentDate < mdEndDate);

            // Compute Antardashas (9 sub-periods)
            var antardashas = [];
            var adCursor = new Date(mdStartDate);
            var mdFullSpanDays = totalYears * 365.2422;

            for (var j = 0; j < 9; j++) {
                var adLordIdx = (lordIdx + j) % 9;
                var adLordName = DASHA_LORDS[adLordIdx];
                var adLordEn = DASHA_LORDS_EN[adLordIdx];
                var adYears = DASHA_YEARS[adLordIdx];
                
                // Ratio of Antardasha in full Mahadasha
                var adSpanDays = (mdFullSpanDays * (adYears / 120.0));
                
                // If this is the balance first Mahadasha, prorate proportionally
                if (i === 0) {
                    adSpanDays = adSpanDays * balanceFrac;
                }

                var adStartDate = new Date(adCursor);
                var adEndDate = addDays(adStartDate, adSpanDays);
                adCursor = new Date(adEndDate);

                var isAdActive = (currentDate >= adStartDate && currentDate < adEndDate);

                // Compute Pratyantardashas (level 3)
                var pratyantars = [];
                var pdCursor = new Date(adStartDate);
                var adFullSpanDays = (totalYears * (adYears / 120.0)) * 365.2422;

                for (var k = 0; k < 9; k++) {
                    var pdLordIdx = (adLordIdx + k) % 9;
                    var pdLordName = DASHA_LORDS[pdLordIdx];
                    var pdYears = DASHA_YEARS[pdLordIdx];
                    var pdSpanDays = (adSpanDays * (pdYears / 120.0));

                    var pdStartDate = new Date(pdCursor);
                    var pdEndDate = addDays(pdStartDate, pdSpanDays);
                    pdCursor = new Date(pdEndDate);

                    var isPdActive = (currentDate >= pdStartDate && currentDate < pdEndDate);

                    // Compute Sookshma (level 4) and Pran (level 5) if active or requested
                    var sookshmas = [];
                    if (isPdActive || (isAdActive && k < 3)) {
                        var sdCursor = new Date(pdStartDate);
                        for (var s = 0; s < 9; s++) {
                            var sdLordIdx = (pdLordIdx + s) % 9;
                            var sdLordName = DASHA_LORDS[sdLordIdx];
                            var sdYears = DASHA_YEARS[sdLordIdx];
                            var sdSpanDays = (pdSpanDays * (sdYears / 120.0));

                            var sdStartDate = new Date(sdCursor);
                            var sdEndDate = addDays(sdStartDate, sdSpanDays);
                            sdCursor = new Date(sdEndDate);

                            var isSdActive = (currentDate >= sdStartDate && currentDate < sdEndDate);

                            // Prana (level 5)
                            var pranas = [];
                            if (isSdActive) {
                                var prCursor = new Date(sdStartDate);
                                for (var p = 0; p < 9; p++) {
                                    var prLordIdx = (sdLordIdx + p) % 9;
                                    var prLordName = DASHA_LORDS[prLordIdx];
                                    var prYears = DASHA_YEARS[prLordIdx];
                                    var prSpanDays = (sdSpanDays * (prYears / 120.0));

                                    var prStartDate = new Date(prCursor);
                                    var prEndDate = addDays(prStartDate, prSpanDays);
                                    prCursor = new Date(prEndDate);

                                    var isPrActive = (currentDate >= prStartDate && currentDate < prEndDate);

                                    pranas.push({
                                        lord: prLordName,
                                        start: formatDate(prStartDate),
                                        end: formatDate(prEndDate),
                                        isActive: isPrActive
                                    });
                                }
                            }

                            sookshmas.push({
                                lord: sdLordName,
                                start: formatDate(sdStartDate),
                                end: formatDate(sdEndDate),
                                isActive: isSdActive,
                                prana: pranas
                            });
                        }
                    }

                    pratyantars.push({
                        lord: pdLordName,
                        start: formatDate(pdStartDate),
                        end: formatDate(pdEndDate),
                        isActive: isPdActive,
                        sookshma: sookshmas
                    });
                }

                antardashas.push({
                    lord: adLordName,
                    lordEn: adLordEn,
                    start: formatDate(adStartDate),
                    end: formatDate(adEndDate),
                    isActive: isAdActive,
                    pratyantar: pratyantars
                });
            }

            mahadashas.push({
                lord: lordName,
                lordEn: lordEn,
                start: formatDate(mdStartDate),
                end: formatDate(mdEndDate),
                totalYears: totalYears,
                isActive: isMdActive,
                antardasha: antardashas
            });
        }

        return {
            birthDate: formatDate(birthDate),
            mahadashas: mahadashas
        };
    }

    // -------------------------------------------------------------------------
    // 2. JAIMINI CHARA DASHA ENGINE (12 Rashi Cycles)
    // -------------------------------------------------------------------------
    function computeJaiminiCharaDasha(dobStr, lagnaSignName, planetsTable) {
        var birthDate = new Date(dobStr);
        if (isNaN(birthDate.getTime())) birthDate = new Date();

        var lagnaIdx = SIGNS_HI.indexOf(lagnaSignName);
        if (lagnaIdx === -1) lagnaIdx = 0; // Default Mesha

        // Direct signs (Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius) = forward counting
        // Odd signs from Aries: 0 (Mesha), 1 (Vrishabha), 2 (Mithuna), 6 (Tula), 7 (Vrischika), 8 (Dhanu)
        // Jaimini classic order based on 9th house or Lagna:
        var isLagnaDirect = [0, 1, 2, 6, 7, 8].indexOf(lagnaIdx) !== -1;

        // Sequence of signs
        var signSequence = [];
        for (var i = 0; i < 12; i++) {
            var sIdx = isLagnaDirect ? (lagnaIdx + i) % 12 : (lagnaIdx - i + 12) % 12;
            signSequence.push(sIdx);
        }

        // Map planet locations by sign
        var planetSignMap = {};
        if (Array.isArray(planetsTable)) {
            planetsTable.forEach(function(pt) {
                var pName = pt.p ? pt.p.split(' ')[0] : '';
                var pSign = pt.r || pt.sign || '';
                var sIdx = SIGNS_HI.indexOf(pSign);
                if (pName && sIdx !== -1) {
                    planetSignMap[pName] = sIdx;
                }
            });
        }

        var currentDate = new Date();
        var charaList = [];
        var dateCursor = new Date(birthDate);

        signSequence.forEach(function(sIdx) {
            var signName = SIGNS_HI[sIdx];
            var lordName = SIGN_LORDS[sIdx];
            var lordSignIdx = planetSignMap[lordName];
            if (lordSignIdx === undefined) lordSignIdx = sIdx;

            // Direct sign counts forward; Indirect counts backward
            var isSignDirect = [0, 1, 2, 6, 7, 8].indexOf(sIdx) !== -1;
            var dashaYears = 0;

            if (lordSignIdx === sIdx) {
                dashaYears = 12; // Own sign gives full 12 years
            } else {
                if (isSignDirect) {
                    var diff = (lordSignIdx - sIdx + 12) % 12;
                    dashaYears = diff; // (lordSign - sign)
                } else {
                    var diff = (sIdx - lordSignIdx + 12) % 12;
                    dashaYears = diff;
                }
            }
            if (dashaYears <= 0) dashaYears = 12;

            var dDays = dashaYears * 365.2422;
            var startDate = new Date(dateCursor);
            var endDate = addDays(startDate, dDays);
            dateCursor = new Date(endDate);

            var isActive = (currentDate >= startDate && currentDate < endDate);

            // Antardashas within Chara Dasha (12 sub-periods)
            var adDays = dDays / 12.0;
            var adList = [];
            var adCursor = new Date(startDate);
            for (var a = 0; a < 12; a++) {
                var adSignIdx = isSignDirect ? (sIdx + a) % 12 : (sIdx - a + 12) % 12;
                var aStart = new Date(adCursor);
                var aEnd = addDays(aStart, adDays);
                adCursor = new Date(aEnd);

                adList.push({
                    sign: SIGNS_HI[adSignIdx],
                    start: formatDate(aStart),
                    end: formatDate(aEnd),
                    isActive: (currentDate >= aStart && currentDate < aEnd)
                });
            }

            charaList.push({
                sign: signName,
                lord: lordName,
                years: dashaYears,
                start: formatDate(startDate),
                end: formatDate(endDate),
                isActive: isActive,
                antardashas: adList
            });
        });

        return charaList;
    }

    // -------------------------------------------------------------------------
    // 3. KP CUSPAL & SUB-LORD DASHA EVALUATOR
    // -------------------------------------------------------------------------
    function evaluateKPDasha(activeChart, mdLord, adLord, pdLord) {
        if (!activeChart || !activeChart.kp) return null;

        var cusps = activeChart.kp.cusps || {};
        var planets = activeChart.planet_table || [];

        function getPlanetSignifications(pName) {
            var occupiedHouse = 1;
            var ownedHouses = [];
            
            planets.forEach(function(pt) {
                if (pt.p && pt.p.indexOf(pName) !== -1) {
                    occupiedHouse = parseInt(pt.h || '1');
                }
            });

            for (var h = 1; h <= 12; h++) {
                var c = cusps[h];
                if (c && c.signLord === pName) {
                    ownedHouses.push(h);
                }
            }

            return {
                occupied: occupiedHouse,
                owned: ownedHouses,
                all: [occupiedHouse].concat(ownedHouses)
            };
        }

        var mdSig = getPlanetSignifications(mdLord);
        var adSig = getPlanetSignifications(adLord);

        // Analyze Event Significations
        var careerHouses = [2, 6, 10, 11];
        var marriageHouses = [2, 7, 11];
        var obstacleHouses = [6, 8, 12];
        var financeHouses = [2, 11];

        function checkIntersect(arr1, arr2) {
            return arr1.filter(function(x) { return arr2.indexOf(x) !== -1; });
        }

        var activeAll = mdSig.all.concat(adSig.all);
        var careerHits = checkIntersect(activeAll, careerHouses);
        var marriageHits = checkIntersect(activeAll, marriageHouses);
        var obstacleHits = checkIntersect(activeAll, obstacleHouses);
        var financeHits = checkIntersect(activeAll, financeHouses);

        var careerVerdict = careerHits.length >= 2 ? "अनुकूल (उन्नति, पदोन्नति एवं कार्य सिद्धि)" : "सामान्य (धैर्य आवश्यक)";
        var financeVerdict = financeHits.length >= 1 ? "धन लाभ एवं आर्थिक संवृद्धि" : "नियमित आय";
        var obstacleVerdict = obstacleHits.length >= 2 ? "सचेत रहें (कार्य में अस्थायी विलंब या स्वास्थ्य ध्यान)" : "न्यून बाधाएं";

        return {
            md: { lord: mdLord, houses: mdSig.all },
            ad: { lord: adLord, houses: adSig.all },
            verdicts: {
                career: careerVerdict,
                finance: financeVerdict,
                obstacle: obstacleVerdict
            }
        };
    }

    // Exports
    global.VyasDashaEngine = {
        computeVimshottari5Levels: computeVimshottari5Levels,
        computeJaiminiCharaDasha: computeJaiminiCharaDasha,
        evaluateKPDasha: evaluateKPDasha
    };

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = global.VyasDashaEngine;
    }
})(typeof window !== 'undefined' ? window : (typeof global !== 'undefined' ? global : this));

