const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const sIdx = html.indexOf('function calcVargasDetailed(');
const eIdx = html.indexOf('var ascVargas = calcVargasDetailed(ascSid);', sIdx);
const code = html.substring(sIdx, eIdx);

const SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
const SIGNS_EN = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
const D60_DEITIES = new Array(60).fill("Deity");

eval(code);

// Test different ascendants:
const testLagnas = [
    { name: "Taurus 15° (वृषभ)", deg: 45.0 },
    { name: "Leo 10° (सिंह)", deg: 130.0 },
    { name: "Scorpio 20° (वृश्चिक)", deg: 230.0 },
    { name: "Aquarius 5° (कुंभ)", deg: 315.0 },
    { name: "Pisces 18° (मीन)", deg: 348.0 }
];

for (const t of testLagnas) {
    const v = calcVargasDetailed(t.deg);
    console.log(`\n--- Test Lagna: ${t.name} (lon=${t.deg}) ---`);
    console.log(`  D1: ${v.D1.sign_name} (${v.D1.sign_index + 1})`);
    console.log(`  D2: ${v.D2.sign_name} (${v.D2.sign_index + 1})`);
    console.log(`  D3: ${v.D3.sign_name} (${v.D3.sign_index + 1})`);
    console.log(`  D4: ${v.D4.sign_name} (${v.D4.sign_index + 1})`);
    console.log(`  D7: ${v.D7.sign_name} (${v.D7.sign_index + 1})`);
    console.log(`  D9: ${v.D9.sign_name} (${v.D9.sign_index + 1})`);
    console.log(`  D10: ${v.D10.sign_name} (${v.D10.sign_index + 1})`);
    console.log(`  D12: ${v.D12.sign_name} (${v.D12.sign_index + 1})`);
    console.log(`  D60: ${v.D60.sign_name} (${v.D60.sign_index + 1})`);
}

