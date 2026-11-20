const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let match, count = 0, script4Code = '';

while ((match = scriptRegex.exec(html)) !== null) {
    count++;
    if (count === 4) { script4Code = match[2]; break; }
}

const mockWindow = {
    localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
    document: { getElementById: () => ({ classList: { add: ()=>{}, remove: ()=>{} }, style: {} }), querySelectorAll: () => [], createElement: () => ({}), addEventListener: () => {} },
    console: console, Math: Math, Date: Date, parseInt: parseInt, parseFloat: parseFloat, isNaN: isNaN
};
mockWindow.window = mockWindow; mockWindow.global = mockWindow;

const ctx = vm.createContext(mockWindow);
vm.runInContext(script4Code, ctx);

const VyasDesktop = mockWindow.VyasDesktop;
// Test pure calculation without founder anchor
const testChart = VyasDesktop.computeMathematicalKundli("Someone", "1984-11-23", "16:51", "Falna", "Male", 25.24, 73.24);
console.log("Calculated Asc Sign:", testChart.profile.asc_sign, "DMS:", testChart.profile.asc_dms);
testChart.planet_table.forEach(p => console.log(p.p, p.r, p.d));

