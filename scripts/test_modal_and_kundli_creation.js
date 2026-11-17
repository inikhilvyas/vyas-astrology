// scripts/test_modal_and_kundli_creation.js
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf-8');

const elements = {};
function mockElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            innerText: '',
            textContent: '',
            value: '',
            style: {
                setProperty: function(k, v) { this[k] = v; }
            },
            classList: {
                classes: new Set(),
                add: function(c) { this.classes.add(c); },
                remove: function(c) { this.classes.delete(c); },
                contains: function(c) { return this.classes.has(c); }
            },
            querySelectorAll: () => [],
            querySelector: () => mockElement('sub_' + id),
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
        if (sel === '.modal-overlay') return [mockElement('modalEditProfile'), mockElement('modalGoogleAuth')];
        if (sel === '.tab-nav-btn') return [mockElement('tab1'), mockElement('tab2')];
        if (sel === '.view-panel') return [mockElement('p1'), mockElement('p2')];
        if (sel === '.vchip') return [mockElement('vc1')];
        return [];
    },
    querySelector: (sel) => mockElement('query_' + sel),
    addEventListener: () => {},
    documentElement: { 
        setAttribute: () => {},
        getAttribute: () => 'dark'
    }
};

const storage = {};
const mockWindow = {
    document: mockDoc,
    localStorage: {
        getItem: (k) => storage[k] || null,
        setItem: (k, v) => { storage[k] = String(v); },
        removeItem: (k) => { delete storage[k]; }
    },
    alert: (msg) => { /* quiet alert in test */ },
    addEventListener: () => {},
    Date: Date,
    Math: Math
};

// Extract main VyasDesktop script
const scriptRegex = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let fullScript = '';
while ((match = scriptRegex.exec(html)) !== null) {
    if (match[1].includes('VyasDesktop = {')) {
        fullScript = match[1];
        break;
    }
}

if (!fullScript) {
    console.error("Could not find VyasDesktop script in index.html");
    process.exit(1);
}

const context = vm.createContext({
    window: mockWindow,
    document: mockDoc,
    localStorage: mockWindow.localStorage,
    alert: mockWindow.alert,
    console: console,
    setTimeout: (fn) => { try { fn(); } catch(e){} },
    clearTimeout: () => {},
    Date: Date,
    Math: Math,
    parseInt: parseInt,
    parseFloat: parseFloat,
    isNaN: isNaN,
    String: String
});

vm.runInContext(fullScript, context);
const VyasDesktop = context.VyasDesktop || mockWindow.VyasDesktop;

console.log("=== STRICT PRINCIPAL AUDITOR TEST SUITE ===");
let passed = 0;
let failed = 0;

function assert(condition, testName) {
    if (condition) {
        console.log(`[PASS] ${testName}`);
        passed++;
    } else {
        console.error(`[FAIL] ${testName}`);
        failed++;
    }
}

// TEST 1: Blank Slate Verification
console.log("\n--- TEST 1: Blank Slate & Daily Horoscope Protection ---");
VyasDesktop.activeChartData = null;
VyasDesktop.updateDailyHoroscopeUI();

const vVal = mockDoc.getElementById('vIndexVal').textContent;
assert(vVal === '--', `Day Index is '--' (got '${vVal}')`);

const vSub = mockDoc.getElementById('vIndexSub').textContent;
assert(vSub === 'कुण्डली आवश्यक', `Day Index Sub is 'कुण्डली आवश्यक' (got '${vSub}')`);

const taraDesc = mockDoc.getElementById('vTodayTaraDesc').textContent;
assert(taraDesc.includes('+ नई कुण्डली'), `Tara prompt guides to '+ नई कुण्डली' (got '${taraDesc}')`);

const dhWealth = mockDoc.getElementById('dhWealthText').textContent;
assert(dhWealth.includes('जन्म कुण्डली बनाएं'), `dhWealthText is blank slate protected (got '${dhWealth}')`);

const dhCareer = mockDoc.getElementById('dhCareerText').textContent;
assert(dhCareer.includes('जन्म कुण्डली बनाएं'), `dhCareerText is blank slate protected (got '${dhCareer}')`);

const dhRelations = mockDoc.getElementById('dhRelationsText').textContent;
assert(dhRelations.includes('जन्म कुण्डली बनाएं'), `dhRelationsText is blank slate protected (got '${dhRelations}')`);

