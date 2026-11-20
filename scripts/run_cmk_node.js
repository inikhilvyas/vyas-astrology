global.window = {};
const fs = require('fs');

const content = fs.readFileSync('index.html', 'utf8');

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
fs.writeFileSync('scripts/extracted_cmk.js', 'module.exports = ' + funcCode);

const fn = require('./extracted_cmk.js');
const res = fn("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Res profile:", res.profile.name, res.profile.asc_sign, res.profile.asc_dms);
console.log("Charts D1 title:", res.charts.d1.title);
console.log("Charts D1 houses[1]:", res.charts.d1.houses[1]);
console.log("Charts D9 title:", res.charts.d9.title);
console.log("Charts D9 ascSign:", res.charts.d9.ascSign);
console.log("Charts D9 houses:", JSON.stringify(res.charts.d9.houses, null, 2));
