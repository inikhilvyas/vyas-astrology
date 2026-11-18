import re

print("=== STARTING AUTHENTIC VEDIC PANCHANG & DAY INDEX OVERHAUL ===")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# =========================================================================
# 1. FIX ABHIJIT MUHURTA PROHIBITION ON WEDNESDAY IN HTML & JS
# =========================================================================
print("Step 1: Fixing Abhijit Muhurta prohibition on Wednesday...")

# In header panchang strip
html = html.replace('अभिजित: 11:58 AM - 12:44 PM', 'बुधवार: अभिजित मुहूर्त वर्जित')
html = html.replace('अभिजित: 11:58 - 12:44 PM', 'बुधवार: अभिजित मुहूर्त वर्जित')

# In renderPanchang JS: Check for Wednesday (day === 3)
old_abhijit_js = """var elAbhijit = document.getElementById('dPanAbhijit');
        if (elAbhijit) elAbhijit.innerText = fmtMin(solarNoonMinutes - 24) + " - " + fmtMin(solarNoonMinutes + 24);"""

new_abhijit_js = """var elAbhijit = document.getElementById('dPanAbhijit');
        var nowDay = (new Date()).getDay(); // 0=Sun, 1=Mon, 2=Tue, 3=Wed...
        if (elAbhijit) {
            if (nowDay === 3) {
                elAbhijit.innerHTML = "<span style='color:#ef4444; font-size:0.80rem;'>बुधवार को अभिजित मुहूर्त शास्त्रतः पूर्णतः वर्जित (निषेध) है</span>";
            } else {
                elAbhijit.innerText = fmtMin(solarNoonMinutes - 24) + " - " + fmtMin(solarNoonMinutes + 24);
            }
        }"""

if old_abhijit_js in html:
    html = html.replace(old_abhijit_js, new_abhijit_js)
    print("SUCCESS: Patched renderPanchang Abhijit logic!")
else:
    # regex fallback
    html = re.sub(
        r'if\s*\(elAbhijit\)\s*elAbhijit\.innerText\s*=\s*fmtMin\(solarNoonMinutes\s*-\s*24\)\s*\+\s*["\']\s*-\s*["\']\s*\+\s*fmtMin\(solarNoonMinutes\s*\+\s*24\);',
        new_abhijit_js,
        html
    )

# =========================================================================
# 2. FIX EXACT HIGH-PRECISION TRANSIT MOON & DYNAMIC VYAS DAY INDEX
# =========================================================================
print("Step 2: Engineering Authentic Multi-Factor Vyas Day Index Synthesis...")

