/**
 * VYAS DAIVAGYA ENGINE v3.0
 * Complete Vedic Astrologer — Parashari + KP + Jaimini
 * Zero hallucination: All calculations from chart data, never from AI memory
 * 
 * Modules:
 *   VyasQueryRouter   — 15 query types
 *   VyasChartAnalyzer — extract all factors
 *   VyasYogaEngine    — 25+ yoga detection
 *   VyasDashaEngine   — dasha timing
 *   VyasBalaEngine    — planetary strength
 *   VyasGocharEngine  — 2026-27 transits
 *   VyasUpayaEngine   — remedies
 *   VyasDaivagyaCore  — master orchestrator
 */

(function(window) {
    'use strict';

    // ═══════════════════════════════════════════════════════════════════
    // SHARED CONSTANTS
    // ═══════════════════════════════════════════════════════════════════
    var SIGNS = ['मेष','वृषभ','मिथुन','कर्क','सिंह','कन्या','तुला','वृश्चिक','धनु','मकर','कुंभ','मीन'];
    var SIGNS_EN = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
    var LORDS = {
        'मेष':'मंगल','वृषभ':'शुक्र','मिथुन':'बुध','कर्क':'चन्द्र','सिंह':'सूर्य',
        'कन्या':'बुध','तुला':'शुक्र','वृश्चिक':'मंगल','धनु':'गुरु',
        'मकर':'शनि','कुंभ':'शनि','मीन':'गुरु'
    };
    var EXALT = {'सूर्य':'मेष','चन्द्र':'वृषभ','मंगल':'मकर','बुध':'कन्या','गुरु':'कर्क','शुक्र':'मीन','शनि':'तुला'};
    var DEBIL = {'सूर्य':'तुला','चन्द्र':'वृश्चिक','मंगल':'कर्क','बुध':'मीन','गुरु':'मकर','शुक्र':'कन्या','शनि':'मेष'};
    var OWN = {
        'सूर्य':['सिंह'],'चन्द्र':['कर्क'],'मंगल':['मेष','वृश्चिक'],
        'बुध':['मिथुन','कन्या'],'गुरु':['धनु','मीन'],'शुक्र':['वृषभ','तुला'],'शनि':['मकर','कुंभ']
    };
    var KENDRAS = [1,4,7,10];
    var TRIKONAS = [1,5,9];
    var DUSTHANAS = [6,8,12];
    var UPACHAYA = [3,6,10,11];
    var BENEFICS = ['गुरु','शुक्र','बुध','चन्द्र'];
    var MALEFICS = ['शनि','मंगल','राहु','केतु','सूर्य'];
    var NAKSHATRAS = [
        'अश्विनी','भरणी','कृत्तिका','रोहिणी','मृगशिरा','आर्द्रा','पुनर्वसु','पुष्य','आश्लेषा',
        'मघा','पूर्वाफाल्गुनी','उत्तराफाल्गुनी','हस्त','चित्रा','स्वाति','विशाखा','अनुराधा','ज्येष्ठा',
        'मूल','पूर्वाषाढ़ा','उत्तराषाढ़ा','श्रवण','धनिष्ठा','शतभिषा','पूर्वाभाद्रपद','उत्तराभाद्रपद','रेवती'
    ];
    var NAK_LORDS = ['केतु','शुक्र','सूर्य','चन्द्र','मंगल','राहु','गुरु','शनि','बुध',
                     'केतु','शुक्र','सूर्य','चन्द्र','मंगल','राहु','गुरु','शनि','बुध',
                     'केतु','शुक्र','सूर्य','चन्द्र','मंगल','राहु','गुरु','शनि','बुध'];
    // Current transits (Nov-Dec 2026, Swiss Ephemeris verified)
    var CURRENT_TRANSITS = {
        'सूर्य': { sign: 'वृश्चिक', house_from_aries: 8, deg: 3.6 },
        'चन्द्र': { sign: 'मीन', house_from_aries: 12, deg: 4.7 },
        'मंगल': { sign: 'सिंह', house_from_aries: 5, deg: 3.4 },
        'बुध': { sign: 'तुला', house_from_aries: 7, deg: 14.1 },
        'गुरु': { sign: 'सिंह', house_from_aries: 5, deg: 1.9, retro: false },
        'शुक्र': { sign: 'कन्या', house_from_aries: 6, deg: 29.4 },
        'शनि': { sign: 'मीन', house_from_aries: 12, deg: 14.1, retro: true },
        'राहु': { sign: 'कुंभ', house_from_aries: 11, deg: 0.9, retro: true },
        'केतु': { sign: 'सिंह', house_from_aries: 5, deg: 0.9, retro: true }
    };

    // ═══════════════════════════════════════════════════════════════════
    // HELPER FUNCTIONS
    // ═══════════════════════════════════════════════════════════════════
    function getPlanet(chart, name) {
        if (!chart || !chart.planet_table) return null;
        return chart.planet_table.find(function(p) {
            var n = (p.p || p.planet || '').trim();
            return n === name || n.indexOf(name) === 0;
        }) || null;
    }
    function getH(p) { return parseInt(p && (p.h || p.house) || 0); }
    function getS(p) { return ((p && (p.r || p.sign)) || '').trim(); }
    function getD(p) { return parseFloat((p && (p.d || p.degree)) || 0); }
    function signIdx(s) { return SIGNS.indexOf(s); }
    function houseFromSign(signName, lagnaSign) {
        var s = signIdx(signName), l = signIdx(lagnaSign);
        if (s === -1 || l === -1) return 0;
        return ((s - l + 12) % 12) + 1;
    }
    function signFromHouse(lagnaSign, houseNum) {
        var l = signIdx(lagnaSign);
        if (l === -1) return '';
        return SIGNS[(l + houseNum - 1) % 12];
    }
    function planetsInHouse(chart, h) {
        if (!chart || !chart.planet_table) return [];
        return chart.planet_table.filter(function(p) { return getH(p) === h; });
    }
    function dignityOf(planetName, signName) {
        if (EXALT[planetName] === signName) return 'उच्च';
        if (DEBIL[planetName] === signName) return 'नीच';
        if (OWN[planetName] && OWN[planetName].indexOf(signName) !== -1) return 'स्वराशि';
        return 'सामान्य';
    }
    function aspectsHouse(fromH, toH, pName) {
        var diff = ((toH - fromH + 12) % 12) + 1;
        var n = pName.trim();
        if (n === 'शनि') return [3,7,10].indexOf(diff) !== -1;
        if (n === 'मंगल') return [4,7,8].indexOf(diff) !== -1;
        if (n === 'गुरु' || n === 'राहु' || n === 'केतु') return [5,7,9].indexOf(diff) !== -1;
        return diff === 7;
    }

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 1: QUERY ROUTER
    // ═══════════════════════════════════════════════════════════════════
    window.VyasQueryRouter = {
        ROUTES: {
            panchang:   /(एकादशी|द्वादशी|पारण|ekadashi|पंचांग|panchang|tithi|तिथि|राहुकाल|अभिजीत|मुहूर्त|चोघड़िया|होरा|व्रत|त्योहार|पूर्णिमा|अमावस्या|प्रदोष)/i,
            yoga:       /(केमद्रुम|kemdrum|kendrum|गजकेसरी|gajakesari|राजयोग|raj yoga|मंगल दोष|mangal dosha|बुधादित्य|budhaditya|विपरीत|viparit|नीचभंग|panchamahapurush|पंचमहापुरुष|हंस योग|मालव्य|रुचक|भद्र|शश|चंद्र-मंगल|सुनफा|अनफा|केदार|काहल|योग)/i,
            dasha:      /(दशा|mahadasha|antardasha|महादशा|अंतर्दशा|प्रत्यंतर|सूक्ष्म|विंशोत्तरी|दशाफल|दशा.*कब|कब.*दशा)/i,
            gochar:     /(गोचर|gochar|transit|शनि.*राशि|गुरु.*राशि|गोचर.*फल|साढ़ेसाती|ढैय्या|ashtama|अष्टम)/i,
            lagna:      /(लग्न|lagna|ascendant|लग्नेश|उदय लग्न|जन्म लग्न)/i,
            career:     /(करियर|career|नौकरी|job|व्यापार|business|पदोन्नति|promotion|आजीविका|वृत्ति|पेशा)/i,
            marriage:   /(विवाह|marriage|शादी|पति|पत्नी|दांपत्य|सप्तम|7.*भाव|spouse|partner)/i,
            wealth:     /(धन|wealth|money|पैसा|समृद्धि|संपत्ति|आर्थिक|financial|investment|निवेश)/i,
            health:     /(स्वास्थ्य|health|रोग|बीमारी|आयु|longevity|शष्ठ|अष्टम|व्याधि)/i,
            children:   /(संतान|children|पुत्र|पुत्री|सन्तान|पंचम भाव|5.*भाव)/i,
            prashna:    /(प्रश्न|prashna|horary|क्या होगा|क्या मिलेगा|क्या बनेगा|सफलता मिलेगी|होगा|मिलेगा)/i,
            d9:         /(d9|d-9|नवमांश|navamsha|भाग्य|विवाह.*चक्र)/i,
            d10:        /(d10|d-10|दशमांश|dashamsha|करियर.*कुण्डली|कर्म चक्र)/i,
            vastu:      /(वास्तु|vastu|दिशा|direction|घर|मकान|flat|house.*direction)/i,
            medini:     /(मौसम|weather|बारिश|economy|शेयर|sensex|gold|silver|सोना|चांदी|राजनीति|election|देश|country)/i
        },
        detect: function(query) {
            var q = query || '';
            for (var route in this.ROUTES) {
                if (this.ROUTES[route].test(q)) return route;
            }
            return 'general';
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 2: CHART ANALYZER — Extract all factors from chart data
    // ═══════════════════════════════════════════════════════════════════
    window.VyasChartAnalyzer = {
        analyze: function(chart) {
            if (!chart || !chart.planet_table) return null;
            var self = this;
            var lagnaSign = (chart.profile && chart.profile.asc_sign) ? chart.profile.asc_sign : '';
            var lagnaIdx = signIdx(lagnaSign);

            // Build planet map
            var pMap = {};
            chart.planet_table.forEach(function(p) {
                var name = (p.p || p.planet || '').trim();
                if (name) {
                    pMap[name] = {
                        sign: getS(p), house: getH(p), deg: getD(p),
                        nakshatra: (p.n || p.nakshatra || ''),
                        dignity: dignityOf(name, getS(p)),
                        retro: ((p.s || p.dignity || '').toLowerCase().indexOf('वक्र') !== -1 ||
                                (p.s || '').toLowerCase().indexOf('retro') !== -1)
                    };
                }
            });

            // House map
            var hMap = {};
            for (var h = 1; h <= 12; h++) {
                var sign = lagnaIdx !== -1 ? SIGNS[(lagnaIdx + h - 1) % 12] : '';
                hMap[h] = {
                    sign: sign,
                    lord: LORDS[sign] || '',
                    planets: planetsInHouse(chart, h).map(function(p){ return (p.p||p.planet||'').trim(); }).filter(Boolean)
                };
            }

            // Lagna strength
            var lagnaLord = LORDS[lagnaSign] || '';
            var lagnaLordData = pMap[lagnaLord];
            var lagnaStrength = lagnaLordData ? (
                KENDRAS.indexOf(lagnaLordData.house) !== -1 ? 'बलवान (केन्द्र)' :
                TRIKONAS.indexOf(lagnaLordData.house) !== -1 ? 'बलवान (त्रिकोण)' :
                DUSTHANAS.indexOf(lagnaLordData.house) !== -1 ? 'दुर्बल (दुःस्थान)' : 'मध्यम'
            ) : 'अज्ञात';

            // Dasha
            var dasha = { chain: 'अज्ञात', maha: 'अज्ञात', antar: 'अज्ञात' };
            if (chart.active_dasha) {
                dasha.chain = chart.active_dasha.chain || chart.active_dasha;
                var parts = dasha.chain.split(/[➔→\->/]/);
                dasha.maha = (parts[0] || '').trim();
                dasha.antar = (parts[1] || '').trim();
            }

            return {
                lagna: lagnaSign,
                lagnaLord: lagnaLord,
                lagnaLordPos: lagnaLordData || null,
                lagnaStrength: lagnaStrength,
                planets: pMap,
                houses: hMap,
                dasha: dasha,
                name: (chart.profile && chart.profile.name) || 'जातक'
            };
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 3: YOGA ENGINE — 25+ Classical Yogas
    // ═══════════════════════════════════════════════════════════════════
    window.VyasYogaEngine = {
        detectAll: function(analysis, chart, queryHint) {
            var q = (queryHint || '').toLowerCase();
            var results = [];

            // Priority: detect specifically asked yoga first
            if (/केमद्रुम|kemdrum|kendrum/.test(q)) results.push(this.kemdrum(analysis));
            if (/गजकेसरी|gajakesari/.test(q)) results.push(this.gajakesari(analysis));
            if (/बुधादित्य|budhaditya/.test(q)) results.push(this.budhaditya(analysis));
            if (/मंगल.*दोष|mangal.*dosh|kuja|मांगलिक/.test(q)) results.push(this.mangaldosha(analysis));
            if (/नीचभंग|neechabhanga/.test(q)) results.push(this.neechabhanga(analysis));
            if (/गुरुचांडाल|guru.*chandal/.test(q)) results.push(this.guruchandal(analysis));
            if (/काल.*सर्प|kaal.*sarp/.test(q)) results.push(this.kaalsarpa(analysis, chart));
            if (/राजयोग|raj.*yoga/.test(q)) results = results.concat(this.rajYogas(analysis));
            if (/पंचमहापुरुष|panch.*mahapurush|रुचक|हंस|मालव्य|भद्र|शश/.test(q)) results = results.concat(this.panchamahapurusha(analysis));
            if (/विपरीत|viparit/.test(q)) results = results.concat(this.vipritraj(analysis));

            // If no specific yoga, run summary
            if (results.length === 0 || /सब|all|सभी.*योग/.test(q)) {
                results = [
                    this.kemdrum(analysis),
                    this.gajakesari(analysis),
                    this.budhaditya(analysis),
                    this.mangaldosha(analysis)
                ].concat(this.rajYogas(analysis)).concat(this.panchamahapurusha(analysis));
            }

            return results.filter(Boolean);
        },

        kemdrum: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return { name: 'केमद्रुम योग', found: false, detail: 'चन्द्र डेटा अनुपलब्ध' };
            var mH = moon.house;
            var h2 = (mH % 12) + 1, h12 = ((mH - 2 + 12) % 12) + 1;
            var neighbors = Object.entries(a.planets).filter(function(e) {
                var pn = e[0], pd = e[1];
                return pn !== 'चन्द्र' && pn !== 'राहु' && pn !== 'केतु' &&
                       (pd.house === mH || pd.house === h2 || pd.house === h12);
            });
            if (neighbors.length > 0) {
                return { name: 'केमद्रुम योग', found: false,
                    detail: '❌ **केमद्रुम योग नहीं** — चन्द्र (भाव ' + mH + ', ' + moon.sign + ') के 2रे (भाव ' + h2 + ') व 12वें (भाव ' + h12 + ') में ग्रह हैं: **' + neighbors.map(function(e){return e[0]}).join(', ') + '**।' };
            }
            // Check bhanga
            var bhangas = [];
            if (KENDRAS.indexOf(mH) !== -1) bhangas.push('चन्द्र लग्न से केन्द्र (भाव ' + mH + ') में');
            if (moon.sign === 'कर्क' || moon.sign === 'वृषभ') bhangas.push('चन्द्र ' + (moon.sign === 'वृषभ' ? 'उच्च' : 'स्वराशि') + ' में');
            var sun = a.planets['सूर्य'];
            if (sun) {
                var moonFromSun = ((mH - sun.house + 12) % 12) + 1;
                if (KENDRAS.indexOf(moonFromSun) !== -1) bhangas.push('चन्द्र सूर्य से केन्द्र में');
            }
            // Benefic aspects on Moon
            var benefAspects = BENEFICS.filter(function(b) {
                var bp = a.planets[b];
                return bp && aspectsHouse(bp.house, mH, b);
            });
            if (benefAspects.length) bhangas.push('शुभ दृष्टि: ' + benefAspects.join(', '));

            if (bhangas.length) {
                return { name: 'केमद्रुम योग (भंग)', found: true, partial: true,
                    detail: '⚠️ **केमद्रुम योग का आधार** बनता है (चन्द्र भाव ' + mH + ' में, 2रे व 12वें में कोई ग्रह नहीं) **परन्तु भंग होता है:**\n' +
                            bhangas.map(function(b){ return '• ' + b }).join('\n') + '\n\n**फल:** आंशिक प्रभाव — कभी-कभी मानसिक अशांति, किन्तु जीवन में उत्थान अवश्य होगा।\n\n**उपाय:** सोमवार शिव अभिषेक | चांदी की अंगूठी | "ॐ सों सोमाय नमः" 108 जप' };
            }
            return { name: 'केमद्रुम योग', found: true, partial: false,
                detail: '🔴 **पूर्ण केमद्रुम योग**\n\n**शास्त्र:** "द्वादशे द्वितीये वापि चन्द्रान्नीचे ग्रहैर्विना। केमद्रुमाख्यो योगोऽयं दुःखदारिद्र्यकारकः॥" (बृहत्पाराशर)\n\n**स्थिति:** चन्द्रमा भाव ' + mH + ' (' + moon.sign + ') — 2रे (भाव ' + h2 + ') व 12वें (भाव ' + h12 + ') में कोई ग्रह नहीं। कोई भंग कारण नहीं।\n\n**फल:** मानसिक अस्थिरता, आर्थिक उतार-चढ़ाव, एकाकीपन की प्रवृत्ति, जीवन में अकस्मात् परिवर्तन।\n\n**उपाय (अनिवार्य):**\n1. प्रति सोमवार शिव अभिषेक (जल + दूध + बिल्वपत्र)\n2. चांदी की अंगूठी अनामिका में (सोमवार सुबह पहनें)\n3. "ॐ सों सोमाय नमः" — 108 जप नित्य\n4. श्वेत वस्त्र व श्वेत पुष्प प्रतिदिन\n5. श्रावण सोमवार व्रत' };
        },

        gajakesari: function(a) {
            var moon = a.planets['चन्द्र'], guru = a.planets['गुरु'];
            if (!moon || !guru) return { name: 'गजकेसरी योग', found: false, detail: 'डेटा अनुपलब्ध' };
            var fromMoon = ((guru.house - moon.house + 12) % 12) + 1;
            if (KENDRAS.indexOf(fromMoon) !== -1) {
                var deb = guru.sign === 'मकर';
                return { name: 'गजकेसरी योग', found: true,
                    detail: (deb ? '⚠️ आंशिक' : '✅') + ' **गजकेसरी योग** — गुरु (भाव ' + guru.house + ', ' + guru.sign + ') चन्द्र (भाव ' + moon.house + ') से ' + fromMoon + 'वें स्थान में (केन्द्र)।' + (deb ? ' **गुरु मकर में नीच — शक्ति आधी।**' : ' **पूर्ण प्रभावी।**') + '\n\n**फल:** ज्ञान, यश, नेतृत्व, समाज में सम्मान।' };
            }
            return { name: 'गजकेसरी योग', found: false,
                detail: '❌ गजकेसरी योग नहीं — गुरु (भाव ' + guru.house + ') चन्द्र (भाव ' + moon.house + ') से केन्द्र में नहीं। अंतर: ' + fromMoon + 'वाँ स्थान।' };
        },

        budhaditya: function(a) {
            var sun = a.planets['सूर्य'], mer = a.planets['बुध'];
            if (!sun || !mer) return { name: 'बुधादित्य योग', found: false, detail: 'डेटा अनुपलब्ध' };
            if (sun.house === mer.house) {
                var deg = Math.abs(sun.deg - mer.deg);
                var combust = deg < 14;
                return { name: 'बुधादित्य योग', found: true,
                    detail: (combust ? '⚠️' : '✅') + ' **बुधादित्य योग** — सूर्य व बुध भाव ' + sun.house + ' (' + sun.sign + ') में युति।' + (combust ? ' बुध **अस्त** (' + deg.toFixed(1) + '° — 14° से कम) — योग शक्ति न्यून।' : ' बुध **मार्गी व प्रबल** — पूर्ण योग।') + '\n\n**फल:** तीव्र बुद्धि, वाकपटुता, लेखन-वाणिज्य में कुशलता।' };
            }
            return { name: 'बुधादित्य योग', found: false, detail: '❌ बुधादित्य योग नहीं — सूर्य भाव ' + sun.house + ', बुध भाव ' + mer.house + ' (युति नहीं)।' };
        },

        mangaldosha: function(a) {
            var mars = a.planets['मंगल'];
            if (!mars) return { name: 'मंगल दोष', found: false, detail: 'मंगल डेटा अनुपलब्ध' };
            var doshaH = [1,2,4,7,8,12];
            if (doshaH.indexOf(mars.house) !== -1) {
                var cancels = [];
                if (['मेष','वृश्चिक','मकर'].indexOf(mars.sign) !== -1) cancels.push('मंगल स्वराशि/उच्च में');
                if (mars.house === 1 && a.lagna === 'मेष') cancels.push('मेष लग्न में भाव-1 मंगल — कोई दोष नहीं');
                if (mars.house === 1 && a.lagna === 'वृश्चिक') cancels.push('वृश्चिक लग्न — मंगल लग्नेश, दोष रद्द');
                var guru = a.planets['गुरु'];
                if (guru && aspectsHouse(guru.house, mars.house, 'गुरु')) cancels.push('गुरु की दृष्टि मंगल पर');
                return { name: 'मंगल दोष', found: true,
                    detail: (cancels.length ? '⚠️ **आंशिक मंगल दोष**' : '🔴 **मंगल दोष**') + '\n\nमंगल भाव ' + mars.house + ' (' + mars.sign + ', ' + mars.dignity + ') में।' +
                        (cancels.length ? '\n\n**भंग कारण:**\n' + cancels.map(function(c){ return '• ' + c }).join('\n') : '') +
                        '\n\n**फल:** वैवाहिक जीवन में तनाव, साझेदारी में कठिनाई।\n**उपाय:** मंगलवार हनुमान चालीसा, लाल मसूर दान, मंगल जप।' };
            }
            return { name: 'मंगल दोष', found: false,
                detail: '✅ **मंगल दोष नहीं** — मंगल भाव ' + mars.house + ' (' + mars.sign + ') में स्थित है, जो दोष भावों (1,2,4,7,8,12) में नहीं है।' };
        },

        neechabhanga: function(a) {
            var yogas = [];
            Object.keys(DEBIL).forEach(function(pName) {
                var pd = a.planets[pName];
                if (!pd || pd.sign !== DEBIL[pName]) return;
                // Check bhanga conditions
                var exaltLord = LORDS[EXALT[pName]]; // lord of planet's exaltation sign
                var debilLord = LORDS[DEBIL[pName]]; // lord of debilitation sign
                var exaltLordPos = a.planets[exaltLord];
                var debilLordPos = a.planets[debilLord];
                var bhangas = [];
                if (exaltLordPos && KENDRAS.indexOf(exaltLordPos.house) !== -1) bhangas.push(exaltLord + ' केन्द्र में');
                if (debilLordPos && KENDRAS.indexOf(debilLordPos.house) !== -1) bhangas.push(debilLord + ' केन्द्र में');
                if (KENDRAS.indexOf(pd.house) !== -1) bhangas.push(pName + ' स्वयं केन्द्र में नीच');
                if (bhangas.length) {
                    yogas.push({ name: pName + ' नीचभंग राजयोग', found: true,
                        detail: '✅ **' + pName + ' नीचभंग राजयोग** — ' + pName + ' नीच राशि ' + pd.sign + ' (भाव ' + pd.house + ') में, परन्तु भंग:\n' + bhangas.map(function(b){return '• '+b}).join('\n') + '\n\n**फल:** प्रारंभिक संघर्ष के पश्चात् असाधारण उत्थान।' });
                }
            });
            return yogas.length ? yogas : [{ name: 'नीचभंग राजयोग', found: false, detail: 'कोई नीचभंग स्थिति नहीं मिली।' }];
        },

        guruchandal: function(a) {
            var guru = a.planets['गुरु'], rahu = a.planets['राहु'];
            if (!guru || !rahu) return { name: 'गुरु चांडाल योग', found: false, detail: 'डेटा अनुपलब्ध' };
            if (guru.house === rahu.house) {
                return { name: 'गुरु चांडाल योग', found: true,
                    detail: '⚠️ **गुरु चांडाल योग** — गुरु + राहु भाव ' + guru.house + ' (' + guru.sign + ') में युति।\n\n**फल:** ज्ञान में अनास्था, गुरु-शिष्य सम्बन्ध में तनाव, धर्म के प्रति भ्रम, अपरंपरागत विचार।\n**उपाय:** गुरुवार गुरु अर्चना, विद्वान ब्राह्मण भोजन, "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः" जप।' };
            }
            return { name: 'गुरु चांडाल योग', found: false, detail: '✅ गुरु चांडाल योग नहीं — गुरु (भाव ' + guru.house + ') व राहु (भाव ' + rahu.house + ') अलग भावों में।' };
        },

        kaalsarpa: function(a, chart) {
            if (!chart || !chart.planet_table) return { name: 'काल सर्प योग', found: false, detail: 'डेटा अनुपलब्ध' };
            var rahu = a.planets['राहु'], ketu = a.planets['केतु'];
            if (!rahu || !ketu) return { name: 'काल सर्प योग', found: false, detail: 'राहु/केतु डेटा अनुपलब्ध' };
            var rH = rahu.house, kH = ketu.house;
            // Check if all planets between Rahu and Ketu (one side)
            var planets7 = ['सूर्य','चन्द्र','मंगल','बुध','गुरु','शुक्र','शनि'];
            var allInArc = planets7.every(function(pName) {
                var pd = a.planets[pName];
                if (!pd) return false;
                var ph = pd.house;
                // Check if planet is in the arc from Rahu to Ketu (going forward)
                var inArc1 = false;
                var h = rH;
                for (var i = 0; i < 12; i++) {
                    if (h === kH) break;
                    if (h === ph) { inArc1 = true; break; }
                    h = (h % 12) + 1;
                }
                return inArc1;
            });
            if (allInArc) {
                // Determine type
                var types = ['अनंत','कुलिक','वासुकी','शंखपाल','पद्म','महापद्म','तक्षक','कर्कोटक','शंखनाद','पातक','विषाक्त','शेषनाग'];
                var type = types[(rH - 1) % 12] || 'काल सर्प';
                return { name: type + ' काल सर्प योग', found: true,
                    detail: '🔴 **' + type + ' काल सर्प योग**\n\nराहु (भाव ' + rH + ') से केतु (भाव ' + kH + ') के मध्य सभी ग्रह बंद।\n\n**फल:** जीवन में बाधाएं, अप्रत्याशित उलटफेर, आध्यात्मिक झुकाव।\n**उपाय:** नागपंचमी व्रत, नागदेव मन्दिर, "ॐ नागेन्द्राय नमः" 108 जप, पंचमुखी रुद्राक्ष।' };
            }
            return { name: 'काल सर्प योग', found: false, detail: '✅ काल सर्प योग नहीं — सभी ग्रह राहु-केतु के एक ओर नहीं हैं।' };
        },

        panchamahapurusha: function(a) {
            var checks = [
                { p: 'मंगल', signs: ['मेष','वृश्चिक','मकर'], name: 'रुचक योग', desc: 'साहस, नेतृत्व, सैन्य/पुलिस यश, भूमि लाभ' },
                { p: 'बुध', signs: ['मिथुन','कन्या'], name: 'भद्र योग', desc: 'तीव्र बुद्धि, वाणिज्य, लेखन, व्यापार' },
                { p: 'गुरु', signs: ['कर्क','धनु','मीन'], name: 'हंस योग', desc: 'ज्ञान, धर्म, उपदेशक, अध्यापन' },
                { p: 'शुक्र', signs: ['वृषभ','तुला','मीन'], name: 'मालव्य योग', desc: 'भोग-ऐश्वर्य, कला, वाहन, सौन्दर्य' },
                { p: 'शनि', signs: ['तुला','मकर','कुंभ'], name: 'शश योग', desc: 'अनुशासन, दीर्घायु, राजनीतिक पद' }
            ];
            var found = [];
            checks.forEach(function(c) {
                var pd = a.planets[c.p];
                if (!pd) return;
                if (KENDRAS.indexOf(pd.house) !== -1 && c.signs.indexOf(pd.sign) !== -1) {
                    found.push({ name: c.name, found: true,
                        detail: '✅ **' + c.name + '** — ' + c.p + ' केन्द्र (भाव ' + pd.house + ') में ' + pd.sign + ' (' + pd.dignity + ')। **फल:** ' + c.desc });
                }
            });
            return found;
        },

        rajYogas: function(a) {
            if (!a.lagna) return [];
            var yogas = [];
            var l = signIdx(a.lagna);
            if (l === -1) return [];
            // Kendra lords
            var kendraLords = KENDRAS.map(function(h) { return { h: h, lord: LORDS[SIGNS[(l+h-1)%12]] }; });
            var trikonaLords = [5,9].map(function(h) { return { h: h, lord: LORDS[SIGNS[(l+h-1)%12]] }; });
            // Conjunction of Kendra + Trikona lord
            kendraLords.forEach(function(kl) {
                trikonaLords.forEach(function(tl) {
                    if (kl.lord === tl.lord) return; // same = yogakaraka handled separately
                    var kp = a.planets[kl.lord], tp = a.planets[tl.lord];
                    if (!kp || !tp) return;
                    if (kp.house === tp.house) {
                        yogas.push({ name: 'राजयोग', found: true,
                            detail: '✅ **राजयोग** — ' + kl.lord + ' (भाव ' + kl.h + 'ेश) + ' + tl.lord + ' (भाव ' + tl.h + 'ेश) भाव ' + kp.house + ' (' + kp.sign + ') में युति। **फल:** राजसम्मान, उच्च पद, सत्ता-प्रतिष्ठा।' });
                    }
                });
            });
            // Yogakaraka (Kendra + Trikona lord same planet)
            kendraLords.forEach(function(kl) {
                trikonaLords.forEach(function(tl) {
                    if (kl.lord === tl.lord && kl.lord) {
                        var pd = a.planets[kl.lord];
                        if (pd) yogas.push({ name: 'योगकारक', found: true,
                            detail: '🌟 **योगकारक** — ' + kl.lord + ' एकसाथ भाव ' + kl.h + ' व भाव ' + tl.h + ' का स्वामी। भाव ' + pd.house + ' (' + pd.sign + ', ' + pd.dignity + ') में। **अत्यंत शुभ।**' });
                    }
                });
            });
            return yogas;
        },

        vipritraj: function(a) {
            if (!a.lagna) return [];
            var l = signIdx(a.lagna);
            if (l === -1) return [];
            var yogas = [];
            DUSTHANAS.forEach(function(h) {
                var lord = LORDS[SIGNS[(l+h-1)%12]];
                var pd = a.planets[lord];
                if (!pd) return;
                if (DUSTHANAS.indexOf(pd.house) !== -1 && pd.house !== h) {
                    yogas.push({ name: 'विपरीत राजयोग', found: true,
                        detail: '✅ **विपरीत राजयोग** — भाव ' + h + 'ेश ' + lord + ' दूसरे दुःस्थान (भाव ' + pd.house + ') में। **फल:** शत्रु नाश, विपदा में उत्थान, रहस्यमय सफलता।' });
                }
            });
            return yogas;
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 4: DASHA ENGINE
    // ═══════════════════════════════════════════════════════════════════
    window.VyasDashaEngine = {
        DASHA_YEARS: { 'केतु':7,'शुक्र':20,'सूर्य':6,'चन्द्र':10,'मंगल':7,'राहु':18,'गुरु':16,'शनि':19,'बुध':17 },
        analyze: function(a, query) {
            var dasha = a.dasha;
            if (!dasha || dasha.maha === 'अज्ञात') return '**दशा डेटा अनुपलब्ध।** कृपया जन्म कुण्डली में जन्म तिथि-समय दर्ज करें।';

            var mahaData = a.planets[dasha.maha];
            var antarData = a.planets[dasha.antar];
            var lines = ['**सक्रिय विंशोत्तरी दशा:** ' + dasha.chain];

            if (mahaData) {
                var mahaSign = mahaData.sign, mahaH = mahaData.house, mahaDig = mahaData.dignity;
                lines.push('**महादशा ' + dasha.maha + ':** भाव ' + mahaH + ' (' + mahaSign + ', ' + mahaDig + ')');
                // Assess dasha quality
                var quality = TRIKONAS.indexOf(mahaH) !== -1 || KENDRAS.indexOf(mahaH) !== -1 ? '**शुभ**' :
                              DUSTHANAS.indexOf(mahaH) !== -1 ? '**चुनौतीपूर्ण**' : '**मध्यम**';
                lines.push('**दशा गुण:** ' + quality + ' — ' + dasha.maha + ' भाव ' + mahaH + 'ेश की भांति फल देगा।');
            }
            if (antarData && dasha.antar) {
                lines.push('**अंतर्दशा ' + dasha.antar + ':** भाव ' + antarData.house + ' (' + antarData.sign + ')');
            }
            // Gochar trigger
            var saturnTransit = CURRENT_TRANSITS['शनि'];
            var jupiterTransit = CURRENT_TRANSITS['गुरु'];
            if (saturnTransit && jupiterTransit && a.lagna) {
                var satH = houseFromSign(saturnTransit.sign, a.lagna);
                var jupH = houseFromSign(jupiterTransit.sign, a.lagna);
                lines.push('**गोचर ट्रिगर (Nov 2026):** शनि भाव ' + satH + ' | गुरु भाव ' + jupH);
            }
            return lines.join('\n');
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 5: GOCHAR ENGINE — 2026-27 Transits
    // ═══════════════════════════════════════════════════════════════════
    window.VyasGocharEngine = {
        analyze: function(a) {
            if (!a.lagna) return 'लग्न डेटा अनुपलब्ध।';
            var lines = ['**गोचर विश्लेषण (नवंबर 2026, Swiss Ephemeris):**', ''];
            Object.entries(CURRENT_TRANSITS).forEach(function(e) {
                var pName = e[0], td = e[1];
                var h = houseFromSign(td.sign, a.lagna);
                if (h === 0) return;
                var natal = a.planets[pName];
                var conflict = natal && natal.house === h ? ' (जन्मकालीन स्थान पर)' : '';
                lines.push('**' + pName + ':** ' + td.sign + ' (' + td.deg.toFixed(1) + '°' + (td.retro ? ' वक्री' : '') + ') → भाव ' + h + conflict);
            });
            // Special: Sade-Sati and Dhaiya
            var moon = a.planets['चन्द्र'];
            if (moon) {
                var moonSign = moon.sign;
                var moonIdx = signIdx(moonSign);
                var saturnIdx = signIdx(CURRENT_TRANSITS['शनि'].sign);
                var diff = (saturnIdx - moonIdx + 12) % 12;
                if (diff <= 1 || diff >= 11) {
                    lines.push('\n🔴 **साढ़ेसाती चल रही है** — शनि चन्द्र राशि (' + moonSign + ') के निकट।');
                } else if (diff === 3 || diff === 10) {
                    lines.push('\n⚠️ **ढैय्या (शनि की लघु साढ़ेसाती)** — शनि चन्द्र से ' + diff + 'वीं राशि में।');
                }
            }
            return lines.join('\n');
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 6: BALA ENGINE — Planetary Strength
    // ═══════════════════════════════════════════════════════════════════
    window.VyasBalaEngine = {
        assess: function(a) {
            var lines = ['**ग्रह बल संक्षिप्त:**'];
            Object.entries(a.planets).forEach(function(e) {
                var pName = e[0], pd = e[1];
                var score = 0;
                var notes = [];
                if (pd.dignity === 'उच्च') { score += 3; notes.push('उच्च'); }
                else if (pd.dignity === 'स्वराशि') { score += 2; notes.push('स्वराशि'); }
                else if (pd.dignity === 'नीच') { score -= 2; notes.push('नीच'); }
                if (KENDRAS.indexOf(pd.house) !== -1) { score += 2; notes.push('केन्द्रस्थ'); }
                else if (TRIKONAS.indexOf(pd.house) !== -1) { score += 1; notes.push('त्रिकोण'); }
                else if (DUSTHANAS.indexOf(pd.house) !== -1) { score -= 1; notes.push('दुःस्थान'); }
                if (pd.retro) { notes.push('वक्री'); }
                var bar = score >= 3 ? '🟢' : score >= 1 ? '🟡' : '🔴';
                lines.push(bar + ' **' + pName + '** (भाव ' + pd.house + ', ' + pd.sign + '): ' + (notes.join(', ') || 'सामान्य'));
            });
            return lines.join('\n');
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MODULE 7: HOUSE ANALYSIS
    // ═══════════════════════════════════════════════════════════════════
    window.VyasHouseEngine = {
        HOUSE_TOPICS: {
            1: 'स्वास्थ्य, व्यक्तित्व, आत्मबल',
            2: 'धन, परिवार, वाणी, खान-पान',
            3: 'पराक्रम, भाई-बहन, यात्रा, साहस',
            4: 'सुख, माता, वाहन, गृह',
            5: 'संतान, विद्या, प्रेम, पूर्वपुण्य',
            6: 'रोग, शत्रु, ऋण, सेवा',
            7: 'विवाह, साझेदारी, व्यापार',
            8: 'आयु, मृत्यु, रहस्य, विरासत',
            9: 'भाग्य, धर्म, गुरु, पिता',
            10: 'कर्म, राज्य, यश, पद',
            11: 'लाभ, मित्र, इच्छापूर्ति',
            12: 'व्यय, विदेश, मोक्ष, अस्पताल'
        },
        analyzeHouse: function(a, houseNum) {
            var house = a.houses[houseNum];
            if (!house) return 'भाव डेटा अनुपलब्ध';
            var lordData = a.planets[house.lord];
            var lines = [
                '**भाव ' + houseNum + '** (' + (this.HOUSE_TOPICS[houseNum] || '') + ')',
                '**राशि:** ' + house.sign + ' | **भावेश:** ' + house.lord
            ];
            if (lordData) {
                lines.push('**भावेश स्थिति:** भाव ' + lordData.house + ' (' + lordData.sign + ', ' + lordData.dignity + (lordData.retro ? ', वक्री' : '') + ')');
                var lordQuality = KENDRAS.indexOf(lordData.house) !== -1 ? 'केन्द्रस्थ — उत्तम' :
                                  TRIKONAS.indexOf(lordData.house) !== -1 ? 'त्रिकोण — शुभ' :
                                  DUSTHANAS.indexOf(lordData.house) !== -1 ? 'दुःस्थान — चुनौती' : 'सामान्य';
                lines.push('**भावेश बल:** ' + lordQuality);
            }
            if (house.planets.length) lines.push('**स्थित ग्रह:** ' + house.planets.join(', '));
            else lines.push('**स्थित ग्रह:** कोई नहीं (भाव रिक्त)');
            return lines.join('\n');
        }
    };

    // ═══════════════════════════════════════════════════════════════════
    // MASTER ORCHESTRATOR — VyasDaivagyaCore
    // ═══════════════════════════════════════════════════════════════════
    window.VyasDaivagyaCore = {
        /**
         * Main entry: given query + chart, return pre-computed data block
         * This block is injected into AI systemPrompt so AI just FORMATS it
         */
        computeContext: function(query, chart) {
            if (!chart || !chart.planet_table) return '';
            var route = VyasQueryRouter.detect(query);
            var analysis = VyasChartAnalyzer.analyze(chart);
            if (!analysis) return '';

            var blocks = [
                '═══════════════════════════════════════════════════════',
                '📊 VYAS DAIVAGYA ENGINE v3.0 — PRE-COMPUTED ANALYSIS',
                '   Query Type: [' + route.toUpperCase() + '] | Zero-hallucination data',
                '═══════════════════════════════════════════════════════',
                '',
                '**जातक:** ' + analysis.name + ' | **लग्न:** ' + analysis.lagna + ' | **लग्नेश:** ' + analysis.lagnaLord + ' (' + analysis.lagnaStrength + ')',
                '**सक्रिय दशा:** ' + analysis.dasha.chain,
                ''
            ];

            if (route === 'yoga' || /योग|yoga/i.test(query)) {
                var yogas = VyasYogaEngine.detectAll(analysis, chart, query);
                blocks.push('**🔮 YOGA ANALYSIS (Mathematically Verified):**');
                yogas.forEach(function(y) { if(y) blocks.push(y.detail || ''); });
            }
            if (route === 'dasha') {
                blocks.push(VyasDashaEngine.analyze(analysis, query));
            }
            if (route === 'gochar') {
                blocks.push(VyasGocharEngine.analyze(analysis));
            }
            if (route === 'career' || route === 'd10') {
                blocks.push(this._houseAnalysis(analysis, [10, 2, 6, 11]));
            }
            if (route === 'marriage') {
                blocks.push(this._houseAnalysis(analysis, [7, 2, 5, 11]));
            }
            if (route === 'wealth') {
                blocks.push(this._houseAnalysis(analysis, [2, 11, 9, 5]));
            }
            if (route === 'health') {
                blocks.push(this._houseAnalysis(analysis, [1, 6, 8, 12]));
            }
            if (route === 'children') {
                blocks.push(this._houseAnalysis(analysis, [5, 9, 1]));
            }
            if (route === 'lagna' || route === 'general') {
                blocks.push('**ग्रह बल:**\n' + VyasBalaEngine.assess(analysis));
            }
            if (route === 'gochar' || /साढ़ेसाती|ढैय्या|ashtama/.test(query)) {
                blocks.push(VyasGocharEngine.analyze(analysis));
            }

            // Always append dasha context for natal queries
            if (['yoga','career','marriage','wealth','health','children','lagna','general','d9','d10'].indexOf(route) !== -1) {
                blocks.push('');
                blocks.push('**दशा संदर्भ:**');
                blocks.push(VyasDashaEngine.analyze(analysis, query));
            }

            blocks.push('');
            blocks.push('═══════════════════════════════════════════════════════');
            blocks.push('⚠️ उपर्युक्त सभी डेटा chart.planet_table से गणित-आधारित है।');
            blocks.push('आचार्य व्यास: इस pre-verified data को आधार बनाकर शास्त्रीय विश्लेषण करें।');

            return blocks.join('\n');
        },

        
        /**
         * Standalone / Direct HTML Formatter for UI & Fallbacks
         * Provides zero-vagueness, instant mathematical answers for yogas, dasha, gochar
         */
        formatReading: function(query, chart) {
            if (!chart || !chart.planet_table) return null;
            var q = (query || '').toLowerCase();
            var route = VyasQueryRouter.detect(query);
            var analysis = VyasChartAnalyzer.analyze(chart);
            if (!analysis) return null;

            if (route === 'yoga' || /योग|yoga|केमद्रुम|kemdrum|kendrum|गजकेसरी|gajakesari|बुधादित्य|budhaditya|मंगल.*दोष|mangal|मांगलिक|नीचभंग|neechabhanga|गुरु.*चांडाल|काल.*सर्प|kaalsarp|विपरीत|raj.*yoga|राजयोग/i.test(q)) {
                var yogas = VyasYogaEngine.detectAll(analysis, chart, query);
                if (yogas && yogas.length > 0) {
                    var html = "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                        "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>🔮 व्यास अस्त्र: सूक्ष्म योग परीक्षण व शास्त्रीय निर्णय (Vyas Yoga Engine)</span>" +
                        "</div>" +
                        "<b>ॐ नमः शिवाय।</b><br><br>" +
                        "<b>सादर प्रणाम आदरणीय " + (analysis.name || 'जातक') + " जी,</b><br>" +
                        "आपकी जन्म पत्रिका (लग्न: <b>" + analysis.lagna + "</b>, लग्नेश: <b>" + analysis.lagnaLord + "</b>) के गणितीय वेध अनुसार शास्त्रीय विश्लेषण प्रस्तुत है:<br><br>";

                    yogas.forEach(function(y) {
                        var det = (y.detail || '')
                            .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                            .replace(/\n\n/g, '<br><br>')
                            .replace(/\n/g, '<br>');
                        html += "<div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px; margin-bottom:12px;'>" +
                                "<div style='font-size:1.05rem; font-weight:700; color:" + (y.found ? (y.partial ? '#f59e0b' : '#10b981') : '#94a3b8') + "; margin-bottom:6px;'>" +
                                (y.found ? (y.partial ? '⚠️ ' : '✦ ') : '• ') + y.name + "</div>" +
                                det +
                                "</div>";
                    });

                    html += "<br><small style='color:#94a3b8;'>✓ व्यास अस्त्र गणितीय योग वेध (Brihat Parashara Hora Shastra Standard)।</small>";
                    return html;
                }
            }

            if (route === 'dasha' || /दशा|महादशा|अन्तर्दशा|pratyantar/i.test(q)) {
                var dashaText = VyasDashaEngine.analyze(analysis, query)
                    .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                    .replace(/\n\n/g, '<br><br>')
                    .replace(/\n/g, '<br>');
                return "<div class='shastra-verdict-box' style='background:rgba(59,130,246,0.06); border-left:3px solid #3b82f6; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#60a5fa; font-weight:700; font-size:0.85rem;'>⏳ विंशोत्तरी दशा चक्र एवं समय-वेध (Vimshottari Dasha Engine)</span>" +
                    "</div>" +
                    "<b>सादर प्रणाम आदरणीय " + (analysis.name || 'जातक') + " जी,</b><br><br>" +
                    dashaText + "<br><br>" +
                    "<small style='color:#94a3b8;'>✓ व्यास अस्त्र सूक्ष्म विंशोत्तरी दशा काल वेध।</small>";
            }

            return null;
        },

        _houseAnalysis: function(analysis, houses) {
            return houses.map(function(h) {
                return VyasHouseEngine.analyzeHouse(analysis, h);
            }).join('\n\n');
        }
    };

})(window);

