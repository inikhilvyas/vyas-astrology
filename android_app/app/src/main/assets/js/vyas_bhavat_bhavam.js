/**
 * VYAS ASTRA — BHAVAT BHAVAM (12x12 = 144 COMBINATIONS) & SHODH GRANTH SYNTHESIZER
 * Based on Nikhil Vyas, M.A. Jyotish, LL.B. Master Treatise (vyasastro.in)
 * Formula: Z = ((Y - 1 + X - 1) % 12) + 1
 */

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.VyasBhavatBhavam = factory();
    }
}(typeof self !== 'undefined' ? self : this, function () {

    var BHAVA_NAMES = [
        "तनु (Lagna) • शरीर, आत्मबल व व्यक्तित्व",
        "धन (Dhana) • संचित संपत्ति, वाणी व कुटुंब",
        "सहज (Bhratri) • पराक्रम, साहस व भाई-बहन",
        "सुख (Matri) • माता, भूमि, भवन, वाहन व आंतरिक सुख",
        "पुत्र (Suta) • बुद्धि, संतान, पूर्वपुण्य व विद्या",
        "रिपु (Ripu) • रोग, ऋण, शत्रु व प्रतिस्पर्धा",
        "जाया (Jaya) • जीवनसाथी, साझेदारी व लोक संपर्क",
        "रंध्र (Ayur) • आयु, गूढ़ विद्या, आकस्मिक धन व शोध",
        "धर्म (Bhagya) • भाग्य, धर्म, उच्च शिक्षा व पिता",
        "कर्म (Karma) • आजीविका, पद, प्रतिष्ठा व राज्य सम्मान",
        "आय (Labha) • आय, मित्र, ज्येष्ठ भ्राता व सर्वकार्य सिद्धि",
        "व्यय (Vyaya) • विदेश वास, मोक्ष, अध्यात्म व व्यय"
    ];

    var BHAVA_SHORT = [
        "1st (तनु)", "2nd (धन)", "3rd (सहज)", "4th (सुख)",
        "5th (पुत्र)", "6th (रिपु)", "7th (जाया)", "8th (रंध्र)",
        "9th (धर्म)", "10th (कर्म)", "11th (आय)", "12th (व्यय)"
    ];

    var X_FROM_X_SIGNIFICANCE = {
        1: { target: 1, title: "1 से 1 (1ला भाव)", sutra: "स्वयं का मूल अस्तित्व, प्राण-शक्ति व आत्मा", desc: "लग्न ही सम्पूर्ण कुण्डली का आधार है। तनु से तनु भाव स्वयं के अस्तित्व, आत्मबल और शारीरिक आरोग्यता का निर्धारण करता है।" },
        2: { target: 3, title: "2 से 2 (3रा भाव)", sutra: "धन का पोषण, पुरुषार्थ, संचित प्रयास व संवाद", desc: "द्वितीय (धन) से द्वितीय भाव तृतीय (सहज) है। यह दर्शाता है कि धन की वृद्धि जातक के निरंतर पराक्रम, लेखनी और व्यावसायिक संवाद से ही संभव है।" },
        3: { target: 5, title: "3 से 3 (5वाँ भाव)", sutra: "पराक्रम का सृजन, कौशल, विवेक व प्रतिभा", desc: "तृतीय (पराक्रम) से तृतीय भाव पंचम (बुद्धि) है। अदम्य साहस केवल शारीरिक नहीं बल्कि जब विवेक और पूर्वपुण्य से युक्त होता है, तभी पराक्रम सिद्धि देता है।" },
        4: { target: 7, title: "4 से 4 (7वाँ भाव)", sutra: "गृहस्थ सुख का विस्तार व लोक-साझेदारी", desc: "चतुर्थ (सुख) से चतुर्थ भाव सप्तम (जाया) है। घर की आंतरिक शांति का बाह्य विस्तार जीवनसाथी और लोक-व्यवहार की सामंजस्यता से होता है।" },
        5: { target: 9, title: "5 से 5 (9वाँ भाव)", sutra: "बुद्धि व पूर्वपुण्य से भाग्योदय, धर्म व ईश्वरीय कृपा", desc: "पंचम (संतान/ज्ञान) से पंचम भाव नवम (धर्म) है। जातक की बुद्धि और साधना जब धर्म से जुड़ती है, तभी चिरस्थायी भाग्योदय घटित होता है।" },
        6: { target: 11, title: "6 से 6 (11वाँ भाव)", sutra: "रोग, शत्रु व ऋण पर विजय और प्रचुर लाभ", desc: "षष्ठ (शत्रु/प्रतिस्पर्धा) से षष्ठ भाव एकादश (लाभ) है। कठिन संघर्षों, कर्जों और कानूनी वादों पर विजय प्राप्त कर जातक विपुल लाभ अर्जित करता है।" },
        7: { target: 1, title: "7 से 7 (1ला भाव)", sutra: "जीवनसाथी का प्रभाव व स्वयं का यथार्थ प्रतिबिंब", desc: "सप्तम (साझेदार) से सप्तम भाव पुनः लग्न (1ला भाव) है। जीवनसाथी वस्तुतः जातक के अपने ही अंतर्मन और प्रारब्ध का भौतिक दर्पण होता है।" },
        8: { target: 3, title: "8 से 8 (3रा भाव)", sutra: "आयु-शक्ति, गूढ़ संकट में अदम्य धैर्य व साहस", desc: "अष्टम (आयु/संकट) से अष्टम भाव तृतीय (पराक्रम) है। जीवन-मरण के संकट और गंभीर विपत्तियों से उबरने की शक्ति जातक के 3रे भाव के जीवट से आती है।" },
        9: { target: 5, title: "9 से 9 (5वाँ भाव)", sutra: "धर्म, साधना व गुरु कृपा से मंत्र-सिद्धि व संतान", desc: "नवम (भाग्य/गुरु) से नवम भाव पंचम (मंत्र/संतान) है। गुरु के आशीर्वाद और धर्म-पालन से इष्ट-कृपा व तीव्र मंत्र-सिद्धि फलित होती है।" },
        10: { target: 7, title: "10 से 10 (7वाँ भाव)", sutra: "कर्म का लोक-विस्तार, व्यापारिक सत्ता व सामाजिक मान", desc: "दशम (कर्म/प्रतिष्ठा) से दशम भाव सप्तम (लोक-व्यवहार) है। कार्यक्षेत्र की सर्वोच्च सफलता जनता से संपर्क और बड़े व्यापारिक गठबंधनों से स्थापित होती है।" },
        11: { target: 9, title: "11 से 11 (9वाँ भाव)", sutra: "लाभ की निरंतरता, अक्षय समृद्धि व धर्म-परायणता", desc: "एकादश (आय) से एकादश भाव नवम (धर्म) है। संचित लाभ तभी स्थायी और पुण्यदायी बनता है जब वह धर्म, परोपकार और नीति-सम्मत मार्ग से अर्जित हो।" },
        12: { target: 11, title: "12 से 12 (11वाँ भाव)", sutra: "व्यय, त्याग व विदेशी निवेश से भौतिक-आध्यात्मिक लाभ", desc: "द्वादश (मोक्ष/व्यय) से द्वादश भाव एकादश (लाभ) है। विवेकपूर्ण त्याग, धर्मार्थ दान और सुदूर निवेश अंततः जातक को मान और आत्म-संतोष रूपी लाभ देता है।" }
    };

    function calculateResultantBhava(baseY, relativeX) {
        var y = parseInt(baseY, 10);
        var x = parseInt(relativeX, 10);
        if (isNaN(y) || y < 1 || y > 12) y = 1;
        if (isNaN(x) || x < 1 || x > 12) x = 1;
        var z = ((y - 1 + x - 1) % 12) + 1;
        return {
            baseY: y,
            relativeX: x,
            resultZ: z,
            baseName: BHAVA_NAMES[y - 1],
            relativeName: BHAVA_SHORT[x - 1],
            resultName: BHAVA_NAMES[z - 1],
            formula: "Z = ((" + y + " - 1 + " + x + " - 1) mod 12) + 1 = भाव " + z
        };
    }

    function synthesizeBhavatBhavam(chart, baseY, relativeX) {
        var res = calculateResultantBhava(baseY, relativeX);
        var z = res.resultZ;
        var y = res.baseY;
        var x = res.relativeX;

        var ascSignIdx = 0;
        if (chart && chart.profile && chart.profile.asc_sign) {
            var signNames = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var found = signNames.indexOf(chart.profile.asc_sign);
            if (found !== -1) ascSignIdx = found;
        }

        var zSignIdx = (ascSignIdx + z - 1) % 12;
        var ySignIdx = (ascSignIdx + y - 1) % 12;

        var signNamesHi = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
        var signLordsHi = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];

        var zSign = signNamesHi[zSignIdx];
        var zLord = signLordsHi[zSignIdx];
        var yLord = signLordsHi[ySignIdx];

        // KP Cusp info
        var kpCusp = (chart && chart.kp && chart.kp.cusps && chart.kp.cusps[z - 1]) ? chart.kp.cusps[z - 1] : null;
        var csl = kpCusp ? (kpCusp.sl || kpCusp.subLord || "अविदित") : "बुध";
        var cDeg = kpCusp ? (kpCusp.deg || kpCusp.dms_str || "15°00'") : "15°00'";

        // Occupying planets
        var occupying = [];
        if (chart && chart.planet_table) {
            for (var i = 0; i < chart.planet_table.length; i++) {
                var pl = chart.planet_table[i];
                var plSign = pl.sign || "";
                if (plSign === zSign) {
                    occupying.push(pl.name || pl.p);
                }
            }
        }

        // Natural Panchadha Maitri between Y-Lord and Z-Lord
        var relation = (yLord === zLord) ? "स्वयं (अभिन्न)" : "पंचधा मैत्री सम्बद्ध";

        // Synthesis Prediction
        var synthesis = "भाव " + y + " (" + BHAVA_SHORT[y - 1] + ") का " + x + "वाँ भाव = भाव " + z + " (" + BHAVA_SHORT[z - 1] + ")। " +
            "परिणामी राशि: " + zSign + ", भावेश: " + zLord + ", केपी कस्पल सब-लॉर्ड (CSL): " + csl + " (" + cDeg + ")। " +
            (occupying.length > 0 ? ("इस भाव में स्थित ग्रह: " + occupying.join(", ") + "। ") : "यह भाव प्रत्यक्ष ग्रहों से रिक्त है, भावेश " + zLord + " व CSL " + csl + " द्वारा फल नियंत्रित है। ") +
            "शास्त्रीय भावात् भावम् सूत्र के अनुसार, भाव " + y + " का कार्य-फल भाव " + z + " के माध्यम से ही प्रस्फुटित होता है।";

        return {
            calc: res,
            zSign: zSign,
            zLord: zLord,
            yLord: yLord,
            csl: csl,
            cDeg: cDeg,
            occupying: occupying,
            relation: relation,
            synthesis: synthesis,
            isXfromX: (y === x),
            xFromXDetail: (y === x) ? X_FROM_X_SIGNIFICANCE[y] : null
        };
    }

    return {
        BHAVA_NAMES: BHAVA_NAMES,
        BHAVA_SHORT: BHAVA_SHORT,
        X_FROM_X_SIGNIFICANCE: X_FROM_X_SIGNIFICANCE,
        calculateResultantBhava: calculateResultantBhava,
        synthesizeBhavatBhavam: synthesizeBhavatBhavam
    };
}));
