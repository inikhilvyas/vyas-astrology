const fs = require('fs');

const SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
const SIGNS_EN = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
const PLANET_NAMES_HI = {
    Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Mercury: "बुध",
    Jupiter: "गुरु", Venus: "शुक्र", Saturn: "शनि", Rahu: "राहु", Ketu: "केतु"
};

const D60_DEITIES = [
    "Ghora", "Rakshasa", "Deva", "Kubera", "Yaksha", "Kinnara", "Bhrashta", "Kulaghna", "Garala", "Vahni",
    "Maya", "Purishaka", "Apampati", "Marutvana", "Kaala", "Sarpa", "Amrita", "Indu", "Mridu", "Komala",
    "Heramba", "Brahma", "Vishnu", "Maheshwara", "Deva", "Aardra", "Kalinasha", "Kshiteesha", "Kamalakara", "Gulika",
    "Mrityu", "Kaala", "Davagni", "Ghora", "Adhama", "Kantaka", "Sudha", "Amrita", "Poornachandra", "Vishadagdha",
    "Kulanasha", "Vamshakshaya", "Utpata", "Kaalarupa", "Saumya", "Komala", "Sheetala", "Karaladamshtra", "Chandramukhi", "Praveena",
    "Kaalapavaka", "Dandayudha", "Nirmala", "Saumya", "Krura", "Atisheetala", "Amrita", "Payodhi", "Bhramana", "Chandrarekha"
];

const VARGA_TITLES = {
    D1: "D-1 लग्न कुण्डली • जन्मपत्रिका (शारीरिक स्वरूप, आरोग्य व स्वभाव)",
    D2: "D-2 होरा चक्र (धन, संचित संपत्ति व समृद्धि)",
    D3: "D-3 द्रेष्काण चक्र (पराक्रम, सहोदर व ऊर्जा)",
    D4: "D-4 चतुर्थांश चक्र (भूमि, भवन, वाहन व अचल संपत्ति)",
    D7: "D-7 सप्तांश चक्र (संतान सुख, वंश वृद्धि व पूर्व पुण्य)",
    D9: "D-9 नवमांश कुण्डली (भाग्य, जीवनसाथी व आंतरिक आत्मिक शक्ति)",
    D10: "D-10 दशमांश कुण्डली (करियर, पद, प्रतिष्ठा व सामाजिक सम्मान)",
    D12: "D-12 द्वादशांश चक्र (माता-पिता, पितृ ऋण व वंशज)",
    D16: "D-16 षोडशांश चक्र (वाहन सुख, मानसिक आनंद व सुख-साधन)",
    D20: "D-20 विंशांश चक्र (आध्यात्मिक साधना, उपासना व सिद्धि)",
    D24: "D-24 चतुर्विंशांश चक्र (उच्च विद्या, ज्ञान व शोध कौशल)",
    D27: "D-27 सप्तविंशांश चक्र (शारीरिक बल, सामर्थ्य व दुर्बलता)",
    D30: "D-30 त्रिंशांश चक्र (अरिष्ट, व्याधि व प्रारब्ध कष्ट)",
    D40: "D-40 खवेदांश चक्र (शुभ-अशुभ फल व कुल प्रारब्ध)",
    D45: "D-45 अक्षवेदांश चक्र (चारित्रिक शुचिता व सूक्ष्म चेतना)",
    D60: "D-60 षष्ट्यंश चक्र (पूर्व जन्म प्रारब्ध व सम्पूर्ण फल निर्णय)"
};

