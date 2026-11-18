const fs = require('fs');
const vm = require('vm');
const content = fs.readFileSync('index.html', 'utf8');
const mStart = content.indexOf('computeMathematicalKundli(name, dobStr');
const mEnd = content.indexOf('askQuickSage(text)', mStart);
const idxClose = content.lastIndexOf('},', mEnd);

let fnCode = 'function ' + content.substring(mStart, idxClose + 1).trim();
fnCode = fnCode.replace('var sids = { Sun: sunSid, Moon: moonSid, Rahu: rahuSid, Ketu: ketuSid };',
`console.log("ayanamsa:", ayanamsa, "sunTrop:", sunTrop, "sunSid:", sunSid, "moonTrop:", moonTrop, "moonSid:", moonSid);
var sids = { Sun: sunSid, Moon: moonSid, Rahu: rahuSid, Ketu: ketuSid };`);

const sandbox = { console: console };
vm.createContext(sandbox);
vm.runInContext(fnCode, sandbox);
sandbox.computeMathematicalKundli('Nikhil Vyas', '1984-11-23', '16:51', 'Falna', 'Male');
