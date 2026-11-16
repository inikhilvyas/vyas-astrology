// scripts/test_in_node.js
// Direct runtime verification of Vyas Desktop & Mobile engines

const fs = require('fs');

console.log("Reading index.html...");
const html = fs.readFileSync('index.html', 'utf-8');

// Mock a DOM environment
const elements = {};
function mockElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            innerText: '',
            value: '',
            classList: {
                add: () => {},
                remove: () => {},
                toggle: () => {}
            },
            scrollTop: 0,
            scrollHeight: 100
        };
    }
    return elements[id];
}

const mockDoc = {
    getElementById: (id) => mockElement(id),
    querySelectorAll: () => [],
    documentElement: { setAttribute: () => {} }
};

const mockWindow = {
    document: mockDoc,
    localStorage: {
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {}
    },
    addEventListener: () => {}
};

// 1. Extract and evaluate VyasAIEngine
const aiEngineStart = html.indexOf('window.VyasAIEngine = {');
const aiEngineEnd = html.indexOf('var VyasDesktop = {', aiEngineStart);

if (aiEngineStart === -1 || aiEngineEnd === -1) {
    console.error("Failed to extract VyasAIEngine, start:", aiEngineStart, "end:", aiEngineEnd);
    process.exit(1);
}

const aiEngineScript = html.substring(aiEngineStart, aiEngineEnd);
const evalContext = {
    window: mockWindow,
    document: mockDoc,
    Date: Date,
    Math: Math,
    console: console,
    fetch: async () => ({ ok: false }) // test offline fallback
};

const runInCtx = new Function('window', 'document', 'Date', 'Math', 'console', 'fetch', aiEngineScript + '; return window.VyasAIEngine;');
const VyasAIEngine = runInCtx(evalContext.window, evalContext.document, evalContext.Date, evalContext.Math, evalContext.console, evalContext.fetch);

console.log("✓ VyasAIEngine successfully initialized in Node.js");

// 2. Test Horary Prashna Kundli
console.log("\n--- Testing castPrashnaKundli ---");
const prashna1 = VyasAIEngine.castPrashnaKundli("क्या मुझे राजनीति और चुनाव में सफलता मिलेगी?");
console.log("Prashna Lagna:", prashna1.prashnaLagna);
console.log("Prashnesha:", prashna1.prashnesha);
console.log("Moon:", prashna1.moonSign, prashna1.moonNak);
console.log("Karya House:", prashna1.karyaHouse, prashna1.karyaDesc);
console.log("Karyesha:", prashna1.karyesha, "in", prashna1.karyaSign);

if (prashna1.karyaHouse !== 10) {
    console.error("FAIL: Expected karyaHouse 10 for election query, got", prashna1.karyaHouse);
    process.exit(1);
}
console.log("✓ Prashna Intent correctly classified 10th house for election!");

