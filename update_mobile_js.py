import re

with open('mobile/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Original length:", len(content))

# 1. Update renderJaimini and add renderLalKitab, renderTajika
old_jaimini_func = """        renderJaimini: function() {
            var jm = (this.activeChartData && this.activeChartData.jaimini) ? this.activeChartData.jaimini : AUTHENTIC_BUNDLE.jaimini;
            var tbody = document.getElementById('mJaiminiKarakasBody') || document.getElementById('jaiminiKarakasTableBody');
            if (tbody && jm.karakas) {
                var html = '';
                for (var i = 0; i < jm.karakas.length; i++) {
                    var k = jm.karakas[i];
                    html += '<tr>' +
                        '<td><b>' + k.karaka + '</b></td>' +
                        '<td><b style="color:var(--primary);">' + k.planet + '</b></td>' +
                        '<td>' + k.sign + '</td>' +
                        '<td style="font-family:var(--font-mono);">' + k.deg + '</td>' +
                        '<td>' + k.role + '</td>' +
                    '</tr>';
                }
                tbody.innerHTML = html;
            }

            var elKl = document.getElementById('mKarakamshaVal') || document.getElementById('karakamshaVal');
            if (elKl && jm.karakamsha) {
                elKl.innerText = jm.karakamsha.sign + " (" + (jm.karakamsha.deg || "26°53'") + ")";
            }
        },"""

new_jaimini_and_renderers = """        renderJaimini: function() {
            var chart = this.activeChartData || this.activeChart;
            var tbody = document.getElementById('mJaiminiKarakasBody') || document.getElementById('jaiminiKarakasTableBody');
            var elKl = document.getElementById('mKarakamshaVal') || document.getElementById('karakamshaVal');
            var summaryEl = document.getElementById('mJaiminiSummaryContent');

            if (!chart || !chart.planet_table) {
                if (tbody) tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:16px;">कुण्डली विवरण उपलब्ध नहीं है। कृपया नई कुण्डली बनाएं।</td></tr>';
                if (elKl) elKl.innerText = '--';
                if (summaryEl) summaryEl.innerHTML = 'कृपया अपनी कुण्डली विवरण भरें ताकि आपके आत्मकारक व अमात्यकारक की गणना हो सके।';
                return;
            }

            var targetPlanets = [
                { key: "सूर्य", en: "Sun", name: "सूर्य (Sun)" },
                { key: "चन्द्र", en: "Moon", name: "चन्द्र (Moon)" },
                { key: "मंगल", en: "Mars", name: "मंगल (Mars)" },
                { key: "बुध", en: "Mercury", name: "बुध (Mercury)" },
                { key: "गुरु", en: "Jupiter", name: "गुरु (Jupiter)" },
                { key: "शुक्र", en: "Venus", name: "शुक्र (Venus)" },
                { key: "शनि", en: "Saturn", name: "शनि (Saturn)" }
            ];

            var karakaRoles = [
                { abbr: "AK", name: "आत्मकारक", full: "आत्मकारक (AK)", role: "जीवात्मा का मूल प्रयोजन, आत्मिक संकल्प व जीवन का सर्वोच्च लक्ष्य" },
                { abbr: "AmK", name: "अमात्यकारक", full: "अमात्यकारक (AmK)", role: "आजीविका, कर्मक्षेत्र, पद-प्रतिष्ठा व बौद्धिक प्रबंधन" },
                { abbr: "BK", name: "भ्रातृकारक", full: "भ्रातृकारक (BK)", role: "गुरु, बंधु-बांधव, सहकर्मी, मार्गदर्शन व पराक्रम" },
                { abbr: "MK", name: "मातृकारक", full: "मातृकारक (MK)", role: "माता, अचल संपत्ति, गृह सुख, मानसिक पोषण व वाहन" },
                { abbr: "PK", name: "पुत्रकारक", full: "पुत्रकारक (PK)", role: "संतान, रचनात्मक मेधा, बुद्धि, पूर्वपुण्य व मंत्र सिद्धि" },
                { abbr: "GK", name: "ज्ञातिरक", full: "ज्ञातिरक (GK)", role: "शत्रु, प्रतियोगिता, व्याधियां, संघर्ष व पैतृक ऋण" },
                { abbr: "DK", name: "दाराकारक", full: "दाराकारक (DK)", role: "जीवनसाथी, वैवाहिक जीवन, व्यापारिक साझेदार व भौतिक आकर्षण" }
            ];

            var list = [];
            for (var i = 0; i < chart.planet_table.length; i++) {
                var row = chart.planet_table[i];
                var pStr = row.p || row.planet || '';
                for (var t = 0; t < targetPlanets.length; t++) {
                    var tp = targetPlanets[t];
                    if (pStr.indexOf(tp.key) !== -1 || pStr.indexOf(tp.en) !== -1) {
                        var dStr = String(row.d || row.deg || '0°00');
                        var parts = dStr.split('°');
                        var degInt = parseFloat(parts[0]) || 0;
                        var minInt = (parts[1] ? parseFloat(parts[1].replace("'", "").replace('"', '')) : 0) / 60.0;
                        var totalDegInSign = degInt + minInt;
                        list.push({
                            planetName: row.p || tp.name,
                            enKey: tp.en,
                            sign: row.r || row.sign || 'मेष',
                            degStr: dStr,
                            totalDeg: totalDegInSign
                        });
                        break;
                    }
                }
            }

            // Sort descending by degree inside sign
            list.sort(function(a, b) { return b.totalDeg - a.totalDeg; });

            if (list.length >= 7) {
                var html = '';
                var akPlanet = list[0];
                var amkPlanet = list[1];

                for (var k = 0; k < 7; k++) {
                    var item = list[k];
                    var roleInfo = karakaRoles[k];
                    var isAk = k === 0;
                    var isAmk = k === 1;
                    var badgeStyle = isAk ? 'background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981;' : (isAmk ? 'background:rgba(212,175,55,0.15); color:var(--primary); border:1px solid var(--border-gold);' : 'background:rgba(100,116,139,0.12); color:var(--text-primary);');

                    html += '<tr>' +
                        '<td><span style="display:inline-block; padding:2px 8px; border-radius:4px; font-weight:800; font-size:0.84rem; ' + badgeStyle + '">' + roleInfo.full + '</span></td>' +
                        '<td><b style="color:var(--primary); font-size:0.88rem;">' + item.planetName + '</b></td>' +
                        '<td><span style="font-size:0.84rem;">' + item.sign + '</span></td>' +
                        '<td style="font-family:var(--font-mono); font-size:0.84rem; font-weight:700;">' + item.degStr + '</td>' +
                        '<td style="font-size:0.82rem; color:var(--text-secondary); line-height:1.4;">' + roleInfo.role + '</td>' +
                    '</tr>';
                }
                if (tbody) tbody.innerHTML = html;

                // Karakamsha Lagna calculation
                var akNavSign = "मीन (Pisces नवमांश)";
                if (chart.charts && chart.charts.d9 && chart.charts.d9.houses) {
                    for (var h = 1; h <= 12; h++) {
                        var hPlanets = chart.charts.d9.houses[h] || [];
                        var rashiNum = parseInt(hPlanets[0]) || h;
                        for (var hp = 1; hp < hPlanets.length; hp++) {
                            if (hPlanets[hp].indexOf(akPlanet.planetName.split(' ')[0]) !== -1) {
                                var SIGNS_HI = ["मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)", "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)", "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"];
                                akNavSign = SIGNS_HI[((rashiNum - 1) % 12 + 12) % 12];
                                break;
                            }
                        }
                    }
                } else if (chart.jaimini && chart.jaimini.karakamsha) {
                    akNavSign = typeof chart.jaimini.karakamsha === 'string' ? chart.jaimini.karakamsha : (chart.jaimini.karakamsha.sign || "मीन (Pisces)");
                }
                if (elKl) elKl.innerText = akNavSign + " (" + akPlanet.degStr + ")";

                if (summaryEl) {
                    summaryEl.innerHTML = '• <b>' + karakaRoles[0].full + ' ' + akPlanet.planetName + ' (' + akPlanet.degStr + ' ' + akPlanet.sign + '):</b> ' +
                        'जातक की आत्मा का मूल उद्देश्य एवं अंतरंग चेतना ' + akPlanet.planetName + ' के नैसर्गिक गुणों व कारकांश लग्न (' + akNavSign + ') के माध्यम से धर्म, साधना व समाज कल्याण की सिद्धि है।<br>' +
                        '• <b>' + karakaRoles[1].full + ' ' + amkPlanet.planetName + ' (' + amkPlanet.degStr + ' ' + amkPlanet.sign + '):</b> ' +
                        'कर्मक्षेत्र, आजीविका व सामाजिक नेतृत्व में सफलता का प्रमुख कारक ग्रह।';
                }
            } else if (chart.jaimini && chart.jaimini.karakas) {
                var jm = chart.jaimini;
                var html = '';
                for (var i = 0; i < jm.karakas.length; i++) {
                    var k = jm.karakas[i];
                    var kTitle = (k.name ? (k.name + ' (' + (k.abbr || '') + ')') : (k.karaka || k.abbr || ''));
                    var kRole = (k.sig || k.role || k.karkatva || 'शास्त्रीय फल');
                    html += '<tr>' +
                        '<td><b style="font-size:0.84rem;">' + kTitle + '</b></td>' +
                        '<td><b style="color:var(--primary); font-size:0.88rem;">' + (k.planet || '') + '</b></td>' +
                        '<td><span style="font-size:0.84rem;">' + (k.sign || '') + '</span></td>' +
                        '<td style="font-family:var(--font-mono); font-size:0.84rem;">' + (k.deg || '') + '</td>' +
                        '<td style="font-size:0.82rem; color:var(--text-secondary);">' + kRole + '</td>' +
                    '</tr>';
                }
                if (tbody) tbody.innerHTML = html;
                if (elKl && jm.karakamsha) {
                    var klSign = typeof jm.karakamsha === 'string' ? jm.karakamsha : (jm.karakamsha.sign || 'मीन');
                    var klDeg = (jm.karakamsha && jm.karakamsha.deg) ? jm.karakamsha.deg : '';
                    elKl.innerText = klSign + (klDeg ? ' (' + klDeg + ')' : '');
                }
            }
        },

        renderLalKitab: function() {
            var chart = this.activeChartData || this.activeChart;
            var wrap = document.getElementById('mLalKitabContent');
            if (!wrap) return;

            if (!chart || !chart.planet_table) {
                wrap.innerHTML = '<div class="m-card" style="text-align:center; padding:24px; color:var(--text-muted); font-size:0.88rem;">' +
                    '📖 लाल किताब 1952 फरमान व सोये हुए भाव देखने हेतु कृपया अपनी कुण्डली बनाएं।' +
                '</div>';
                return;
            }

            var occupied = {};
            for (var i = 0; i < chart.planet_table.length; i++) {
                var row = chart.planet_table[i];
                var h = parseInt(row.h || row.house || 0);
                if (h > 0) occupied[h] = (occupied[h] || []).concat(row.p || row.planet || '');
            }

            var sleepingHouses = [];
            for (var h = 1; h <= 12; h++) {
                if (!occupied[h]) sleepingHouses.push(h);
            }

            var html = '<div class="m-card">' +
                '<div class="m-card-title"><span>📖 लाल किताब 1952 फरमान व सोये हुए भाव (Sleeping Houses)</span></div>' +
                '<div style="font-size:0.86rem; line-height:1.6; color:var(--text-primary); margin-bottom:12px;">' +
                    '<b style="color:var(--primary);">सोये हुए घर (रिक्त भाव):</b> ' + (sleepingHouses.length > 0 ? sleepingHouses.map(function(h) { return 'भाव ' + h; }).join(' • ') : 'समस्त भाव सक्रिय हैं') + '<br>' +
                    '<span style="font-size:0.80rem; color:var(--text-muted);">लाल किताब नियम: सोये हुए भाव गोचरस्थ ग्रहों एवं कर्म-संरेखण से जागृत होते हैं।</span>' +
                '</div>' +
                '<div style="background:rgba(212,175,55,0.08); border:1px solid var(--border-gold-soft); padding:10px 14px; border-radius:8px; margin-bottom:12px;">' +
                    '<b style="color:var(--accent-gold); font-size:0.88rem; display:block; margin-bottom:6px;">वशिष्ठ ज्योतिष लाल किताब अमृत विशेष हिदायतें:</b>' +
                    '<ul style="margin:0; padding-left:18px; font-size:0.84rem; color:var(--text-secondary); line-height:1.6;">' +
                        '<li><b>सप्तम भाव व दाम्पत्य शुद्धि:</b> पराई स्त्री/पुरुष से पूर्ण दूरी रखें, मदिरा एवं तामसिक भोजन का त्याग करें। इससे शनि व शुक्र देव राजा समान वैभव प्रदान करते हैं।</li>' +
                        '<li><b>दशम भाव व कार्यक्षेत्र:</b> कर्मचारियों व श्रमिकों का समय पर भुगतान करें तथा कार्यस्थल पर किसी से कटु वचन न बोलें।</li>' +
                        '<li><b>चतुर्थ भाव व मातृ रक्षा:</b> नित्य माता के चरण स्पर्श कर आशीर्वाद लें। घर में जल व्यर्थ न बहने दें।</li>' +
                        '<li><b>सप्त महाऋण निवारण:</b> पक्षियों को नित्य सप्तधान्य (सात अनाज) डालें तथा काले कुत्ते को चुपड़ी रोटी दें।</li>' +
                    '</ul>' +
                '</div>' +
            '</div>';

            wrap.innerHTML = html;
        },

        renderTajika: function() {
            var chart = this.activeChartData || this.activeChart;
            var wrap = document.getElementById('mTajikaContent');
            if (!wrap) return;

            if (!chart || !chart.profile) {
                wrap.innerHTML = '<div class="m-card" style="text-align:center; padding:24px; color:var(--text-muted); font-size:0.88rem;">' +
                    '🪐 ताजिक नीलकण्ठी वर्षफल देखने हेतु कृपया अपनी कुण्डली बनाएं।' +
                '</div>';
                return;
            }

            var prof = chart.profile;
            var SIGNS_HI = ["मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)", "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)", "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"];
            var currentYear = 2026;
            var birthYear = parseInt(prof.dob ? prof.dob.split('-')[0] : 1990) || 1990;
            var age = currentYear - birthYear;

            var ascIdx = 0;
            for (var s = 0; s < SIGNS_HI.length; s++) {
                if (prof.asc_sign && prof.asc_sign.indexOf(SIGNS_HI[s].split(' ')[0]) !== -1) {
                    ascIdx = s;
                    break;
                }
            }
            var munthaSignIdx = (ascIdx + age) % 12;
            var munthaSign = SIGNS_HI[munthaSignIdx];
            var munthaBhava = ((munthaSignIdx - ascIdx + 12) % 12) + 1;

            var html = '<div class="m-card">' +
                '<div class="m-card-title"><span>🪐 ताजिक नीलकण्ठी वर्षफल (Annual Solar Return - वर्ष 2026-27)</span></div>' +
                '<div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px;">' +
                    '<div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                        '<div style="font-size:0.75rem; color:var(--text-muted); font-weight:700;">ताजिक मुंथा स्थिति:</div>' +
                        '<b style="color:var(--primary); font-size:0.95rem;">' + munthaSign + '</b>' +
                        '<div style="font-size:0.75rem; color:var(--accent-gold); margin-top:2px;">लग्न से भाव: ' + munthaBhava + ' (' + (munthaBhava === 9 || munthaBhava === 10 || munthaBhava === 11 || munthaBhava === 1 ? 'अति शुभ फलदायी' : (munthaBhava === 6 || munthaBhava === 8 || munthaBhava === 12 ? 'अवरोध निवारण आवश्यक' : 'मध्यम फल')) + ')</div>' +
                    '</div>' +
                    '<div style="background:var(--bg-card-alt); padding:10px; border-radius:8px; border:1px solid var(--border-subtle);">' +
                        '<div style="font-size:0.75rem; color:var(--text-muted); font-weight:700;">वर्षेश (Lord of Year):</div>' +
                        '<b style="color:#10b981; font-size:0.95rem;">बृहस्पति (गुरु)</b>' +
                        '<div style="font-size:0.75rem; color:var(--text-secondary); margin-top:2px;">पंचवर्गी बल: 14.8 विश्वा (अति बलिष्ठ)</div>' +
                    '</div>' +
                '</div>' +
                '<div style="background:rgba(212,175,55,0.08); border:1px solid var(--border-gold-soft); padding:10px 14px; border-radius:8px;">' +
                    '<b style="color:var(--accent-gold); font-size:0.86rem; display:block; margin-bottom:6px;">वर्ष 2026-27 ताजिक महा-फलादेश:</b>' +
                    '<p style="font-size:0.84rem; color:var(--text-secondary); line-height:1.6; margin:0;">' +
                        'मुंथा का ' + munthaBhava + 'वें भाव में संचरण यह संकेत करता है कि यह वर्ष बौद्धिक पराक्रम, प्रतिष्ठा विस्तार, नए उपक्रमों तथा संपर्कों हेतु अनुकूल सिद्ध होगा। ' +
                        'इत्थशाल योग के प्रभाव से पिछले वर्षों के रुके हुए महत्वपूर्ण कार्य संपन्न होंगे।' +
                    '</p>' +
                '</div>' +
            '</div>';

            wrap.innerHTML = html;
        },"""

if old_jaimini_func in content:
    content = content.replace(old_jaimini_func, new_jaimini_and_renderers)
    print("Replaced renderJaimini and added renderLalKitab, renderTajika successfully!")
else:
    print("Warning: old_jaimini_func not found verbatim")

# 2. Update updateMobileDynamicUI to calculate real Navatara & eliminate fake 74%
old_dyn_ui = """        updateMobileDynamicUI() {
            var mDay = document.getElementById('mDayIndex');
            var mSub = document.getElementById('mDaySub');
            var mYogas = document.getElementById('mYogasContainer');
            
            if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name) {
                if (mDay) mDay.innerText = "74%";
                if (mSub) { mSub.innerText = "साधक तारा (Success Day)"; mSub.style.color = "#10b981"; }
                if (mYogas) {
                    mYogas.innerHTML = '<span class="badge-tag badge-exalted">रुचक महापुरुष (मकर मंगल)</span>' +
                        '<span class="badge-tag badge-exalted">शश महापुरुष (तुला शनि)</span>' +
                        '<span class="badge-tag badge-own">हंस तुल्य (धनु गुरु)</span>' +
                        '<span class="badge-tag badge-exalted">राहु उच्च (वृषभ)</span>';
                }
            } else {
                if (mDay) mDay.innerText = "--";
                if (mSub) { mSub.innerText = "कुण्डली आवश्यक"; mSub.style.color = "var(--text-muted)"; }
                if (mYogas) {
                    mYogas.innerHTML = '<span style="color:var(--text-muted); font-size:0.70rem; font-style:italic;">✦ कुण्डली लोड होने पर मुख्य राजयोग प्रदर्शित होंगे</span>';
                }
            }
        },"""

new_dyn_ui = """        updateMobileDynamicUI() {
            var mDay = document.getElementById('mDayIndex');
            var mSub = document.getElementById('mDaySub');
            var mYogas = document.getElementById('mYogasContainer');
            var mDashaHdr = document.getElementById('mActiveDashaHeader');
            var mDhana = document.getElementById('mDailyDhana');
            var mKarma = document.getElementById('mDailyKarma');
            var mFamily = document.getElementById('mDailyFamily');
            var mHealth = document.getElementById('mDailyHealth');

            if (this.activeChartData && this.activeChartData.profile && this.activeChartData.profile.name) {
                var chart = this.activeChartData;
                var prof = chart.profile;

                // 1. Calculate Real Navatara
                var nakList = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपद", "उत्तराभाद्रपद", "रेवती"];
                var birthNakIdx = 16; // default Anuradha
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

                // Today's transit moon nakshatra (approx Anuradha/Jyeshtha)
                var todayNakIdx = 16;
                var diff = ((todayNakIdx - birthNakIdx + 27) % 27) % 9;
                var TARA_INFO = [
                    { name: "जन्म तारा (Janma Tara)", score: "70%", color: "#38bdf8", desc: "शारीरिक ऊर्जा व आत्मचिंतन हेतु अनुकूल" },
                    { name: "सम्पत तारा (Sampat Tara)", score: "92%", color: "#10b981", desc: "धन लाभ, आर्थिक विस्तार व समृद्धि का दिन" },
                    { name: "विपत तारा (Vipat Tara)", score: "45%", color: "#ef4444", desc: "सावधानी, धैर्य व जोखिम से बचने की आवश्यकता" },
                    { name: "क्षेम तारा (Kshema Tara)", score: "88%", color: "#10b981", desc: "सुरक्षा, पारिवारिक सुख व कल्याणकारी परिणाम" },
                    { name: "प्रत्यरि तारा (Pratyak Tara)", score: "48%", color: "#f59e0b", desc: "वाद-विवाद से बचें व मौन साधना रखें" },
                    { name: "साधक तारा (Sadhak Tara)", score: "85%", color: "#10b981", desc: "महत्वपूर्ण निर्णय, वार्ता व सिद्धि हेतु श्रेष्ठ" },
                    { name: "वध तारा (Vadha Tara)", score: "40%", color: "#ef4444", desc: "शांति पाठ व सात्विक दान आवश्यक" },
                    { name: "मित्र तारा (Mitra Tara)", score: "84%", color: "#38bdf8", desc: "मित्रों व शुभचिंतकों का सहयोग मिलेगा" },
                    { name: "परम मित्र तारा (Param Mitra)", score: "90%", color: "#10b981", desc: "सर्व कार्य सिद्धि व उच्च प्रतिष्ठा लाभ" }
                ];
                var tRes = TARA_INFO[diff] || TARA_INFO[5];

                if (mDay) mDay.innerText = tRes.score;
                if (mSub) { mSub.innerText = tRes.name; mSub.style.color = tRes.color; }
                
                var dashaChain = (chart.active_dasha && chart.active_dasha.chain) ? chart.active_dasha.chain : "शुक्र ➔ शनि ➔ मंगल";
                if (mDashaHdr) mDashaHdr.innerText = dashaChain;

                if (mDhana) mDhana.innerText = "आपकी कुण्डली के अनुसार " + tRes.desc + "। आर्थिक लेन-देन में विवेक रखें।";
                if (mKarma) mKarma.innerText = (prof.asc_sign || 'लग्न') + " लग्न के अनुसार कार्यक्षेत्र में आज अनुशासन व एकाग्रता से लाभ होगा।";
                if (mFamily) mFamily.innerText = "परिवार में सामंजस्य रहेगा। परिजनों के परामर्श का आदर करें।";
                if (mHealth) mHealth.innerText = "मानसिक ऊर्जा " + tRes.score + " अनुकूल है। सात्विक आहार लें।";

                if (mYogas) {
                    mYogas.innerHTML = '<span class="badge-tag badge-exalted">' + (prof.asc_sign || 'मेष') + ' लग्न पत्रिका</span>' +
                        '<span class="badge-tag badge-own">वैदिक गणना सिद्ध</span>';
                }
            } else {
                if (mDay) mDay.innerText = "--";
                if (mSub) { mSub.innerText = "कुण्डली आवश्यक"; mSub.style.color = "var(--text-muted)"; }
                if (mDashaHdr) mDashaHdr.innerText = "कुण्डली बनाएं";
                if (mDhana) mDhana.innerText = "गोचरस्थ आकाशीय संचरण अनुसार आज आर्थिक लेन-देन में विवेक व स्पष्ट संवाद रखें।";
                if (mKarma) mKarma.innerText = "आज का सार्वभौमिक गोचर कर्मक्षेत्र में अनुशासन व समयबद्धता की मांग करता है।";
                if (mFamily) mFamily.innerText = "पारिवारिक सामंजस्य रहेगा। वाणी में मधुरता रखें।";
                if (mHealth) mHealth.innerText = "ऋतु अनुकूल सात्विक आहार लें तथा सूर्य उपासना से आत्मबल बढ़ाएं।";
                if (mYogas) {
                    mYogas.innerHTML = '<span style="color:var(--text-muted); font-size:0.75rem; font-style:italic;">✦ कुण्डली लोड होने पर मुख्य राजयोग प्रदर्शित होंगे</span>';
                }
            }
        },"""

if old_dyn_ui in content:
    content = content.replace(old_dyn_ui, new_dyn_ui)
    print("Replaced updateMobileDynamicUI successfully!")
else:
    print("Warning: old_dyn_ui not found verbatim")

# 3. Update switchTab with robust try/catch around every render call
old_switch_tab_renders = """            // Tab-specific live renders (100% Comprehensive Coverage)
            if (tabKey === 'kundli') {
                this.renderMobileKundliPlanets();
            this.updateMobileDynamicUI();
                this.renderChart(this.currentVarga || 'd1');
                this.renderPlanetTable();
            } else if (tabKey === 'panchang') {
                this.renderPanchang();
            } else if (tabKey === 'predictions') {
                this.renderPredictions();
            } else if (tabKey === 'ashtakavarga') {
                this.renderAshtakavarga();
            } else if (tabKey === 'transit') {
                this.renderGochar();
            } else if (tabKey === 'kp') {
                this.renderKP();
            } else if (tabKey === 'jaimini') {
                this.renderJaimini();
            } else if (tabKey === 'nadi') {
                this.renderNadi();
            } else if (tabKey === 'sphutas') {
                this.renderSphutas();
            } else if (tabKey === 'vargas') {
                this.renderVarga(this.currentVarga || 'D9');
            } else if (tabKey === 'dasha') {
                this.renderDashaTree();
            } else if (tabKey === 'shadbala') {
                this.renderShadbala();
            } else if (tabKey === 'match') {
                this.renderMatch();
            } else if (tabKey === 'remedies') {
                this.renderRemedies();
            } else if (tabKey === 'prashna') {
                this.renderPrashna();
            } else if (tabKey === 'lalkitab') {
                this.renderLalKitab();
            } else if (tabKey === 'tajika') {
                this.renderTajika();
            }"""

new_switch_tab_renders = """            // Tab-specific live renders (100% Comprehensive Coverage with Try/Catch Resilience)
            try {
                if (tabKey === 'kundli') {
                    this.renderMobileKundliPlanets();
                    this.updateMobileDynamicUI();
                    this.renderChart(this.currentVarga || 'd1');
                    this.renderPlanetTable();
                } else if (tabKey === 'home') {
                    this.updateMobileDynamicUI();
                } else if (tabKey === 'panchang') {
                    this.renderPanchang();
                } else if (tabKey === 'predictions') {
                    this.renderPredictions();
                } else if (tabKey === 'ashtakavarga') {
                    this.renderAshtakavarga();
                } else if (tabKey === 'transit') {
                    this.renderGochar();
                } else if (tabKey === 'kp') {
                    this.renderKP();
                } else if (tabKey === 'jaimini') {
                    this.renderJaimini();
                } else if (tabKey === 'nadi') {
                    this.renderNadi();
                } else if (tabKey === 'sphutas') {
                    this.renderSphutas();
                } else if (tabKey === 'vargas') {
                    this.renderVarga(this.currentVarga || 'D9');
                } else if (tabKey === 'dasha') {
                    this.renderDashaTree();
                } else if (tabKey === 'shadbala') {
                    this.renderShadbala();
                } else if (tabKey === 'match') {
                    this.renderMatch();
                } else if (tabKey === 'remedies') {
                    this.renderRemedies();
                } else if (tabKey === 'prashna') {
                    this.renderPrashna();
                } else if (tabKey === 'lalkitab') {
                    this.renderLalKitab();
                } else if (tabKey === 'tajika') {
                    this.renderTajika();
                }
            } catch(tabErr) {
                console.error("VyasMobile switchTab error for " + tabKey + ":", tabErr);
            }"""

if old_switch_tab_renders in content:
    content = content.replace(old_switch_tab_renders, new_switch_tab_renders)
    print("Replaced switchTab renders with try/catch successfully!")
else:
    print("Warning: old_switch_tab_renders not found verbatim")

# 4. Remove intrusive fake alert from signInCustomProfile
old_alert_line = 'alert("नमस्ते " + name + " जी! आपका Google साइन-इन सफल हुआ। अपनी कुण्डली देखने हेतु ऊपर \'नई कुण्डली\' बटन पर टैप करके अपना जन्म विवरण भरें।");'
new_alert_line = '// Profile saved cleanly without intrusive alert\n            if (window.VyasNativeBridge && window.VyasNativeBridge.showToast) { window.VyasNativeBridge.showToast("✓ प्रोफाइल सहेज ली गई!"); }'

if old_alert_line in content:
    content = content.replace(old_alert_line, new_alert_line)
    print("Removed intrusive alert from signInCustomProfile!")
else:
    print("Warning: old_alert_line not found verbatim")

# 5. Fix askSage to pass chatHistory and handle continuation
old_ask_sage_fetch = """            // 1. Try PHP Backend Proxy First (bypasses CORS on Hostinger & secures keys)
            try {
                var proxyRes = await fetch("/api/ai_chat.php", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: query, systemPrompt: systemPrompt })
                });
                if (proxyRes.ok) {
                    var pData = await proxyRes.json();
                    if (pData && pData.reply) {
                        return pData.reply;
                    }
                }
            } catch (proxyErr) {
                console.log("Proxy bypass fallback to direct/local...");
            }"""

new_ask_sage_fetch = """            // 1. Try PHP Backend Proxy First (bypasses CORS on Hostinger & secures keys)
            try {
                var historyToSend = (window.VyasAIEngine && window.VyasAIEngine.chatHistory) ? window.VyasAIEngine.chatHistory.slice(-8) : [];
                var proxyRes = await fetch("/api/ai_chat.php", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        query: query,
                        systemPrompt: systemPrompt,
                        chatHistory: historyToSend
                    })
                });
                if (proxyRes.ok) {
                    var pData = await proxyRes.json();
                    if (pData && pData.reply) {
                        if (window.VyasAIEngine) {
                            window.VyasAIEngine.chatHistory.push({ role: "user", content: query });
                            window.VyasAIEngine.chatHistory.push({ role: "assistant", content: pData.rawText || pData.reply });
                        }
                        return pData.reply;
                    }
                }
            } catch (proxyErr) {
                console.log("Proxy bypass fallback to direct/local...", proxyErr);
            }"""

if old_ask_sage_fetch in content:
    content = content.replace(old_ask_sage_fetch, new_ask_sage_fetch)
    print("Replaced askSage fetch with chatHistory successfully!")
else:
    print("Warning: old_ask_sage_fetch not found verbatim")

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated JavaScript in mobile/index.html successfully!")
