// scripts/test_day_index_tara.js
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');

const elements = {};
function mockElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            textContent: '',
            innerText: '',
            style: {}
        };
    }
    return elements[id];
}

const mockDoc = {
    getElementById: (id) => mockElement(id),
    querySelectorAll: () => [],
    querySelector: () => null,
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

const desktopStart = html.indexOf('var VyasDesktop = {');
const desktopEnd = html.indexOf("document.addEventListener('DOMContentLoaded'", desktopStart);
const desktopScript = html.substring(desktopStart, desktopEnd);

const helperDefs = `
    var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
    var LORDS_HI = { "मेष": "मंगल", "वृषभ": "शुक्र", "मिथुन": "बुध", "कर्क": "चन्द्रमा", "सिंह": "सूर्य", "कन्या": "बुध", "तुला": "शुक्र", "वृश्चिक": "मंगल", "धनु": "गुरु", "मकर": "शनि", "कुंभ": "शनि", "मीन": "गुरु" };
    var AUTHENTIC_BUNDLE = { planet_table: [] };
`;

const runDesktop = new Function('window', 'document', 'Date', 'Math', 'console', helperDefs + desktopScript + '; return VyasDesktop;');
const VyasDesktop = runDesktop(mockWindow, mockDoc, Date, Math, console);

console.log("=== SCENARIO 1: Incognito / No Kundli Loaded ===");
VyasDesktop.activeChartData = null;
VyasDesktop.updateDailyHoroscopeUI();

console.log("Day Index Value:", elements['vIndexVal'].textContent);
console.log("Day Index Sub:", elements['vIndexSub'].textContent);
console.log("Today's Tara:", elements['vTodayTaraVal'].textContent);
console.log("Tara Description:", elements['vTodayTaraDesc'].textContent);
console.log("Heading:", elements['personalizedDailyHeading'].innerHTML);

if (elements['vIndexVal'].textContent === '--' && 
    elements['vIndexSub'].textContent === 'कुण्डली आवश्यक' && 
    elements['vTodayTaraVal'].textContent.includes('अज्ञात')) {
    console.log(">>> PASS: Incognito shows clean blank slate without leaking Sadhak Tara!");
} else {
    console.error(">>> FAIL: Incognito leaked Tara data!");
    process.exit(1);
}

console.log("\n=== SCENARIO 2: Kundli Loaded (e.g. Rohini Moon native) ===");
// Native born in Rohini (Moon in Taurus ~15 deg)
const chartData = VyasDesktop.computeMathematicalKundli("रोहिणी जातक", "1995-05-20", "14:30", "Delhi", "Male");
VyasDesktop.activeChartData = chartData;
VyasDesktop.updateDailyHoroscopeUI();

console.log("Day Index Value:", elements['vIndexVal'].textContent);
console.log("Day Index Sub:", elements['vIndexSub'].textContent);
console.log("Today's Tara:", elements['vTodayTaraVal'].textContent);
console.log("Tara Description:", elements['vTodayTaraDesc'].textContent);
console.log("Heading:", elements['personalizedDailyHeading'].innerHTML);

if (elements['vIndexVal'].textContent !== '--' && 
    !elements['vTodayTaraVal'].textContent.includes('अज्ञात')) {
    console.log(">>> PASS: Loaded chart calculates real dynamic Day Index and real Navatara!");
} else {
    console.error(">>> FAIL: Loaded chart did not compute dynamic Day Index or Navatara!");
    process.exit(1);
}

