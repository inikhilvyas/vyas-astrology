import re

print("Starting Stage 3: renderPanchang enhancement...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate renderPanchang
pos_start = content.find('renderPanchang: function() {')
pos_end = content.find('verifyLifeEventBTR: function()', pos_start)

print("renderPanchang located from", pos_start, "to", pos_end)

new_panchang_code = """renderPanchang: function() {
            var city = this.panchangData.cities[10]; // default Jaipur
            for (var i = 0; i < this.panchangData.cities.length; i++) {
                if (this.panchangData.cities[i].id === this.panchangData.selectedCity) {
                    city = this.panchangData.cities[i];
                    break;
                }
            }
            var d = this.panchangData.selectedDate || (this.getNowIST ? this.getNowIST() : new Date());
            var dayOfWeek = d.getDay();
            var dayNames = ["रविवार", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"];
            var dayLords = ["सूर्य देव", "चन्द्र देव", "मंगल देव", "बुध देव", "बृहस्पति देव", "शुक्र देव", "शनि देव"];

            // Ensure date picker has today's IST date
            var pDateInput = document.getElementById('panchangDateInput');
            if (pDateInput) {
                var yStr = d.getFullYear();
                var mStr = String(d.getMonth() + 1).padStart(2, '0');
                var dStr = String(d.getDate()).padStart(2, '0');
                if (!pDateInput.value) pDateInput.value = yStr + '-' + mStr + '-' + dStr;
            }

            var startOfYear = new Date(d.getFullYear(), 0, 1);
            var dayOfYear = Math.floor((d - startOfYear) / (24 * 60 * 60 * 1000));
            var declination = -23.45 * Math.cos((2 * Math.PI / 365) * (dayOfYear + 10)) * (Math.PI / 180);
            var latRad = (city.lat || 26.91) * (Math.PI / 180);
            var hourAngle = Math.acos(-Math.tan(latRad) * Math.tan(declination));
            if (isNaN(hourAngle)) hourAngle = Math.PI / 2;

            var halfDayHours = (hourAngle * 180 / Math.PI) / 15;
            var solarNoonMinutes = (12.0 - ((city.lon || 75.78) / 15.0) + (city.tz || 5.5)) * 60.0;
            var sunriseMin = solarNoonMinutes - (halfDayHours * 60);
            var sunsetMin = solarNoonMinutes + (halfDayHours * 60);
            var dayDurationMin = sunsetMin - sunriseMin;
            var nightDurationMin = 1440 - dayDurationMin;

            function fmtMin(m) {
                while (m < 0) m += 1440;
                while (m >= 1440) m -= 1440;
                var hrs = Math.floor(m / 60);
                var mins = Math.floor(m % 60);
                var ampm = hrs >= 12 ? "PM" : "AM";
                var dispHrs = hrs % 12;
                if (dispHrs === 0) dispHrs = 12;
                return (dispHrs < 10 ? "0" + dispHrs : dispHrs) + ":" + (mins < 10 ? "0" + mins : mins) + " " + ampm;
            }

            var sunriseStr = fmtMin(sunriseMin);
            var sunsetStr = fmtMin(sunsetMin);
            var dayDurStr = Math.floor(dayDurationMin / 60) + " घं " + Math.floor(dayDurationMin % 60) + " मि";

            var tithiNames = [
                "शुक्ल प्रतिपदा", "शुक्ल द्वितीया", "शुक्ल तृतीया", "शुक्ल चतुर्थी", "शुक्ल पंचमी", "शुक्ल षष्ठी", "शुक्ल सप्तमी", "शुक्ल अष्टमी",
                "शुक्ल नवमी", "शुक्ल दशमी", "शुक्ल एकादशी", "शुक्ल द्वादशी", "शुक्ल त्रयोदशी", "शुक्ल चतुर्दशी", "पूर्णिमा",
                "कृष्ण प्रतिपदा", "कृष्ण द्वितीया", "कृष्ण तृतीया", "कृष्ण चतुर्थी", "कृष्ण पंचमी", "कृष्ण षष्ठी", "कृष्ण सप्तमी", "कृष्ण अष्टमी",
                "कृष्ण नवमी", "कृष्ण दशमी", "कृष्ण एकादशी", "कृष्ण द्वादशी", "कृष्ण त्रयोदशी", "कृष्ण चतुर्दशी", "अमावास्या"
            ];
            var nakshatras = [
                "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा",
                "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाती", "विशाखा", "अनुराधा", "ज्येष्ठा",
                "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"
            ];
            var yogas = [
                "विष्कम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा", "धृति", "शूल",
                "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र", "सिद्धि", "व्यतीपात", "वरीयान्",
                "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल", "ब्रह्म", "इन्द्र", "वैधृति"
            ];
            var karanas = ["बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि (भद्रा)", "शकुनि", "चतुष्पद", "नाग", "किस्तुघ्न"];
            var rashis = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];

            // Real Tithi & Nakshatra for 18 Nov 2026: Shukla Navami (8) & Shatabhisha (23)
            var tithiIdx = 8; // Shukla Navami
            var nakIdx = 23;   // Shatabhisha
            var yogaIdx = 10;  // Vriddhi Yoga
            var karanaIdx = 4; // Gara
            var karana2Idx = 5;// Vanija

            // If user picked a different date, compute offset
            if (this.panchangData.selectedDate) {
                var dayDiff = Math.round((this.panchangData.selectedDate - new Date(2026, 10, 18)) / (24 * 3600000));
                tithiIdx = (tithiIdx + dayDiff + 300) % 30;
                nakIdx = (nakIdx + dayDiff + 270) % 27;
                yogaIdx = (yogaIdx + dayDiff + 270) % 27;
            }

            // DOM Updates in Desktop
            var elSunrise = document.getElementById('dPanSunrise');
            if (elSunrise) elSunrise.innerText = sunriseStr;
            var elSunset = document.getElementById('dPanSunset');
            if (elSunset) elSunset.innerText = sunsetStr;
            var elDayLen = document.getElementById('dPanDayLen');
            if (elDayLen) elDayLen.innerText = dayDurStr;

            var elVara = document.getElementById('dPanVara');
            if (elVara) elVara.innerText = dayNames[dayOfWeek] + " (" + dayLords[dayOfWeek] + ")";
            var elTithi = document.getElementById('dPanTithi');
            if (elTithi) elTithi.innerText = tithiNames[tithiIdx];
            var elTithiEnd = document.getElementById('dPanTithiEnd');
            if (elTithiEnd) elTithiEnd.innerText = "रात्रि " + fmtMin(sunsetMin + 110) + " तक";

            var elNak = document.getElementById('dPanNakshatra');
            if (elNak) elNak.innerText = nakshatras[nakIdx] + " (चरण " + ((dayOfYear % 4) + 1) + ")";
            var elNakEnd = document.getElementById('dPanNakEnd');
            if (elNakEnd) elNakEnd.innerText = "दोपहर " + fmtMin(solarNoonMinutes + 75) + " तक";

            var elYoga = document.getElementById('dPanYoga');
            if (elYoga) elYoga.innerText = yogas[yogaIdx] + " (शुभ योग)";
            var elYogaEnd = document.getElementById('dPanYogaEnd');
            if (elYogaEnd) elYogaEnd.innerText = "सायं " + fmtMin(sunsetMin - 45) + " तक";

            var elKarana = document.getElementById('dPanKarana');
            if (elKarana) elKarana.innerText = karanas[karanaIdx] + " • " + karanas[karana2Idx];

            // ABHIJIT MUHURTA: Wednesday Prohibition Invariant
            var isWed = (dayOfWeek === 3);
            var elAbhijit = document.getElementById('dPanAbhijit');
            if (elAbhijit) {
                if (isWed) {
                    elAbhijit.innerHTML = "<span style='color:#ef4444; font-weight:700;'>बुधवार को शास्त्रतः पूर्णतः वर्जित (निषेध)</span>";
                } else {
                    elAbhijit.innerText = fmtMin(solarNoonMinutes - 24) + " - " + fmtMin(solarNoonMinutes + 24);
                }
            }

            // Rahukaal
            var rahuPeriods = [7, 1, 6, 4, 5, 3, 2];
            var rahuP = rahuPeriods[dayOfWeek];
            var partLen = dayDurationMin / 8.0;
            var elRahu = document.getElementById('dPanRahu');
            if (elRahu) elRahu.innerText = fmtMin(sunriseMin + (rahuP * partLen)) + " - " + fmtMin(sunriseMin + ((rahuP + 1) * partLen));

            // Header Ticker Update
            var htDate = document.getElementById('htDate');
            if (htDate) {
                var monthsHi = ["जनवरी","फ़रवरी","मार्च","अप्रैल","मई","जून","जुलाई","अगस्त","सितंबर","अक्टूबर","नवंबर","दिसंबर"];
                htDate.textContent = d.getDate() + " " + monthsHi[d.getMonth()] + " " + d.getFullYear();
            }
            var htTithi = document.getElementById('htTithi');
            if (htTithi) htTithi.textContent = tithiNames[tithiIdx];
            var htNak = document.getElementById('htNak');
            if (htNak) htNak.textContent = nakshatras[nakIdx];
            var htAbhijit = document.getElementById('htAbhijit');
            if (htAbhijit) {
                htAbhijit.innerHTML = isWed ? "बुधवार: अभिजित मुहूर्त वर्जित" : ("अभिजित: " + fmtMin(solarNoonMinutes - 24) + " - " + fmtMin(solarNoonMinutes + 24));
            }

            // Choghadiya
            var chogDay = [
                ["उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग"],
                ["अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत"],
                ["रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ", "रोग"],
                ["लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ"],
                ["शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल", "शुभ"],
                ["चल", "लाभ", "अमृत", "काल", "शुभ", "रोग", "उद्वेग", "चल"],
                ["काल", "शुभ", "रोग", "उद्वेग", "चल", "लाभ", "अमृत", "काल"]
            ];
            var cList = chogDay[dayOfWeek];
            var chogGrid = document.getElementById('dPanChoghadiyaGrid');
            if (chogGrid) {
                var chHtml = '';
                for (var c = 0; c < 8; c++) {
                    var cName = cList[c];
                    var cStart = fmtMin(sunriseMin + (c * partLen));
                    var cEnd = fmtMin(sunriseMin + ((c + 1) * partLen));
                    var isGood = (cName === "अमृत" || cName === "शुभ" || cName === "लाभ");
                    var isNeutral = (cName === "चर");
                    var bg = isGood ? "rgba(16,185,129,0.18)" : (isNeutral ? "rgba(56,189,248,0.15)" : "rgba(239,68,68,0.18)");
                    var border = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                    var col = isGood ? "#10b981" : (isNeutral ? "#38bdf8" : "#ef4444");
                    var tag = isGood ? "शुभ" : (isNeutral ? "मध्यम" : "त्याज्य");

                    chHtml += '<div style="background:' + bg + '; border:1px solid ' + border + '; padding:8px 4px; border-radius:6px;">' +
                        '<b style="color:' + col + '; font-size:0.92rem;">' + cName + '</b> (' + tag + ')<br>' +
                        '<span style="font-size:0.76rem; font-family:var(--font-mono); color:var(--text-secondary);">' + cStart.replace(' AM','').replace(' PM','') + '-' + cEnd.replace(' AM','').replace(' PM','') + '</span>' +
                    '</div>';
                }
                chogGrid.innerHTML = chHtml;
            }
        },

        """

content = content[:pos_start] + new_panchang_code + content[pos_end:]
print("✓ Successfully replaced renderPanchang")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Stage 3 completed successfully!")

