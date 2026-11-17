const vm = require('vm');
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

const mStart = html.indexOf('computeMathematicalKundli(name, dobStr');
const mEnd = html.indexOf('// ACHARYA VYAS AI SAGE CHAT', mStart);
let fnCode = 'function ' + html.substring(mStart, mEnd).trim();
fnCode = fnCode.replace(/,\s*$/, '');

const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(fnCode, sandbox);

// Test for 1990-05-15 10:30 at Jaipur
const res = sandbox.computeMathematicalKundli("Test Native", "1990-05-15", "10:30", "Jaipur", "Male");

console.log("Calculated Lagna:", res.profile.asc_sign, res.profile.asc_dms);
console.log("Calculated Planets:");
for (let p of res.planet_table) {
    console.log(`  ${p.p}: ${p.r} ${p.d} (House ${p.h}, ${p.s})`);
}
