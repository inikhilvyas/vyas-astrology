const fs = require('fs');
const html = fs.readFileSync('mobile/index.html', 'utf-8');

const elements = {};
function mockElement(id) {
    if (!elements[id]) {
        elements[id] = {
            id: id,
            innerHTML: '',
            innerText: '',
            value: '',
            style: {},
            classList: {
                add: () => {},
                remove: () => {},
                toggle: () => {},
                contains: () => false
            },
            querySelectorAll: () => [],
            querySelector: () => null,
            appendChild: () => {},
            closest: () => ({ appendChild: () => {} }),
            getContext: () => ({
                fillRect: () => {},
                beginPath: () => {},
                arc: () => {},
                fill: () => {},
                moveTo: () => {},
                lineTo: () => {},
                stroke: () => {},
                createLinearGradient: () => ({ addColorStop: () => {} })
            })
        };
    }
    return elements[id];
}

const mockDoc = {
    getElementById: (id) => mockElement(id),
    querySelectorAll: () => [],
    querySelector: () => null,
    createElement: () => ({ style: {}, innerHTML: '', appendChild: () => {} }),
    documentElement: { setAttribute: () => {} },
    addEventListener: () => {}
};

const mockWindow = {
    document: mockDoc,
    navigator: { userAgent: 'node', standalone: false },
    matchMedia: () => ({ matches: false }),
    localStorage: {
        getItem: () => null,
        setItem: () => {},
        removeItem: () => {}
    },
    addEventListener: () => {}
};
global.window = mockWindow;
global.document = mockDoc;
global.localStorage = mockWindow.localStorage;
global.AUTHENTIC_BUNDLE = null;
global.requestAnimationFrame = () => {};

const scriptMatches = html.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
let ran = 0;
scriptMatches.forEach((s) => {
    const code = s.replace(/<script[\s\S]*?>/i, '').replace(/<\/script>/i, '');
    if (code.trim()) {
        eval(code);
        ran++;
    }
});

console.log(`PASS: All ${ran} mobile scripts evaluated cleanly!`);
if (global.VyasDaivagyaVision && global.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay) {
    console.log("PASS: synthesizeConsolidatedPhalitEssay is present in mobile!");
    const essay = global.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay({ profile: { name: "Test Native" } });
    if (essay.includes("वृहद् संश्लेषित जीवन फलादेश महा-निबंध")) {
        console.log("PASS: Essay generated properly in mobile!");
    }
}
