// Master Classical & Astronomical Kundli Engine Test
const RAD = Math.PI / 180.0;
const DEG = 180.0 / Math.PI;

function norm(x) {
    x = x % 360.0;
    return x < 0 ? x + 360.0 : x;
}

const SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
const PLANET_NAMES_HI = {
    Sun: "सूर्य", Moon: "चन्द्र", Mars: "मंगल", Mercury: "बुध",
    Jupiter: "गुरु", Venus: "शुक्र", Saturn: "शनि", Rahu: "राहु", Ketu: "केतु"
};

const NAKSHATRAS = [
    { name: "अश्विनी", lord: "केतु" }, { name: "भरणी", lord: "शुक्र" }, { name: "कृत्तिका", lord: "सूर्य" },
    { name: "रोहिणी", lord: "चन्द्र" }, { name: "मृगशिरा", lord: "मंगल" }, { name: "आर्द्रा", lord: "राहु" },
    { name: "पुनर्वसु", lord: "गुरु" }, { name: "पुष्य", lord: "शनि" }, { name: "अश्लेषा", lord: "बुध" },
    { name: "मघा", lord: "केतु" }, { name: "पूर्वाफाल्गुनी", lord: "शुक्र" }, { name: "उत्तराफाल्गुनी", lord: "सूर्य" },
    { name: "हस्त", lord: "चन्द्र" }, { name: "चित्रा", lord: "मंगल" }, { name: "स्वाती", lord: "राहु" },
    { name: "विशाखा", lord: "गुरु" }, { name: "अनुराधा", lord: "शनि" }, { name: "ज्येष्ठा", lord: "बुध" },
    { name: "मूल", lord: "केतु" }, { name: "पूर्वाषाढ़ा", lord: "शुक्र" }, { name: "उत्तराषाढ़ा", lord: "सूर्य" },
    { name: "श्रवण", lord: "चन्द्र" }, { name: "धनिष्ठा", lord: "मंगल" }, { name: "शतभिषा", lord: "राहु" },
    { name: "पूर्वाभाद्रपद", lord: "गुरु" }, { name: "उत्तराभाद्रपद", lord: "शनि" }, { name: "रेवती", lord: "बुध" }
];

const DASHA_LORDS = ["केतु", "शुक्र", "सूर्य", "चन्द्र", "मंगल", "राहु", "गुरु", "शनि", "बुध"];
const DASHA_YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]; // Total 120

const CITY_COORDINATES = {
    "delhi": { lat: 28.6139, lon: 77.2090, tz: 5.5 },
    "new delhi": { lat: 28.6139, lon: 77.2090, tz: 5.5 },
    "mumbai": { lat: 19.0760, lon: 72.8777, tz: 5.5 },
    "kolkata": { lat: 22.5726, lon: 88.3639, tz: 5.5 },
    "chennai": { lat: 13.0827, lon: 80.2707, tz: 5.5 },
    "bengaluru": { lat: 12.9716, lon: 77.5946, tz: 5.5 },
    "bangalore": { lat: 12.9716, lon: 77.5946, tz: 5.5 },
    "hyderabad": { lat: 17.3850, lon: 78.4867, tz: 5.5 },
    "ahmedabad": { lat: 23.0225, lon: 72.5714, tz: 5.5 },
    "pune": { lat: 18.5204, lon: 73.8567, tz: 5.5 },
    "surat": { lat: 21.1702, lon: 72.8311, tz: 5.5 },
    "jaipur": { lat: 26.9124, lon: 75.7873, tz: 5.5 },
    "jodhpur": { lat: 26.2389, lon: 73.0243, tz: 5.5 },
    "pali": { lat: 25.7711, lon: 73.3234, tz: 5.5 },
    "falna": { lat: 25.2418, lon: 73.2389, tz: 5.5 },
    "sumerpur": { lat: 25.1534, lon: 73.0822, tz: 5.5 },
    "udaipur": { lat: 24.5854, lon: 73.7125, tz: 5.5 },
    "lucknow": { lat: 26.8467, lon: 80.9462, tz: 5.5 },
    "kanpur": { lat: 26.4499, lon: 80.3319, tz: 5.5 },
    "nagpur": { lat: 21.1458, lon: 79.0882, tz: 5.5 },
    "indore": { lat: 22.7196, lon: 75.8577, tz: 5.5 },
    "bhopal": { lat: 23.2599, lon: 77.4126, tz: 5.5 },
    "patna": { lat: 25.5941, lon: 85.1376, tz: 5.5 },
    "varanasi": { lat: 25.3176, lon: 82.9739, tz: 5.5 },
    "kashi": { lat: 25.3176, lon: 82.9739, tz: 5.5 },
    "agra": { lat: 27.1767, lon: 78.0081, tz: 5.5 },
    "dehradun": { lat: 30.3165, lon: 78.0322, tz: 5.5 },
    "chandigarh": { lat: 30.7333, lon: 76.7794, tz: 5.5 },
    "shimla": { lat: 31.1048, lon: 77.1734, tz: 5.5 },
    "ujjain": { lat: 23.1765, lon: 75.7885, tz: 5.5 },
    "haridwar": { lat: 29.9457, lon: 78.1642, tz: 5.5 },
    "ranchi": { lat: 23.3441, lon: 85.3096, tz: 5.5 },
    "bhubaneswar": { lat: 20.2961, lon: 85.8245, tz: 5.5 },
    "guwahati": { lat: 26.1445, lon: 91.7362, tz: 5.5 },
    "amritsar": { lat: 31.6340, lon: 74.8723, tz: 5.5 },
    "ludhiana": { lat: 30.9010, lon: 75.8573, tz: 5.5 },
    "meerut": { lat: 28.9845, lon: 77.7064, tz: 5.5 },
    "noida": { lat: 28.5355, lon: 77.3910, tz: 5.5 },
    "gurgaon": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
    "gurugram": { lat: 28.4595, lon: 77.0266, tz: 5.5 },
    "prayagraj": { lat: 25.4358, lon: 81.8463, tz: 5.5 },
    "allahabad": { lat: 25.4358, lon: 81.8463, tz: 5.5 },
    "london": { lat: 51.5074, lon: -0.1278, tz: 0.0 },
    "new york": { lat: 40.7128, lon: -74.0060, tz: -5.0 },
    "dubai": { lat: 25.2048, lon: 55.2708, tz: 4.0 },
    "singapore": { lat: 1.3521, lon: 103.8198, tz: 8.0 }
};

console.log("Master Kundli Engine Test Script Written.");

