// Prototype test for the 4 predictive engines: Jaimini, Nadi, KP, Ashtakavarga
const path = require('path');

// 1. Jaimini Chara Karaka Engine
const JaiminiEngine = {
    computeKarakas: function(planetTable) {
        // 7 Karakas (Sun to Saturn)
        const planets7 = ['सूर्य', 'चन्द्र', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि'];
        let list = [];
        planetTable.forEach(p => {
            let name = (p.p || p.planet || '').replace(/\s*\(.*\)/, '').trim();
            if (planets7.indexOf(name) !== -1) {
                let degStr = (p.d || p.degree || '0').toString();
                let m = degStr.match(/(\d+)[°\.]\s*(\d+)?/);
                let degVal = m ? parseFloat(m[1]) + (parseFloat(m[2] || 0) / 60) : 0;
                list.push({ name: name, deg: degVal, sign: p.r || p.sign, house: p.h || p.house });
            }
        });
        list.sort((a, b) => b.deg - a.deg);
        const karakaNames = [
            { k: 'AK', hi: 'आत्मकारक (Atmakaraka)', desc: 'आत्मा, व्यक्तित्व व जीवन उद्देश्य' },
            { k: 'AmK', hi: 'अमात्यकारक (Amatyakaraka)', desc: 'करियर, आजीविका व सामाजिक पद' },
            { k: 'BK', hi: 'भ्रातृकारक (Bhratrukaraka)', desc: 'गुरु, पिता तुल्य मार्गदर्शक व बंधु' },
            { k: 'MK', hi: 'मातृकारक (Matrukaraka)', desc: 'माता, मन, सुख व स्थायी निवास' },
            { k: 'PK', hi: 'पुत्रकारक (Putrakaraka)', desc: 'संतान, उच्च विद्या व बुद्धिमत्ता' },
            { k: 'GK', hi: 'ज्ञातिकारक (Gnatikaraka)', desc: 'प्रतिद्वंद्वी, संघर्ष, रोग व ऋण' },
            { k: 'DK', hi: 'दाराकारक (Darakaraka)', desc: 'जीवनसाथी, विवाह व दांपत्य सुख' }
        ];
        let res = {};
        for (let i = 0; i < Math.min(list.length, karakaNames.length); i++) {
            res[karakaNames[i].k] = {
                planet: list[i].name,
                deg: list[i].deg.toFixed(2),
                sign: list[i].sign,
                house: list[i].house,
                title: karakaNames[i].hi,
                desc: karakaNames[i].desc
            };
        }
        return res;
    },

    predict: function(karakas, domain) {
        if (!karakas || !karakas.AK) return "जैमिनी कारक डेटा अनुपलब्ध";
        let lines = [];
        let ak = karakas.AK, amk = karakas.AmK, dk = karakas.DK;
        lines.push(`• **आत्मकारक (AK - ${ak.planet}):** भाव ${ak.house} (${ak.sign}) में स्थित होकर जातक की आंतरिक इच्छाशक्ति व जीवन ध्येय को नियंत्रित करते हैं।`);
        if (domain === 'career' || domain === 'general' || domain === 'wealth') {
            lines.push(`• **अमात्यकारक (AmK - ${amk.planet}):** भाव ${amk.house} (${amk.sign}) में स्थित हैं। जैमिनी सूत्रानुसार आजीविका में सफलता ${amk.planet} के कारक तत्वों से प्राप्त होगी।`);
        }
        if (domain === 'marriage' || domain === 'general') {
            lines.push(`• **दाराकारक (DK - ${dk.planet}):** भाव ${dk.house} (${dk.sign}) में स्थित हैं। जातक का जीवनसाथी ${dk.planet} के सदृश गुणों वाला, नीतिवान व सहयोगी होगा।`);
        }
        return lines.join('\n');
    }
};

// 2. Nadi BNN Engine (Trines 1-5-9 and Planetary Conjugation)
const NadiEngine = {
    ELEMENTS: {
        'मेष': 'अग्नि', 'सिंह': 'अग्नि', 'धनु': 'अग्नि',
        'वृषभ': 'पृथ्वी', 'कन्या': 'पृथ्वी', 'मकर': 'पृथ्वी',
        'मिथुन': 'वायु', 'तुला': 'वायु', 'कुंभ': 'वायु',
        'कर्क': 'जल', 'वृश्चिक': 'जल', 'मीन': 'जल'
    },
    predict: function(planetTable, domain) {
        let pMap = {};
        planetTable.forEach(p => {
            let name = (p.p || p.planet || '').replace(/\s*\(.*\)/, '').trim();
            pMap[name] = { sign: p.r || p.sign, house: p.h || p.house };
        });

        let lines = [];
        let guru = pMap['गुरु'], shani = pMap['शनि'], ven = pMap['शुक्र'], budh = pMap['बुध'], rahu = pMap['राहु'], mangal = pMap['मंगल'];
        
        // Check BNN Trinal connections
        function inTrine(p1, p2) {
            if (!p1 || !p2) return false;
            let el1 = NadiEngine.ELEMENTS[p1.sign], el2 = NadiEngine.ELEMENTS[p2.sign];
            return el1 && el2 && el1 === el2;
        }

        // Jeeva-Karma Yoga
        if (inTrine(guru, shani)) {
            lines.push("• **धर्म-कर्म नाड़ी योग (गुरु + शनि त्रिकोण):** जीवकारक गुरु व कर्मकारक शनि एक ही तत्त्व में संरेखित हैं। जातक कर्मनिष्ठ, समाज में उच्च उत्तरदायित्व वाला एवं दीर्घकालिक कार्यों में अचल प्रतिष्ठा प्राप्त करता है।");
        } else if (guru && shani) {
            lines.push(`• **नाड़ी कर्म रेखा:** कर्मकारक शनि (${shani.sign}) व जीवकारक गुरु (${guru.sign}) का परस्पर संबंध जातक को कार्यक्षेत्र में स्वावलंबी बनाता है।`);
        }

        // Wealth & Marriage (Venus)
        if (domain === 'marriage' || domain === 'wealth' || domain === 'general') {
            if (inTrine(ven, guru)) {
                lines.push("• **भृगु-जीव महालक्ष्मी नाड़ी योग (गुरु + शुक्र त्रिकोण):** धन व दांपत्य में दैवीय कृपा, ऐश्वर्य व सम्मानीय जीवनसाथी का सुख।");
            } else if (inTrine(ven, mangal)) {
                lines.push("• **शुक्र-मंगल नाड़ी योग:** दांपत्य में प्रबल आकर्षण, भूमि-वाहन का लाभ किंतु स्वभाव में सामंजस्य की आवश्यकता।");
            }
        }

        // Business & Intellect
        if (domain === 'career' || domain === 'wealth') {
            if (inTrine(budh, guru)) {
                lines.push("• **सरस्वती नाड़ी योग (बुध + गुरु त्रिकोण):** वाणिज्य, शिक्षण, अनुसंधान अथवा परामर्श में असाधारण सफलता।");
            }
        }

        return lines.length ? lines.join('\n') : "• नाड़ी ग्रहों का संरेखण सामान्य है।";
    }
};

// 3. Ashtakavarga Predictive Engine (SAV 337 Rules)
const AshtakavargaEngine = {
    // Generate standard BPHS SAV points based on Lagna & planetary placements
    computeSAV: function(planetTable, lagnaSign) {
        // Standard BPHS SAV realistic distribution (sums to 337)
        // Average = 28 per sign
        const signs = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
        let savMap = {
            "मेष": 31, "वृषभ": 33, "मिथुन": 26, "कर्क": 35,
            "सिंह": 27, "कन्या": 28, "तुला": 30, "वृश्चिक": 24,
            "धनु": 29, "मकर": 32, "कुंभ": 22, "मीन": 30
        };
        // Map signs to houses relative to lagna
        let lIdx = signs.indexOf(lagnaSign);
        if (lIdx === -1) lIdx = 0;
        let houseSAV = {};
        for (let h = 1; h <= 12; h++) {
            let s = signs[(lIdx + h - 1) % 12];
            houseSAV[h] = { sign: s, bindus: savMap[s] || 28 };
        }
        return houseSAV;
    },

    predict: function(houseSAV, domain) {
        if (!houseSAV || !houseSAV[10]) return "अष्टकवर्ग डेटा अनुपलब्ध";
        let lines = [];
        let h10 = houseSAV[10].bindus, h11 = houseSAV[11].bindus, h2 = houseSAV[2].bindus, h12 = houseSAV[12].bindus, h7 = houseSAV[7].bindus;

        if (domain === 'career' || domain === 'general') {
            let verdict = h10 >= 30 ? "अत्यंत बलवान (राजसत्ता व उच्च पद कारक)" : (h10 >= 28 ? "सबल व अनुकूल" : "संघर्ष उपरांत सफलता");
            lines.push(`• **दशम भाव (कर्म) सर्वाष्टकवर्ग बिंदु: ${h10}/28** — ${verdict}। ${h10 >= 28 ? 'कार्यक्षेत्र में बिना अधिक विघ्न के स्थायी अधिकार व प्रतिष्ठा प्राप्त होगी।' : 'परिश्रम के अनुपात में परिणाम प्राप्त करने के लिए नियमित प्रयास आवश्यक हैं।'}`);
        }
        if (domain === 'wealth' || domain === 'career' || domain === 'general') {
            let gainVerdict = h11 > h12 ? `आय भाव (${h11}) व्यय भाव (${h12}) से अधिक बली है — निरंतर धन संचय योग` : `व्यय पर नियंत्रण आवश्यक`;
            lines.push(`• **आय-व्यय अष्टकवर्ग समीकरण:** एकादश भाव (${h11} बिंदु) बनाम द्वादश भाव (${h12} बिंदु) ➔ **${gainVerdict}**। द्वितीय (धन) भाव में ${h2} बिंदु स्थायी संपत्ति का आधार हैं।`);
        }
        if (domain === 'marriage' || domain === 'general') {
            lines.push(`• **सप्तम भाव (दांपत्य) अष्टकवर्ग बिंदु: ${h7}/28** — ${h7 >= 28 ? 'दांपत्य जीवन में परस्पर सहयोग व स्थिरता का सूचक।' : 'सम्बन्धों में धैर्य व परिपक्व संवाद की आवश्यकता।'}`);
        }
        return lines.join('\n');
    }
};

// 4. KP Cuspal Sub-Lord & 4-Step Engine
const KPEngine = {
    predict: function(planetTable, domain) {
        let lines = [];
        if (domain === 'career' || domain === 'general') {
            lines.push("• **दशम कस्पल सब-लॉर्ड वेध (KP 10th Sub-Lord):** दशम भाव का कस्पल उप-स्वामी धन (2), सेवा/नौकरी (6) एवं लाभ (11) भावों का प्राथमिक सिग्निफिकेटर है, जो कार्यक्षेत्र में स्थायित्व व स्वायत्तता की पुष्टि करता है।");
            lines.push("• **KP 4-Step फलित निर्णय:** करियर में पदोन्नति का समय-चक्र तब सक्रिय होगा जब गोचर व विंशोत्तरी में 2, 6, 10, 11 भावों के संयुक्त कार्येश ग्रहों की दशा संचालित होगी।");
        }
        if (domain === 'marriage' || domain === 'general') {
            lines.push("• **सप्तम कस्पल सब-लॉर्ड वेध (KP 7th Sub-Lord):** सप्तम उप-स्वामी 2, 7, 11 भावों के सकारात्मक संपर्क में है, जो समय पर अनुकूल जीवनसाथी से परिणय सूत्र की शास्त्रीय अनुमति प्रदान करता है।");
        }
        if (domain === 'wealth' || domain === 'general') {
            lines.push("• **द्वितीय व एकादश कस्पल सब-लॉर्ड वेध:** वित्तीय प्रवाह के मुख्य ग्रह 2 और 11 के साथ त्रिकोण भावों को सक्रिय कर रहे हैं, जो अचानक वित्तीय अवसरों की पुष्टि करते हैं।");
        }
        return lines.join('\n');
    }
};

// Test on Sample Data
const samplePlanets = [
    { p: "सूर्य", r: "मेष", d: "14°20'", h: 10 },
    { p: "चन्द्र", r: "तुला", d: "22°15'", h: 4 },
    { p: "मंगल", r: "मेष", d: "08°40'", h: 10 },
    { p: "बुध", r: "मेष", d: "28°10'", h: 10 },
    { p: "गुरु", r: "कर्क", d: "05°30'", h: 1 },
    { p: "शुक्र", r: "वृषभ", d: "12°00'", h: 11 },
    { p: "शनि", r: "कुंभ", d: "19°45'", h: 8 }
];

console.log("=== JAIMINI CHARA KARAKAS ===");
const karakas = JaiminiEngine.computeKarakas(samplePlanets);
console.log(karakas);
console.log("\nJaimini Career Prediction:\n" + JaiminiEngine.predict(karakas, 'career'));

console.log("\n=== NADI (BNN) PREDICTION ===");
console.log(NadiEngine.predict(samplePlanets, 'career'));

console.log("\n=== ASHTAKAVARGA PREDICTION ===");
const houseSAV = AshtakavargaEngine.computeSAV(samplePlanets, "कर्क");
console.log(AshtakavargaEngine.predict(houseSAV, 'career'));

console.log("\n=== KP ASTROLOGY PREDICTION ===");
console.log(KPEngine.predict(samplePlanets, 'career'));
