// scripts/test_all_mobile_tabs.js
const fs = require('fs');
const html = fs.readFileSync('mobile/index.html', 'utf-8');

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
                classes: new Set(),
                add: function(c) { this.classes.add(c); },
                remove: function(c) { this.classes.delete(c); },
                toggle: function(c) { if (this.classes.has(c)) this.classes.delete(c); else this.classes.add(c); },
                contains: function(c) { return this.classes.has(c); }
            },
            querySelectorAll: () => [],
            querySelector: () => null,
            appendChild: () => {},
            closest: () => ({ appendChild: () => {} }),
            getContext: () => ({
                fillRect: () => {},
                beginPath: () => {},
                arc: () => {},
                fill: () => {},
                moveTo: () => {},
                lineTo: () => {},
                stroke: () => {},
                createLinearGradient: () => ({ addColorStop: () => {} })
            }),
            scrollIntoView: () => {},
            getAttribute: (attr) => ''
        };
    }
    return elements[id];
}

const mockDoc = {
    getElementById: (id) => mockElement(id),
    querySelectorAll: (sel) => {
        if (sel === '.tab-view-container') {
            return [mockElement('view-home'), mockElement('view-kundli')];
        }
        if (sel === '.tab-btn') {
            return [mockElement('tb1'), mockElement('tb2')];
        }
        if (sel === '.b-nav-item') {
            return [mockElement('bn1'), mockElement('bn2')];
        }
        return [];
    },
    querySelector: () => null,
    createElement: () => mockElement('created_' + Math.random()),
    documentElement: { setAttribute: () => {}, getAttribute: (attr) => 'dark' },
    addEventListener: () => {}
};

const mockWindow = {
    document: mockDoc,
    navigator: { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)', standalone: false },
    matchMedia: () => ({ matches: false }),
    localStorage: {
        store: {},
        getItem: function(k) { return this.store[k] || null; },
        setItem: function(k, v) { this.store[k] = String(v); },
        removeItem: function(k) { delete this.store[k]; }
    },
    addEventListener: () => {},
    scrollTo: () => {}
};

global.window = mockWindow;
global.document = mockDoc;
global.localStorage = mockWindow.localStorage;
global.AUTHENTIC_BUNDLE = null;
global.requestAnimationFrame = () => {};

// Extract scripts and eval
let VyasMobile = null;
const scriptMatches = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
scriptMatches.forEach((s) => {
    const code = s.replace(/<script[\s\S]*?>/i, '').replace(/<\/script>/i, '');
    if (code.trim()) {
        try {
            eval(code);
            if (typeof VyasMobile !== 'undefined' && VyasMobile) {
                global.VyasMobile = VyasMobile;
                global.window.VyasMobile = VyasMobile;
            }
        } catch (e) {
            console.error("Eval error in script:", e);
        }
    }
});

const tabs = [
    'home', 'kundli', 'shadbala', 'match', 'prashna', 'remedies',
    'sphutas', 'dasha', 'predictions', 'ashtakavarga', 'transit',
    'vargas', 'kp', 'nadi', 'jaimini', 'lalkitab', 'tajika', 'panchang', 'chat', 'pdf'
];

console.log("\n=== TEST 1: ALL MOBILE TABS WITH NULL CHART (BLANK SLATE) ===");
global.VyasMobile.activeChartData = null;
tabs.forEach(tab => {
    try {
        global.VyasMobile.switchTab(tab);
        console.log(`  ✓ Tab '${tab}' switched cleanly (null chart)`);
    } catch (err) {
        console.error(`  ✗ Tab '${tab}' FAILED (null chart):`, err.message);
    }
});

console.log("\n=== TEST 2: ALL MOBILE TABS WITH LOADED AUTHENTIC BUNDLE ===");
global.VyasMobile.activeChartData = global.AUTHENTIC_BUNDLE;
tabs.forEach(tab => {
    try {
        global.VyasMobile.switchTab(tab);
        console.log(`  ✓ Tab '${tab}' switched cleanly (loaded chart)`);
    } catch (err) {
        console.error(`  ✗ Tab '${tab}' FAILED (loaded chart):`, err.message);
    }
});
