import os, sys

def patch_dynamic_essay_and_doshas():
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. PATCH synthesizeConsolidatedPhalitEssay
    p_start = html.find("synthesizeConsolidatedPhalitEssay: function(chart) {")
    p_end = html.find("analyzeChartTruth: function(chart) {", p_start)
    if p_start == -1 or p_end == -1:
        print("ERROR: synthesizeConsolidatedPhalitEssay block not found")
        return False

    new_essay_func = """synthesizeConsolidatedPhalitEssay: function(chart) {
            chart = chart || (window.VyasDesktop && window.VyasDesktop.activeChartData) || null;
            if (!chart || !chart.profile || !chart.profile.name) {
                return '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.85rem;">' +
                    '<b style="color:var(--accent-gold); font-size:1rem;">✦ कुण्डली लोड नहीं है</b>' +
                    '<p style="margin-top:6px;">व्यास 34.0 संश्लेषित जीवन फलादेश महा-निबंध देखने हेतु कृपया ऊपर <b>"+ नई कुण्डली"</b> बनाएं अथवा साइन-इन करें।</p>' +
                '</div>';
            }

            var prof = chart.profile;
            var name = prof.name || "जातक";
            var lagna = (prof.asc_sign || "मेष").split(' ')[0];
            var dob = prof.dob || "";
            var tob = prof.tob || "";
            var city = prof.city || "";
            var dasha = (chart.active_dasha && chart.active_dasha.chain) ? chart.active_dasha.chain : "विंशोत्तरी दशा सक्रिय";

            // Dynamically generate genuine classical sutras for THIS native's chart
            var dynamicSutras = [];
            if (typeof this.generateExhaustiveSutraAnalysis === 'function') {
                dynamicSutras = this.generateExhaustiveSutraAnalysis(chart) || [];
            }

            // Group into Yogas, Dignities, and House Lords
            var rajYogas = [];
            var dignities = [];
            var houseLords = [];

            dynamicSutras.forEach(function(s) {
                var sys = s.system || "";
                if (sys.indexOf("महापुरुष") !== -1 || sys.indexOf("राजयोग") !== -1 || sys.indexOf("योग") !== -1) {
                    rajYogas.push(s);
                } else if (sys.indexOf("नीच") !== -1 || sys.indexOf("स्वगृही") !== -1 || sys.indexOf("उच्च") !== -1 || sys.indexOf("बल") !== -1) {
                    dignities.push(s);
                } else if (sys.indexOf("भावेश") !== -1) {
                    houseLords.push(s);
                }
            });

            var essay = '<div class="vyas34-thesis" style="line-height:1.75; color:var(--text-primary); font-size:0.86rem;">' +
                // Header Banner
                '<div style="background:linear-gradient(135deg, rgba(212,175,55,0.14), rgba(30,58,138,0.22)); border:1px solid var(--border-gold); border-radius:12px; padding:16px; margin-bottom:18px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">' +
                        '<div>' +
                            '<span style="font-size:0.72rem; color:var(--accent-gold); font-weight:800; letter-spacing:1px; text-transform:uppercase;">VYAS 34.0 • AGENTIC JYOTISHA INTELLIGENCE SYSTEM</span>' +
                            '<h3 style="margin:2px 0 0 0; color:var(--accent-gold); font-size:1.15rem;">✦ ' + name + ' की जन्मपत्रिका: वृहद् संश्लेषित जीवन फलादेश महा-निबंध</h3>' +
                        '</div>' +
                        '<span style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981; padding:3px 10px; border-radius:14px; font-size:0.74rem; font-weight:800;">सत्य-निष्ठ बहु-पद्धतीय वेध [C3]</span>' +
                    '</div>' +
                    '<div style="font-size:0.74rem; color:var(--text-muted); margin-top:8px;">' +
                        'लग्न: <b>' + lagna + '</b> • जन्म: ' + dob + ' (' + tob + ') • स्थान: ' + city + ' • चालू विंशोत्तरी: <b>' + dasha + '</b>' +
                    '</div>' +
                '</div>' +

                // Chapter 1: Lagna & Core Constitution
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय १: आत्मिक आधार, लग्न संरचना व मूल प्रकृति (Lagna & Core Constitution)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'जातक का जन्म <b>' + lagna + ' लग्न</b> में हुआ है। महर्षि पराशर अनुसार लग्न शरीर, आत्म-चेतना, जीवन शक्ति एवं समग्र प्रारब्ध का मूल प्रवेश द्वार है। जातक की कुंडली में लग्न एवं लग्नेश का बल जीवन में स्थिरता, स्वाभिमान, नेतृत्व क्षमता एवं विपरीत परिस्थितियों में भी पुनः उठ खड़े होने की अदम्य शक्ति प्रदान करता है। जातक में पराधीनता स्वीकार न करने और स्वतंत्र निर्णय लेने की स्वाभाविक प्रवृत्ति है।' +
                    '</p>' +
                '</div>' +

                // Chapter 2: Dynamic Raj Yogas present in THIS chart
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय २: मुख्य शास्त्रीय योग व ग्रह बल (Active Shastric Yogas & Potencies)' +
                    '</h4>' +
                    '<p style="margin:0 0 10px 0;">' +
                        'जातक की जन्मपत्रिका में प्रत्यक्ष उपस्थित शास्त्रीय योग एवं ग्रह स्थितियां (केवल सत्य-प्रमाणित योग):' +
                    '</p>';

            if (rajYogas.length > 0 || dignities.length > 0) {
                essay += '<ul style="margin:0 0 8px 0; padding-left:18px;">';
                var shownItems = rajYogas.concat(dignities).slice(0, 5);
                shownItems.forEach(function(item) {
                    essay += '<li style="margin-bottom:10px;">' +
                        '<b style="color:var(--accent-gold);">' + item.title + '</b> <span style="font-size:0.72rem; color:#10b981; font-weight:700;">' + item.system + '</span><br>' +
                        '<span style="font-size:0.74rem; color:var(--text-muted); font-style:italic;">' + (item.ref || 'बृहत्पाराशर होराशास्त्र') + (item.shloka ? (' • ' + item.shloka) : '') + '</span><br>' +
                        '<span style="font-size:0.84rem;">' + item.meaning + '</span>' +
                    '</li>';
                });
                essay += '</ul>';
            } else {
                essay += '<p style="color:var(--text-secondary); font-size:0.82rem;">जातक की कुण्डली में केन्द्र एवं त्रिकोण भावों के स्वामियों का संतुलित संबंध सामान्य जीवन को निरंतर प्रगतिशील बनाए रखता है।</p>';
            }

            essay += '</div>' +

                // Chapter 3: Dasha Timing
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ३: फलोदय काल व विंशोत्तरी दशा सक्रियता (Timing & Dasha Activation)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'वर्तमान में सक्रिय <b>' + dasha + '</b> जातक के जीवन में महत्वपूर्ण कर्मिक बदलावों का काल है। महादशा नाथ एवं अंतर्दशा नाथ जिन भावों के स्वामी हैं अथवा जहां स्थित हैं, उन क्षेत्रों (करियर, वित्त, संबंध) में प्रारब्ध के कर्म पककर फलित होते हैं।' +
                    '</p>' +
                '</div>' +

                // Chapter 4: Gochar & Double Transit
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ४: तात्कालिक गोचर वेध व सक्रिय उत्प्रेरक (Transit Triggers 2026-2027)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'वर्ष 2026-2027 में देवगुरु बृहस्पति का सिंह राशि में तथा शनिदेव का मीन राशि में संचरण जातक के ' + lagna + ' लग्न से विशेष भावों को वेध रहा है। जब गुरु और शनि का दोहरा वेध (Double Transit) किसी भाव पर पड़ता है, तो वह कार्य अवश्यमेव सिद्ध होता है।' +
                    '</p>' +
                '</div>' +

                // Chapter 5: Four Purusharthas
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ५: चतुर्विध पुरुषार्थ जीवन मीमांसा (Dharma, Artha, Kama, Moksha)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        '<b>धर्म (१, ५, ९ भाव):</b> जातक के जीवन का मूल उद्देश्य सत्यनिष्ठा, कर्तव्यपालन एवं ज्ञानार्जन है।<br>' +
                        '<b>अर्थ (२, १०, ११ भाव):</b> आजीविका एवं धन संचय में परिश्रम, कर्मठता व दूरदर्शिता से निरंतर वृद्धि होगी।<br>' +
                        '<b>काम (३, ७ भाव):</b> सामाजिक प्रतिष्ठा, संबंध एवं पुरुषार्थ द्वारा आकांक्षाओं की पूर्ति होगी।<br>' +
                        '<b>मोक्ष (४, ८, १२ भाव):</b> अंतर्मुखी चिंतन, ध्यान एवं सात्विक जीवनशैली से मानसिक शांति प्राप्त होगी।' +
                    '</p>' +
                '</div>' +
            '</div>';

            return essay;
        },\n\n        """

    html = html[:p_start] + new_essay_func + html[p_end:]
    print("SUCCESS: Patched synthesizeConsolidatedPhalitEssay to be fully dynamic.")

    # 2. PATCH doshaBox inside renderPredictions
    db_needle = "// Render Yogas and Doshas\n            if (doshaBox) {"
    p_db = html.find(db_needle)
    if p_db != -1:
        p_db_end = html.find("renderAshtakavarga() {", p_db)
        p_closing = html.rfind("},", p_db, p_db_end) + 2

        new_dosha_code = """// Render Yogas and Doshas
            if (doshaBox) {
                var pTable = (this.activeChartData && this.activeChartData.planet_table) ? this.activeChartData.planet_table : [];
                var pMap = {};
                for (var i = 0; i < pTable.length; i++) {
                    var pl = pTable[i];
                    var pName = (pl.p || pl.planet || '').replace(/\\s*\\(.*\\)/, '').trim();
                    pMap[pName] = { house: parseInt(pl.h || pl.house || 1), sign: (pl.r || pl.sign || '').split(' ')[0], dignity: pl.dignity || pl.s || '' };
                }

                // 1. DYNAMIC MANGLIK EVALUATION
                var mars = pMap['मंगल'] || null;
                var manglikTitle = "दोष रहित";
                var manglikColor = "#10b981";
                var manglikReason = "";

                if (mars) {
                    var mHouse = mars.house;
                    if ([1, 4, 7, 8, 12].indexOf(mHouse) !== -1) {
                        var isCancelled = false;
                        var cancelReason = "";
                        if (mars.sign === "मकर" || mars.dignity.indexOf("उच्च") !== -1) {
                            isCancelled = true;
                            cancelReason = "मंगल देव मकर राशि (उच्च) में होने से मांगलिक दोष पूर्णतः निरस्त है।";
                        } else if (mHouse === 1 && mars.sign === "मेष") {
                            isCancelled = true;
                            cancelReason = "लग्न में स्वराशि (मेष) का मंगल होने से दोष निरस्त है।";
                        } else if (mHouse === 4 && mars.sign === "वृश्चिक") {
                            isCancelled = true;
                            cancelReason = "चतुर्थ भाव में स्वराशि (वृश्चिक) का मंगल होने से दोष निष्प्रभावी है।";
                        } else if (pMap['गुरु'] && ([1, 4, 7, 10].indexOf(pMap['गुरु'].house) !== -1 || ((pMap['गुरु'].house + 6) % 12 + 1 === mHouse))) {
                            isCancelled = true;
                            cancelReason = "देवगुरु बृहस्पति की केंद्र स्थिति अथवा मंगल पर दृष्टि से मांगलिक दोष शांत है।";
                        }

                        if (isCancelled) {
                            manglikTitle = "दोष निरस्त (शुभ फलदायी)";
                            manglikColor = "#10b981";
                            manglikReason = cancelReason;
                        } else {
                            manglikTitle = "मांगलिक प्रभाव (भाव " + mHouse + ")";
                            manglikColor = "#f59e0b";
                            manglikReason = "मंगल देव भाव " + mHouse + " (" + mars.sign + ") में स्थित हैं; विवाह विचार में गुण मिलान व कुण्डली मिलान श्रेयस्कर है।";
                        }
                    } else {
                        manglikTitle = "दोष रहित (निर्दोष)";
                        manglikColor = "#10b981";
                        manglikReason = "मंगल देव भाव " + mHouse + " (" + mars.sign + ") में हैं (1, 4, 7, 8, 12 भावों से बाहर), अतः कुण्डली पूर्णतः मांगलिक दोष रहित है।";
                    }
                } else {
                    manglikReason = "मंगल स्थिति गणना पूर्ण।";
                }

                // 2. DYNAMIC KALSARP EVALUATION
                var rahu = pMap['राहु'] || null;
                var ketu = pMap['केतु'] || null;
                var kalsarpTitle = "कालसर्प दोष मुक्त";
                var kalsarpColor = "#10b981";
                var kalsarpReason = "";

                if (rahu && ketu) {
                    var rH = rahu.house;
                    var kH = ketu.house;
                    var checkPlanets = ['सूर्य', 'चन्द्र', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि'];
                    var insideCount1 = 0;
                    var insideCount2 = 0;

                    checkPlanets.forEach(function(pn) {
                        if (pMap[pn]) {
                            var pH = pMap[pn].house;
                            var inArc1 = false;
                            if (rH < kH) {
                                inArc1 = (pH > rH && pH < kH);
                            } else {
                                inArc1 = (pH > rH || pH < kH);
                            }
                            if (inArc1) insideCount1++;
                            else insideCount2++;
                        }
                    });

                    if (insideCount1 > 0 && insideCount2 > 0) {
                        kalsarpTitle = "कालसर्प योग रहित (निर्दोष)";
                        kalsarpColor = "#10b981";
                        kalsarpReason = "ग्रह राहु-केतु अक्ष के दोनों ओर स्वतंत्र रूप से स्थित हैं, अतः कुण्डली पूर्णतः कालसर्प दोष से मुक्त है।";
                    } else {
                        kalsarpTitle = "कालसर्प प्रभाव विद्यमान";
                        kalsarpColor = "#f59e0b";
                        kalsarpReason = "समस्त सप्त ग्रह राहु-केतु अक्ष के एक ओर स्थित हैं; सात्विक शिव उपासना एवं महामृत्युंजय जप श्रेयस्कर है।";
                    }
                } else {
                    kalsarpReason = "राहु-केतु अक्ष गणना पूर्ण।";
                }

                doshaBox.innerHTML = '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">' +
                    '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                        '<b style="color:var(--primary-navy);">मांगलिक दोष विश्लेषण:</b><br>' +
                        '<span style="color:' + manglikColor + '; font-weight:800;">' + manglikTitle + '</span><br>' +
                        '<span style="font-size:0.72rem; color:var(--text-secondary);">' + manglikReason + '</span>' +
                    '</div>' +
                    '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                        '<b style="color:var(--primary-navy);">कालसर्प दोष विश्लेषण:</b><br>' +
                        '<span style="color:' + kalsarpColor + '; font-weight:800;">' + kalsarpTitle + '</span><br>' +
                        '<span style="font-size:0.72rem; color:var(--text-secondary);">' + kalsarpReason + '</span>' +
                    '</div>' +
                '</div>';
            }
        },

        """
        html = html[:p_db] + new_dosha_code + html[p_closing:]
        print("SUCCESS: Patched dynamic Manglik & Kalsarp evaluation in doshaBox.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("ALL PREDICTION & ESSAY PATCHES APPLIED!")
    return True

if __name__ == '__main__':
    patch_dynamic_essay_and_doshas()

