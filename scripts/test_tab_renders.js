// scripts/test_tab_renders.js
const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf-8');

const elements = {};
function mockElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            innerText: '',
            value: '',
            style: {},
            classList: {
                add: (c) => { elements[id].classes = elements[id].classes || new Set(); elements[id].classes.add(c); },
                remove: (c) => { if (elements[id].classes) elements[id].classes.delete(c); },
                toggle: () => {},
                contains: (c) => elements[id].classes ? elements[id].classes.has(c) : false
            },
            querySelectorAll: () => [],
            querySelector: () => null,
            appendChild: () => {},
            scrollTop: 0,
            scrollHeight: 100
        };
    }
    return elements[id];
}

const mockDoc = {
    getElementById: (id) => mockElement(id),
    querySelectorAll: (sel) => {
        if (sel === '.tab-nav-btn') return [mockElement('tab1'), mockElement('tab2')];
        if (sel === '.view-panel') return [mockElement('p1'), mockElement('p2')];
        return [];
    },
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

const tabs = ['daily', 'dasha', 'predictions', 'ashtakavarga', 'shadbala', 'match', 'prashna', 'remedies', 'sphutas', 'transit', 'vargas', 'kp', 'jaimini', 'nadi', 'pdf'];

console.log("=== TEST 1: Testing all 15 tabs with NULL activeChartData ===");
VyasDesktop.activeChartData = null;
for (const t of tabs) {
    try {
        VyasDesktop.switchTab(t, mockElement('btn_' + t));
        console.log(`  ✓ Tab '${t}' switched cleanly (null chart)`);
    } catch (e) {
        console.error(`  ❌ ERROR switching tab '${t}' (null chart):`, e.message);
    }
}

console.log("\n=== TEST 2: Testing all 15 tabs with LOADED activeChartData ===");
VyasDesktop.activeChartData = VyasDesktop.computeMathematicalKundli("परीक्षण जातक", "1992-04-14", "08:15", "Jaipur", "Male");
for (const t of tabs) {
    try {
        VyasDesktop.switchTab(t, mockElement('btn_' + t));
        console.log(`  ✓ Tab '${t}' switched cleanly (loaded chart)`);
    } catch (e) {
        console.error(`  ❌ ERROR switching tab '${t}' (loaded chart):`, e.message);
    }
}

