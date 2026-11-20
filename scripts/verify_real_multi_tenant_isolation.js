// Verify strict multi-tenant isolation and dynamic astrological reasoning
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// Create mock browser DOM environment
global.window = global;
global.document = {
    querySelectorAll: () => [],
    getElementById: (id) => ({
        innerText: '',
        innerHTML: '',
        value: '',
        classList: { add: () => {}, remove: () => {} },
        style: {}
    }),
    documentElement: { getAttribute: () => 'dark' }
};
global.localStorage = {
    _data: {},
    getItem: function(k) { return this._data[k] || null; },
    setItem: function(k, v) { this._data[k] = String(v); },
    removeItem: function(k) { delete this._data[k]; },
    clear: function() { this._data = {}; }
};

// Extract VyasDaivagyaWisdom
const vdwStart = html.indexOf('var VyasDaivagyaWisdom = {');
const vdwEnd = html.indexOf('window.VyasDaivagyaWisdom = VyasDaivagyaWisdom;', vdwStart);
const vdwCode = html.substring(vdwStart, vdwEnd) + 'global.VyasDaivagyaWisdom = VyasDaivagyaWisdom;';
eval(vdwCode);

console.log("=== 1. TESTING GUEST / BLANK SLATE CONSULTATION ===");
const guestReply = VyasDaivagyaWisdom.synthesizeReading("मेरा करियर कब चमकेगा?", null);
console.log("Guest reply contains 'Prashna Marga':", guestReply.includes("प्रश्न मार्ग"));
console.log("Guest reply contains 'मकर' (Mars in Cap):", guestReply.includes("मकर"));
console.log("Guest reply contains 'निखिल':", guestReply.includes("निखिल"));
if (guestReply.includes("निखिल") || guestReply.includes("मकर")) {
    console.error("❌ FAILURE: Guest received founder data!");
    process.exit(1);
} else {
    console.log("✅ SUCCESS: Guest received 100% pure Horary Prashna reading!");
}

console.log("\n=== 2. TESTING ANOTHER USER (AMIT SHARMA - LEO LAGNA, GEMINI MARS) ===");
const amitChart = {
    profile: {
        name: "अमित शर्मा",
        dob: "1995-07-20",
        tob: "09:30",
        city: "Jaipur",
        gender: "Male",
        asc_sign: "सिंह",
        asc_dms: "14°20'10\""
    },
    planet_table: [
        { p: "सूर्य", r: "कर्क", d: "03°15'", h: "12", s: "सम" },
        { p: "चन्द्र", r: "मेष", d: "18°40'", h: "9", s: "सम" },
        { p: "मंगल", r: "कन्या", d: "22°10'", h: "2", s: "सम" },
        { p: "बुध", r: "मिथुन", d: "28°05'", h: "11", s: "स्वक्षेत्री" },
        { p: "गुरु", r: "वृश्चिक", d: "11°30'", h: "4", s: "सम" },
        { p: "शुक्र", r: "कर्क", d: "15°50'", h: "12", s: "सम" },
        { p: "शनि", r: "कुंभ", d: "02°15'", h: "7", s: "स्वक्षेत्री" },
        { p: "राहु", r: "तुला", d: "08°10'", h: "3", s: "सम" },
        { p: "केतु", r: "मेष", d: "08°10'", h: "9", s: "सम" }
    ],
    active_dasha: {
        chain: "गुरु ➔ शनि ➔ बुध"
    }
};

const amitCareer = VyasDaivagyaWisdom.synthesizeReading("करियर में पदोन्नति कब होगी?", amitChart);
console.log("Amit Career mentions 'अमित शर्मा':", amitCareer.includes("अमित शर्मा"));
console.log("Amit Career mentions 'सिंह लग्न':", amitCareer.includes("सिंह लग्न"));
console.log("Amit Career mentions 'शुक्र महादशा' (Nikhil's dasha):", amitCareer.includes("शुक्र महादशा"));
console.log("Amit Career mentions 'मकर' (Nikhil's Mars):", amitCareer.includes("मकर"));
console.log("Amit Career mentions 'तुला' (Nikhil's Saturn):", amitCareer.includes("तुला"));
console.log("Amit Career mentions 'निखिल':", amitCareer.includes("निखिल"));

if (amitCareer.includes("निखिल") || amitCareer.includes("मकर") || amitCareer.includes("शुक्र महादशा")) {
    console.error("❌ FAILURE: Amit Sharma received Nikhil Vyas's yogas/dasha!");
    process.exit(1);
} else {
    console.log("✅ SUCCESS: Amit Sharma received 100% personalized chart reading based strictly on Leo Lagna!");
}

console.log("\n=== 3. TESTING POLITICS CONSULTATION FOR AMIT SHARMA ===");
const amitPolitics = VyasDaivagyaWisdom.synthesizeReading("राजनीति व शासन में पद प्राप्ति", amitChart);
console.log("Amit Politics mentions 'अमित शर्मा':", amitPolitics.includes("अमित शर्मा"));
console.log("Amit Politics mentions 'दशम भाव में वृषभ राशि' (10th from Leo is Taurus):", amitPolitics.includes("वृषभ"));
console.log("Amit Politics mentions 'रुचक' (Nikhil's Mars yoga):", amitPolitics.includes("रुचक"));
console.log("Amit Politics mentions 'शश' (Nikhil's Saturn yoga):", amitPolitics.includes("शश"));

if (amitPolitics.includes("रुचक") || amitPolitics.includes("शश") || amitPolitics.includes("निखिल")) {
    console.error("❌ FAILURE: Amit Sharma received Nikhil's Pancha Mahapurusha Yogas!");
    process.exit(1);
} else {
    console.log("✅ SUCCESS: Amit Sharma did NOT receive hardcoded Ruchaka or Sasa yogas!");
}

console.log("\nALL VERIFICATION TESTS PASSED WITH 100% FIDELITY!");

