global.window = {};
const fn = require('./extracted_cmk.js');
const res = fn("NIKHIL VYAS", "1984-11-23", "16:51", "Falna, Pali, Rajasthan", "Male", 25.2354, 73.2384);
console.log("Computed SAV:", res.ashtakavarga.sav);
console.log("Sum:", res.ashtakavarga.sav.reduce((a,b)=>a+b, 0));

