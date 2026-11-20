const fs = require('fs');
const vm = require('vm');

// Create mock browser DOM environment
const localStorageData = {};
const mockLocalStorage = {
    getItem: (k) => localStorageData[k] || null,
    setItem: (k, v) => { localStorageData[k] = String(v); },
    removeItem: (k) => { delete localStorageData[k]; },
    clear: () => { Object.keys(localStorageData).forEach(k => delete localStorageData[k]); }
};

const domElements = {};
function createMockEl(id) {
    if (!domElements[id]) {
        domElements[id] = {
            id: id,
            value: '',
            textContent: '',
            innerHTML: '',
            style: {},
            classList: { add: () => { }, remove: () => { }, contains: () => false, toggle: () => { } }
        };
    }
    return domElements[id];
}

const mockDocument = {
    getElementById: (id) => createMockEl(id),
    querySelectorAll: () => [],
    createElement: (tag) => createMockEl('dyn_' + Math.random()),
    addEventListener: () => { }
};

const mockWindow = {
    localStorage: mockLocalStorage,
    document: mockDocument,
    console: console,
    Math: Math,
    Date: Date,
    parseInt: parseInt,
    parseFloat: parseFloat,
    isNaN: isNaN,
    alert: (msg) => { mockWindow._lastAlert = msg; },
    confirm: () => true
};

mockWindow.window = mockWindow;
mockWindow.global = mockWindow;

const html = fs.readFileSync('index.html', 'utf8');

// Extract Script #4
const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
let script4Code = '';

while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    if (count === 4) {
        script4Code = match[2];
        break;
    }
}

const ctx = vm.createContext(mockWindow);
vm.runInContext(script4Code, ctx);

console.log("=== RUNNING RIGOROUS TEST SUITE FOR ALL 6 ISSUES ===");

// TEST 1: TOB PARSING & MESHA LAGNA FOR NIKHIL VYAS
console.log("\n--- TEST 1: TOB Parsing & Mesha Lagna for Nikhil Vyas ---");
const VyasDesktop = mockWindow.VyasDesktop;
if (!VyasDesktop) throw new Error("VyasDesktop not defined!");

// Case 1A: 04:51 PM
const chart1A = VyasDesktop.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "04:51 PM", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Input: '04:51 PM' -> Asc Sign:", chart1A.profile.asc_sign, "DMS:", chart1A.profile.asc_dms);
if (chart1A.profile.asc_sign !== "मेष" || !chart1A.profile.asc_dms.includes("23°42")) {
    throw new Error(`FAIL: Expected Mesha Lagna 23°42' for 04:51 PM, got ${chart1A.profile.asc_sign} ${chart1A.profile.asc_dms}`);
}
console.log("✓ PASSED: '04:51 PM' yields Mesha Lagna (23°42'00\")");

// Case 1B: 16:51
const chart1B = VyasDesktop.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Input: '16:51' -> Asc Sign:", chart1B.profile.asc_sign, "DMS:", chart1B.profile.asc_dms);
if (chart1B.profile.asc_sign !== "मेष" || !chart1B.profile.asc_dms.includes("23°42")) {
    throw new Error(`FAIL: Expected Mesha Lagna 23°42' for 16:51, got ${chart1B.profile.asc_sign} ${chart1B.profile.asc_dms}`);
}
console.log("✓ PASSED: '16:51' yields Mesha Lagna (23°42'00\")");

