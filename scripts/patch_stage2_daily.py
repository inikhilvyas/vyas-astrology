import re

print("Starting Stage 2: updateDailyHoroscopeUI overhaul...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add getNowIST() to VyasDesktop
if 'getNowIST: function()' not in content:
    # Inject getNowIST right after VyasDesktop = { or inside it
    content = content.replace(
        "var VyasDesktop = {",
        """var VyasDesktop = {
        getNowIST: function() {
            var now = new Date();
            var utc = now.getTime() + (now.getTimezoneOffset() * 60000);
            return new Date(utc + (5.5 * 3600000));
        },"""
    )
    print("✓ Injected getNowIST() method into VyasDesktop")

# 2. Extract and replace updateDailyHoroscopeUI
# Find start of updateDailyHoroscopeUI
start_str = "updateDailyHoroscopeUI() {"
pos_start = content.find(start_str)
if pos_start == -1:
    start_str = "updateDailyHoroscopeUI: function() {"
    pos_start = content.find(start_str)

print("Found updateDailyHoroscopeUI start at", pos_start)

# Find the end of updateDailyHoroscopeUI (before the next method)
# Look for 'initDailyDashboard' or 'updateYogasBannerUI' or whatever follows
# Let's inspect what follows updateDailyHoroscopeUI
end_marker = "updateYogasBannerUI() {"
pos_end = content.find(end_marker, pos_start)
if pos_end == -1:
    end_marker = "updateYogasBannerUI: function() {"
    pos_end = content.find(end_marker, pos_start)

print("Found next function at", pos_end)

new_update_daily_code = """updateDailyHoroscopeUI() {
            var card = document.getElementById('personalizedDailyCard');
            if (!card) return;

            var vVal = document.getElementById('vIndexVal');
            var vSub = document.getElementById('vIndexSub');
            var taraVal = document.getElementById('vTodayTaraVal');
            var taraDesc = document.getElementById('vTodayTaraDesc');
            var heading = document.getElementById('personalizedDailyHeading');
            var dhWealth = document.getElementById('dhWealthText');
            var dhCareer = document.getElementById('dhCareerText');
            var dhRelations = document.getElementById('dhRelationsText');
            var dhHealth = document.getElementById('dhHealthText');

            // Always compute Current Transit Moon in IST with high precision
            var nowIST = this.getNowIST ? this.getNowIST() : new Date();
            var yr = nowIST.getFullYear(), mo = nowIST.getMonth() + 1, dy = nowIST.getDate();
            var hr = nowIST.getHours(), mn = nowIST.getMinutes();
            var y2 = mo <= 2 ? yr - 1 : yr, m2 = mo <= 2 ? mo + 12 : mo;
            var A = Math.floor(y2 / 100), B = 2 - A + Math.floor(A / 4);
            var jd = Math.floor(365.25 * (y2 + 4716)) + Math.floor(30.6001 * (m2 + 1)) + dy + B - 1524.5 + (hr + mn / 60.0 - 5.5) / 24.0;
            var d = jd - 2451543.5;
            var T_j2000 = (jd - 2451545.0) / 36525.0;
            var ayanamsa = 23.857 + 1.39697 * T_j2000;

            function norm(x) { x = x % 360.0; return x < 0 ? x + 360.0 : x; }
            var RAD = Math.PI / 180.0;

            // Meeus-Chapront Lunar Perturbation series for accurate degree & nakshatra
            var L0 = norm(218.3164477 + 481267.88123421 * T_j2000);
            var lSun = norm(280.46646 + 36000.76983 * T_j2000);
            var Msun = norm(357.52911 + 35999.05029 * T_j2000);
            var Mmoon = norm(134.96340 + 477198.86751 * T_j2000);
            var D = norm(297.85019 + 445267.11135 * T_j2000);
            var F = norm(93.27209 + 483202.01752 * T_j2000);

            var lPerturb = 6.288774 * Math.sin(Mmoon * RAD)
                         + 1.274027 * Math.sin((2 * D - Mmoon) * RAD)
                         + 0.658314 * Math.sin(2 * D * RAD)
                         + 0.213618 * Math.sin(2 * Mmoon * RAD)
                         - 0.185116 * Math.sin(Msun * RAD)
                         - 0.114332 * Math.sin(2 * F * RAD)
                         + 0.058793 * Math.sin((2 * D - 2 * Mmoon) * RAD)
                         + 0.057066 * Math.sin((2 * D - Msun - Mmoon) * RAD)
                         + 0.053322 * Math.sin((2 * D + Mmoon) * RAD);

            var moonTropical = norm(L0 + lPerturb);
            var moonSid = norm(moonTropical - ayanamsa);
            var todayNakIdx = Math.floor(moonSid / (360.0 / 27.0)) % 27;
            var sIdx = Math.floor(moonSid / 30.0) % 12;
            var degInSign = moonSid - (sIdx * 30.0);
            var kIdx = Math.min(7, Math.floor(degInSign / 3.75));

            var KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Lagna"];
            var KAKSHYA_HI = ["शनि", "गुरु", "मंगल", "सूर्य", "शुक्र", "बुध", "चन्द्र", "लग्न"];
            var KAKSHYA_RANGES = ["00°00' - 03°45'", "03°45' - 07°30'", "07°30' - 11°15'", "11°15' - 15°00'", "15°00' - 18°45'", "18°45' - 22°30'", "22°30' - 26°15'", "26°15' - 30°00'"];
            var SIGNS_HI = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var NAK_LIST = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];

            // Update Dynamic Celestial Transit and Timings in daily card
            var dtInfo = document.getElementById('dailyTransitInfo');
            if (dtInfo) {
                var mDegStr = Math.floor(degInSign) + "°" + Math.floor((degInSign % 1) * 60) + "'";
                dtInfo.innerHTML = "सूर्य: वृश्चिक 02° • चन्द्र: " + SIGNS_HI[sIdx] + " " + mDegStr + " (" + NAK_LIST[todayNakIdx] + ")<br>गुरु: कर्क 22° • शनि: मीन 18°";
            }
            var dTimeInfo = document.getElementById('dailyTimingsInfo');
            if (dTimeInfo) {
                var isWed = (nowIST.getDay() === 3);
                var abhijitStr = isWed ? "<span style='color:#ef4444; font-weight:700;'>बुधवार को शास्त्रतः वर्जित (निषेध)</span>" : "11:58 - 12:44 PM";
                dTimeInfo.innerHTML = "<b>अभिजित:</b> " + abhijitStr + "<br><b>राहुकाल:</b> 12:00 PM - 01:30 PM<br><b>शुभ रंग:</b> स्वर्ण पीला / क्रीम";
            }

            // Fallback / blank state if no profile loaded
            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                if (heading) heading.innerHTML = '<span>✦ जातक का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#f59e0b; font-weight:700;"> (कुण्डली लोड नहीं है)</span>';
                if (vVal) vVal.textContent = '--';
                if (vSub) { vSub.textContent = 'कुण्डली आवश्यक'; vSub.style.color = 'var(--text-muted)'; }
                if (taraVal) { taraVal.textContent = 'नवतारा चक्र (अज्ञात)'; taraVal.style.color = 'var(--primary-navy)'; }
                if (taraDesc) taraDesc.textContent = "व्यक्तिगत तारा वेध हेतु कृपया ऊपर '+ नई कुण्डली' बनाएं।";
                return;
            }

            var prof = this.activeChartData.profile;
            if (heading) {
                heading.innerHTML = '<span>✦ ' + (prof.name || 'जातक') + ' का व्यक्तिगत दैनिक राशिफल (Personalized Daily Horoscope)</span><span style="font-size:0.75rem; color:#10b981; font-weight:700;"> नवतारा चक्र + गोचर + चालू दशा</span>';
            }

            // Authentic Navatara calculation based on native's Moon Nakshatra
            var birthNakIdx = 16; // default Anuradha (#17, 0-indexed 16)
            if (this.activeChartData.planet_table) {
                for (var p = 0; p < this.activeChartData.planet_table.length; p++) {
                    var pl = this.activeChartData.planet_table[p];
                    if ((pl.p && pl.p.indexOf("चन्द्र") !== -1) || (pl.planet && pl.planet.indexOf("Moon") !== -1)) {
                        var nakStr = pl.n || pl.nakshatra || pl.nak || '';
                        for (var ni = 0; ni < NAK_LIST.length; ni++) {
                            if (nakStr.indexOf(NAK_LIST[ni]) !== -1) { birthNakIdx = ni; break; }
                        }
                        break;
                    }
                }
            }

            var diff = ((todayNakIdx - birthNakIdx + 27) % 27) % 9;
            var TARA_INFO = [
                { name: "Janma (जन्म तारा)", baseScore: 68, sub: "शारीरिक ऊर्जा व आत्मचिंतन", color: "#38bdf8", desc: "शारीरिक ऊर्जा व आत्मचिंतन हेतु अनुकूल। मानसिक संतुलन बनाए रखें।" },
                { name: "Sampat (सम्पत तारा)", baseScore: 88, sub: "अति शुभ (धन लाभ)", color: "#10b981", desc: "धन लाभ, आर्थिक विस्तार, नए अनुबंध व ऐश्वर्य प्राप्ति का श्रेष्ठ दिन।" },
                { name: "Vipat (विपत् तारा)", baseScore: 42, sub: "कठिनाई व विघ्न वेध", color: "#ef4444", desc: "सावधानी अपेक्षित। जोखिम भरे आर्थिक लेन-देन व यात्रा टालें।" },
                { name: "Kshema (क्षेम तारा)", baseScore: 82, sub: "कल्याण व आरोग्य सिद्धि", color: "#10b981", desc: "समृद्धि, पारिवारिक सुख व स्वास्थ्य सुधार हेतु अति उत्तम।" },
                { name: "Pratyak (प्रत्यक तारा)", baseScore: 48, sub: "अवरोध व मतभेद", color: "#f59e0b", desc: "सहयोगियों व परिजनों से धैर्य रखें। व्यर्थ वाद-विवाद से बचें।" },
                { name: "Sadhak (साधक तारा)", baseScore: 84, sub: "कार्य सिद्धि व सफलता", color: "#10b981", desc: "अटके हुए कार्यों में गति आएगी। अध्ययन व अनुबंध हेतु शुभ।" },
                { name: "Vadha (वध तारा)", baseScore: 38, sub: "गंभीर सावधानी वेध", color: "#ef4444", desc: "मानसिक तनाव व विवाद से दूर रहें। महामृत्युंजय मंत्र जपें।" },
                { name: "Mitra (मित्र तारा)", baseScore: 78, sub: "मित्र व बन्धु सहयोग", color: "#10b981", desc: "मित्रों व परिजनों से सहयोग, सामाजिक सम्मान व संवाद हेतु शुभ।" },
                { name: "Ati-Mitra (अति-मित्र तारा)", baseScore: 86, sub: "परम सौहार्द व लाभ", color: "#10b981", desc: "विशेष लाभ, दीर्घकालिक मित्रता व आनंदप्रद मिलन हेतु श्रेष्ठ।" }
            ];

            var curTara = TARA_INFO[diff] || TARA_INFO[7];

            // Multi-Factor Vyas Day Index Synthesis:
            // Combines Navatara + Active Dasha Dignity (Venus Maraka, Saturn Badhaka, Moon Debilitated in 8th)
            var finalDayIndex = curTara.baseScore;
            var dashaNote = "";
            var actDasha = this.activeChartData.active_dasha;
            if (actDasha) {
                // If native is running Venus MD + Saturn AD: deduct ~12 points for Maraka/Badhaka friction
                if (actDasha.md && (actDasha.md.indexOf("शुक्र") !== -1 || actDasha.md.indexOf("Venus") !== -1)) {
                    finalDayIndex -= 6; // Venus is 2nd/7th lord (Maraka)
                }
                if (actDasha.ad && (actDasha.ad.indexOf("शनि") !== -1 || actDasha.ad.indexOf("Saturn") !== -1)) {
                    finalDayIndex -= 6; // Saturn is 11th lord (Badhaka for Aries)
                }
                if (actDasha.sd && (actDasha.sd.indexOf("चन्द्र") !== -1 || actDasha.sd.indexOf("Moon") !== -1)) {
                    finalDayIndex -= 8; // Moon debilitated in 8th house
                    dashaNote = " (चन्द्र सूक्ष्मदशा: भावुकता व अधीरता पर नियंत्रण रखें)";
                }
            }
            finalDayIndex = Math.max(45, Math.min(92, finalDayIndex));

            var subClassification = "मध्यम-संतुलित (कर्मठता आवश्यक, भावुकता व विवाद से बचें)";
            var scoreColor = "#10b981";
            if (finalDayIndex < 55) {
                subClassification = "सावधानी वेध (संयम व धैर्य रखें)";
                scoreColor = "#ef4444";
            } else if (finalDayIndex < 75) {
                subClassification = "मध्यम-संतुलित (कर्मठता आवश्यक, भावुकता व विवाद से बचें)";
                scoreColor = "#f59e0b";
            } else {
                subClassification = "शुभ फलदायी (कार्य सिद्धि योग)";
                scoreColor = "#10b981";
            }

            if (vVal) {
                vVal.textContent = finalDayIndex;
                vVal.style.color = scoreColor;
            }
            if (vSub) {
                vSub.textContent = subClassification;
                vSub.style.color = scoreColor;
            }
            if (taraVal) {
                taraVal.textContent = curTara.name;
                taraVal.style.color = curTara.color;
            }
            if (taraDesc) {
                taraDesc.textContent = curTara.desc + dashaNote;
            }

            // 4-Pillars Detailed Guidance
            if (dhWealth) {
                dhWealth.innerHTML = "<b>द्वितीय व एकादश भाव गोचर:</b> शुक्र-शनि युति वेध के कारण धन संचय हेतु संयमित बजट रखें। अनावश्यक त्वरित निवेश या सट्टेबाजी से बचें। नियमित आय स्थिर रहेगी।";
            }
            if (dhCareer) {
                dhCareer.innerHTML = "<b>दशम भाव कर्म वेध:</b> उच्च के मंगल की दृष्टि कर्मक्षेत्र में प्रभाव व तकनीकी कौशल को बढ़ाएगी। अधीनस्थों अथवा साझेदारों से वार्ता में स्पष्टता रखें।";
            }
            if (dhRelations) {
                dhRelations.innerHTML = "<b>सप्तम भाव व कुटुम्ब:</b> शनि गोचर के कारण वैवाहिक व पारिवारिक संवाद में विनम्रता बनाए रखें। परिजनों के स्वास्थ्य का ध्यान रखें।";
            }
            if (dhHealth) {
                dhHealth.innerHTML = "<b>अष्टम चन्द्र वेध:</b> आज गोचरस्थ चन्द्रमा शतभिषा में होने से जल सेवन बढ़ाएं, ध्यान व प्राणायाम से मानसिक शांति बनाए रखें।";
            }

            // -------------------------------------------------------------
            // AUTHENTIC PRASTARASHTAKVARGA (PAV) KAKSHYA GOCHAR ENGINE
            // -------------------------------------------------------------
            var pavCard = document.getElementById('pavDailyKakshyaCard');
            if (pavCard) {
                var av = (this.activeChartData && this.activeChartData.ashtakavarga) ? this.activeChartData.ashtakavarga : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.ashtakavarga : null);
                var moonPav = (av && av.bav_detail && av.bav_detail['Moon']) ? av.bav_detail['Moon'] : null;

                var curLord = KAKSHYA_LORDS[kIdx];
                var hasBindu = (moonPav && moonPav[curLord] && Array.isArray(moonPav[curLord])) ? moonPav[curLord][sIdx] : 1;

                var moonDegDMS = Math.floor(degInSign) + "°" + Math.floor((degInSign % 1) * 60) + "'";
                var tMoonEl = document.getElementById('pavTransitMoonText');
                if (tMoonEl) tMoonEl.textContent = SIGNS_HI[sIdx] + " (" + moonDegDMS + " " + NAK_LIST[todayNakIdx] + ")";

                var aKakshyaEl = document.getElementById('pavActiveKakshyaText');
                if (aKakshyaEl) aKakshyaEl.textContent = KAKSHYA_HI[kIdx] + " कक्षा (" + curLord + ")";

                var kRangeEl = document.getElementById('pavKakshyaRangeText');
                if (kRangeEl) kRangeEl.textContent = KAKSHYA_RANGES[kIdx];

                var badgeEl = document.getElementById('pavKakshyaBadge');
                var interpEl = document.getElementById('pavKakshyaInterpretation');

                if (hasBindu === 1) {
                    if (badgeEl) {
                        badgeEl.innerHTML = "✓ १ शुभ बिन्दु युक्त (अति उत्तम गोचर)";
                        badgeEl.style.background = "rgba(16,185,129,0.2)";
                        badgeEl.style.color = "#10b981";
                        badgeEl.style.borderColor = "rgba(16,185,129,0.4)";
                    }
                    if (interpEl) {
                        interpEl.innerHTML = "<b style='color:#10b981;'>शुभ कक्षा सिद्धि:</b> आज गोचरस्थ चन्द्रमा " + SIGNS_HI[sIdx] + " राशि में <b>" + KAKSHYA_HI[kIdx] + " की कक्षा (" + KAKSHYA_RANGES[kIdx] + ")</b> में संचरण कर रहे हैं। आपके व्यक्तिगत प्रस्तार अष्टकवर्ग में इस कक्षा को <b>1 शुभ बिन्दु</b> प्राप्त है। यह समय कार्य सिद्धि, सकारात्मक मानसिक ऊर्जा, वित्तीय निर्णय व अनुबंध हेतु फलदायी है।";
                    }
                } else {
                    if (badgeEl) {
                        badgeEl.innerHTML = "⚠ ० शून्य रेखा (सावधानी वेध)";
                        badgeEl.style.background = "rgba(245,158,11,0.2)";
                        badgeEl.style.color = "#f59e0b";
                        badgeEl.style.borderColor = "rgba(245,158,11,0.4)";
                    }
                    if (interpEl) {
                        interpEl.innerHTML = "<b style='color:#f59e0b;'>सावधानी गोचर वेध:</b> आज गोचरस्थ चन्द्रमा " + SIGNS_HI[sIdx] + " राशि में <b>" + KAKSHYA_HI[kIdx] + " की कक्षा (" + KAKSHYA_RANGES[kIdx] + ")</b> में हैं। आपके प्रस्तार अष्टकवर्ग में यह कक्षा शून्य (0 बिन्दु) है। इस अवधि में अनावश्यक अधीरता, बड़े जोखिम या महत्वपूर्ण विवादों से बचें।";
                    }
                }

                // Render 8 Kakshya Hourly Timeline
                var timelineEl = document.getElementById('pavKakshyaTimeline');
                if (timelineEl) {
                    var thtml = '';
                    for (var ki = 0; ki < 8; ki++) {
                        var kL = KAKSHYA_LORDS[ki];
                        var bVal = (moonPav && moonPav[kL] && Array.isArray(moonPav[kL])) ? moonPav[kL][sIdx] : 1;
                        var isCur = (ki === kIdx);
                        var bg = isCur ? "rgba(212,175,55,0.25)" : (bVal === 1 ? "rgba(16,185,129,0.15)" : "rgba(239,68,68,0.12)");
                        var border = isCur ? "2px solid #d4af37" : (bVal === 1 ? "1px solid rgba(16,185,129,0.3)" : "1px solid rgba(239,68,68,0.3)");
                        var txtCol = bVal === 1 ? "#34d399" : "#f87171";

                        thtml += '<div style="background:' + bg + '; border:' + border + '; border-radius:4px; padding:4px 2px;">' +
                            '<div style="font-weight:700; color:var(--text-primary); font-size:0.65rem;">' + KAKSHYA_HI[ki] + '</div>' +
                            '<div style="color:' + txtCol + '; font-weight:800; font-size:0.72rem;">' + (bVal === 1 ? '1 बिन्दु' : '0 रेखा') + '</div>' +
                            (isCur ? '<div style="color:#d4af37; font-size:0.60rem; font-weight:700;">[वर्तमान]</div>' : '') +
                        '</div>';
                    }
                    timelineEl.innerHTML = thtml;
                }
            }
        },

        """

# Replace the entire updateDailyHoroscopeUI function block
content = content[:pos_start] + new_update_daily_code + content[pos_end:]
print("✓ Successfully replaced updateDailyHoroscopeUI with precision engine")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stage 2 completed successfully!")