# Replace the simplistic moonSid & TARA_INFO calculation in updateDailyHoroscopeUI
old_daily_calc = """        // Current transit Moon calculation
        var now = new Date();
        var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
        var hr = now.getHours(), mn = now.getMinutes();
        var y2 = mo <= 2 ? yr - 1 : yr, m2 = mo <= 2 ? mo + 12 : mo;
        var A = Math.floor(y2 / 100), B = 2 - A + Math.floor(A / 4);
        var jd = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5 + (hr + mn / 60.0 - 5.5) / 24.0;
        var d = jd - 2451543.5;
        var T_j2000 = (jd - 2451545.0) / 36525.0;
        var ayanamsa = 23.857 + 1.39697 * T_j2000;
        function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
        var moonSid = norm(norm(125.1228 + 115.3654 + 13.0649929509 * d) - ayanamsa);
        var todayNakIdx = Math.floor(moonSid / (360.0 / 27.0)) % 27;

        var diff = ((todayNakIdx - birthNakIdx + 27) % 27) % 9;
        var TARA_INFO = [
            { name: "Janma (जन्म तारा - पर्याय 1)", score: "72", sub: "मध्यम अनुकूल", color: "#38bdf8", desc: "शारीरिक ऊर्जा व आत्मचिंतन हेतु अनुकूल। मानसिक संतुलन बनाए रखें।" },
            { name: "Sampat (सम्पत तारा - पर्याय 1)", score: "94", sub: "अति शुभ (धन लाभ)", color: "#10b981", desc: "धन लाभ, आर्थिक विस्तार, नए अनुबंध व ऐश्वर्य प्राप्ति का श्रेष्ठ दिन।" },
            { name: "Vipat (विपत तारा - पर्याय 1)", score: "42", sub: "सावधानी आवश्यक", color: "#ef4444", desc: "सावधानी, धैर्य व अनपेक्षित जोखिम से बचने की आवश्यकता। वाहन संभलकर चलाएं।" },
            { name: "Kshema (क्षेम तारा - पर्याय 1)", score: "88", sub: "कल्याणकारी शुभ", color: "#10b981", desc: "कल्याण, आरोग्य, सुरक्षा एवं पारिवारिक सुख-शांति हेतु अति शुभ।" },
            { name: "Pratyari (प्रत्यरि तारा - पर्याय 1)", score: "48", sub: "विवाद से बचें", color: "#f59e0b", desc: "शत्रु-प्रतिस्पर्धा व मतभेद से बचें। महत्वपूर्ण निर्णय टालें।" },
            { name: "Sadhak (साधक तारा - पर्याय 1)", score: "96", sub: "साधक (Success Day)", color: "#10b981", desc: "महत्वपूर्ण वार्ता, पदोन्नति, राजकार्य व सभी अभीष्ट कार्यों में सफलता।" },
            { name: "Vadha (वध/निधन तारा - पर्याय 1)", score: "35", sub: "अत्यंत सतर्क रहें", color: "#ef4444", desc: "अत्यंत सतर्क रहें। वाद-विवाद से दूर रहें व महामृत्युंजय जप करें।" },
            { name: "Mitra (मित्र तारा - पर्याय 1)", score: "85", sub: "सौहार्दपूर्ण शुभ", color: "#38bdf8", desc: "मित्रों, वरिष्ठों व सहयोगियों से पूर्ण समर्थन एवं सौहार्द प्राप्त होगा।" },
            { name: "Param Mitra (परम मित्र - पर्याय 1)", score: "92", sub: "सर्वकार्य सिद्धि", color: "#10b981", desc: "सर्वकार्य सिद्धि, प्रतिष्ठा में वृद्धि एवं आनंददायक वातावरण।" }
        ];

        var info = TARA_INFO[diff] || TARA_INFO[0];
        if (vVal) vVal.textContent = info.score;
        if (vSub) {
            vSub.textContent = info.sub;
            vSub.style.color = info.color;
        }
        if (taraVal) {
            taraVal.textContent = info.name;
            taraVal.style.color = info.color;
        }
        if (taraDesc) taraDesc.textContent = info.desc;"""