// Case 1C: 4:51 pm (lowercase, no leading zero)
const chart1C = VyasDesktop.computeMathematicalKundli("NIKHIL VYAS", "1984-11-23", "4:51 pm", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Input: '4:51 pm' -> Asc Sign:", chart1C.profile.asc_sign, "DMS:", chart1C.profile.asc_dms);
if (chart1C.profile.asc_sign !== "मेष" || !chart1C.profile.asc_dms.includes("23°42")) {
    throw new Error(`FAIL: Expected Mesha Lagna 23°42' for 4:51 pm, got ${chart1C.profile.asc_sign} ${chart1C.profile.asc_dms}`);
}
console.log("✓ PASSED: '4:51 pm' yields Mesha Lagna (23°42'00\")");

// TEST 2: AUTO-HEAL OF STALE KANYA LAGNA WHEN NIKHIL LOGS IN
console.log("\n--- TEST 2: Auto-Heal of Stale Kanya Lagna Cache ---");
// Authenticate Nikhil
VyasDesktop.googleUser = { name: "NIKHIL VYAS", email: "nikhilvyas007@gmail.com" };
// Simulate corrupted cache in localStorage
mockLocalStorage.setItem('vyas_active_profile', JSON.stringify({
    profile: {
        name: "NIKHIL VYAS",
        dob: "1984-11-23",
        tob: "04:51 PM",
        city: "Falna",
        asc_sign: "कन्या",
        asc_dms: "26°55'52\""
    }
}));
mockLocalStorage.setItem('vyas_engine_version', 'v5.0_pure_math_parashari_2026');
VyasDesktop.loadStoredProfile();
const healedAct = JSON.parse(mockLocalStorage.getItem('vyas_active_profile'));
console.log("Healed Profile Asc Sign:", healedAct.profile.asc_sign, "DMS:", healedAct.profile.asc_dms);
if (healedAct.profile.asc_sign !== "मेष" || !healedAct.profile.asc_dms.includes("23°42")) {
    throw new Error(`FAIL: Auto-heal failed to restore Mesha Lagna 23°42'`);
}
console.log("✓ PASSED: Stale Kanya Lagna cache automatically rectified to Mesha Lagna 23°42'00\"");

// TEST 3: UNIFIED KUNDLI VAULT & SYNC COUNT
console.log("\n--- TEST 3: Dynamic Vault Count in syncCloudProfiles ---");
// Setup user with 2 saved charts
VyasDesktop.googleUser = { name: "Nikhil Vyas", email: "nikhilvyas007@gmail.com" };
mockLocalStorage.setItem('vyas_custom_profiles', JSON.stringify([
    { name: "Family Member 1", dob: "1990-01-01", tob: "10:00", city: "Jaipur" },
    { name: "Family Member 2", dob: "1992-05-15", tob: "14:30", city: "Jodhpur" }
]));
const list = VyasDesktop.getUserProfilesList();
console.log("Total aggregated profiles in vault:", list.length);
VyasDesktop.syncCloudProfiles();
console.log("Sync alert output:\n" + mockWindow._lastAlert);
if (!mockWindow._lastAlert.includes(`कुल सुरक्षित चार्ट: ${list.length}`)) {
    throw new Error(`FAIL: syncCloudProfiles alert did not display dynamic count ${list.length}`);
}
if (mockWindow._lastAlert.includes("कुल सुरक्षित चार्ट: 4") && list.length !== 4) {
    throw new Error(`FAIL: syncCloudProfiles still has hardcoded 4!`);
}
console.log("✓ PASSED: Dynamic profile count correctly calculated and displayed");

// TEST 4: DYNAMIC PLANET INSPECTOR
console.log("\n--- TEST 4: Dynamic Planet Inspector ---");
// Set an active chart with unique degrees
VyasDesktop.activeChartData = {
    profile: { name: "Test Native", asc_sign: "सिंह" },
    planet_table: [
        { p: "सूर्य (Sun)", r: "मेष", d: "14°20'10\"", n: "Bharani (1)", h: "9", s: "उच्च" },
        { p: "चन्द्र (Moon)", r: "कर्क", d: "05°12'30\"", n: "Pushya (1)", h: "12", s: "स्वक्षेत्री" }
    ]
};
VyasDesktop.inspectPlanet("Moon");
const piBody = domElements['piModalBody'].innerHTML;
console.log("Planet Inspector HTML for Moon snippet:", piBody.substring(0, 200));
if (!piBody.includes("05°12'30\"") || !piBody.includes("कर्क") || !piBody.includes("Pushya")) {
    throw new Error("FAIL: Planet inspector did not use active chart's dynamic data!");
}
if (piBody.includes("Anuradha") || piBody.includes("Scorpio")) {
    throw new Error("FAIL: Planet inspector still leaked hardcoded Scorpio/Anuradha Moon!");
}
console.log("✓ PASSED: Planet Inspector extracts 100% dynamic data from active chart");

// TEST 5: DYNAMIC TARA BALA & CELESTIAL SIGN
console.log("\n--- TEST 5: Dynamic Tara Bala & Celestial Sign ---");
VyasDesktop.activeChartData = {
    profile: { name: "Test Native", asc_sign: "सिंह" },
    planet_table: [
        { p: "चन्द्र (Moon)", r: "कर्क", d: "05°12'30\"", n: "पुष्य (1)", h: "12", s: "स्वक्षेत्री" }
    ]
};
VyasDesktop.updateDailyHoroscopeUI();
const taraVal = domElements['vTodayTaraVal'].textContent;
console.log("Computed Tara for Pushya Moon:", taraVal);
if (!taraVal || taraVal.includes("अज्ञात")) {
    throw new Error("FAIL: Dynamic Tara computation failed!");
}
console.log("✓ PASSED: Dynamic Tara computed successfully without Anuradha default");

// TEST 6: MULTI-TENANT ISOLATION - GUEST GETS BLANK / GUEST CHART
console.log("\n--- TEST 6: Strict Multi-Tenant Guest Isolation ---");
VyasDesktop.googleUser = null; // Guest user
VyasDesktop.loadStoredProfile();
console.log("Guest Active Chart:", VyasDesktop.activeChartData ? VyasDesktop.activeChartData.profile.name : "None (Clean slate)");
if (VyasDesktop.activeChartData && VyasDesktop.activeChartData.profile.dob === '1984-11-23') {
    throw new Error("FAIL: Multi-tenant breach! Guest loaded Nikhil's birth chart!");
}
console.log("✓ PASSED: Guest session is completely isolated from Nikhil Vyas's chart");

console.log("\n=======================================================");
console.log("ALL VERIFICATION TESTS PASSED WITH 100% ZERO ERRORS!");
console.log("=======================================================");
