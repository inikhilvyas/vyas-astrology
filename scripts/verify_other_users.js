global.window = {};
const fn = require('./extracted_cmk_test.js');

const users = [
    { name: "Vikram Rathore", dob: "1990-07-28", tob: "06:15", city: "Udaipur, Rajasthan", gender: "Male", lat: 24.5854, lon: 73.7125 },
    { name: "Ananya Sen", dob: "1995-12-10", tob: "21:30", city: "Kolkata, WB", gender: "Female", lat: 22.5726, lon: 88.3639 }
];

users.forEach(u => {
    const k = fn(u.name, u.dob, u.tob, u.city, u.gender, u.lat, u.lon);
    console.log(`\n=================== USER: ${u.name} ===================`);
    console.log(`D1 Lagna: ${k.profile.asc_sign} (${k.profile.asc_dms})`);
    console.log(`D9 Lagna: ${k.charts.d9.ascSign}`);
    console.log(`D9 House 1 Sign: ${k.charts.d9.houses[1][0]}`);
    console.log(`D9 Special Yogas:`, k.charts.d9.specialYogas);
    console.log(`SAV Sum: ${k.ashtakavarga.sav.reduce((a,b)=>a+b, 0)}`);
});

