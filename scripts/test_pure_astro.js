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
// Test general calculation
const generalChart = VyasDesktop.computeMathematicalKundli("General User", "1995-05-15", "10:30 AM", "New Delhi", "Male", 28.6139, 77.2090);
console.log("General User Asc:", generalChart.profile.asc_sign, generalChart.profile.asc_dms);
console.log("Planets count:", generalChart.planet_table.length);
generalChart.planet_table.forEach(p => console.log(p.p, p.r, p.d));
