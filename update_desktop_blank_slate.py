import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original index.html length:", len(content))

# 1. Update header jatak-name
old_header_jatak = """                <span class="jatak-name">NIKHIL VYAS</span>
                <span class="jatak-lagna">मेष लग्न 23°27′</span>"""

new_header_jatak = """                <span class="jatak-name" id="jatakName">✨ अपनी कुण्डली बनाएं</span>
                <span class="jatak-lagna" id="jatakLagna">विवरण दर्ज करें (निःशुल्क)</span>"""

if old_header_jatak in content:
    content = content.replace(old_header_jatak, new_header_jatak)
    print("Updated desktop header jatak name successfully!")
else:
    print("Warning: old_header_jatak not found verbatim")

# 2. Update vIndexVal in HTML
old_vindex = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">VYAS DAY INDEX</div>
                                <div style="font-size:1.6rem; font-weight:900; color:var(--primary-navy);" id="vIndexVal">74</div>
                                <div style="font-size:0.72rem; color:#10b981; font-weight:800;">साधक (Success Day)</div>"""

new_vindex = """                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:700;">VYAS DAY INDEX</div>
                                <div style="font-size:1.6rem; font-weight:900; color:var(--primary-navy);" id="vIndexVal">--</div>
                                <div style="font-size:0.72rem; color:var(--text-muted); font-weight:800;" id="vIndexSub">कुण्डली आवश्यक</div>"""

if old_vindex in content:
    content = content.replace(old_vindex, new_vindex)
    print("Updated vIndexVal successfully!")
else:
    print("Warning: old_vindex not found verbatim")

# 3. Update updateDailyHoroscopeUI in index.html to eliminate fake 74
old_daily_fn = """        updateDailyHoroscopeUI() {
            var vVal = document.getElementById('vIndexVal');
            if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name) {
                if (vVal) vVal.innerText = "74";
            } else {
                if (vVal) vVal.innerText = "--";
            }
        },"""

new_daily_fn = """        updateDailyHoroscopeUI() {
            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name) {
                var chart = this.activeChartData;
                var nakList = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];
                var birthNakIdx = 16;
                if (chart.planet_table) {
                    for (var p = 0; p < chart.planet_table.length; p++) {
                        var pl = chart.planet_table[p];
                        if ((pl.p && pl.p.indexOf("चन्द्र") !== -1) || (pl.planet && pl.planet.indexOf("Moon") !== -1)) {
                            var nakStr = pl.n || pl.nak || '';
                            for (var ni = 0; ni < nakList.length; ni++) {
                                if (nakStr.indexOf(nakList[ni]) !== -1) { birthNakIdx = ni; break; }
                            }
                            break;
                        }
                    }
                }
                var diff = ((16 - birthNakIdx + 27) % 27) % 9;
                var TARA_SCORES = ["70%", "92%", "45%", "88%", "48%", "85%", "40%", "84%", "90%"];
                var TARA_NAMES = ["जन्म तारा", "सम्पत तारा", "विपत तारा", "क्षेम तारा", "प्रत्यरि तारा", "साधक तारा", "वध तारा", "मित्र तारा", "परम मित्र"];
                if (vVal) vVal.innerText = TARA_SCORES[diff] || "85%";
                if (vSub) {
                    vSub.innerText = TARA_NAMES[diff] || "साधक तारा";
                    vSub.style.color = (diff === 2 || diff === 4 || diff === 6) ? "#ef4444" : "#10b981";
                }
            } else {
                if (vVal) vVal.innerText = "--";
                if (vSub) {
                    vSub.innerText = "कुण्डली आवश्यक";
                    vSub.style.color = "var(--text-muted)";
                }
            }
        },"""

if old_daily_fn in content:
    content = content.replace(old_daily_fn, new_daily_fn)
    print("Updated updateDailyHoroscopeUI in index.html!")
else:
    print("Warning: old_daily_fn not found verbatim")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully!")