function calcVargasDetailed(lon) {
    var pSign = Math.floor(lon / 30.0) % 12;
    var deg = lon % 30.0;
    var isOdd = (pSign % 2 === 0);
    var v = {};

    function addV(k, num, s, d, deity) {
        v[k] = { key: k, num: num, sign_index: s, sign_name: SIGNS_HI[s], sign_en: SIGNS_EN[s], deg: d, deity: deity || "" };
    }

    // D1 Rashi (30°)
    addV("D1", 1, pSign, deg);

    // D2 Hora (15°)
    var d2_sign = isOdd ? (deg < 15.0 ? 4 : 3) : (deg < 15.0 ? 3 : 4);
    addV("D2", 2, d2_sign, (deg * 2.0) % 30.0);

    // D3 Drekkana (10°)
    var d3_part = Math.floor(deg / 10.0);
    addV("D3", 3, (pSign + d3_part * 4) % 12, (deg * 3.0) % 30.0);

    // D4 Chaturthamsha (7°30')
    var d4_part = Math.floor(deg / 7.5);
    addV("D4", 4, (pSign + d4_part * 3) % 12, (deg * 4.0) % 30.0);

    // D7 Saptamsha (4°17'08.57")
    var d7_part = Math.floor(deg / (30.0 / 7.0));
    var d7_sign = isOdd ? (pSign + d7_part) % 12 : (pSign + 6 + d7_part) % 12;
    addV("D7", 7, d7_sign, (deg * 7.0) % 30.0);

    // D9 Navamsha (3°20' - 4 Tatvas: Agni, Prithvi, Vayu, Jala)
    var d9_part = Math.floor(deg / (30.0 / 9.0));
    var d9_element = pSign % 4; // 0: Fire, 1: Earth, 2: Air, 3: Water
    var d9_starts = [0, 9, 6, 3]; // Aries, Capricorn, Libra, Cancer
    var d9_start = d9_starts[d9_element];
    addV("D9", 9, (d9_start + d9_part) % 12, (deg * 9.0) % 30.0);

    // D10 Dashamsha (3°00')
    var d10_part = Math.floor(deg / 3.0);
    var d10_start = isOdd ? pSign : (pSign + 8) % 12;
    addV("D10", 10, (d10_start + d10_part) % 12, (deg * 10.0) % 30.0);

    // D12 Dwadashamsha (2°30')
    var d12_part = Math.floor(deg / 2.5);
    addV("D12", 12, (pSign + d12_part) % 12, (deg * 12.0) % 30.0);

    // D16 Shodashamsha (1°52'30")
    var d16_part = Math.floor(deg / 1.875);
    var d16_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 4 : 8);
    addV("D16", 16, (d16_start + d16_part) % 12, (deg * 16.0) % 30.0);

    // D20 Vimshamsha (1°30')
    var d20_part = Math.floor(deg / 1.5);
    var d20_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 8 : 4);
    addV("D20", 20, (d20_start + d20_part) % 12, (deg * 20.0) % 30.0);

    // D24 Chaturvimshamsha (1°15')
    var d24_part = Math.floor(deg / 1.25);
    var d24_start = isOdd ? 4 : 3;
    addV("D24", 24, (d24_start + d24_part) % 12, (deg * 24.0) % 30.0);

    // D27 Saptavimshamsha (1°06'40")
    var d27_part = Math.floor(deg / (30.0 / 27.0));
    var d27_starts = [0, 3, 6, 9];
    var d27_start = d27_starts[pSign % 4];
    addV("D27", 27, (d27_start + d27_part) % 12, (deg * 27.0) % 30.0);

    // D30 Trimshamsha (Unequal BPHS 6.19 parts)
    var d30_sign = 0;
    if (isOdd) {
        if (deg < 5.0) d30_sign = 0;
        else if (deg < 10.0) d30_sign = 10;
        else if (deg < 18.0) d30_sign = 8;
        else if (deg < 25.0) d30_sign = 2;
        else d30_sign = 6;
    } else {
        if (deg < 5.0) d30_sign = 1;
        else if (deg < 12.0) d30_sign = 5;
        else if (deg < 20.0) d30_sign = 11;
        else if (deg < 25.0) d30_sign = 9;
        else d30_sign = 7;
    }
    addV("D30", 30, d30_sign, (deg * 30.0) % 30.0);

    // D40 Khavedamsha (0°45')
    var d40_part = Math.floor(deg / 0.75);
    var d40_start = isOdd ? 0 : 6;
    addV("D40", 40, (d40_start + d40_part) % 12, (deg * 40.0) % 30.0);

    // D45 Akshavedamsha (0°40')
    var d45_part = Math.floor(deg / (30.0 / 45.0));
    var d45_start = (pSign % 3 === 0) ? 0 : ((pSign % 3 === 1) ? 4 : 8);
    addV("D45", 45, (d45_start + d45_part) % 12, (deg * 45.0) % 30.0);

    // D60 Shashtyamsha (0°30' with 60 Deities)
    var d60_part = Math.floor(deg / 0.5);
    var d60_sign = (pSign + d60_part) % 12;
    var d60_deity_idx = isOdd ? d60_part : (59 - d60_part);
    var deityName = D60_DEITIES[d60_deity_idx] + " (#" + (d60_deity_idx + 1) + ")";
    addV("D60", 60, d60_sign, (deg * 60.0) % 30.0, deityName);

    return v;
}

