const fs = require('fs');
const vm = require('vm');

// Mock browser environment
const dom = {
    elements: {},
    getElementById: function(id) {
        if (!this.elements[id]) {
            this.elements[id] = { innerHTML: '', textContent: '', value: '2026', style: {} };
        }
        return this.elements[id];
    },
    addEventListener: function(event, cb) {
        if (event === 'DOMContentLoaded') {
            this.onReady = cb;
        }
    }
};

const window = {
    document: dom,
    localStorage: {
        getItem: function(key) {
            if (key === 'vyas_active_profile' || key === 'vyas_user_vault') {
                return JSON.stringify({
                    profile: { name: 'Nikhil Vyas', dob: '1984-11-23', tob: '16:51', city: 'Pali', asc_sign: 'मेष' },
                    lagna_sign_num: 1,
                    planet_table: [
                        { p: 'सूर्य', r: 'वृश्चिक', d: "07°33'", sign: 'वृश्चिक' },
                        { p: 'चन्द्र', r: 'वृश्चिक', d: "14°38'", sign: 'वृश्चिक' },
                        { p: 'मंगल', r: 'मकर', d: "26°11'", sign: 'मकर' },
                        { p: 'बुध', r: 'वृश्चिक', d: "29°17'", sign: 'वृश्चिक' },
                        { p: 'गुरु', r: 'धनु', d: "18°45'", sign: 'धनु' },
                        { p: 'शुक्र', r: 'धनु', d: "14°31'", sign: 'धनु' },
                        { p: 'शनि', r: 'तुला', d: "27°19'", sign: 'तुला' },
                        { p: 'राहु', r: 'वृषभ', d: "03°32'", sign: 'वृषभ' },
                        { p: 'केतु', r: 'वृश्चिक', d: "03°32'", sign: 'वृश्चिक' }
                    ]
                });
            }
            return null;
        }
    },
    parseInt: parseInt,
    Math: Math,
    console: console
};
window.window = window;

const astCode = fs.readFileSync('js/vyas_astronomical_engine.js', 'utf-8');
const renCode = fs.readFileSync('js/vyas_chart_renderers.js', 'utf-8');

const ctx = vm.createContext(window);
vm.runInContext(astCode, ctx);
vm.runInContext(renCode, ctx);

// Extract the script from varshphal/index.html
const vHtml = fs.readFileSync('varshphal/index.html', 'utf-8');
const scriptMatch = vHtml.match(/<script>([\s\S]*?)<\/script>[\s\S]*?<\/body>/);
if (scriptMatch) {
    try {
        vm.runInContext(scriptMatch[1], ctx);
        console.log("Script executed without crash!");
        if (dom.onReady) dom.onReady();
        console.log("DOMContentLoaded executed without crash!");
        console.log("varshChartWrap length:", dom.getElementById('varshChartWrap').innerHTML.length);
        console.log("varshPhalitWrap length:", dom.getElementById('varshPhalitWrap').innerHTML.length);
        console.log("Snippet of varshPhalitWrap:", dom.getElementById('varshPhalitWrap').innerHTML.substring(0, 200));
    } catch(e) {
        console.error("CRASH in varshphal script:", e);
    }
}
