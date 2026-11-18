const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// Extract VyasDesktop object or computeMathematicalKundli
const fnStart = html.indexOf('computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {');
const fnEnd = html.indexOf('// ACHARYA VYAS AI SAGE CHAT', fnStart);
const fnCode = 'function ' + html.substring(fnStart, fnEnd).trim().replace(/,\s*$/, '');

// Wrap in an environment with necessary globals
const mockEnv = `
var window = {};
var document = {
    getElementById: function() { return null; }
};
var localStorage = {
    getItem: function() { return null; },
    setItem: function() {},
    removeItem: function() {}
};
` + fnCode + `
module.exports = computeMathematicalKundli;
`;

const path = require('path');
const tmpPath = path.join(__dirname, '..', 'tmp_test_kundli.js');
fs.writeFileSync(tmpPath, mockEnv, 'utf8');
const computeKundli = require(tmpPath);

console.log("=== 1. TESTING NIKHIL VYAS KUNDLI ===");
const k1 = computeKundli("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Profile:", k1.profile.name, "| Lagna:", k1.profile.asc_sign, k1.profile.asc_dms);
console.log("Total Charts:", Object.keys(k1.charts).length);
console.log("D1 Asc:", k1.charts.d1.ascSign, "| House 1:", k1.charts.d1.houses[1]);
console.log("D2 Asc:", k1.charts.d2.ascSign, "| House 1:", k1.charts.d2.houses[1]);
console.log("D3 Asc:", k1.charts.d3.ascSign, "| House 1:", k1.charts.d3.houses[1]);
console.log("D9 Asc:", k1.charts.d9.ascSign, "| House 1:", k1.charts.d9.houses[1]);
console.log("D10 Asc:", k1.charts.d10.ascSign, "| House 1:", k1.charts.d10.houses[1]);
console.log("D60 Asc:", k1.charts.d60.ascSign, "| House 1:", k1.charts.d60.houses[1]);
console.log("D9 PlanetDetails length:", k1.charts.d9.planetDetails.length);

console.log("\n=== 2. TESTING GENERAL USER (PRIYA - TAURUS LAGNA) ===");
const k2 = computeKundli("PRIYA SHARMA", "1995-05-15", "08:30", "Jaipur, Rajasthan", "Female", 26.9124, 75.7873);
console.log("Profile:", k2.profile.name, "| Lagna:", k2.profile.asc_sign, k2.profile.asc_dms);
console.log("D1 Asc:", k2.charts.d1.ascSign, "| House 1:", k2.charts.d1.houses[1]);
console.log("D2 Asc:", k2.charts.d2.ascSign, "| House 1:", k2.charts.d2.houses[1]);
console.log("D3 Asc:", k2.charts.d3.ascSign, "| House 1:", k2.charts.d3.houses[1]);
console.log("D9 Asc:", k2.charts.d9.ascSign, "| House 1:", k2.charts.d9.houses[1]);
console.log("D10 Asc:", k2.charts.d10.ascSign, "| House 1:", k2.charts.d10.houses[1]);
console.log("D60 Asc:", k2.charts.d60.ascSign, "| House 1:", k2.charts.d60.houses[1]);

console.log("\n=== 3. TESTING GENERAL USER (AMIT - LEO LAGNA) ===");
const k3 = computeKundli("AMIT VERMA", "1990-08-20", "15:45", "Mumbai, Maharashtra", "Male", 19.0760, 72.8777);
console.log("Profile:", k3.profile.name, "| Lagna:", k3.profile.asc_sign, k3.profile.asc_dms);
console.log("D1 Asc:", k3.charts.d1.ascSign, "| House 1:", k3.charts.d1.houses[1]);
console.log("D9 Asc:", k3.charts.d9.ascSign, "| House 1:", k3.charts.d9.houses[1]);
console.log("D10 Asc:", k3.charts.d10.ascSign, "| House 1:", k3.charts.d10.houses[1]);
console.log("D60 Asc:", k3.charts.d60.ascSign, "| House 1:", k3.charts.d60.houses[1]);

// Clean up
try { fs.unlinkSync(tmpPath); } catch(e) {}
