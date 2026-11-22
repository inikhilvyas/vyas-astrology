const fs = require('fs');
const vm = require('vm');

const dom = {
    elements: {},
    getElementById: function(id) {
        if (!this.elements[id]) {
            this.elements[id] = { innerHTML: '', textContent: '', value: '', style: {} };
        }
        return this.elements[id];
    },
    addEventListener: function(event, cb) {
        if (event === 'DOMContentLoaded') {
            this.onReady = cb;
        }
    }
};

const store = {
    'vyas_active_profile': JSON.stringify({
        profile: { name: 'Nikhil Vyas', dob: '1984-11-23', tob: '16:51', city: 'Pali', asc_sign: 'मेष' },
        lagna_sign_num: 1,
        planet_table: [
            { p: 'सूर्य', r: 'वृश्चिक', d: '07°33\'', sign: 'वृश्चिक' },
            { p: 'चन्द्र', r: 'वृश्चिक', d: '14°38\'', sign: 'वृश्चिक' },
            { p: 'मंगल', r: 'मकर', d: '26°11\'', sign: 'मकर' },
            { p: 'बुध', r: 'वृश्चिक', d: '29°17\'', sign: 'वृश्चिक' },
            { p: 'गुरु', r: 'धनु', d: '18°45\'', sign: 'धनु' },
            { p: 'शुक्र', r: 'धनु', d: '14°31\'', sign: 'धनु' },
            { p: 'शनि', r: 'तुला', d: '27°19\'', sign: 'तुला' },
            { p: 'राहु', r: 'वृषभ', d: '03°32\'', sign: 'वृषभ' },
            { p: 'केतु', r: 'वृश्चिक', d: '03°32\'', sign: 'वृश्चिक' }
        ]
    })
};

const window = {
    document: dom,
    localStorage: {
        getItem: function(key) { return store[key] || null; },
        setItem: function(key, val) { store[key] = val; },
        removeItem: function(key) { delete store[key]; }
    },
    parseInt: parseInt,
    Math: Math,
    console: console
};
window.window = window;

const astCode = fs.readFileSync('js/vyas_astronomical_engine.js', 'utf-8');
const daiCode = fs.readFileSync('js/vyas_daivagya_engine.js', 'utf-8');
const renCode = fs.readFileSync('js/vyas_chart_renderers.js', 'utf-8');

const ctx = vm.createContext(window);
vm.runInContext(astCode, ctx);
vm.runInContext(daiCode, ctx);
vm.runInContext(renCode, ctx);

const nHtml = fs.readFileSync('nadi-astrology/index.html', 'utf-8');
const scriptMatch = nHtml.match(/<script>([\s\S]*?)<\/script>[\s\S]*?<\/body>/);
if (scriptMatch) {
    vm.runInContext(scriptMatch[1], ctx);
    dom.onReady();
    const phalit = dom.getElementById('nadiPhalitWrap').innerHTML;
    console.log('nadiPhalitWrap length:', phalit.length);
    const cardMatches = phalit.match(/✦\s*[०-९1-9]+\.[^<]+/g);
    console.log('Cards rendered in Nadi:', cardMatches);
}

