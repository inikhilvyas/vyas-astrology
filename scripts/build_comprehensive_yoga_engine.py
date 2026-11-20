#!/usr/bin/env python3
"""
VYAS ASTRA — Comprehensive Vedic Yoga Engine Builder
Expands VyasYogaEngine in js/vyas_daivagya_engine.js from 10 yogas to 50+ classical yogas
Using raw string literal r'''...''' to ensure all \\n are preserved properly for JS syntax.
"""
import sys, re, os

ENGINE_PATH = r"g:\software\simpa\VYAS\js\vyas_daivagya_engine.js"

with open(ENGINE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "    window.VyasYogaEngine = {"
end_marker = "    // ═══════════════════════════════════════════════════════════════════\n    // MODULE 4: DASHA ENGINE"

if start_marker not in content:
    print("ERROR: start_marker not found!")
    sys.exit(1)

if end_marker not in content:
    print("ERROR: end_marker not found!")
    sys.exit(1)

pos_start = content.find(start_marker)
pos_end = content.find(end_marker)

print(f"Replacing VyasYogaEngine between chars {pos_start} and {pos_end} ...")

NEW_YOGA_ENGINE = r"""    window.VyasYogaEngine = {
        /**
         * Master Yoga Detector — Identifies 50+ classical Vedic Yogas
         * Supports specific query matching and comprehensive chart scanning
         */
        detectAll: function(analysis, chart, queryHint) {
            var q = (queryHint || '').toLowerCase();
            var results = [];

            // 1. SPECIFIC YOGA TARGETING
            if (/केमद्रुम|kemdrum|kendrum/.test(q)) results.push(this.kemdrum(analysis));
            if (/सुनफा|sunapha/.test(q)) results.push(this.sunapha(analysis));
            if (/अनफा|anapha/.test(q)) results.push(this.anapha(analysis));
            if (/दुरुधुरा|durdhura/.test(q)) results.push(this.durdhura(analysis));
            if (/गजकेसरी|gajakesari/.test(q)) results.push(this.gajakesari(analysis));
            if (/चन्द्र.*मंगल|चंद्र.*मंगल|महालक्ष्मी.*योग|chandra.*mangal/.test(q)) results.push(this.chandramangal(analysis));
            if (/अधि.*योग|adhi.*yoga/.test(q)) results.push(this.adhiyoga(analysis));
            if (/वसुमती|vasumati/.test(q)) results.push(this.vasumati(analysis));
            if (/शकट|shakata/.test(q)) results.push(this.shakata(analysis));
            if (/अमला|amala/.test(q)) results.push(this.amala(analysis));
            if (/गौरी|gauri/.test(q)) results.push(this.gauri(analysis));
            if (/पुष्कल|pushkala/.test(q)) results.push(this.pushkala(analysis));

            if (/बुधादित्य|budhaditya/.test(q)) results.push(this.budhaditya(analysis));
            if (/वेशि|वेसी|vesi/.test(q)) results.push(this.vesi(analysis));
            if (/वाशि|वासी|vasi/.test(q)) results.push(this.vasi(analysis));
            if (/उभयचरी|ubhayachari/.test(q)) results.push(this.ubhayachari(analysis));
            if (/भास्कर|bhaskara/.test(q)) results.push(this.bhaskara(analysis));

            if (/रुचक|ruchaka/.test(q)) results.push(this.ruchaka(analysis));
            if (/भद्र|bhadra/.test(q)) results.push(this.bhadra(analysis));
            if (/हंस|hamsa/.test(q)) results.push(this.hamsa(analysis));
            if (/मालव्य|malavya/.test(q)) results.push(this.malavya(analysis));
            if (/शश|sasa|shash/.test(q)) results.push(this.sasa(analysis));
            if (/पंचमहापुरुष|panch.*mahapurush/.test(q)) results = results.concat(this.panchamahapurusha(analysis));

            if (/धर्म.*कर्मा|dharmakarma|9.*10/.test(q)) results.push(this.dharmakarma(analysis));
            if (/परिवर्तन|parivartana/.test(q)) results = results.concat(this.parivartana(analysis));
            if (/नीचभंग|neechabhanga/.test(q)) results.push(this.neechabhanga(analysis));
            if (/विपरीत|viparit|हर्ष|सरल|विमल/.test(q)) results = results.concat(this.vipritraj(analysis));
            if (/लक्ष्मी.*योग|lakshmi.*yoga/.test(q)) results.push(this.lakshmi(analysis));
            if (/सरस्वती|saraswati/.test(q)) results.push(this.saraswati(analysis));
            if (/काहल|kahala/.test(q)) results.push(this.kahala(analysis));
            if (/शंख|shankha/.test(q)) results.push(this.shankha(analysis));
            if (/चामर|chamara/.test(q)) results.push(this.chamara(analysis));
            if (/अखंड.*साम्राज्य|akhanda/.test(q)) results.push(this.akhandasamrajya(analysis));
            if (/महाभाग्य|mahabhagya/.test(q)) results.push(this.mahabhagya(analysis, chart));
            if (/कलानिधि|kalanidhi/.test(q)) results.push(this.kalanidhi(analysis));
            if (/धन.*योग|dhana.*yoga/.test(q)) results = results.concat(this.dhanayogas(analysis));
            if (/राजयोग|raj.*yoga/.test(q)) results = results.concat(this.rajYogas(analysis));

            if (/मंगल.*दोष|mangal.*dosh|kuja|मांगलिक/.test(q)) results.push(this.mangaldosha(analysis));
            if (/काल.*सर्प|kaal.*sarp/.test(q)) results.push(this.kaalsarpa(analysis, chart));
            if (/गुरु.*चांडाल|guru.*chandal/.test(q)) results.push(this.guruchandal(analysis));
            if (/ग्रहण.*योग|grahan.*yoga/.test(q)) results.push(this.grahanyoga(analysis));
            if (/अंगारक|angarak/.test(q)) results.push(this.angarak(analysis));
            if (/श्रापित|shrapit/.test(q)) results.push(this.shrapit(analysis));
            if (/विष.*योग|vish.*yoga/.test(q)) results.push(this.vishyoga(analysis));
            if (/पितृ.*दोष|pitra.*dosh/.test(q)) results.push(this.pitradosha(analysis));
            if (/मातृ.*दोष|matru.*dosh/.test(q)) results.push(this.matrudosha(analysis));
            if (/दरिद्र|daridra/.test(q)) results.push(this.daridra(analysis));
            if (/गंडान्त|gandanta/.test(q)) results.push(this.gandanta(analysis));

            if (/नाभस|रज्जु|मूसल|नल|माला|सर्प योग|nabhasa/.test(q)) results = results.concat(this.nabhasa(analysis));
            if (/वर्गोत्तम|vargottama/.test(q)) results.push(this.vargottama(analysis, chart));

            // If user asked a specific query and we matched it, return those results
            var filtered = results.filter(Boolean);
            if (filtered.length > 0 && !/सब|all|सभी.*योग|मेरी कुण्डली में कौन से योग|योग बताओ/.test(q)) {
                return filtered;
            }

            // 2. COMPREHENSIVE SCAN (Find all formed yogas in chart)
            var fullScan = [];
            // Chandra yogas
            fullScan.push(this.kemdrum(analysis));
            fullScan.push(this.sunapha(analysis));
            fullScan.push(this.anapha(analysis));
            fullScan.push(this.durdhura(analysis));
            fullScan.push(this.gajakesari(analysis));
            fullScan.push(this.chandramangal(analysis));
            fullScan.push(this.adhiyoga(analysis));
            fullScan.push(this.vasumati(analysis));
            fullScan.push(this.shakata(analysis));
            fullScan.push(this.amala(analysis));

            // Surya yogas
            fullScan.push(this.budhaditya(analysis));
            fullScan.push(this.vesi(analysis));
            fullScan.push(this.vasi(analysis));
            fullScan.push(this.ubhayachari(analysis));

            // Pancha Mahapurusha
            fullScan = fullScan.concat(this.panchamahapurusha(analysis));

            // Raja & Dhana Yogas
            fullScan.push(this.dharmakarma(analysis));
            fullScan = fullScan.concat(this.rajYogas(analysis));
            fullScan = fullScan.concat(this.parivartana(analysis));
            fullScan.push(this.neechabhanga(analysis));
            fullScan = fullScan.concat(this.vipritraj(analysis));
            fullScan.push(this.lakshmi(analysis));
            fullScan.push(this.saraswati(analysis));
            fullScan.push(this.akhandasamrajya(analysis));
            fullScan = fullScan.concat(this.dhanayogas(analysis));

            // Doshas & Arishta
            fullScan.push(this.mangaldosha(analysis));
            fullScan.push(this.kaalsarpa(analysis, chart));
            fullScan.push(this.guruchandal(analysis));
            fullScan.push(this.grahanyoga(analysis));
            fullScan.push(this.angarak(analysis));
            fullScan.push(this.shrapit(analysis));
            fullScan.push(this.vishyoga(analysis));
            fullScan.push(this.pitradosha(analysis));
            fullScan.push(this.daridra(analysis));
            fullScan.push(this.gandanta(analysis));

            // Filter out nulls and yogas not found unless partial/bhanga
            return fullScan.filter(function(y) {
                return y && (y.found === true || y.partial === true);
            });
        },

        // ═══════════════════════════════════════════════════════════════
        // A. CHANDRA YOGAS (चन्द्र योग)
        // ═══════════════════════════════════════════════════════════════
        kemdrum: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return { name: 'केमद्रुम योग', found: false, detail: 'चन्द्र डेटा अनुपलब्ध' };
            var mH = moon.house;
            var h2 = (mH % 12) + 1, h12 = ((mH - 2 + 12) % 12) + 1;
            var neighbors = Object.entries(a.planets).filter(function(e) {
                var pn = e[0], pd = e[1];
                return pn !== 'चन्द्र' && pn !== 'राहु' && pn !== 'केतु' && pn !== 'सूर्य' &&
                       (pd.house === h2 || pd.house === h12);
            });
            if (neighbors.length > 0) {
                return { name: 'केमद्रुम योग', found: false,
                    detail: '❌ **केमद्रुम योग अनुपस्थित** — चन्द्रमा (भाव ' + mH + ', ' + moon.sign + ') के 2रे (भाव ' + h2 + ') व 12वें (भाव ' + h12 + ') में शुभ/अन्य ग्रह विद्यमान हैं: **' + neighbors.map(function(e){return e[0]}).join(', ') + '**।' };
            }
            // Check bhanga
            var bhangas = [];
            if (KENDRAS.indexOf(mH) !== -1) bhangas.push('चन्द्रमा लग्न से केन्द्र (भाव ' + mH + ') में स्थित है');
            if (moon.sign === 'कर्क' || moon.sign === 'वृषभ') bhangas.push('चन्द्रमा ' + (moon.sign === 'वृषभ' ? 'उच्च' : 'स्वराशि') + ' में है');
            var sun = a.planets['सूर्य'];
            if (sun) {
                var moonFromSun = ((mH - sun.house + 12) % 12) + 1;
                if (KENDRAS.indexOf(moonFromSun) !== -1) bhangas.push('चन्द्रमा सूर्य से केन्द्र भाव में है');
            }
            var benefAspects = BENEFICS.filter(function(b) {
                var bp = a.planets[b];
                return bp && aspectsHouse(bp.house, mH, b);
            });
            if (benefAspects.length) bhangas.push('शुभ ग्रहों की दृष्टि: ' + benefAspects.join(', '));

            if (bhangas.length) {
                return { name: 'केमद्रुम भंग राजयोग', found: true, partial: true,
                    detail: '⚠️ **केमद्रुम योग का आधार निर्मित होकर पूर्णतः भंग (केमद्रुम भंग राजयोग):**\n' +
                            bhangas.map(function(b){ return '• ' + b; }).join('\n') + '\n\n' +
                            '**शास्त्रीय निर्णय:** शास्त्रों के अनुसार केमद्रुम भंग होने पर दरिद्रता का नाश होता है। प्रारंभिक जीवन में संघर्ष व मानसिक एकाकीपन के उपरांत जातक स्वप्रयासों से अकूत सफलता प्राप्त करता है।\n\n' +
                            '**सात्विक उपाय:** सोमवार शिव जल/दूध अभिषेक, चांदी धारण, माता का चरण स्पर्श।' };
            }
            return { name: 'केमद्रुम योग', found: true, partial: false,
                detail: '🔴 **पूर्ण केमद्रुम योग उपस्थित**\n\n' +
                        '**शास्त्रीय सूत्र:** "द्वादशे द्वितीये वापि चन्द्रान्नीचे ग्रहैर्विना। केमद्रुमाख्यो योगोऽयं दुःखदारिद्र्यकारकः॥" (बृहत्पाराशर)\n\n' +
                        '**स्थिति:** चन्द्रमा भाव ' + mH + ' (' + moon.sign + ') में एकाकी हैं। 2रे (भाव ' + h2 + ') व 12वें (भाव ' + h12 + ') में कोई ग्रह नहीं है।\n\n' +
                        '**प्रभाव:** विचारों में अस्थिरता, मानसिक एकाकीपन, कभी-कभी आकस्मिक वित्तीय उतार-चढ़ाव।\n\n' +
                        '**अचूक सात्विक उपाय:**\n1. प्रत्येक सोमवार शिवलिंग पर कच्चा दूध व जल अर्पित करें।\n2. कनिष्ठिका उंगली में चांदी का छल्ला धारण करें।\n3. नित्य "ॐ सों सोमाय नमः" का 108 बार मानसिक जप करें।' };
        },

        sunapha: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return null;
            var h2 = (moon.house % 12) + 1;
            var pIn2 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h2 && ['सूर्य','राहु','केतु','चन्द्र'].indexOf(e[0]) === -1;
            });
            if (pIn2.length > 0) {
                var pNames = pIn2.map(function(e){ return e[0]; }).join(', ');
                return { name: 'सुनफा योग (Sunapha Yoga)', found: true,
                    detail: '✦ **शुभ सुनफा योग उपस्थित**\n' +
                            '**शास्त्रीय आधार:** चन्द्रमा (भाव ' + moon.house + ') से द्वितीय भाव (भाव ' + h2 + ') में ग्रह (' + pNames + ') स्थित होने से सुनफा योग बनता है।\n' +
                            '**फल:** जातक स्वअर्जित संपत्ति, उत्तम विद्या, बुद्धिमत्ता, समाज में मान-प्रतिष्ठा एवं ऐश्वर्यवान जीवन व्यतीत करता है।\n' +
                            '**उपाय:** इष्टदेव की नित्य आराधना करें तथा शुभ कर्मों में धन का सदुपयोग करें।' };
            }
            return null;
        },

        anapha: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return null;
            var h12 = ((moon.house - 2 + 12) % 12) + 1;
            var pIn12 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h12 && ['सूर्य','राहु','केतु','चन्द्र'].indexOf(e[0]) === -1;
            });
            if (pIn12.length > 0) {
                var pNames = pIn12.map(function(e){ return e[0]; }).join(', ');
                return { name: 'अनफा योग (Anapha Yoga)', found: true,
                    detail: '✦ **शुभ अनफा योग उपस्थित**\n' +
                            '**शास्त्रीय आधार:** चन्द्रमा से द्वादश भाव (भाव ' + h12 + ') में ग्रह (' + pNames + ') स्थित होने से अनफा योग निर्मित होता है।\n' +
                            '**फल:** जातक निरोगी काया, उदार चित्त, उत्तम शील, नीतिज्ञ एवं समाज में लोकप्रिय होता है।\n' +
                            '**उपाय:** नित्य सूर्य अर्घ्य दें एवं संध्या समय शिव स्मरण करें।' };
            }
            return null;
        },

        durdhura: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return null;
            var h2 = (moon.house % 12) + 1;
            var h12 = ((moon.house - 2 + 12) % 12) + 1;
            var pIn2 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h2 && ['सूर्य','राहु','केतु','चन्द्र'].indexOf(e[0]) === -1;
            });
            var pIn12 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h12 && ['सूर्य','राहु','केतु','चन्द्र'].indexOf(e[0]) === -1;
            });
            if (pIn2.length > 0 && pIn12.length > 0) {
                return { name: 'दुरुधुरा योग (Durdhura Yoga)', found: true,
                    detail: '✦ **अति-शुभ दुरुधुरा योग उपस्थित**\n' +
                            '**शास्त्रीय आधार:** चन्द्रमा के दोनों ओर द्वितीय (भाव ' + h2 + ') व द्वादश (भाव ' + h12 + ') में शुभ/अन्य ग्रह स्थित हैं।\n' +
                            '**फल:** जातक अपार धन, वाहन सुख, उदार हृदय, स्थिर बुद्धि एवं उच्च सामाजिक प्रतिष्ठा का स्वामी होता है।\n' +
                            '**उपाय:** श्री सूक्त का नियमित पाठ करें।' };
            }
            return null;
        },

        gajakesari: function(a) {
            var moon = a.planets['चन्द्र'], guru = a.planets['गुरु'];
            if (!moon || !guru) return { name: 'गजकेसरी योग', found: false, detail: 'चन्द्र/गुरु डेटा अनुपलब्ध' };
            var fromMoon = ((guru.house - moon.house + 12) % 12) + 1;
            var fromLagna = guru.house;
            if (KENDRAS.indexOf(fromMoon) !== -1 || KENDRAS.indexOf(fromLagna) !== -1) {
                var deb = guru.sign === 'मकर';
                return { name: 'गजकेसरी योग' + (deb ? ' (नीचस्थ - आंशिक)' : ''), found: true, partial: deb,
                    detail: '✦ **परम शुभ गजकेसरी योग उपस्थित**\n' +
                            '**शास्त्रीय सूत्र:** "केन्द्रे देवगुरौ लग्नाच्चन्द्राद्वापि यदा स्थितः। कीटारिभ्रष्टहीनोऽयं गजकेसरीयोगकृत्॥" (बृहत्पाराशर)\n' +
                            '**स्थिति:** देवगुरु बृहस्पति (भाव ' + guru.house + ', ' + guru.sign + ') चन्द्रमा (भाव ' + moon.house + ') से ' + fromMoon + 'वें (केन्द्र) भाव में संचरण कर रहे हैं।\n' +
                            '**फल:** दीर्घायु, तीव्र मेधा, उत्कृष्ट सामाजिक प्रतिष्ठा, संकटों में ईश्वरीय संरक्षण एवं स्थायी समृद्धि।\n' +
                            '**उपाय:** गुरुवार को चने की दाल व गुड़ गाय को खिलाएं, "ॐ बृं बृहस्पतये नमः" का जप करें।' };
            }
            return { name: 'गजकेसरी योग', found: false,
                detail: '❌ **गजकेसरी योग अनुपस्थित** — चन्द्रमा से देवगुरु बृहस्पति केन्द्र भाव (1, 4, 7, 10) में स्थित नहीं हैं (वर्तमान में ' + fromMoon + 'वें भाव में हैं)।' };
        },

        chandramangal: function(a) {
            var moon = a.planets['चन्द्र'], mars = a.planets['मंगल'];
            if (!moon || !mars) return null;
            var sameHouse = moon.house === mars.house;
            var mutual7th = ((mars.house - moon.house + 12) % 12) + 1 === 7;
            if (sameHouse || mutual7th) {
                return { name: 'चन्द्र-मंगल योग (महालक्ष्मी योग)', found: true,
                    detail: '✦ **चन्द्र-मंगल (महालक्ष्मी) योग उपस्थित**\n' +
                            '**स्थिति:** चन्द्रमा (भाव ' + moon.house + ') एवं मंगल (भाव ' + mars.house + ') परस्पर ' + (sameHouse ? 'युति' : 'सप्तम दृष्टि सम्बन्ध') + ' में हैं।\n' +
                            '**फल:** यह शक्तिशाली धन प्रदायक योग है। जातक उद्यमी, व्यापारिक बुद्धि से युक्त, भूमि-भवन लाभ एवं आकस्मिक वित्तीय लाभ प्राप्त करता है।\n' +
                            '**उपाय:** मंगलवार को मीठी रोटी गाय को दें एवं कनकधारा स्तोत्र का पाठ करें।' };
            }
            return null;
        },

        adhiyoga: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return null;
            var mH = moon.house;
            var h6 = ((mH + 5) % 12) + 1, h7 = ((mH + 6) % 12) + 1, h8 = ((mH + 7) % 12) + 1;
            var beneficsIn678 = BENEFICS.filter(function(b){
                var bp = a.planets[b];
                return bp && (bp.house === h6 || bp.house === h7 || bp.house === h8);
            });
            if (beneficsIn678.length >= 2) {
                return { name: 'चांद्र अधि योग (Chandra Adhi Yoga)', found: true,
                    detail: '✦ **दुर्लभ चांद्र अधि योग उपस्थित**\n' +
                            '**शास्त्रीय सूत्र:** चन्द्रमा से 6, 7, 8वें भाव में शुभ ग्रह (' + beneficsIn678.join(', ') + ') स्थित हैं।\n' +
                            '**फल:** यह जातक को सेनापति, मंत्री, उच्च प्रशासक, शत्रुओं पर अजेय विजय एवं अखंड ऐश्वर्य प्रदान करता है।\n' +
                            '**उपाय:** श्री सूक्त व विष्णु सहस्रनाम का नियमित श्रवण करें।' };
            }
            return null;
        },

        vasumati: function(a) {
            var upachayas = [3, 6, 10, 11];
            var countLagna = 0, countMoon = 0;
            var moon = a.planets['चन्द्र'];
            BENEFICS.forEach(function(b){
                var bp = a.planets[b];
                if (bp) {
                    if (upachayas.indexOf(bp.house) !== -1) countLagna++;
                    if (moon) {
                        var fromM = ((bp.house - moon.house + 12) % 12) + 1;
                        if (upachayas.indexOf(fromM) !== -1) countMoon++;
                    }
                }
            });
            if (countLagna >= 3 || countMoon >= 3) {
                return { name: 'वसुमती योग (Vasumati Yoga)', found: true,
                    detail: '✦ **परम धनदायक वसुमती योग उपस्थित**\n' +
                            '**शास्त्रीय आधार:** उपचय भावों (3, 6, 10, 11) में 3 या अधिक शुभ ग्रह संचरण कर रहे हैं।\n' +
                            '**फल:** जातक कभी पराधीन नहीं रहता, अपने बाहुबल से अकूत धन-संपत्ति अर्जित करता है और राजतुल्य जीवन जीता है।' };
            }
            return null;
        },

        shakata: function(a) {
            var moon = a.planets['चन्द्र'], guru = a.planets['गुरु'];
            if (!moon || !guru) return null;
            var fromGuru = ((moon.house - guru.house + 12) % 12) + 1;
            if ([6, 8, 12].indexOf(fromGuru) !== -1) {
                var isBhanga = (KENDRAS.indexOf(moon.house) !== -1) || (moon.sign === 'वृषभ' || moon.sign === 'कर्क');
                if (isBhanga) {
                    return { name: 'शकट योग (भंग)', found: true, partial: true,
                        detail: '⚠️ **शकट योग निर्मित होकर भंग:** चन्द्रमा गुरु से ' + fromGuru + 'वें भाव में है, किन्तु चन्द्रमा के केन्द्रस्थ/उच्चस्थ होने से दोष निष्प्रभावी हो गया है।\n' +
                                '**उपाय:** शिव पंचाक्षर मंत्र "ॐ नमः शिवाय" का जप करें।' };
                }
                return { name: 'शकट योग (Shakata Yoga)', found: true, partial: false,
                    detail: '🔴 **शकट योग उपस्थित:** चन्द्रमा देवगुरु से ' + fromGuru + 'वें (त्रिक) भाव में स्थित हैं।\n' +
                            '**फल:** जीवन में गाड़ी के पहिये की भांति उतार-चढ़ाव, कभी अपार संपन्नता तो कभी संघर्ष।\n' +
                            '**उपाय:** पूर्णिमा का व्रत अथवा चन्द्र अर्घ्य दें, गुरु मंत्र का जप करें।' };
            }
            return null;
        },

        amala: function(a) {
            var beneficsIn10 = BENEFICS.filter(function(b){
                var bp = a.planets[b];
                return bp && bp.house === 10;
            });
            if (beneficsIn10.length > 0) {
                return { name: 'अमला योग (Amala Yoga)', found: true,
                    detail: '✦ **अमला योग उपस्थित:** दशम (कर्म) भाव में शुभ ग्रह (' + beneficsIn10.join(', ') + ') स्थित हैं।\n' +
                            '**फल:** निष्कलंक कीर्ति, परोपकारी स्वभाव, राजदरबार/शासन में सम्मान एवं स्थायी आजीविका।' };
            }
            return null;
        },

        gauri: function(a) {
            var moon = a.planets['चन्द्र'], guru = a.planets['गुरु'];
            if (!moon || !guru) return null;
            if ((moon.sign === 'कर्क' || moon.sign === 'वृषभ') && aspectsHouse(guru.house, moon.house, 'गुरु')) {
                return { name: 'गौरी योग (Gauri Yoga)', found: true,
                    detail: '✦ **परम पावन गौरी योग उपस्थित:** चन्द्रमा स्व/उच्च राशि में हैं तथा देवगुरु बृहस्पति की पूर्ण अमृत दृष्टि से युक्त हैं।\n' +
                            '**फल:** दिव्य आकर्षण, सुंदर रूप, पवित्र चरित्र, ऐश्वर्य एवं माता का विशेष संबल।' };
            }
            return null;
        },

        pushkala: function(a) {
            var moon = a.planets['चन्द्र'];
            if (!moon) return null;
            var moonLord = LORDS[moon.sign];
            var mlData = a.planets[moonLord];
            var lagnaLordData = a.planets[a.lagnaLord];
            if (mlData && KENDRAS.indexOf(mlData.house) !== -1 && lagnaLordData) {
                return { name: 'पुष्कल योग (Pushkala Yoga)', found: true,
                    detail: '✦ **पुष्कल योग उपस्थित:** चन्द्र राशि का अधिपति केन्द्र में बली है। जातक विद्वान, धनी एवं प्रसिद्ध होता है।' };
            }
            return null;
        },

        // ═══════════════════════════════════════════════════════════════
        // B. SURYA YOGAS (सौर योग)
        // ═══════════════════════════════════════════════════════════════
        budhaditya: function(a) {
            var sun = a.planets['सूर्य'], merc = a.planets['बुध'];
            if (!sun || !merc) return { name: 'बुधादित्य योग', found: false, detail: 'सूर्य/बुध डेटा अनुपलब्ध' };
            if (sun.house === merc.house) {
                var diffDeg = Math.abs(sun.deg - merc.deg);
                var isCombust = diffDeg < 14.0;
                return { name: 'बुधादित्य योग' + (isCombust ? ' (अस्त - आंशिक)' : ''), found: true, partial: isCombust,
                    detail: '✦ **बुधादित्य योग उपस्थित**\n' +
                            '**स्थिति:** सूर्य एवं बुध दोनों भाव ' + sun.house + ' (' + sun.sign + ' राशि) में परस्पर ' + diffDeg.toFixed(1) + '° की दूरी पर स्थित हैं। ' +
                            (isCombust ? 'बुध सूर्य के समीप (14° के भीतर) होने से अस्त हैं, अतः यह योग बौद्धिक तेज तो देता है किंतु कभी-कभी एकाग्रता में चंचलता लाता है।' : 'बुध पूर्ण उदित होकर प्रखर राजयोग फल दे रहे हैं।') + '\n\n' +
                            '**फल:** तीव्र बुद्धि, उत्कृष्ट गणितीय/तार्किक विश्लेषण, प्रभावी वाणी, प्रशासनिक व तकनीकी सिद्धि।\n\n' +
                            '**उपाय:** नित्य प्रातः सूर्य देव को तांबे के लोटे से अर्घ्य दें, बुधवार को हरी मूंग पक्षियों को डालें।' };
            }
            return { name: 'बुधादित्य योग', found: false,
                detail: '❌ **बुधादित्य योग अनुपस्थित** — सूर्य (भाव ' + sun.house + ') एवं बुध (भाव ' + merc.house + ') भिन्न भावों में हैं।' };
        },

        vesi: function(a) {
            var sun = a.planets['सूर्य'];
            if (!sun) return null;
            var h2 = (sun.house % 12) + 1;
            var pIn2 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h2 && ['चन्द्र','राहु','केतु','सूर्य'].indexOf(e[0]) === -1;
            });
            if (pIn2.length > 0) {
                var pNames = pIn2.map(function(e){ return e[0]; }).join(', ');
                var isBenefic = pIn2.some(function(e){ return BENEFICS.indexOf(e[0]) !== -1; });
                return { name: 'वेशि योग (' + (isBenefic ? 'शुभ वेशि' : 'पाप वेशि') + ')', found: true,
                    detail: '✦ **' + (isBenefic ? 'शुभ वेशि' : 'पाप वेशि') + ' योग उपस्थित:** सूर्य से द्वितीय भाव में ' + pNames + ' स्थित हैं।\n' +
                            '**फल:** ' + (isBenefic ? 'सत्यवादी, तेजस्वी, धनवान व यशस्वी जीवन।' : 'कठिन परिश्रम उपरांत सिद्धि।') };
            }
            return null;
        },

        vasi: function(a) {
            var sun = a.planets['सूर्य'];
            if (!sun) return null;
            var h12 = ((sun.house - 2 + 12) % 12) + 1;
            var pIn12 = Object.entries(a.planets).filter(function(e){
                return e[1].house === h12 && ['चन्द्र','राहु','केतु','सूर्य'].indexOf(e[0]) === -1;
            });
            if (pIn12.length > 0) {
                var pNames = pIn12.map(function(e){ return e[0]; }).join(', ');
                return { name: 'वाशि योग (Vasi Yoga)', found: true,
                    detail: '✦ **वाशि योग उपस्थित:** सूर्य से द्वादश भाव में ग्रह (' + pNames + ') स्थित हैं। जातक बुद्धिमान, विद्यावान व प्रतापी होता है।' };
            }
            return null;
        },

        ubhayachari: function(a) {
            var sun = a.planets['सूर्य'];
            if (!sun) return null;
            var h2 = (sun.house % 12) + 1;
            var h12 = ((sun.house - 2 + 12) % 12) + 1;
            var pIn2 = Object.entries(a.planets).filter(function(e){ return e[1].house === h2 && ['चन्द्र','राहु','केतु','सूर्य'].indexOf(e[0]) === -1; });
            var pIn12 = Object.entries(a.planets).filter(function(e){ return e[1].house === h12 && ['चन्द्र','राहु','केतु','सूर्य'].indexOf(e[0]) === -1; });
            if (pIn2.length > 0 && pIn12.length > 0) {
                return { name: 'उभयचरी योग (Ubhayachari Yoga)', found: true,
                    detail: '✦ **उभयचरी योग उपस्थित:** सूर्य के दोनों ओर (2रे व 12वें भाव में) ग्रह स्थित हैं। जातक राजा या सरकार का कृपापात्र, स्थिर बुद्धि व सर्वप्रिय होता है।' };
            }
            return null;
        },

        bhaskara: function(a) {
            var sun = a.planets['सूर्य'], moon = a.planets['चन्द्र'], merc = a.planets['बुध'], guru = a.planets['गुरु'];
            if (!sun || !moon || !merc || !guru) return null;
            var sunFromMoon = ((sun.house - moon.house + 12) % 12) + 1;
            var mercFromSun = ((merc.house - sun.house + 12) % 12) + 1;
            var guruFromMoon = ((guru.house - moon.house + 12) % 12) + 1;
            if (sunFromMoon === 2 && (mercFromSun === 2 || mercFromSun === 3) && (guruFromMoon === 5 || guruFromMoon === 9)) {
                return { name: 'भास्कर योग (Bhaskara Yoga)', found: true,
                    detail: '✦ **दिव्य भास्कर योग उपस्थित:** सूर्य, बुध व गुरु का पावन त्रिकोण/केन्द्र संरेखण। जातक प्रतापी, संगीत/कला मर्मज्ञ एवं सर्वशास्त्र ज्ञाता होता है।' };
            }
            return null;
        },

        // ═══════════════════════════════════════════════════════════════
        // C. PANCHA MAHAPURUSHA YOGAS (पंचमहापुरुष योग)
        // ═══════════════════════════════════════════════════════════════
        ruchaka: function(a) {
            var mars = a.planets['मंगल'];
            if (!mars) return null;
            if (KENDRAS.indexOf(mars.house) !== -1 && ['मेष','वृश्चिक','मकर'].indexOf(mars.sign) !== -1) {
                return { name: 'रुचक महापुरुष योग (Ruchaka Yoga)', found: true,
                    detail: '✦ **रुचक पंचमहापुरुष योग उपस्थित**\n' +
                            '**स्थिति:** मंगल देव भाव ' + mars.house + ' में ' + mars.sign + ' (' + (mars.sign === 'मकर' ? 'उच्च' : 'स्वराशि') + ') होकर केन्द्र में विराजमान हैं।\n' +
                            '**फल:** असाधारण पराक्रम, साहस, भूमि-भवन स्वामित्त्व, उच्च तकनीकी या प्रशासनिक पद, विरोधियों पर पूर्ण विजय।\n' +
                            '**उपाय:** मंगलवार हनुमान चालीसा पाठ करें।' };
            }
            return null;
        },

        bhadra: function(a) {
            var merc = a.planets['बुध'];
            if (!merc) return null;
            if (KENDRAS.indexOf(merc.house) !== -1 && ['मिथुन','कन्या'].indexOf(merc.sign) !== -1) {
                return { name: 'भद्र महापुरुष योग (Bhadra Yoga)', found: true,
                    detail: '✦ **भद्र पंचमहापुरुष योग उपस्थित**\n' +
                            '**स्थिति:** बुध देव भाव ' + merc.house + ' में ' + merc.sign + ' (' + (merc.sign === 'कन्या' ? 'उच्च' : 'स्वराशि') + ') होकर केन्द्र में स्थित हैं।\n' +
                            '**फल:** कुशाग्र मेधा, वाणी का जादू, व्यापार/वाणिज्य में शीर्ष सफलता, गणितज्ञ, उत्कृष्ट सलाहकार।\n' +
                            '**उपाय:** बुधवार को पक्षियों को हरी मूंग डालें।' };
            }
            return null;
        },

        hamsa: function(a) {
            var guru = a.planets['गुरु'];
            if (!guru) return null;
            if (KENDRAS.indexOf(guru.house) !== -1 && ['धनु','मीन','कर्क'].indexOf(guru.sign) !== -1) {
                return { name: 'हंस महापुरुष योग (Hamsa Yoga)', found: true,
                    detail: '✦ **हंस पंचमहापुरुष योग उपस्थित**\n' +
                            '**स्थिति:** देवगुरु बृहस्पति भाव ' + guru.house + ' में ' + guru.sign + ' (' + (guru.sign === 'कर्क' ? 'उच्च' : 'स्वराशि') + ') होकर केन्द्र में स्थित हैं।\n' +
                            '**फल:** धर्मनिष्ठता, आध्यात्मिक ज्ञान, समाज में पूज्यनीय पद, राजसम्मान, आदर्श गुरु व मार्गदर्शक का जीवन।\n' +
                            '**उपाय:** गुरुवार को गुरु मंत्र का जप करें, माता-पिता/गुरु का चरण स्पर्श करें।' };
            }
            return null;
        },

        malavya: function(a) {
            var ven = a.planets['शुक्र'];
            if (!ven) return null;
            if (KENDRAS.indexOf(ven.house) !== -1 && ['वृषभ','तुला','मीन'].indexOf(ven.sign) !== -1) {
                return { name: 'मालव्य महापुरुष योग (Malavya Yoga)', found: true,
                    detail: '✦ **मालव्य पंचमहापुरुष योग उपस्थित**\n' +
                            '**स्थिति:** शुक्र देव भाव ' + ven.house + ' में ' + ven.sign + ' (' + (ven.sign === 'मीन' ? 'उच्च' : 'स्वराशि') + ') होकर केन्द्र में स्थित हैं।\n' +
                            '**फल:** राजसी सुख, वाहन, कला/सौंदर्य में सिद्धि, उत्तम दांपत्य, जनआकर्षण एवं प्रचुर वैभव।\n' +
                            '**उपाय:** शुक्रवार को श्वेत वस्तुओं का दान करें, श्री सूक्त का पाठ करें।' };
            }
            return null;
        },

        sasa: function(a) {
            var sat = a.planets['शनि'];
            if (!sat) return null;
            if (KENDRAS.indexOf(sat.house) !== -1 && ['मकर','कुंभ','तुला'].indexOf(sat.sign) !== -1) {
                return { name: 'शश महापुरुष योग (Sasa Yoga)', found: true,
                    detail: '✦ **शश पंचमहापुरुष योग उपस्थित**\n' +
                            '**स्थिति:** न्याय के देवता शनि देव भाव ' + sat.house + ' में ' + sat.sign + ' (' + (sat.sign === 'तुला' ? 'उच्च' : 'स्वराशि') + ') होकर केन्द्र में स्थित हैं।\n' +
                            '**फल:** दीर्घायु, गहन कूटनीति, जनसमूह का नेतृत्व, न्यायप्रियता, अचल संपत्ति, कठोर परिश्रम से स्थायी साम्राज्य निर्माण।\n' +
                            '**उपाय:** शनिवार को निर्धनों को भोजन कराएं, पीपल तले दीप जलाएं।' };
            }
            return null;
        },

        panchamahapurusha: function(a) {
            var res = [];
            var r = this.ruchaka(a); if(r) res.push(r);
            var b = this.bhadra(a); if(b) res.push(b);
            var h = this.hamsa(a); if(h) res.push(h);
            var m = this.malavya(a); if(m) res.push(m);
            var s = this.sasa(a); if(s) res.push(s);
            return res;
        },

        // ═══════════════════════════════════════════════════════════════
        // D. RAJA YOGAS & DHANA YOGAS (राजयोग एवं धन योग)
        // ═══════════════════════════════════════════════════════════════
        dharmakarma: function(a) {
            var l9 = a.houses[9].lord, l10 = a.houses[10].lord;
            if (!l9 || !l10) return null;
            var p9 = a.planets[l9], p10 = a.planets[l10];
            if (!p9 || !p10) return null;
            var isConjoined = p9.house === p10.house;
            var isMutualAspect = ((p10.house - p9.house + 12) % 12) + 1 === 7;
            var isExchange = p9.house === 10 && p10.house === 9;
            if (isConjoined || isMutualAspect || isExchange) {
                return { name: 'धर्म-कर्माधिपति राजयोग (Dharma-Karma Raja Yoga)', found: true,
                    detail: '✦ **सर्वोच्च धर्म-कर्माधिपति राजयोग उपस्थित**\n' +
                            '**शास्त्रीय सूत्र:** नवमेश (' + l9 + ') और दशमेश (' + l10 + ') का परस्पर ' + (isExchange ? 'राशि परिवर्तन' : (isConjoined ? 'युति संबंध' : 'सप्तम दृष्टि संबंध')) + ' है।\n' +
                            '**फल:** यह कुण्डली का मुकुटमणि राजयोग है। जातक को उच्च पद, नीति निर्धारण की शक्ति, समाज में अमिट कीर्ति एवं धर्मनिष्ठ सफलता प्रदान करता है।\n' +
                            '**उपाय:** नित्य सूर्य अर्घ्य एवं कुलदेवता की वंदना करें।' };
            }
            return null;
        },

        rajYogas: function(a) {
            var kendraLords = [a.houses[1].lord, a.houses[4].lord, a.houses[7].lord, a.houses[10].lord].filter(Boolean);
            var trikonaLords = [a.houses[1].lord, a.houses[5].lord, a.houses[9].lord].filter(Boolean);
            var pairs = [];
            kendraLords.forEach(function(kl) {
                trikonaLords.forEach(function(tl) {
                    if (kl !== tl) {
                        var kp = a.planets[kl], tp = a.planets[tl];
                        if (kp && tp && kp.house === tp.house) {
                            var pairKey = [kl, tl].sort().join('+');
                            if (pairs.indexOf(pairKey) === -1) {
                                pairs.push(pairKey);
                            }
                        }
                    }
                });
            });
            if (pairs.length > 0) {
                return [{
                    name: 'केन्द्र-त्रिकोण राजयोग (' + pairs.join(', ') + ')',
                    found: true,
                    detail: '✦ **केन्द्र-त्रिकोण राजयोग उपस्थित** (' + pairs.join(', ') + ')\n' +
                            '**शास्त्रीय आधार:** केन्द्र के स्वामी एवं त्रिकोण के स्वामियों की शुभ युति जातक को समाज में अधिकार, समृद्धि व भाग्य का सतत सहयोग प्रदान करती है।'
                }];
            }
            return [];
        },

        parivartana: function(a) {
            var exchanges = [];
            for (var h1 = 1; h1 <= 12; h1++) {
                for (var h2 = h1 + 1; h2 <= 12; h2++) {
                    var l1 = a.houses[h1].lord, l2 = a.houses[h2].lord;
                    if (l1 && l2 && l1 !== l2) {
                        var p1 = a.planets[l1], p2 = a.planets[l2];
                        if (p1 && p2 && p1.house === h2 && p2.house === h1) {
                            var isDusthana = DUSTHANAS.indexOf(h1) !== -1 || DUSTHANAS.indexOf(h2) !== -1;
                            var type = isDusthana ? 'दैन्य परिवर्तन योग' : 'महा परिवर्तन राजयोग';
                            exchanges.push({
                                name: type + ' (भाव ' + h1 + ' ↔ भाव ' + h2 + ')',
                                found: true,
                                partial: isDusthana,
                                detail: '✦ **' + type + ' उपस्थित:** भाव ' + h1 + ' के स्वामी (' + l1 + ') एवं भाव ' + h2 + ' के स्वामी (' + l2 + ') के मध्य परस्पर राशि परिवर्तन है। ' +
                                        (isDusthana ? 'यह जीवन में कड़े संघर्ष के बाद अप्रत्याशित सफलता दिलाता है।' : 'यह दोनों भावों को अत्यंत शक्तिशाली राजयोग बल प्रदान करता है।')
                            });
                        }
                    }
                }
            }
            return exchanges;
        },

        neechabhanga: function(a) {
            var debPlanets = [];
            Object.entries(a.planets).forEach(function(e) {
                var pName = e[0], pd = e[1];
                if (DEBIL[pName] === pd.sign) debPlanets.push({ name: pName, data: pd });
            });
            if (debPlanets.length === 0) return { name: 'नीचभंग राजयोग', found: false, detail: 'कुण्डली में कोई ग्रह नीच राशि में नहीं है।' };

            var results = [];
            debPlanets.forEach(function(dp) {
                var p = dp.name, d = dp.data;
                var debSign = d.sign;
                var debLord = LORDS[debSign];
                var debLordData = a.planets[debLord];
                var exaltLord = LORDS[EXALT[p]];
                var exaltLordData = a.planets[exaltLord];
                var moon = a.planets['चन्द्र'];

                var reasons = [];
                if (debLordData && KENDRAS.indexOf(debLordData.house) !== -1) reasons.push('नीच राशि का स्वामी (' + debLord + ') लग्न से केन्द्र में है');
                if (moon && debLordData) {
                    var fromMoon = ((debLordData.house - moon.house + 12) % 12) + 1;
                    if (KENDRAS.indexOf(fromMoon) !== -1) reasons.push('नीच राशि का स्वामी चन्द्र से केन्द्र में है');
                }
                if (exaltLordData && KENDRAS.indexOf(exaltLordData.house) !== -1) reasons.push('उस ग्रह की उच्च राशि का स्वामी (' + exaltLord + ') केन्द्र में है');
                if (d.retro) reasons.push('ग्रह वक्री होकर चेष्टा बली है');

                if (reasons.length > 0) {
                    results.push({
                        name: 'नीचभंग राजयोग (' + p + ')',
                        found: true,
                        detail: '✦ **' + p + ' का नीचभंग राजयोग उपस्थित**\n' +
                                '**शास्त्रीय नियम:** ' + reasons.join('; ') + '।\n' +
                                '**फल:** यह ग्रह प्रारंभिक जीवन में नीचता का अनुभव कराने के उपरांत राजा के समान वैभव, अधिकार एवं असाधारण प्रतिष्ठा प्रदान करता है।'
                    });
                }
            });
            return results.length > 0 ? results[0] : { name: 'नीचभंग राजयोग', found: false, detail: 'नीच ग्रह उपस्थित हैं किंतु नीचभंग की अनिवार्य शर्तें अपूर्ण हैं।' };
        },

        vipritraj: function(a) {
            var res = [];
            var h6Lord = a.houses[6].lord, h8Lord = a.houses[8].lord, h12Lord = a.houses[12].lord;
            var p6 = a.planets[h6Lord], p8 = a.planets[h8Lord], p12 = a.planets[h12Lord];

            if (p6 && (p6.house === 8 || p6.house === 12)) {
                res.push({ name: 'हर्ष विपरीत राजयोग (Harsha Yoga)', found: true,
                    detail: '✦ **हर्ष विपरीत राजयोग उपस्थित:** 6ठे भाव के स्वामी (' + h6Lord + ') भाव ' + p6.house + ' में स्थित हैं। शत्रुहंता, उत्तम स्वास्थ्य, संकटों पर विजय एवं अप्रत्याशित लाभ।' });
            }
            if (p8 && (p8.house === 6 || p8.house === 12)) {
                res.push({ name: 'सरल विपरीत राजयोग (Sarala Yoga)', found: true,
                    detail: '✦ **सरल विपरीत राजयोग उपस्थित:** 8वें भाव के स्वामी (' + h8Lord + ') भाव ' + p8.house + ' में स्थित हैं। दीर्घायु, निर्भीक व्यक्तित्व, आकस्मिक धनलाभ एवं गुप्त शत्रुओं का विनाश।' });
            }
            if (p12 && (p12.house === 6 || p12.house === 8)) {
                res.push({ name: 'विमल विपरीत राजयोग (Vimala Yoga)', found: true,
                    detail: '✦ **विमल विपरीत राजयोग उपस्थित:** 12वें भाव के स्वामी (' + h12Lord + ') भाव ' + p12.house + ' में स्थित हैं। स्वतंत्र सोच, स्वावलंबन, संचित धन एवं आध्यात्मिक संपन्नता।' });
            }
            return res;
        },

        lakshmi: function(a) {
            var l9 = a.houses[9].lord;
            var p9 = a.planets[l9];
            var ven = a.planets['शुक्र'];
            if (p9 && ven && (KENDRAS.indexOf(p9.house) !== -1 || TRIKONAS.indexOf(p9.house) !== -1) && ['वृषभ','तुला','मीन'].indexOf(ven.sign) !== -1) {
                return { name: 'महालक्ष्मी योग (Lakshmi Yoga)', found: true,
                    detail: '✦ **महालक्ष्मी राजयोग उपस्थित:** नवमेश बली केन्द्र/त्रिकोण में हैं एवं शुक्र स्व/उच्च राशि में हैं। जातक परम भाग्यशाली, उच्च कोटि का धनवान व सर्वगुण सम्पन्न होता है।' };
            }
            return null;
        },

        saraswati: function(a) {
            var jup = a.planets['गुरु'], ven = a.planets['शुक्र'], merc = a.planets['बुध'];
            if (!jup || !ven || !merc) return null;
            var validHouses = [1, 2, 4, 5, 7, 9, 10];
            if (validHouses.indexOf(jup.house) !== -1 && validHouses.indexOf(ven.house) !== -1 && validHouses.indexOf(merc.house) !== -1 && jup.dignity !== 'नीच') {
                return { name: 'सरस्वती योग (Saraswati Yoga)', found: true,
                    detail: '✦ **ज्ञान-मुकुट सरस्वती योग उपस्थित:** गुरु, शुक्र एवं बुध तीनों केन्द्र, त्रिकोण अथवा द्वितीय भाव में बली हैं। जातक अद्वितीय वक्ता, कवि, लेखक, शिक्षक अथवा शास्त्र मर्मज्ञ होता है।' };
            }
            return null;
        },

        kahala: function(a) {
            var l4 = a.houses[4].lord, l9 = a.houses[9].lord;
            var p4 = a.planets[l4], p9 = a.planets[l9];
            if (p4 && p9) {
                var diff = ((p9.house - p4.house + 12) % 12) + 1;
                if (KENDRAS.indexOf(diff) !== -1 && a.lagnaStrength.indexOf('बलवान') !== -1) {
                    return { name: 'काहल योग (Kahala Yoga)', found: true,
                        detail: '✦ **काहल योग उपस्थित:** चतुर्थेश व नवमेश परस्पर केन्द्र में हैं तथा लग्नेश बली हैं। जातक साहसी, उच्च पदस्थ एवं सेना/प्रशासन में प्रमुख होता है।' };
                }
            }
            return null;
        },

        shankha: function(a) {
            var l5 = a.houses[5].lord, l6 = a.houses[6].lord;
            var p5 = a.planets[l5], p6 = a.planets[l6];
            if (p5 && p6) {
                var diff = ((p6.house - p5.house + 12) % 12) + 1;
                if (KENDRAS.indexOf(diff) !== -1 && a.lagnaStrength.indexOf('बलवान') !== -1) {
                    return { name: 'शंख योग (Shankha Yoga)', found: true,
                        detail: '✦ **शंख योग उपस्थित:** पंचमेश व षष्ठेश परस्पर केन्द्र में हैं। जातक दयालु, नीतिवान, दीर्घायु एवं शास्त्रज्ञ होता है।' };
                }
            }
            return null;
        },

        chamara: function(a) {
            var l1Data = a.lagnaLordPos;
            var guru = a.planets['गुरु'];
            if (l1Data && guru && l1Data.dignity === 'उच्च' && KENDRAS.indexOf(l1Data.house) !== -1 && aspectsHouse(guru.house, l1Data.house, 'गुरु')) {
                return { name: 'चामर योग (Chamara Yoga)', found: true,
                    detail: '✦ **परम राजयोग चामर योग उपस्थित:** लग्नेश उच्च राशि में केन्द्र में स्थित हैं तथा देवगुरु बृहस्पति की अमृत दृष्टि से युक्त हैं। जातक राजा या राजा तुल्य सम्मान प्राप्त करता है।' };
            }
            return null;
        },

        akhandasamrajya: function(a) {
            var moon = a.planets['चन्द्र'];
            var jup = a.planets['गुरु'];
            if (!moon || !jup) return null;
            var jupLords = [a.houses[2].lord, a.houses[5].lord, a.houses[11].lord];
            if (jupLords.indexOf('गुरु') !== -1) {
                var l9 = a.houses[9].lord, l11 = a.houses[11].lord;
                var p9 = a.planets[l9], p11 = a.planets[l11];
                var fromMoon9 = p9 ? ((p9.house - moon.house + 12) % 12) + 1 : 0;
                var fromMoon11 = p11 ? ((p11.house - moon.house + 12) % 12) + 1 : 0;
                if (KENDRAS.indexOf(fromMoon9) !== -1 || KENDRAS.indexOf(fromMoon11) !== -1) {
                    return { name: 'अखंड साम्राज्य योग (Akhanda Samrajya Yoga)', found: true,
                        detail: '✦ **दुर्लभ अखंड साम्राज्य योग उपस्थित:** गुरु 2/5/11 के स्वामी होकर बली हैं तथा नवमेश/एकादशेश चन्द्रमा से केन्द्र में स्थित हैं। जातक अचल साम्राज्य, विशाल संपत्ति व स्थायी अधिकार प्राप्त करता है।' };
                }
            }
            return null;
        },

        mahabhagya: function(a, chart) {
            var sun = a.planets['सूर्य'], moon = a.planets['चन्द्र'];
            if (!sun || !moon) return null;
            var lagnaOdd = signIdx(a.lagna) % 2 === 0;
            var sunOdd = signIdx(sun.sign) % 2 === 0;
            var moonOdd = signIdx(moon.sign) % 2 === 0;
            if (lagnaOdd && sunOdd && moonOdd) {
                return { name: 'महाभाग्य योग (Mahabhagya Yoga)', found: true,
                    detail: '✦ **महाभाग्य योग उपस्थित:** लग्न, सूर्य एवं चन्द्र तीनों विषम (पुरुष) राशियों में स्थित हैं। जातक अत्यंत भाग्यशाली, उदार एवं सर्वत्र ख्याति प्राप्त करता है।' };
            }
            return null;
        },

        kalanidhi: function(a) {
            var jup = a.planets['गुरु'], ven = a.planets['शुक्र'], merc = a.planets['बुध'];
            if (jup && (jup.house === 2 || jup.house === 5) && (jup.sign === 'धनु' || jup.sign === 'मीन' || (ven && ven.house === jup.house) || (merc && merc.house === jup.house))) {
                return { name: 'कलानिधि योग (Kalanidhi Yoga)', found: true,
                    detail: '✦ **कलानिधि योग उपस्थित:** गुरु द्वितीय या पंचम भाव में बुध/शुक्र के प्रभाव में हैं। जातक सभी कलाओं में निपुण, विद्वान एवं समाज में आदरणीय होता है।' };
            }
            return null;
        },

        dhanayogas: function(a) {
            var res = [];
            var l2 = a.houses[2].lord, l11 = a.houses[11].lord, l5 = a.houses[5].lord, l9 = a.houses[9].lord;
            var p2 = a.planets[l2], p11 = a.planets[l11];
            if (p2 && p11 && p2.house === p11.house) {
                res.push({ name: '2-11 धन योग (द्वितीयेश व एकादशेश युति)', found: true,
                    detail: '✦ **प्रबल धन योग उपस्थित:** धन भाव के स्वामी (' + l2 + ') एवं लाभ भाव के स्वामी (' + l11 + ') एक साथ विराजमान हैं। संचित धन एवं आय में निरंतर वृद्धि।' });
            }
            if (p2 && (p2.house === 11 || p2.house === 9 || p2.house === 5)) {
                res.push({ name: 'लक्ष्मी कारक धन योग (द्वितीयेश त्रिकोण/लाभ में)', found: true,
                    detail: '✦ **धन योग उपस्थित:** द्वितीयेश शुभ भाव ' + p2.house + ' में स्थित होकर स्थायी संपत्ति का निर्माण करते हैं।' });
            }
            return res;
        },

        // ═══════════════════════════════════════════════════════════════
        // E. DOSHAS & ARISHTA YOGAS (दोष एवं अरिष्ट योग)
        // ═══════════════════════════════════════════════════════════════
        mangaldosha: function(a) {
            var mars = a.planets['मंगल'];
            if (!mars) return { name: 'मंगल दोष', found: false, detail: 'मंगल डेटा अनुपलब्ध' };
            var mH = mars.house;
            var isManglik = [1, 2, 4, 7, 8, 12].indexOf(mH) !== -1;
            if (!isManglik) {
                return { name: 'मंगल दोष (मांगलिक दोष)', found: false,
                    detail: '❌ **मंगल दोष अनुपस्थित** — आपकी कुण्डली में मंगल देव भाव ' + mH + ' (' + mars.sign + ') में स्थित हैं। मंगल दोष केवल 1, 2, 4, 7, 8, 12 भावों में होने पर बनता है।' };
            }
            var bhangas = [];
            if (mars.sign === 'मेष' || mars.sign === 'वृश्चिक') bhangas.push('मंगल अपनी स्वराशि (' + mars.sign + ') में स्थित हैं');
            if (mars.sign === 'मकर') bhangas.push('मंगल उच्च राशि (मकर) में स्थित हैं');
            var guru = a.planets['गुरु'];
            if (guru && aspectsHouse(guru.house, mH, 'गुरु')) bhangas.push('देवगुरु बृहस्पति की पूर्ण अमृत दृष्टि मंगल पर है');

            if (bhangas.length > 0) {
                return { name: 'मंगल दोष (परिहार / भंग)', found: true, partial: true,
                    detail: '⚠️ **मंगल दोष उपस्थित किंतु शास्त्रीय परिहार से भंग:**\n' +
                            'मंगल देव भाव ' + mH + ' में स्थित हैं, परन्तु निम्नलिखित नियमों से दोष भंग होता है:\n' +
                            bhangas.map(function(b){ return '• ' + b; }).join('\n') + '\n\n' +
                            '**फल:** वैवाहिक जीवन में उग्रता का स्वतः शमन होगा। केवल वाणी पर संयम रखें।\n' +
                            '**सात्विक उपाय:** मंगलवार को हनुमान चालीसा का पाठ करें एवं लाल मसूर का दान करें।' };
            }
            return { name: 'मंगल दोष (मांगलिक दोष)', found: true, partial: false,
                detail: '🔴 **मांगलिक दोष उपस्थित:** मंगल देव भाव ' + mH + ' (' + mars.sign + ' राशि) में स्थित हैं।\n' +
                        '**फल:** स्वभाव में तीक्ष्णता, शीघ्र उत्तेजना एवं दांपत्य में सामंजस्य की आवश्यकता।\n' +
                        '**अचूक सात्विक उपाय:**\n1. नित्य हनुमान चालीसा अथवा सुंदरकांड का पाठ करें।\n2. पक्षियों को मीठी रोटी अथवा गुड़-रोटी खिलाएं।\n3. विवाह पूर्व कुण्डली मिलान व गुण-दोष का पूर्ण सामंजस्य अवश्य करें।' };
        },

        kaalsarpa: function(a, chart) {
            var rahu = a.planets['राहु'], ketu = a.planets['केतु'];
            if (!rahu || !ketu) return { name: 'कालसर्प योग', found: false, detail: 'राहु/केतु डेटा अनुपलब्ध' };
            var rH = rahu.house, kH = ketu.house;
            var planets7 = ['सूर्य','चन्द्र','मंगल','बुध','गुरु','शुक्र','शनि'];
            var side1 = 0, side2 = 0;
            planets7.forEach(function(pn) {
                var p = a.planets[pn];
                if (p) {
                    var diffR = ((p.house - rH + 12) % 12);
                    if (diffR > 0 && diffR < 6) side1++;
                    else if (diffR > 6) side2++;
                }
            });
            var types = [
                'अनंत कालसर्प (1-7 भाव)','कुलिक कालसर्प (2-8 भाव)','वासुकि कालसर्प (3-9 भाव)',
                'शंखपाल कालसर्प (4-10 भाव)','पद्म कालसर्प (5-11 भाव)','महापद्म कालसर्प (6-12 भाव)',
                'तक्षक कालसर्प (7-1 भाव)','कर्कोटक कालसर्प (8-2 भाव)','शंखचूड़ कालसर्प (9-3 भाव)',
                'घातक कालसर्प (10-4 भाव)','विषधर कालसर्प (11-5 भाव)','शेषनाग कालसर्प (12-6 भाव)'
            ];
            var typeName = types[rH - 1] || 'कालसर्प';
            if (side1 === 7 || side2 === 7) {
                return { name: 'पूर्ण कालसर्प दोष (' + typeName + ')', found: true, partial: false,
                    detail: '🔴 **पूर्ण ' + typeName + ' उपस्थित**\n' +
                            '**स्थिति:** सभी 7 मुख्य ग्रह राहु (भाव ' + rH + ') और केतु (भाव ' + kH + ') के एक ही ओर स्थित हैं।\n' +
                            '**फल:** 33 वर्ष की आयु तक कड़ा संघर्ष, परिश्रम का श्रेय विलंब से मिलना, किंतु तदुपरांत अप्रत्याशित सफलता।\n' +
                            '**सात्विक उपाय:** महामृत्युंजय मंत्र जप, शिव रुद्राभिषेक, पक्षियों को सप्तधान्य दान।' };
            }
            if (side1 === 6 || side2 === 6) {
                return { name: 'आंशिक कालसर्प दोष', found: true, partial: true,
                    detail: '⚠️ **आंशिक कालसर्प दोष उपस्थित:** एक ग्रह राहु-केतु अक्ष से बाहर है, जिससे पूर्ण दोष भंग हो चुका है।\n' +
                            '**उपाय:** सोमवार को शिवलिंग पर जल अर्पित करें।' };
            }
            return { name: 'कालसर्प दोष', found: false, detail: '❌ **कालसर्प दोष अनुपस्थित** — ग्रह राहु-केतु अक्ष के दोनों ओर स्वतंत्र रूप से संचरण कर रहे हैं।' };
        },

        guruchandal: function(a) {
            var guru = a.planets['गुरु'], rahu = a.planets['राहु'], ketu = a.planets['केतु'];
            if (!guru || !rahu) return null;
            if (guru.house === rahu.house || guru.house === (ketu ? ketu.house : 0)) {
                var isBhanga = ['कर्क','धनु','मीन'].indexOf(guru.sign) !== -1;
                return { name: 'गुरु-चांडाल योग' + (isBhanga ? ' (भंग)' : ''), found: true, partial: isBhanga,
                    detail: (isBhanga ? '⚠️ **गुरु-चांडाल योग भंग:**' : '🔴 **गुरु-चांडाल योग उपस्थित:**') + ' देवगुरु एवं राहु/केतु भाव ' + guru.house + ' में युति में हैं। ' +
                            (isBhanga ? 'गुरु के स्व/उच्च राशि में होने से चांडाल दोष का कुप्रभाव नष्ट हो गया है।' : 'गुरुजनों के प्रति आस्था में संदेह, निर्णय में भटकाव संभव।') + '\n' +
                            '**उपाय:** गुरुवार को विष्णु सहस्रनाम का पाठ करें, पीली वस्तुओं का दान करें।' };
            }
            return null;
        },

        grahanyoga: function(a) {
            var sun = a.planets['सूर्य'], moon = a.planets['चन्द्र'], rahu = a.planets['राहु'], ketu = a.planets['केतु'];
            if (!rahu) return null;
            var isSuryaGrahan = sun && (sun.house === rahu.house || (ketu && sun.house === ketu.house));
            var isChandraGrahan = moon && (moon.house === rahu.house || (ketu && moon.house === ketu.house));
            if (isSuryaGrahan || isChandraGrahan) {
                var name = isSuryaGrahan ? 'सूर्य ग्रहण योग' : 'चन्द्र ग्रहण योग';
                return { name: name, found: true, partial: false,
                    detail: '🔴 **' + name + ' उपस्थित:** ' + (isSuryaGrahan ? 'सूर्य' : 'चन्द्रमा') + ' राहु/केतु के साथ भाव ' + (isSuryaGrahan ? sun.house : moon.house) + ' में संचरण कर रहे हैं।\n' +
                            '**फल:** आत्मविश्वास में उतार-चढ़ाव, पिता या माता के स्वास्थ्य की चिंता।\n' +
                            '**उपाय:** नित्य गायत्री मंत्र अथवा महामृत्युंजय मंत्र का जप करें।' };
            }
            return null;
        },

        angarak: function(a) {
            var mars = a.planets['मंगल'], rahu = a.planets['राहु'], ketu = a.planets['केतु'];
            if (!mars || !rahu) return null;
            if (mars.house === rahu.house || (ketu && mars.house === ketu.house)) {
                return { name: 'अंगारक योग (Angarak Yoga)', found: true, partial: false,
                    detail: '🔴 **अंगारक योग उपस्थित:** मंगल एवं राहु/केतु भाव ' + mars.house + ' में एक साथ स्थित हैं।\n' +
                            '**फल:** रक्त विकार, अत्यधिक क्रोध, आकस्मिक चोट अथवा अग्नि से सावधानी अपेक्षित।\n' +
                            '**उपाय:** मंगलवार को हनुमान जी को सिंदूर व चमेली का तेल अर्पित करें, मीठी रोटी बांटें।' };
            }
            return null;
        },

        shrapit: function(a) {
            var sat = a.planets['शनि'], rahu = a.planets['राहु'];
            if (!sat || !rahu) return null;
            if (sat.house === rahu.house) {
                return { name: 'श्रापित दोष (Shrapit Yoga)', found: true,
                    detail: '🔴 **शनि-राहु श्रापित योग उपस्थित:** शनि और राहु भाव ' + sat.house + ' में युति में हैं।\n' +
                            '**फल:** कार्यों में अकारण विघ्न, पैतृक कर्म ऋण, कठिन परिश्रम के बाद फल।\n' +
                            '**उपाय:** शनिवार को छाया दान (कांसे की कटोरी में तेल में मुख देखकर दान) करें।' };
            }
            return null;
        },

        vishyoga: function(a) {
            var sat = a.planets['शनि'], moon = a.planets['चन्द्र'];
            if (!sat || !moon) return null;
            var isConjoined = sat.house === moon.house;
            var isAspect = aspectsHouse(sat.house, moon.house, 'शनि');
            if (isConjoined || isAspect) {
                return { name: 'विष योग (Vish Yoga)', found: true, partial: !isConjoined,
                    detail: '⚠️ **विष योग उपस्थित:** शनि देव और चन्द्रमा ' + (isConjoined ? 'एक साथ भाव ' + moon.house + ' में हैं' : 'दृष्टि संबंध में हैं') + '।\n' +
                            '**फल:** मन में अकारण उदासी, नकारात्मक विचार, निराशा अथवा अनिद्रा की समस्या।\n' +
                            '**उपाय:** नित्य शिवलिंग पर जल चढ़ाएं, "ॐ नमः शिवाय" का जप करें, माता की सेवा करें।' };
            }
            return null;
        },

        pitradosha: function(a) {
            var sun = a.planets['सूर्य'], rahu = a.planets['राहु'], sat = a.planets['शनि'];
            var l9 = a.houses[9].lord;
            var p9 = a.planets[l9];
            var isAfflicted = (sun && rahu && sun.house === rahu.house) || (p9 && rahu && p9.house === rahu.house);
            if (isAfflicted) {
                return { name: 'पितृ दोष (Pitra Dosha)', found: true,
                    detail: '🔴 **पितृ दोष उपस्थित:** सूर्य अथवा नवमेश राहु के प्रभाव में हैं।\n' +
                            '**फल:** वंश वृद्धि में रुकावट, पैतृक संपत्ति विवाद अथवा जीवन में प्रगति का अवरुद्ध होना।\n' +
                            '**उपाय:** अमावस्या को पितृ तर्पण, पीपल के वृक्ष में जल, निर्धनों को अन्न दान।' };
            }
            return null;
        },

        matrudosha: function(a) {
            var moon = a.planets['चन्द्र'], rahu = a.planets['राहु'], l4 = a.houses[4].lord;
            var p4 = a.planets[l4];
            if ((moon && rahu && moon.house === rahu.house) || (p4 && rahu && p4.house === rahu.house)) {
                return { name: 'मातृ दोष (Matru Dosha)', found: true,
                    detail: '⚠️ **मातृ दोष उपस्थित:** चन्द्रमा अथवा चतुर्थेश राहु से पीड़ित हैं। माता की सेवा व शिव आराधना अनिवार्य है।' };
            }
            return null;
        },

        daridra: function(a) {
            var l11 = a.houses[11].lord;
            var p11 = a.planets[l11];
            if (p11 && DUSTHANAS.indexOf(p11.house) !== -1) {
                return { name: 'दरिद्र योग (Daridra Yoga)', found: true, partial: true,
                    detail: '⚠️ **दरिद्र योग कारक स्थिति:** एकादश (आय) भाव के स्वामी भाव ' + p11.house + ' (दुःस्थान) में स्थित हैं। संचित धन के व्यय पर नियंत्रण रखें।' };
            }
            return null;
        },

        gandanta: function(a) {
            var gandantaPoints = [];
            Object.entries(a.planets).forEach(function(e) {
                var p = e[0], d = e[1];
                if (['कर्क','वृश्चिक','मीन'].indexOf(d.sign) !== -1 && d.deg >= 27.0) {
                    gandantaPoints.push(p + ' (' + d.sign + ' ' + d.deg.toFixed(1) + '°)');
                } else if (['मेष','सिंह','धनु'].indexOf(d.sign) !== -1 && d.deg <= 3.0) {
                    gandantaPoints.push(p + ' (' + d.sign + ' ' + d.deg.toFixed(1) + '°)');
                }
            });
            if (gandantaPoints.length > 0) {
                return { name: 'गंडान्त योग (Gandanta)', found: true,
                    detail: '⚠️ **गंडान्त संधि स्थिति:** ग्रह (' + gandantaPoints.join(', ') + ') जल-अग्नि संधि क्षेत्र में संचरणशील हैं। आध्यात्मिक साधना से आत्मबल सुदृढ़ करें।' };
            }
            return null;
        },

        // ═══════════════════════════════════════════════════════════════
        // F. NABHASA & SPECIAL YOGAS (नाभस एवं विशिष्ट योग)
        // ═══════════════════════════════════════════════════════════════
        nabhasa: function(a) {
            var res = [];
            var movableSigns = ['मेष','कर्क','तुला','मकर'];
            var fixedSigns = ['वृषभ','सिंह','वृश्चिक','कुंभ'];
            var dualSigns = ['मिथुन','कन्या','धनु','मीन'];
            var planets7 = ['सूर्य','चन्द्र','मंगल','बुध','गुरु','शुक्र','शनि'];

            var allMov = planets7.every(function(pn){ return a.planets[pn] && movableSigns.indexOf(a.planets[pn].sign) !== -1; });
            var allFix = planets7.every(function(pn){ return a.planets[pn] && fixedSigns.indexOf(a.planets[pn].sign) !== -1; });
            var allDual = planets7.every(function(pn){ return a.planets[pn] && dualSigns.indexOf(a.planets[pn].sign) !== -1; });

            if (allMov) res.push({ name: 'रज्जु योग (Rajju Yoga)', found: true, detail: '✦ **रज्जु नाभस योग:** सभी ग्रह चर राशियों में स्थित हैं। जातक सतत भ्रमणशील, महत्वाकांक्षी व कर्मठ होता है।' });
            if (allFix) res.push({ name: 'मूसल योग (Musala Yoga)', found: true, detail: '✦ **मूसल नाभस योग:** सभी ग्रह स्थिर राशियों में स्थित हैं। जातक दृढ़प्रतिज्ञ, स्वाभिमानी, धनी व स्थिर साम्राज्य वाला होता है।' });
            if (allDual) res.push({ name: 'नल योग (Nala Yoga)', found: true, detail: '✦ **नल नाभस योग:** सभी ग्रह द्विस्वभाव राशियों में स्थित हैं। जातक चतुर, बहुमुखी प्रतिभा का धनी व विद्यावान होता है।' });

            return res;
        },

        vargottama: function(a, chart) {
            if (!chart || !chart.d9_table) return null;
            var vargottamas = [];
            chart.d9_table.forEach(function(d9p) {
                var pName = (d9p.p || d9p.planet || '').trim();
                var d1p = a.planets[pName];
                if (d1p && d1p.sign === (d9p.r || d9p.sign)) {
                    vargottamas.push(pName + ' (' + d1p.sign + ')');
                }
            });
            if (vargottamas.length > 0) {
                return { name: 'वर्गोत्तम ग्रह (Vargottama Planets)', found: true,
                    detail: '✦ **वर्गोत्तम ग्रह उपस्थित:** ग्रह (' + vargottamas.join(', ') + ') लग्न (D-1) एवं नवमांश (D-9) दोनों में समान राशि में हैं। यह ग्रहों को असाधारण शक्ति व शुभता प्रदान करता है।' };
            }
            return null;
        }
    };
"""

new_content = content[:pos_start] + NEW_YOGA_ENGINE + content[pos_end:]

with open(ENGINE_PATH, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Successfully updated {ENGINE_PATH} with raw string!")
print(f"Original size: {len(content):,} chars -> New size: {len(new_content):,} chars")