function buildAllVargaCharts(sids, ascSid) {
    var order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];
    var ascVargas = calcVargasDetailed(ascSid);
    var planetVargas = {};
    for (var i = 0; i < order.length; i++) {
        var pn = order[i];
        planetVargas[pn] = calcVargasDetailed(sids[pn]);
    }

    var builtCharts = {};
    var shodashaData = {};
    var vKeys = ["D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"];

    for (var vkIdx = 0; vkIdx < vKeys.length; vkIdx++) {
        var vk = vKeys[vkIdx];
        var ascV = ascVargas[vk];
        var aSign = ascV.sign_index;
        var vHouses = {};
        for (var h = 1; h <= 12; h++) {
            vHouses[h] = [String(((aSign + h - 1) % 12) + 1)];
        }

        var pDetails = [];
        for (var pi = 0; pi < order.length; pi++) {
            var pn = order[pi];
            var pv = planetVargas[pn][vk];
            var hNum = ((pv.sign_index - aSign + 12) % 12) + 1;
            var dStr = Math.floor(pv.deg) + "°" + Math.floor((pv.deg * 60) % 60) + "'";
            vHouses[hNum].push(PLANET_NAMES_HI[pn] + (vk === "D1" ? (" " + dStr) : ""));

            pDetails.push({
                planet: PLANET_NAMES_HI[pn],
                sign: SIGNS_HI[pv.sign_index],
                house: hNum,
                degree: dStr + '"',
                deity: pv.deity || ""
            });
        }

        var cKeyLower = vk.toLowerCase();
        var cObj = {
            key: vk,
            title: VARGA_TITLES[vk],
            ascSign: SIGNS_HI[aSign] + " लग्न (" + Math.floor(ascV.deg) + "°" + Math.floor((ascV.deg * 60) % 60) + "')",
            houses: vHouses,
            planetDetails: pDetails
        };

        builtCharts[cKeyLower] = cObj;
        builtCharts[vk] = cObj;
        shodashaData[vk] = cObj;
        shodashaData[cKeyLower] = cObj;
    }

    return { builtCharts, shodashaData };
}

// 1. Test Nikhil Vyas
const nikhilSids = {
    Sun: 217.7139, Moon: 224.6494, Mars: 282.1561, Mercury: 239.2581,
    Jupiter: 259.3522, Venus: 257.7408, Saturn: 206.8822, Rahu: 33.5458, Ketu: 213.5458
};
const resNikhil = buildAllVargaCharts(nikhilSids, 23.7000);
console.log("=== NIKHIL VYAS VARGA CHARTS VERIFICATION ===");
console.log("Charts count:", Object.keys(resNikhil.builtCharts).length);
console.log("D1 Asc:", resNikhil.builtCharts.d1.ascSign, "| House 1:", resNikhil.builtCharts.d1.houses[1]);
console.log("D9 Asc:", resNikhil.builtCharts.d9.ascSign, "| House 1:", resNikhil.builtCharts.d9.houses[1]);
console.log("D10 Asc:", resNikhil.builtCharts.d10.ascSign, "| House 1:", resNikhil.builtCharts.d10.houses[1]);
console.log("D60 Asc:", resNikhil.builtCharts.d60.ascSign, "| House 1:", resNikhil.builtCharts.d60.houses[1]);

// 2. Test General User (Leo Lagna 132.5°)
const userSids = {
    Sun: 55.0, Moon: 120.0, Mars: 200.0, Mercury: 60.0,
    Jupiter: 15.0, Venus: 45.0, Saturn: 340.0, Rahu: 310.0, Ketu: 130.0
};
const resUser = buildAllVargaCharts(userSids, 132.5);
console.log("\n=== GENERAL USER (LEO LAGNA 132.5°) VERIFICATION ===");
console.log("D1 Asc:", resUser.builtCharts.d1.ascSign, "| House 1:", resUser.builtCharts.d1.houses[1]);
console.log("D9 Asc:", resUser.builtCharts.d9.ascSign, "| House 1:", resUser.builtCharts.d9.houses[1]);
console.log("D10 Asc:", resUser.builtCharts.d10.ascSign, "| House 1:", resUser.builtCharts.d10.houses[1]);
console.log("D60 Asc:", resUser.builtCharts.d60.ascSign, "| House 1:", resUser.builtCharts.d60.houses[1]);
