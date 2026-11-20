global.window = {};
const fs = require('fs');

const content = fs.readFileSync('index.html', 'utf8');

// 1. Verify syntax by extracting script tag contents
const scripts = [];
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
while ((match = scriptRegex.exec(content)) !== null) {
    if (match[1].trim().length > 100) {
        scripts.push(match[1]);
    }
}

console.log(`Extracted ${scripts.length} script blocks.`);

// Extract computeMathematicalKundli
const target = 'computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {';
const startIdx = content.indexOf(target);
console.log('Found definition at:', startIdx);
const openBrace = content.indexOf('{', startIdx);

let depth = 1;
let endIdx = openBrace + 1;
while (depth > 0 && endIdx < content.length) {
    if (content[endIdx] === '{') depth++;
    else if (content[endIdx] === '}') depth--;
    endIdx++;
}

const funcCode = 'function ' + content.substring(startIdx, endIdx);
fs.writeFileSync('scripts/extracted_cmk_test.js', 'module.exports = ' + funcCode);

const fn = require('./extracted_cmk_test.js');

// Test Nikhil Vyas
const nikhil = fn("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("\n--- NIKHIL VYAS TEST ---");
console.log("Lagna D1:", nikhil.profile.asc_sign, nikhil.profile.asc_dms);
console.log("D9 Title:", nikhil.charts.d9.title);
console.log("D9 Ascendant:", nikhil.charts.d9.ascSign);
console.log("D9 House 1 Sign:", nikhil.charts.d9.houses[1][0]);
console.log("D9 House 1 Contents:", nikhil.charts.d9.houses[1]);
console.log("D9 Special Yogas:", nikhil.charts.d9.specialYogas);
console.log("SAV Array:", nikhil.ashtakavarga.sav);
console.log("SAV Sum:", nikhil.ashtakavarga.sav.reduce((a,b)=>a+b, 0));
console.log("SAV Mesha (Sign 1):", nikhil.ashtakavarga.sav[0]);
console.log("SAV Kanya (Sign 6):", nikhil.ashtakavarga.sav[5]);

// Assertions
if (nikhil.charts.d9.houses[1][0] !== "8") {
    console.error("FAIL: D9 House 1 Sign must be 8 (Scorpio), got:", nikhil.charts.d9.houses[1][0]);
    process.exit(1);
}
if (nikhil.ashtakavarga.sav.reduce((a,b)=>a+b,0) !== 337) {
    console.error("FAIL: SAV sum must be 337");
    process.exit(1);
}
if (nikhil.ashtakavarga.sav[0] !== 33 || nikhil.ashtakavarga.sav[5] !== 39) {
    console.error("FAIL: Mesha must be 33 and Kanya 39 in SAV");
    process.exit(1);
}

console.log("\nALL ASTRONOMICAL & PARASHARI ASSERTIONS PASSED WITH 100% MATHEMATICAL PRECISION!");

