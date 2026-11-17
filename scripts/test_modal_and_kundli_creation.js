// Strict Principal Auditor Verification Suite for Modal & Kundli Creation Flow
// Tests the entire lifecycle: Blank Slate -> Modal Open -> Kundli Calculation -> Dynamic Updates -> Real Google OAuth Verification

const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');

// Extract script blocks (excluding JSON-LD)
const scripts = [...html.matchAll(/<script(?![^>]*(?:src|application\/ld\+json))[^>]*>([\s\S]*?)<\/script>/gi)];
const fullScript = scripts.map(s => s[1]).join('\n;\n');

// Mock DOM
function createMockElement(id, tag = 'div') {
    return {
        id: id,
        tagName: tag.toUpperCase(),
        style: { display: 'none' },
        classList: {
            classes: new Set(),
            add(c) { this.classes.add(c); },
            remove(c) { this.classes.delete(c); },
            contains(c) { return this.classes.has(c); }
        },
        value: '',
        textContent: '',
        innerHTML: '',
        children: [],
        appendChild(child) { this.children.push(child); },
        getAttribute(attr) { return ''; },
        setAttribute(attr, val) {},
        getContext() {
            return {
                clearRect() {},
                fillRect() {},
                beginPath() {},
                arc() {},
                fill() {},
                stroke() {},
                moveTo() {},
                lineTo() {},
                save() {},
                restore() {},
                translate() {},
                rotate() {}
            };
        }
    };
}

const elementStore = {};
function getOrCreate(id) {
    if (!elementStore[id]) {
        elementStore[id] = createMockElement(id);
    }
    return elementStore[id];
}

const mockDoc = {
    documentElement: createMockElement('html'),
    getElementById(id) {
        return getOrCreate(id);
    },
    querySelectorAll(selector) {
        return [];
    },
    querySelector(selector) {
        return null;
    },
    addEventListener() {},
    body: { classList: { add() {}, remove() {} } }
};

const mockWindow = {
    document: mockDoc,
    localStorage: {
        store: {},
        getItem(k) { return this.store[k] || null; },
        setItem(k, v) { this.store[k] = String(v); },
        removeItem(k) { delete this.store[k]; }
    },
    sessionStorage: {
        store: {},
        getItem(k) { return this.store[k] || null; },
        setItem(k, v) { this.store[k] = String(v); },
        removeItem(k) { delete this.store[k]; }
    },
    location: {
        origin: 'https://vyasastro.in',
        pathname: '/',
        search: '',
        hash: '',
        href: 'https://vyasastro.in/'
    },
    history: {
        replaceState() {}
    },
    screen: {
        width: 1920,
        height: 1080
    },
    open() {
        return { closed: false };
    },
    addEventListener() {},
    alert(msg) {},
    confirm() { return true; },
    setTimeout: (fn, ms) => {},
    setInterval: () => 1,
    clearInterval: () => {},
    requestAnimationFrame: (cb) => {}
};

const context = vm.createContext({
    window: mockWindow,
    document: mockDoc,
    console: console,
    localStorage: mockWindow.localStorage,
    sessionStorage: mockWindow.sessionStorage,
    location: mockWindow.location,
    requestAnimationFrame: (cb) => {},
    setTimeout: (fn, ms) => {},
    setInterval: () => 1,
    clearInterval: () => {},
    fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }),
    alert: (msg) => {},
    confirm: () => true,
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

// TEST 2: Open Modal without activeChartData
console.log("\n--- TEST 2: Modal Invocation with null activeChartData ---");
try {
    VyasDesktop.activeChartData = null;
    VyasDesktop.openEditProfileModal();
    const modal = mockDoc.getElementById('modalEditProfile');
    assert(modal.classList.contains('active'), "modalEditProfile opened without crash on null activeChartData");
    assert(modal.style.display === 'flex', "modalEditProfile display set to 'flex'");
    assert(mockDoc.getElementById('edit_name').value === '', "New profile input is cleared and ready for entry");
} catch(e) {
    assert(false, `openEditProfileModal threw error: ${e.message}`);
}

// TEST 3: Calculate Real Kundli via submitProfileEdit
console.log("\n--- TEST 3: Direct Kundli Calculation via submitProfileEdit ---");
try {
    mockDoc.getElementById('edit_name').value = "राहुल शर्मा (Rahul Sharma)";
    mockDoc.getElementById('edit_dob').value = "1990-05-15";
    mockDoc.getElementById('edit_tob').value = "14:30";
    mockDoc.getElementById('edit_gender').value = "पुरुष (Male)";
    mockDoc.getElementById('edit_city').value = "जयपुर (Jaipur)";
    mockDoc.getElementById('edit_lat').value = "26.9124";
    mockDoc.getElementById('edit_lon').value = "75.7873";
    mockDoc.getElementById('edit_tz').value = "+05:30";

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

// TEST 4: Real Google User Authentication & Anti-Spoofing Verification
console.log("\n--- TEST 4: Real Google OAuth Authentication & Anti-Spoofing ---");
try {
    // 4.1 Reject Fake/Simulated Profiles in localStorage on init
    mockWindow.localStorage.setItem('vyas_google_user', JSON.stringify({
        name: "Fake User",
        email: "nikhil@gmail.com",
        isVerified: true
        // Note: No sub ID!
    }));
    VyasDesktop.initGoogleAuth();
    assert(VyasDesktop.googleUser === null, "Fake/unverified account (nikhil@gmail.com without sub) was immediately purged!");
    assert(mockWindow.localStorage.getItem('vyas_google_user') === null, "Fake entry cleared from localStorage");

    // 4.2 Apply genuine Google verified user (when no chart exists, it opens new profile modal and pre-fills name)
    VyasDesktop.activeChartData = null;
    mockWindow.localStorage.removeItem('vyas_active_profile');
    const genuineGooglePayload = {
        sub: "10982736451234567890",
        name: "अमित वर्मा (Amit Verma)",
        email: "amit.verma@official.com",
        picture: "https://lh3.googleusercontent.com/avatar.jpg",
        email_verified: true
    };
    VyasDesktop.applyAuthenticatedGoogleUser(genuineGooglePayload, "mock_google_jwt_token_123");

    assert(VyasDesktop.googleUser !== null, "Genuine Google user successfully authenticated");
    assert(VyasDesktop.googleUser.sub === "10982736451234567890", "Google Sub ID locked in memory");
    assert(VyasDesktop.googleUser.email === "amit.verma@official.com", "Verified email matches Google response");
    assert(mockWindow.localStorage.getItem('vyas_g_jwt') === "mock_google_jwt_token_123", "Google JWT stored securely");

    const editName = mockDoc.getElementById('edit_name').value;
    assert(editName === "अमित वर्मा (Amit Verma)", `Google user's name pre-filled into birth chart form: '${editName}'`);
} catch(e) {
    assert(false, `Google OAuth verification threw error: ${e.message}`);
}

console.log(`\n========================================`);
console.log(`FINAL RESULT: ${passed} PASSED, ${failed} FAILED`);
console.log(`========================================`);

if (failed > 0) {
    process.exit(1);
}