const dhHealth = mockDoc.getElementById('dhHealthText').textContent;
assert(dhHealth.includes('जन्म कुण्डली बनाएं'), `dhHealthText is blank slate protected (got '${dhHealth}')`);

// TEST 2: Open New Profile Modal & Edit Profile Modal without crashes
console.log("\n--- TEST 2: Modal Invocation with null activeChartData ---");
try {
    VyasDesktop.openEditProfileModal();
    const editModal = mockDoc.getElementById('modalEditProfile');
    assert(editModal.classList.contains('active'), "modalEditProfile opened without crash on null activeChartData");
    assert(editModal.style.display === 'flex', "modalEditProfile display set to 'flex'");
} catch(e) {
    assert(false, `openEditProfileModal threw error: ${e.message}`);
}

try {
    VyasDesktop.openNewProfileModal();
    const nameEl = mockDoc.getElementById('edit_name');
    assert(nameEl.value === "", "New profile input is cleared and ready for entry");
} catch(e) {
    assert(false, `openNewProfileModal threw error: ${e.message}`);
}

// TEST 3: Direct Kundli Calculation & Creation
console.log("\n--- TEST 3: Direct Kundli Calculation via submitProfileEdit ---");
try {
    mockDoc.getElementById('edit_name').value = "राहुल शर्मा (Rahul Sharma)";
    mockDoc.getElementById('edit_dob').value = "1994-06-18";
    mockDoc.getElementById('edit_tob').value = "14:30";
    mockDoc.getElementById('edit_city').value = "Jaipur, Rajasthan";
    mockDoc.getElementById('edit_gender').value = "Male";

    VyasDesktop.submitProfileEdit();

    const chart = VyasDesktop.activeChartData;
    assert(chart !== null, "activeChartData successfully populated by mathematical calculation");
    assert(chart.profile.name === "राहुल शर्मा (Rahul Sharma)", `Profile name saved: ${chart.profile.name}`);
    assert(chart.profile.asc_sign.length > 0, `Lagna sign computed: ${chart.profile.asc_sign}`);
    assert(chart.planet_table.length === 9, `9 sidereal planets calculated: ${chart.planet_table.length}`);

    // Check dynamic Daily Horoscope update
    const updatedVVal = mockDoc.getElementById('vIndexVal').textContent;
    assert(updatedVVal !== '--', `Day Index updated dynamically to score: ${updatedVVal}`);

    const updatedTara = mockDoc.getElementById('vTodayTaraVal').textContent;
    assert(!updatedTara.includes('अज्ञात'), `Tara Insight updated dynamically: ${updatedTara}`);

    const updatedCareer = mockDoc.getElementById('dhCareerText').textContent;
    assert(!updatedCareer.includes('जन्म कुण्डली बनाएं'), `Career forecast is authentic transit text: ${updatedCareer.substring(0, 40)}...`);

    const updatedWealth = mockDoc.getElementById('dhWealthText').textContent;
    assert(!updatedWealth.includes('जन्म कुण्डली बनाएं'), `Wealth forecast is authentic transit text: ${updatedWealth.substring(0, 40)}...`);
} catch(e) {
    assert(false, `submitProfileEdit threw error: ${e.message}`);
}

// TEST 4: Google Sign-in Workflow
console.log("\n--- TEST 4: Google Sign-in Transition ---");
try {
    VyasDesktop.activeChartData = null;
    mockWindow.localStorage.removeItem('vyas_active_profile');
    mockDoc.getElementById('customGoogleName').value = "अमित वर्मा (Amit Verma)";
    mockDoc.getElementById('customGoogleEmail').value = "amit.verma@gmail.com";

    VyasDesktop.signInCustomProfile();

    assert(VyasDesktop.googleUser !== null, "Google user recorded in memory");
    assert(VyasDesktop.googleUser.email === "amit.verma@gmail.com", "Google email matches input");

    const editName = mockDoc.getElementById('edit_name').value;
    assert(editName === "अमित वर्मा (Amit Verma)", `Google user's name pre-filled into birth chart form: '${editName}'`);
} catch(e) {
    assert(false, `signInCustomProfile threw error: ${e.message}`);
}

console.log(`\n========================================`);
console.log(`FINAL RESULT: ${passed} PASSED, ${failed} FAILED`);
console.log(`========================================`);

if (failed > 0) {
    process.exit(1);
}
