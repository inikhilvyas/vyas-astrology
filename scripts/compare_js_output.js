const fs = require('fs');
const vm = require('vm');

const content = fs.readFileSync('index.html', 'utf8');
const mStart = content.indexOf('computeMathematicalKundli(name, dobStr');
const mEnd = content.indexOf('askQuickSage(text)', mStart);
const idxClose = content.lastIndexOf('},', mEnd);

let fnCode = 'function ' + content.substring(mStart, idxClose + 1).trim();
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(fnCode, sandbox);

const res = sandbox.computeMathematicalKundli("Nikhil Vyas", "1984-11-23", "16:51", "Falna", "Male");

console.log('=== CLIENT-SIDE JAVASCRIPT OUTPUT (index.html) ===');
console.log('JS Lagna:', res.profile.asc_sign, res.profile.asc_dms);
console.log('JS Planets:');
for (let p of res.planet_table) {
    console.log(`  ${p.p}: ${p.r} ${p.d}`);
}
console.log('\nJS SAMUDAYA ASHTAKAVARGA (SAV):');
console.log(res.ashtakavarga.sav);
console.log('JS D-9 Navamsha Houses:');
console.log(res.charts.d9.houses);
console.log('JS D-10 Dashamsha Houses:');
console.log(res.charts.d10.houses);
