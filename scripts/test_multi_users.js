global.window = {};
const fn = require('./extracted_cmk.js');

const users = [
    { name: "Rahul Sharma", dob: "1992-05-15", tob: "08:30", city: "Jaipur, Rajasthan", gender: "Male", lat: 26.9124, lon: 75.7873 },
    { name: "Pooja Patel", dob: "1998-10-20", tob: "14:15", city: "Ahmedabad, Gujarat", gender: "Female", lat: 23.0225, lon: 72.5714 },
    { name: "Amit Verma", dob: "1980-01-05", tob: "22:45", city: "Varanasi, UP", gender: "Male", lat: 25.3176, lon: 82.9739 }
];

users.forEach(u => {
    const k = fn(u.name, u.dob, u.tob, u.city, u.gender, u.lat, u.lon);
    console.log(`\n=================== USER: ${u.name} ===================`);
    console.log(`D1 Lagna: ${k.profile.asc_sign} (${k.profile.asc_dms})`);
    console.log(`D9 Lagna: ${k.charts.d9.ascSign}`);
    console.log(`D9 House 1 Sign: ${k.charts.d9.houses[1][0]}`);
    console.log(`D10 Lagna: ${k.charts.d10.ascSign}`);
    console.log(`D10 House 1 Sign: ${k.charts.d10.houses[1][0]}`);
    console.log(`SAV Sum: ${k.ashtakavarga.sav.reduce((a,b)=>a+b, 0)}`);
    console.log(`SAV Array: ${k.ashtakavarga.sav}`);
});

