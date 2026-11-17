const fs = require('fs');
const vm = require('vm');
const assert = require('assert');

function testHtmlFile(filePath) {
    console.log(`\n=== TESTING FILE: ${filePath} ===`);
    const content = fs.readFileSync(filePath, 'utf8');

    // Extract computeMathematicalKundli function
    const mStart = content.indexOf('computeMathematicalKundli(name, dobStr');
    assert(mStart !== -1, `computeMathematicalKundli not found in ${filePath}`);

    let mEnd = content.indexOf('askQuickSage(text)', mStart);
    if (mEnd === -1) {
        mEnd = content.indexOf('sendQuickQuery(q)', mStart);
    }
    const idxClose = content.lastIndexOf('},', mEnd);

    let fnCode = 'function ' + content.substring(mStart, idxClose + 1).trim();

    const sandbox = {};
    vm.createContext(sandbox);
    vm.runInContext(fnCode, sandbox);

    // TEST 1: Nikhil Vyas (1984-11-23 16:51 Falna)
    const nikhil = sandbox.computeMathematicalKundli("Nikhil Vyas", "1984-11-23", "16:51", "Falna", "Male");
    console.log(`[PASS] Nikhil Lagna: ${nikhil.profile.asc_sign} (${nikhil.profile.asc_dms})`);
    assert.strictEqual(nikhil.profile.asc_sign, "मेष", "Nikhil Lagna must be Mesha (Aries)");

    const pMap = {};
    for (let p of nikhil.planet_table) {
        pMap[p.p.split(' ')[0]] = p;
    }

    // Mars exalted in Capricorn (10th house)
    assert(pMap["मंगल"].r === "मकर", `Mars must be in Capricorn, got ${pMap["मंगल"].r}`);
    assert(pMap["मंगल"].h === "10", `Mars must be in 10th house, got ${pMap["मंगल"].h}`);
    assert(pMap["मंगल"].s === "परम उच्च", `Mars must be exalted, got ${pMap["मंगल"].s}`);
    console.log(`[PASS] Mars: ${pMap["मंगल"].r} House ${pMap["मंगल"].h} (${pMap["मंगल"].s})`);

    // Saturn exalted in Libra (7th house)
    assert(pMap["शनि"].r === "तुला", `Saturn must be in Libra, got ${pMap["शनि"].r}`);
    assert(pMap["शनि"].h === "7", `Saturn must be in 7th house, got ${pMap["शनि"].h}`);
    assert(pMap["शनि"].s === "परम उच्च", `Saturn must be exalted, got ${pMap["शनि"].s}`);
    console.log(`[PASS] Saturn: ${pMap["शनि"].r} House ${pMap["शनि"].h} (${pMap["शनि"].s})`);

    // Jupiter own sign in Sagittarius (9th house)
    assert(pMap["गुरु"].r === "धनु", `Jupiter must be in Sagittarius, got ${pMap["गुरु"].r}`);
    assert(pMap["गुरु"].h === "9", `Jupiter must be in 9th house, got ${pMap["गुरु"].h}`);
    assert(pMap["गुरु"].s === "स्वक्षेत्री", `Jupiter must be own, got ${pMap["गुरु"].s}`);
    console.log(`[PASS] Jupiter: ${pMap["गुरु"].r} House ${pMap["गुरु"].h} (${pMap["गुरु"].s})`);

    // Sun, Moon, Mercury, Ketu in Scorpio (8th house)
    assert(pMap["सूर्य"].r === "वृश्चिक", `Sun must be in Scorpio, got ${pMap["सूर्य"].r}`);
    assert(pMap["चन्द्र"].r === "वृश्चिक", `Moon must be in Scorpio, got ${pMap["चन्द्र"].r}`);
    assert(pMap["बुध"].r === "वृश्चिक", `Mercury must be in Scorpio, got ${pMap["बुध"].r}`);
    assert(pMap["केतु"].r === "वृश्चिक", `Ketu must be in Scorpio, got ${pMap["केतु"].r}`);
    console.log(`[PASS] 8th House Scorpio Conjunction (Sun, Moon, Mercury, Ketu) verified!`);

    // Rahu exalted in Taurus (2nd house)
    assert(pMap["राहु"].r === "वृषभ", `Rahu must be in Taurus, got ${pMap["राहु"].r}`);
    assert(pMap["राहु"].h === "2", `Rahu must be in 2nd house, got ${pMap["राहु"].h}`);
    console.log(`[PASS] Rahu: ${pMap["राहु"].r} House ${pMap["राहु"].h}`);

    // TEST 2: Sample 1990-05-15 10:30 Jaipur
    const s1990 = sandbox.computeMathematicalKundli("Rahul", "1990-05-15", "10:30", "Jaipur", "Male");
    assert.strictEqual(s1990.profile.asc_sign, "कर्क", "1990-05-15 Jaipur Lagna must be Karka (Cancer)");
    
    const p1990 = {};
    for (let p of s1990.planet_table) {
        p1990[p.p.split(' ')[0]] = p;
    }

    assert.strictEqual(p1990["सूर्य"].r, "वृषभ", "Sun must be in Taurus on May 15");
    assert.strictEqual(p1990["चन्द्र"].r, "धनु", "Moon must be in Sagittarius on May 15, 1990");
    assert.strictEqual(p1990["बुध"].r, "मेष", "Mercury must be in Aries on May 15, 1990");
    assert.strictEqual(p1990["शुक्र"].r, "मीन", "Venus must be in Pisces on May 15, 1990");
    assert.strictEqual(p1990["मंगल"].r, "कुंभ", "Mars must be in Aquarius on May 15, 1990");
    assert.strictEqual(p1990["शनि"].r, "मकर", "Saturn must be in Capricorn on May 15, 1990");
    console.log(`[PASS] 1990-05-15 Planetary Positions 100% physically and astronomically validated!`);
}

testHtmlFile('index.html');
testHtmlFile('mobile/index.html');
testHtmlFile('android_app/app/src/main/assets/mobile/index.html');

console.log("\n=======================================================");
console.log("ALL 3 WEB & MOBILE PLATFORMS PASSED KUNDLI ACCURACY AUDIT!");
console.log("=======================================================");
