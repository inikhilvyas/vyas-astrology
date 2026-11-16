import re
import sys

def patch_index():
    print("Patching index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Ensure id="personalizedDailyCard" is present
    if 'id="personalizedDailyCard"' not in c:
        c = c.replace('<div class="content-card">', '<div class="content-card" id="personalizedDailyCard">', 1)
        print("  ✓ Added id='personalizedDailyCard'")

    # 2. Ensure id="personalizedDailyHeading" is present
    if 'id="personalizedDailyHeading"' not in c:
        c = c.replace('<div class="card-heading">', '<div class="card-heading" id="personalizedDailyHeading">', 1)
        print("  ✓ Added id='personalizedDailyHeading'")

    # 3. Ensure static HTML has the unknown placeholders for Tara
    old_static_tara = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TODAY'S TARA INSIGHT</div>
                                <div style="font-size:0.82rem; font-weight:800; color:var(--primary-navy);">Sadhak (साधक तारा - पर्याय 1)</div>
                                <div style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;">महत्वपूर्ण वार्ता, निर्णय व सिद्धि हेतु श्रेष्ठ दिन।</div>"""

    new_static_tara = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">TODAY'S TARA INSIGHT</div>
                                <div style="font-size:0.82rem; font-weight:800; color:var(--primary-navy);" id="vTodayTaraVal">नवतारा चक्र (अज्ञात)</div>
                                <div style="font-size:0.70rem; color:var(--text-secondary); margin-top:2px;" id="vTodayTaraDesc">व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।</div>"""

    if old_static_tara in c:
        c = c.replace(old_static_tara, new_static_tara, 1)
        print("  ✓ Updated static Tara block to blank state")

    # 4. Replace updateDailyHoroscopeUI
    m = re.search(r'updateDailyHoroscopeUI\(\)\s*\{', c)
    if not m:
        print("  ✗ updateDailyHoroscopeUI not found!")
        return False

    start = m.start()
    depth = 0
    start_brace = False
    end = -1
    for i in range(start, len(c)):
        if c[i] == '{':
            depth += 1
            start_brace = True
        elif c[i] == '}':
            depth -= 1
            if start_brace and depth == 0:
                end = i + 1
                break

    if end == -1:
        print("  ✗ Matching brace for updateDailyHoroscopeUI not found!")
        return False

    new_code = '''updateDailyHoroscopeUI() {
            var card = document.getElementById('personalizedDailyCard');
            if (!card) return;

            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            var taraVal = document.getElementById('vTodayTaraVal');
            var taraDesc = document.getElementById('vTodayTaraDesc');
            var heading = document.getElementById('personalizedDailyHeading');

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                if (heading) {
                    heading.innerHTML = '<span>✦ जातक का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#f59e0b; font-weight:700;"> (कुण्डली लोड नहीं है)</span>';
                }
                if (vVal) vVal.textContent = '--';
                if (vSub) {
                    vSub.textContent = 'कुण्डली आवश्यक';
                    vSub.style.color = 'var(--text-muted)';
                }
                if (taraVal) {
                    taraVal.textContent = 'नवतारा चक्र (अज्ञात)';
                    taraVal.style.color = 'var(--primary-navy)';
                }
                if (taraDesc) {
                    taraDesc.textContent = "व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।";
                }
                return;
            }

            var prof = this.activeChartData.profile;
            if (heading) {
                heading.innerHTML = '<span>✦ ' + (prof.name || 'जातक') + ' का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#10b981; font-weight:700;"> नवतारा चक्र + गोचर + चालू दशा</span>';
            }

            // Authentic Navatara calculation based on native\\'s Moon Nakshatra
            var nakList = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];
            var birthNakIdx = 0;
            if (this.activeChartData.planet_table) {
                for (var p = 0; p < this.activeChartData.planet_table.length; p++) {
                    var pl = this.activeChartData.planet_table[p];
                    if ((pl.p && pl.p.indexOf("चन्द्र") !== -1) || (pl.planet && pl.planet.indexOf("Moon") !== -1)) {
                        var nakStr = pl.n || pl.nakshatra || pl.nak || '';
                        for (var ni = 0; ni < nakList.length; ni++) {
                            if (nakStr.indexOf(nakList[ni]) !== -1) { birthNakIdx = ni; break; }
                        }
                        break;
                    }
                }
            }

            // Current transit Moon calculation
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
            if (taraDesc) taraDesc.textContent = info.desc;
        },

        renderDashaTree: function() {
            if (typeof this.initDashaTree === 'function') {
                return this.initDashaTree();
            }
        }'''

    c = c[:start] + new_code + c[end:]
    print("  ✓ Injected new dynamic updateDailyHoroscopeUI and renderDashaTree alias")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("  ✓ Saved index.html successfully.")
    return True

if __name__ == '__main__':
    patch_index()

