const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Fix toDMS
html = html.replace('ayanamsa_dms: toDMS(ayanamsa),', 'ayanamsa_dms: (Math.floor(ayanamsa) + "°" + Math.floor((ayanamsa * 60) % 60) + "\'" + Math.floor((ayanamsa * 3600) % 60) + "\\""),');

const fnStart = html.indexOf('computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {');
const scriptStart = html.lastIndexOf('<script', fnStart);
const scriptEnd = html.indexOf('</script>', fnStart);
const scriptCode = html.slice(scriptStart, scriptEnd);

const vm = require('vm');
const sandbox = {
    window: {},
    document: {
        documentElement: { getAttribute: () => 'dark' },
        getElementById: (id) => ({ value: '', innerHTML: '', appendChild: () => {}, querySelector: () => null, style: {}, classList: { add: () => {}, remove: () => {} } }),
        querySelectorAll: () => [],
        querySelector: () => ({ innerHTML: '', style: {}, textContent: '' }),
        addEventListener: () => {}
    },
    navigator: { geolocation: {} },
    localStorage: {
        getItem: () => null,
        setItem: () => null,
        removeItem: () => null
    },
    console: console,
    alert: (m) => console.log('ALERT CALLED WITH:', m),
    Math: Math,
    Date: Date,
    parseInt: parseInt,
    parseFloat: parseFloat,
    isNaN: isNaN,
    JSON: JSON,
    Array: Array,
    String: String,
    Object: Object,
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval
};
sandbox.window = sandbox;
vm.createContext(sandbox);
const cleanCode = scriptCode.replace(/^<script[^>]*>/i, '');
vm.runInContext(cleanCode, sandbox);

if (sandbox.VyasDesktop) {
    console.log('Testing loadVaultProfileByIndex with toDMS fixed...');
    sandbox.VyasDesktop.getUserProfilesList = () => [{
        name: 'Nikhil Vyas',
        dob: '1984-11-23',
        tob: '04:51 PM',
        city: 'Pali, Rajasthan',
        gender: 'Male'
    }];
    try {
        sandbox.VyasDesktop.loadVaultProfileByIndex(0);
        console.log('ACTIVE CHART PROFILE:', sandbox.VyasDesktop.activeChartData.profile);
        console.log('SUCCESS! ALL RENDERING COMPLETE!');
    } catch(err) {
        console.error('ERROR in loadVaultProfileByIndex:', err);
    }
}