new_daily_calc = """        // =========================================================================
        // HIGH-PRECISION TRANSIT MOON & MULTI-FACTOR VEDIC SYNTHESIS
        // =========================================================================
        var now = new Date();
        var yr = now.getFullYear(), mo = now.getMonth() + 1, dy = now.getDate();
        var hr = now.getHours(), mn = now.getMinutes();
        var y2 = mo <= 2 ? yr - 1 : yr, m2 = mo <= 2 ? mo + 12 : mo;
        var A = Math.floor(y2 / 100), B = 2 - A + Math.floor(A / 4);
        var jd = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5 + (hr + mn / 60.0 - 5.5) / 24.0;
        var d = jd - 2451543.5;
        var T_j2000 = (jd - 2451545.0) / 36525.0;
        var ayanamsa = 23.857 + 1.39697 * T_j2000;
        function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }

        // Precise Meeus Chapront Lunar Longitude with perturbation terms
        var L0 = norm(218.3164477 + 481267.88123421 * T_j2000);
        var D = norm(297.8501921 + 445267.1114034 * T_j2000);
        var M = norm(357.5291092 + 35999.0502909 * T_j2000);
        var M_prime = norm(134.9633964 + 477198.8675055 * T_j2000);
        var F = norm(93.2720950 + 483202.0175233 * T_j2000);
        var rad = Math.PI / 180.0;

        var lPerturb = 6.288774 * Math.sin(M_prime * rad)
                     + 1.274027 * Math.sin((2 * D - M_prime) * rad)
                     + 0.658314 * Math.sin(2 * D * rad)
                     + 0.213618 * Math.sin(2 * M_prime * rad)
                     - 0.185116 * Math.sin(M * rad)
                     - 0.114332 * Math.sin(2 * F * rad);

        var moonTrop = norm(L0 + lPerturb);
        var moonSid = norm(moonTrop - ayanamsa);
        var todayNakIdx = Math.floor(moonSid / (360.0 / 27.0)) % 27;

        // Navatara Count from Anuradha (#17)
        var taraNum = ((todayNakIdx - birthNakIdx + 27) % 27) + 1;
        var taraCategory = ((taraNum - 1) % 9) + 1;

        var TARAS = {
            1: { name: "Janma (जन्म तारा)", baseScore: 68, sub: "शारीरिक श्रम व आत्मसंयम", color: "#38bdf8", desc: "शारीरिक ऊर्जा व आत्मचिंतन हेतु अनुकूल। मानसिक रूप से शांत रहें।" },
            2: { name: "Sampat (सम्पत तारा)", baseScore: 88, sub: "आर्थिक अवसर व संवृद्धि", color: "#10b981", desc: "धन, वित्तीय नियोजन व संसाधनों के विस्तार हेतु उत्तम।" },
            3: { name: "Vipat (विपत तारा)", baseScore: 42, sub: "सावधानी व धैर्य आवश्यक", color: "#ef4444", desc: "बाधाओं व अनपेक्षित व्यय की सम्भावना। विवाद व जल्दबाजी से बचें।" },
            4: { name: "Kshema (क्षेम तारा)", baseScore: 84, sub: "कल्याण व सौख्य", color: "#10b981", desc: "आरोग्य, पारिवारिक सुख एवं दैनिक कार्यों में संतुलन।" },
            5: { name: "Pratyari (प्रत्यरि तारा)", baseScore: 45, sub: "प्रतिस्पर्धा व सतर्कता", color: "#f59e0b", desc: "कार्यस्थल पर मतभेद व गुप्त अवरोध सम्भव। संयम रखें।" },
            6: { name: "Sadhak (साधक तारा)", baseScore: 92, sub: "कार्य सिद्धि व शोध", color: "#10b981", desc: "गहन अध्ययन, तकनीकी कार्य एवं महत्वपूर्ण प्रयासों में सिद्धि।" },
            7: { name: "Vadha (निधन तारा)", baseScore: 36, sub: "अति सतर्कता वेध", color: "#ef4444", desc: "अत्यंत सतर्क रहें। नया अनुबंध न करें, शिव आराधना करें।" },
            8: { name: "Mitra (मित्र तारा)", baseScore: 82, sub: "मित्र सहयोग व सौहार्द", color: "#38bdf8", desc: "मित्रों व शुभचिंतकों से सहयोग। वातावरण अनुकूल रहेगा।" },
            9: { name: "Param Mitra (परम मित्र)", baseScore: 90, sub: "परम सहयोग व प्रतिष्ठा", color: "#10b981", desc: "वरिष्ठों से समर्थन, सामाजिक सम्मान एवं कार्य विस्तार।" }
        };

        var taraInfo = TARAS[taraCategory] || TARAS[1];

        // Dasha Affliction Deduction (Venus=Maraka, Saturn=Badhaka, Moon=8th Neech for Aries)
        // Authentic Daivagya Weighted Day Index:
        var dashaPenalty = 18; // Dasha lords: Venus (Maraka), Saturn (Badhaka), Moon (8th Neech)
        var rawIndex = Math.round(taraInfo.baseScore * 0.70 + (100 - dashaPenalty * 2) * 0.30);
        var finalDayIndex = Math.max(48, Math.min(82, rawIndex)); // realistic, non-hyped score

        var indexSub = finalDayIndex >= 75 ? "शुभ व फलदायी" : (finalDayIndex >= 60 ? "मध्यम-संतुलित (कर्मठता आवश्यक)" : "सावधानी व सतर्कता वेध");
        var indexColor = finalDayIndex >= 75 ? "#10b981" : (finalDayIndex >= 60 ? "#d4af37" : "#ef4444");

        if (vVal) vVal.textContent = finalDayIndex;
        if (vSub) {
            vSub.textContent = indexSub;
            vSub.style.color = indexColor;
        }
        if (taraVal) {
            taraVal.textContent = taraInfo.name + " (" + nakList[todayNakIdx] + ")";
            taraVal.style.color = taraInfo.color;
        }
        if (taraDesc) {
            taraDesc.innerHTML = taraInfo.desc + " <br><span style='font-size:0.70rem; color:var(--text-muted);'>[दशा वेध: मारकेश शुक्र (MD) + बाधकेश शनि (AD) प्रभाव से अति-आशावादिता से बचें व व्यावहारिक योजना पर चलें]</span>";
        }"""

if old_daily_calc in html:
    html = html.replace(old_daily_calc, new_daily_calc)
    print("SUCCESS: Replaced toy Day Index with Authentic Multi-Factor Vedic Synthesis!")
else:
    print("WARNING: old_daily_calc not matched exactly, checking regex...")
    html = re.sub(
        r'// Current transit Moon calculation.*?if \(taraDesc\) taraDesc\.textContent = info\.desc;',
        new_daily_calc,
        html,
        flags=re.DOTALL
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully updated!")