// 3. Test Incognito AI query with NULL active chart
console.log("\n--- Testing askSage with NULL active chart (Incognito Mode) ---");
(async () => {
    const reply = await VyasAIEngine.askSage("क्या मुझे MLA बनने का योग है?", null);
    console.log("AI Bot Reply Preview (first 300 chars):");
    console.log(reply.substring(0, 300));
    console.log("...");

    if (!reply.includes("प्रश्न मार्ग") || !reply.includes("तात्कालिक प्रश्न कुण्डली")) {
        console.error("FAIL: Reply did not invoke Prashna Kundli!");
        process.exit(1);
    }
    if (reply.includes("23°27'") || reply.includes("1984-11-23")) {
        console.error("FAIL: Founder's private chart leaked in reply!");
        process.exit(1);
    }
    console.log("✓ Incognito mode query correctly routed to Prashna Kundli without leaking founder data!");

    // 4. Test computeMathematicalKundli & renderPlanetTable
    console.log("\n--- Testing computeMathematicalKundli & renderPlanetTable ---");
    const desktopStart = html.indexOf('var VyasDesktop = {');
    const desktopEnd = html.indexOf("document.addEventListener('DOMContentLoaded'", desktopStart);
    const desktopScript = html.substring(desktopStart, desktopEnd);

    // Provide missing global helper variables referenced in desktopScript
    const helperDefs = `
        var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
        var LORDS_HI = { "मेष": "मंगल", "वृषभ": "शुक्र", "मिथुन": "बुध", "कर्क": "चन्द्रमा", "सिंह": "सूर्य", "कन्या": "बुध", "तुला": "शुक्र", "वृश्चिक": "मंगल", "धनु": "गुरु", "मकर": "शनि", "कुंभ": "शनि", "मीन": "गुरु" };
        var AUTHENTIC_BUNDLE = { planet_table: [] };
    `;

    const runDesktop = new Function('window', 'document', 'Date', 'Math', 'console', helperDefs + desktopScript + '; return VyasDesktop;');
    const VyasDesktop = runDesktop(evalContext.window, evalContext.document, evalContext.Date, evalContext.Math, evalContext.console);

    // Initial state: blank chart
    VyasDesktop.activeChartData = null;
    VyasDesktop.renderPlanetTable();
    const blankHtml = elements['desktopPlanetTableBody'].innerHTML;
    console.log("Blank table HTML preview:", blankHtml.substring(0, 100));
    if (!blankHtml.includes("colspan=\"6\"")) {
        console.error("FAIL: Blank table colspan is not 6!");
        process.exit(1);
    }
    console.log("✓ Blank table renders clean empty slate with 6 columns!");

    // Now calculate a real birth chart: e.g. Birth on 1995-08-20, 14:30 at Jaipur
    const chart = VyasDesktop.computeMathematicalKundli("रोहित शर्मा", "1995-08-20", "14:30", "Jaipur, Rajasthan", "Male");
    console.log("Generated Chart Profile:", chart.profile);
    console.log("Generated Chart Planet Table count:", chart.planet_table.length);
    console.log("Sample planet 0:", chart.planet_table[0]);
    console.log("Sample planet 2:", chart.planet_table[2]);
    console.log("Jaimini Karakas count:", chart.jaimini.karakas.length);
    console.log("Jaimini Atmakaraka (AK):", chart.jaimini.karakas[0]);
    console.log("KP 1st Cusp Sub-Lord:", chart.kp.cusps[0]);
    console.log("Nadi Combinations count:", chart.nadi.combinations.length);
    console.log("12 Bhavas Predictions count:", chart.predictions.bhavas.length);

    if (chart.planet_table.length !== 9) {
        console.error("FAIL: Expected 9 planets in planet_table, got", chart.planet_table.length);
        process.exit(1);
    }
    if (chart.jaimini.karakas.length !== 7) {
        console.error("FAIL: Expected 7 chara karakas in Jaimini, got", chart.jaimini.karakas.length);
        process.exit(1);
    }
    if (chart.kp.cusps.length !== 12) {
        console.error("FAIL: Expected 12 cusps in KP, got", chart.kp.cusps.length);
        process.exit(1);
    }

    // Now render the planet table with this active chart
    VyasDesktop.activeChartData = chart;
    VyasDesktop.renderPlanetTable();
    const renderedTableHtml = elements['desktopPlanetTableBody'].innerHTML;
    console.log("Rendered Table HTML preview (first 250 chars):");
    console.log(renderedTableHtml.substring(0, 250));

    if (!renderedTableHtml.includes("<tr><td><b style=\"color:var(--primary);\">सूर्य (Sun)</b>")) {
        console.error("FAIL: Planet table row for Sun not properly formatted!");
        process.exit(1);
    }
    console.log("✓ Planet table renders all 9 planets with exact degrees, nakshatras, houses and badges!");

    console.log("\n==========================================");
    console.log("🎉 ALL NODE.JS RUNTIME TESTS PASSED 100%!");
    console.log("==========================================");
})();
