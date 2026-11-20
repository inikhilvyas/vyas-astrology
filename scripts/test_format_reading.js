// Test script to verify the new formatReading logic
const path = require('path');
require(path.join(__dirname, '../js/vyas_sutras_bank.js'));
require(path.join(__dirname, '../js/vyas_daivagya_engine.js'));

console.log("VyasSutrasBank count:", global.VyasSutrasBank.getTotalCount());
console.log("VyasDaivagyaCore available:", !!global.VyasDaivagyaCore);

// Sample Chart
const sampleChart = {
    profile: { name: "निखिल व्यास" },
    planet_table: [
        { planet: "सूर्य", sign: "मेष", degree: "14°20'", nakshatra: "भरणी (2)", house: 10, dignity: "उच्च" },
        { planet: "चन्द्र", sign: "तुला", degree: "22°15'", nakshatra: "विशाखा (1)", house: 4, dignity: "सम" },
        { planet: "मंगल", sign: "मेष", degree: "08°40'", nakshatra: "अश्विनी (3)", house: 10, dignity: "स्वराशि" },
        { planet: "बुध", sign: "मेष", degree: "28°10'", nakshatra: "कृत्तिका (1)", house: 10, dignity: "मित्र" },
        { planet: "गुरु", sign: "कर्क", degree: "05°30'", nakshatra: "पुष्य (1)", house: 1, dignity: "उच्च" },
        { planet: "शुक्र", sign: "वृषभ", degree: "12°00'", nakshatra: "रोहिणी (1)", house: 11, dignity: "स्वराशि" },
        { planet: "शनि", sign: "कुंभ", degree: "19°45'", nakshatra: "शतभिषा (4)", house: 8, dignity: "मूलत्रिकोण" },
        { planet: "राहु", sign: "मीन", degree: "11°20'", nakshatra: "उत्तरभाद्रपदा (3)", house: 9, dignity: "सम" },
        { planet: "केतु", sign: "कन्या", degree: "11°20'", nakshatra: "हस्त (1)", house: 3, dignity: "सम" }
    ]
};

const testQueries = [
    "मेरी कुंडली में केमद्रुम योग है या नहीं?",
    "मेरे करियर और आजीविका के बारे में बताइए",
    "मेरी कुंडली में धन योग और आर्थिक स्थिति कैसी है?",
    "विवाह और दांपत्य जीवन के योग कैसे हैं?",
    "वर्तमान विंशोत्तरी दशा का क्या फल होगा?"
];

testQueries.forEach(q => {
    console.log(`\n========================================`);
    console.log(`QUERY: ${q}`);
    console.log(`========================================`);
    const reading = global.VyasDaivagyaCore.formatReading(q, sampleChart);
    console.log(reading ? reading.substring(0, 350) + "...\n[Length: " + reading.length + "]" : "NULL");
});

