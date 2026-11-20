const path = require('path');
require(path.join(__dirname, '../js/vyas_sutras_bank.js'));

const MASTER_DATA = global.VyasSutrasBank.data;

function smartSearchSutras(query, limit) {
    limit = limit || 10;
    if (!query) return [];
    var q = query.toLowerCase().trim();
    var results = [];
    var seen = {};

    var searchTokens = [];
    var astroKeywords = [
        'केमद्रुम', 'kemdrum', 'kendrum', 'गजकेसरी', 'gajakesari', 'बुधादित्य', 'budhaditya',
        'रुचक', 'ruchaka', 'भद्र', 'bhadra', 'हंस', 'hamsa', 'मालव्य', 'malavya', 'शश', 'sasa',
        'मांगलिक', 'manglik', 'मंगल दोष', 'कालसर्प', 'kaalsarp', 'चांडाल', 'chandal', 'नीचभंग', 'neechabhanga',
        'विपरीत', 'viparita', 'साढ़ेसाती', 'sadesati', 'ढैय्या', 'dhayya', 'अधि योग', 'अमला योग', 'लक्ष्मी योग',
        'सूर्य', 'sun', 'चन्द्र', 'चंद्र', 'moon', 'मंगल', 'mars', 'बुध', 'mercury',
        'गुरु', 'बृहस्पति', 'jupiter', 'शुक्र', 'venus', 'शनि', 'saturn', 'राहु', 'rahu', 'केतु', 'ketu',
        'दशम भाव', '10th', 'दशम', 'कर्म', 'सप्तम भाव', '7th', 'सप्तम', 'विवाह', 'द्वितीय भाव', '2nd', 'द्वितीय', 'धन',
        'पंचम भाव', '5th', 'संतान', 'नवम भाव', '9th', 'भाग्य', 'षष्ठ भाव', '6th', 'रोग', 'अष्टम भाव', '8th', 'आयु',
        'द्वादश भाव', '12th', 'मोक्ष', 'करियर', 'career', 'आजीविका', 'नौकरी', 'व्यापार', 'व्यवसाय', 'दांपत्य', 'स्वास्थ्य'
    ];
    astroKeywords.forEach(function(kw) {
        if (q.indexOf(kw.toLowerCase()) !== -1) {
            searchTokens.push(kw.toLowerCase());
        }
    });
    if (searchTokens.length === 0) {
        var words = q.split(/\s+/).filter(function(w){ return w.length >= 3; });
        searchTokens = words.slice(0, 3);
    }
    if (searchTokens.length === 0) {
        searchTokens = [q];
    }

    function scanList(arr, catName, term) {
        if (!arr || !arr.length) return false;
        for (var i = 0; i < arr.length; i++) {
            var s = arr[i];
            var cond = s[0], pred = s[1], src = s[2], dom = s[3];
            var full = (cond + ' ' + pred + ' ' + src).toLowerCase();
            if (full.indexOf(term) !== -1) {
                var k = (cond + ' ' + pred).substring(0, 45);
                if (!seen[k]) {
                    seen[k] = true;
                    results.push({
                        type: catName,
                        cond: cond,
                        pred: pred,
                        src: src,
                        domain: dom
                    });
                    if (results.length >= limit) return true;
                }
            }
        }
        return false;
    }

    for (var t = 0; t < searchTokens.length; t++) {
        var term = searchTokens[t];
        for (var y in MASTER_DATA.yogas) {
            if (scanList(MASTER_DATA.yogas[y], 'शास्त्रीय महायोग', term)) return results;
        }
        for (var h in MASTER_DATA.planet_houses) {
            if (scanList(MASTER_DATA.planet_houses[h], 'भाव फल', term)) return results;
        }
        for (var s in MASTER_DATA.planet_signs) {
            if (scanList(MASTER_DATA.planet_signs[s], 'ग्रह-राशि', term)) return results;
        }
        for (var u in MASTER_DATA.yutis) {
            if (scanList(MASTER_DATA.yutis[u], 'ग्रह युति', term)) return results;
        }
        for (var d in MASTER_DATA.domains) {
            if (scanList(MASTER_DATA.domains[d], 'विषय फलित', term)) return results;
        }
    }

    return results;
}

const queries = [
    "केमद्रुम योग क्या है और इसके भंग के नियम क्या हैं?",
    "कुंडली में गजकेसरी योग कैसे बनता है?",
    "सूर्य जब दशम भाव में हो तो क्या प्रभाव देता है?",
    "मांगलिक दोष के क्या प्रभाव और उपाय हैं?",
    "विवाह कब होगा और जीवनसाथी कैसा मिलेगा?"
];

queries.forEach(q => {
    let res = smartSearchSutras(q, 3);
    console.log(`\nQuery: "${q}" => Found ${res.length} sutras:`);
    res.forEach((r, idx) => {
        console.log(`  ${idx+1}. [${r.src}] ${r.cond} => ${r.pred.substring(0, 80)}...`);
    });
});
