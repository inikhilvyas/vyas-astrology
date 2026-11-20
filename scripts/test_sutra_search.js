// Test search in VyasSutrasBank
const path = require('path');
require(path.join(__dirname, '../js/vyas_sutras_bank.js'));

console.log("Total in bank:", global.VyasSutrasBank.getTotalCount());

const queries = [
    "केमद्रुम",
    "गजकेसरी",
    "दशम",
    "मंगल",
    "साढ़ेसाती",
    "बुधादित्य",
    "विवाह",
    "करियर"
];

queries.forEach(q => {
    let res = global.VyasSutrasBank.searchSutras(q, 3);
    console.log(`\nQuery: "${q}" => Found ${res.length} sutras:`);
    res.forEach((r, idx) => {
        console.log(`  ${idx+1}. [${r.src}] ${r.cond} => ${r.pred.substring(0, 80)}...`);
    });
});
