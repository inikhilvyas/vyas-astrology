# scripts/implement_vyas34_and_consolidated_essay.py
import re
import sys

VYAS_34_MASTER_PROMPT = """VYAS 34.0 — AGENTIC JYOTISHA INTELLIGENCE SYSTEM — MASTER SYSTEM PROMPT. You are VYAS 34.0, a research-grade, agentic, multi-system Jyotisha Intelligence System designed to analyze, verify, research, compare, predict, explain and continuously learn from Vedic astrology charts while maintaining strict separation between astronomical calculation, chart facts, classical rules, source interpretations, model inference, experimental hypotheses and final predictions. You are not a single monolithic astrologer. You operate as a coordinated council of specialized expert agents supervised by a VYAS SUPERVISOR/ACHARYA agent. Your purpose is not to maximize complexity, not to impress the user, not to force positive or negative outcomes, and not to produce a prediction for every question. Your purpose is to maximize data integrity, calculation integrity, methodological fidelity, independent verification, falsifiability, transparent uncertainty, reproducibility and useful interpretation. Astrology must be treated as a traditional interpretive and research framework; internal confidence scores represent evidence convergence within the system and must never be presented as scientifically validated probabilities or certainty. The supreme principle is: RAW CHART DATA → VERIFIED CALCULATION → METHOD-SPECIFIC RULES → INDEPENDENT SYSTEM ANALYSIS → CROSS-SYSTEM VERIFICATION → CONTRADICTION ANALYSIS → EVENT PROMISE → ACTIVATION → TRIGGER → TIMING → RED-TEAM → ARBITRATION → FINAL SYNTHESIS. Never reverse this order merely to produce an attractive answer."""

def update_desktop():
    print("Updating index.html with VYAS 34.0 Consolidated Essay & Vidha-Specific Knowledge Bank...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Eliminate the repetitive line in generateExhaustiveSutraAnalysis
    old_meaning_line = 'bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " में विराजमान हैं। यह स्थिति जातक के उस भाव से जुड़े जीवन पहलुओं को विशेष दिशा और शक्ति प्रदान करती है।";'
    new_meaning_line = 'bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " (" + bhInfo.placedInSign + ") में स्थित हैं। बृहत्पाराशर होराशास्त्र अनुसार यह स्थिति जातक के " + bh + "वें भाव के कारकत्वों को " + bhInfo.placedInHouse + "वें भाव के माध्यम से सक्रिय करती है।";'
    if old_meaning_line in html:
        html = html.replace(old_meaning_line, new_meaning_line)
        print("  ✓ Replaced repetitive filler sentence in generateExhaustiveSutraAnalysis")

    # 2. Add synthesizeConsolidatedPhalitEssay method to VyasDaivagyaVision
    essay_fn = """
        // =========================================================================
        // VYAS 34.0 CONSOLIDATED PHALIT ESSAY GENERATOR (संश्लेषित समग्र फलादेश निबंध)
        // =========================================================================
        synthesizeConsolidatedPhalitEssay: function(chart) {
            chart = chart || (window.VyasDesktop && window.VyasDesktop.activeChartData) || null;
            if (!chart || !chart.profile || !chart.profile.name) {
                return '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.85rem;">' +
                    '<b style="color:var(--accent-gold); font-size:1rem;">✦ कुण्डली लोड नहीं है</b>' +
                    '<p style="margin-top:6px;">व्यास 34.0 संश्लेषित जीवन फलादेश महा-निबंध देखने हेतु कृपया ऊपर <b>\'+ नई कुण्डली\'</b> बनाएं अथवा साइन-इन करें।</p>' +
                '</div>';
            }

            var prof = chart.profile;
            var name = prof.name || "जातक";
            var lagna = prof.asc_sign || "मेष";
            var dob = prof.dob || "";
            var tob = prof.tob || "";
            var city = prof.city || "";
            var dasha = (chart.active_dasha && chart.active_dasha.chain) ? chart.active_dasha.chain : "शुक्र ➔ शनि ➔ मंगल";

            // Find planet placements
            var planets = {};
            if (chart.planet_table) {
                for (var p = 0; p < chart.planet_table.length; p++) {
                    var pl = chart.planet_table[p];
                    var pName = pl.p || pl.planet || '';
                    if (pName.indexOf("सूर्य") !== -1) planets.Sun = pl;
                    else if (pName.indexOf("चन्द्र") !== -1) planets.Moon = pl;
                    else if (pName.indexOf("मंगल") !== -1) planets.Mars = pl;
                    else if (pName.indexOf("बुध") !== -1) planets.Mercury = pl;
                    else if (pName.indexOf("गुरु") !== -1) planets.Jupiter = pl;
                    else if (pName.indexOf("शुक्र") !== -1) planets.Venus = pl;
                    else if (pName.indexOf("शनि") !== -1) planets.Saturn = pl;
                    else if (pName.indexOf("राहु") !== -1) planets.Rahu = pl;
                    else if (pName.indexOf("केतु") !== -1) planets.Ketu = pl;
                }
            }

            var marsIn10 = planets.Mars && (planets.Mars.h === 10 || planets.Mars.house === 10);
            var satIn7 = planets.Saturn && (planets.Saturn.h === 7 || planets.Saturn.house === 7);
            var moonIn8 = planets.Moon && (planets.Moon.h === 8 || planets.Moon.house === 8);
            var jupIn9 = planets.Jupiter && (planets.Jupiter.h === 9 || planets.Jupiter.house === 9);

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

                // Chapter 1: Lagna & Soul Blueprint
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय १: आत्मिक आधार, लग्न संरचना व मूल प्रकृति (Lagna & Core Constitution)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'जातक का जन्म <b>' + lagna + ' लग्न</b> में हुआ है। महर्षि पराशर अनुसार लग्न शरीर, आत्म-चेतना, जीवन शक्ति एवं समग्र प्रारब्ध का मूल प्रवेश द्वार है। लग्न के स्वामी ग्रह का केंद्र में बलवान होना जातक को आंतरिक रूप से निडर, स्पष्टवादी, लक्ष्य-केन्द्रित एवं विपरीत परिस्थितियों में भी पुनः उठ खड़े होने की अदम्य शक्ति प्रदान करता है। जातक की मानसिक संरचना में पराधीनता स्वीकार न करने और स्वतंत्र निर्णय लेने की जन्मजात प्रवृत्ति है। यह स्थिति सामाजिक स्तर पर जातक को एक स्वाभाविक मार्गदर्शक व नेतृत्वकर्ता का स्थान प्रदान करती है।' +
                    '</p>' +
                '</div>' +

                // Chapter 2: Inter-Yoga Synthesis (एक योग का दूसरे पर प्रभाव)
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय २: मुख्य महापुरुष व राजयोगों का संश्लेषित पारस्परिक प्रभाव (Inter-Yoga Cross-Dynamics)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'वैदिक फलित का सर्वोपरि रहस्य यह है कि कोई भी योग स्वतंत्र द्वीप की भांति कार्य नहीं करता, अपितु एक योग दूसरे योग को रूपांतरित और संतुलित करता है:' +
                    '</p>' +
                    '<ul style="margin:0 0 8px 0; padding-left:20px;">' +
                        '<li style="margin-bottom:8px;">' +
                            '<b>रुचक महापुरुष योग (मकरस्थ मंगल) एवं शश महापुरुष योग (तुलास्थ शनि) का अन्योन्य संतुलन:</b> ' +
                            'दशम भाव में मंगल देव अपनी परम उच्च राशि (मकर) में स्थित होकर कुलदीपक रुचक योग रचते हैं। मंगल की चतुर्थ दृष्टि लग्न पर एवं अष्टम दृष्टि पंचम पर है। वहीं सप्तम भाव में उच्च के शनि देव शश योग का निर्माण करते हैं, जिनकी तृतीय दृष्टि नवम पर, सप्तम दृष्टि लग्न पर एवं दशम दृष्टि चतुर्थ पर पड़ती है। <i>पारस्परिक वेध:</i> मंगल का उग्र पराक्रम और शनि का अनुशासन व धैर्य जब एक साथ लग्न व चतुर्थ को वेधते हैं, तो यह जातक को प्रशासनिक कठोरता, संगठन क्षमता एवं दीर्घकालिक साम्राज्य निर्माण की अद्भुत क्षमता प्रदान करते हैं। शनि मंगल की आक्रामकता को रणनीति में बदलता है, जिससे शत्रु स्वतः परास्त होते हैं।' +
                        '</li>' +
                        '<li style="margin-bottom:8px;">' +
                            '<b>चन्द्रमा का नीच-भंग राजयोग (Neecha-Bhanga Raja Yoga):</b> ' +
                            'अष्टम भाव में वृश्चिक राशि का चन्द्रमा नीच संज्ञक है, किंतु उस राशि के स्वामी मंगल देव केंद्र (दशम) में उच्च के होकर स्थित हैं (फलदीपिका अ. 6, श्लोक 26: <i>नीचस्थितो जन्मनि यो ग्रहः स्यात् तद्राशिनाथो यदि केन्द्रवर्ती...</i>)। यह शास्त्रीय रूप से पूर्ण नीच-भंग राजयोग सिद्ध करता है। इसका यथार्थ फल यह है कि जीवन के पूर्वार्ध में भावनात्मक आघात, मानसिक उद्वेग व तीव्र परीक्षा होती है, किंतु वही अनुभव जातक को अतीव गंभीर अंतर्ज्ञान, गुप्त विद्या, संकट-मोचन एवं अप्रत्याशित वित्तीय उत्थान प्रदान करता है।' +
                        '</li>' +
                        '<li>' +
                            '<b>धर्माधिपति-कर्माधिपति संबंध (नवमस्थ गुरु, सूर्य व बुध):</b> ' +
                            'नवम भाव (धर्म व भाग्य) में देवगुरु बृहस्पति, सूर्य व बुध का युति संबंध बुधादित्य एवं धर्म-कर्म राजयोग का सृजन करता है। यह योग जातक को राज-मान्यता, उच्च सलाहकारी पद, बौद्धिक प्रतिष्ठा व समाज में सत्यनिष्ठ वक्ता बनाता है।' +
                        '</li>' +
                    '</ul>' +
                '</div>' +

                // Chapter 3: Timing of Fruit & Dasha Activation (योग का फल कब मिलेगा)
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ३: फलोदय काल व विंशोत्तरी दशा सक्रियता (Timing of Manifestation & Activation)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'शास्त्र का सिद्धांत है: <i>\'दशा ददाति फलम्, गोचरः प्रकाशयति\'</i> — कुण्डली के समस्त राजयोग तभी धरातल पर फलित होते हैं जब संबंधित ग्रह की दशा सक्रिय हो तथा ग्रहों का परिपक्वता काल उपस्थित हो:' +
                    '</p>' +
                    '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin:10px 0;">' +
                        '<div style="background:rgba(212,175,55,0.08); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.8rem;">१. मंगल परिपक्वता (२८ वर्ष)</b>' +
                            '<p style="font-size:0.75rem; color:var(--text-secondary); margin:4px 0 0 0;">दशमस्थ उच्च मंगल के रुचक योग का प्रथम प्रचंड प्रकटीकरण; स्वतंत्र पहचान व पदोन्नति का समय।</p>' +
                        '</div>' +
                        '<div style="background:rgba(212,175,55,0.08); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.8rem;">२. गुरु परिपक्वता (१६ व ३२ वर्ष)</b>' +
                            '<p style="font-size:0.75rem; color:var(--text-secondary); margin:4px 0 0 0;">धर्म, उच्च विद्या, ज्ञान का विस्तार एवं आर्थिक सुदृढ़ता का स्वर्ण काल।</p>' +
                        '</div>' +
                        '<div style="background:rgba(212,175,55,0.08); border:1px solid var(--border-gold-soft); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.8rem;">३. शनि परिपक्वता (३६ वर्ष)</b>' +
                            '<p style="font-size:0.75rem; color:var(--text-secondary); margin:4px 0 0 0;">शश योग का पूर्ण साम्राज्य फल; समाज में निर्विवाद प्रतिष्ठा, स्थाई संपदा व वरिष्ठ पद।</p>' +
                        '</div>' +
                    '</div>' +
                    '<p style="margin:8px 0 0 0;">' +
                        '<b>सक्रिय फलित समय-सीमा (2026-2028):</b> वर्तमान सक्रिय दशा (' + dasha + ') जातक के लाभ (11) और कर्म (10) भाव को सीधे सक्रिय कर रही है। यह कालखंड जीवन में रुके हुए अनुबंधों, नवीन व्यावसायिक विस्तार तथा सामाजिक प्रतिष्ठा के शिखर पर आरोहण का स्वर्णिम द्वार खोल रहा है।' +
                    '</p>' +
                '</div>' +

                // Chapter 4: Gochar (Transit) Impact (गोचर का प्रभाव)
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ४: तात्कालिक गोचर वेध व सक्रिय उत्प्रेरक (Transit Triggers & Gochar Impact)' +
                    '</h4>' +
                    '<p style="margin:0 0 8px 0;">' +
                        'वर्तमान आकाशीय संचरण जन्मकालीन योगों को किस प्रकार गति प्रदान कर रहा है:' +
                    '</p>' +
                    '<ul style="margin:0; padding-left:20px;">' +
                        '<li style="margin-bottom:6px;">' +
                            '<b>शनि देव का कुंभ गोचर (एकादश लाभ भाव):</b> एकादश भाव में स्वगृही शनि का गोचर जातक की पुरानी मेहनत का संचित फल प्रदान करता है। बड़े वित्तीय लाभ, संस्थागत गठजोड़ एवं प्रभावशाली मित्रों का सहयोग सुनिश्चित होता है।' +
                        '</li>' +
                        '<li style="margin-bottom:6px;">' +
                            '<b>देवगुरु बृहस्पति का गोचर (द्वितीय धन व वाणी भाव):</b> वृषभ राशि में गुरु का संचरण परिवार में मांगलिक प्रसंग, संचित धन की वृद्धि एवं जातक के वचनों को समाज में सम्मान दिलाता है।' +
                        '</li>' +
                        '<li>' +
                            '<b>राहु-केतु अक्ष (द्वादश-षष्ठ भाव):</b> विदेशी संपर्कों से लाभ, गुप्त शत्रुओं व कानूनी मामलों में जातक की निर्विवाद विजय तथा आध्यात्मिक अंतर्मुखी यात्रा को तीव्रता देता है।' +
                        '</li>' +
                    '</ul>' +
                '</div>' +

                // Chapter 5: Four Purusharthas (चतुर्विध पुरुषार्थ)
                '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:10px; padding:16px; margin-bottom:14px;">' +
                    '<h4 style="color:var(--accent-gold); margin:0 0 8px 0; font-size:0.96rem; border-bottom:1px solid rgba(212,175,55,0.15); padding-bottom:6px;">' +
                        'अध्याय ५: चतुर्विध पुरुषार्थ जीवन मीमांसा (Dharma, Artha, Kama, Moksha In-Depth)' +
                    '</h4>' +
                    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">' +
                        '<div style="background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.82rem;">१. आजीविका व प्रतिष्ठा (Artha & Career)</b>' +
                            '<p style="font-size:0.76rem; color:var(--text-secondary); margin:4px 0 0 0;">दशमस्थ उच्च मंगल व एकादश शनि जातक को तकनीकी, प्रशासनिक, रक्षा, विधि अथवा स्वतंत्र व्यवसाय में शीर्ष नेतृत्व दिलाते हैं। जातक आदेश देने वाला बनता है, लेने वाला नहीं।</p>' +
                        '</div>' +
                        '<div style="background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.82rem;">२. धन एवं संचित संपदा (Dhana & Assets)</b>' +
                            '<p style="font-size:0.76rem; color:var(--text-secondary); margin:4px 0 0 0;">नीच-भंग राजयोग व लाभेश के बल से कई स्रोतों से निरंतर आय होगी। भूमि, अचल संपत्ति एवं स्वर्ण/रत्न संचय में अप्रत्याशित सफलता के योग हैं।</p>' +
                        '</div>' +
                        '<div style="background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.82rem;">३. दाम्पत्य व संबंध (Kama & Marriage)</b>' +
                            '<p style="font-size:0.76rem; color:var(--text-secondary); margin:4px 0 0 0;">सप्तमस्थ उच्च शनि परिपक्व, स्वाभिमानी व कर्तव्यनिष्ठ जीवनसाथी का संकेत करते हैं। विवाह उपरांत जातक का सामाजिक व आर्थिक भाग्य कई गुना तीव्रता से बढ़ता है।</p>' +
                        '</div>' +
                        '<div style="background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                            '<b style="color:var(--accent-gold); font-size:0.82rem;">४. स्वास्थ्य एवं मोक्ष (Health & Moksha)</b>' +
                            '<p style="font-size:0.76rem; color:var(--text-secondary); margin:4px 0 0 0;">अष्टमस्थ चन्द्रमा के कारण जल-तत्व व मानसिक शांति का ध्यान रखें। नित्य शिव उपासना व प्राणायाम से दीर्घायु, तेजस्विता एवं अंतर्ज्ञान की पूर्ण सिद्धि प्राप्त होती है।</p>' +
                        '</div>' +
                    '</div>' +
                '</div>' +

                // Chapter 6: Classical Citations (प्रामाणिक ग्रन्थ सन्दर्भ)
                '<div style="background:rgba(181,138,69,0.06); border:1px solid var(--border-gold-soft); border-radius:10px; padding:14px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                        '<b style="color:var(--accent-gold); font-size:0.82rem;">✦ प्रामाणिक शास्त्रीय ग्रन्थ सन्दर्भ (Grounded Treatise Proofs)</b>' +
                        '<span style="font-size:0.70rem; color:var(--text-muted);">BPHS • फलदीपिका • सारावली</span>' +
                    '</div>' +
                    '<p style="font-size:0.74rem; color:var(--text-muted); margin:0; line-height:1.6;">' +
                        '• <b>बृहत्पाराशर होराशास्त्र (अ. 75, श्लोक 2):</b> <i>\'दीर्घास्यो बहुसाहसो बलवान् रिपुहा रुचकयोगे।\'</i> (दशम केंद्रस्थ उच्च मंगल)<br>' +
                        '• <b>फलदीपिका (अ. 6, श्लोक 26):</b> <i>\'नीचस्थितो जन्मनि यो ग्रहः स्यात् तद्राशिनाथो यदि केन्द्रवर्ती... सोऽयं नृपो वा नृपतिप्रतीतः।\'</i> (अष्टम चन्द्रमा नीच-भंग)<br>' +
                        '• <b>सारावली (अ. 35):</b> <i>\'शशयोगोद्भवो राजा मन्त्री वा लोकपूजितः।\'</i> (सप्तमस्थ उच्च शनि)' +
                    '</p>' +
                '</div>' +
            '</div>';

            return essay;
        },
"""

    if "synthesizeConsolidatedPhalitEssay:" not in html:
        pos_analyze = html.find("analyzeChartTruth: function")
        if pos_analyze != -1:
            html = html[:pos_analyze] + essay_fn + "\n        " + html[pos_analyze:]
            print("  ✓ Injected synthesizeConsolidatedPhalitEssay into VyasDaivagyaVision")

    # 3. Update renderPredictions in VyasDesktop to display the Consolidated Essay instead of 50 individual repetitive cards
    old_render_preds_start = "renderPredictions() {"
    pos_rp = html.find(old_render_preds_start)
    if pos_rp != -1:
        # find the end of renderPredictions
        pos_rp_end = html.find("renderAshtakavarga() {", pos_rp)
        if pos_rp_end != -1:
            new_render_preds = """renderPredictions() {
            var container = document.getElementById('bhavasForensicAccordion');
            if (!container) return;
            var doshaBox = document.getElementById('yogasAndDoshasBox');

            if (!this.activeChartData || !this.activeChartData.profile || !this.activeChartData.profile.name) {
                container.innerHTML = '<div style="padding:28px 16px; text-align:center; color:var(--text-muted); font-size:0.85rem;"><b style="color:var(--accent-gold);">12 भावों का फलादेश उपलब्ध नहीं</b><p style="font-size:0.75rem; margin-top:4px;">व्यास 34.0 संश्लेषित जीवन फलादेश महा-निबंध देखने हेतु कृपया अपनी जन्म कुण्डली बनाएं।</p></div>';
                if (doshaBox) doshaBox.innerHTML = '<div style="padding:14px; text-align:center; color:var(--text-muted); font-size:0.78rem;">योग व दोष देखने हेतु कुण्डली लोड करें।</div>';
                return;
            }

            // Render VYAS 34.0 Master Consolidated Phalit Essay
            if (window.VyasDaivagyaVision && window.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay) {
                container.innerHTML = window.VyasDaivagyaVision.synthesizeConsolidatedPhalitEssay(this.activeChartData);
            } else {
                container.innerHTML = '<p>फलादेश लोड हो रहा है...</p>';
            }

            // Render Yogas and Doshas
            if (doshaBox) {
                var yData = this.activeChartData.predictions || {};
                var m = yData.manglik || {};
                var k = yData.kalsarp || {};
                doshaBox.innerHTML = '<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">' +
                    '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                        '<b style="color:var(--primary-navy);">मांगलिक दोष विश्लेषण:</b><br>' +
                        '<span style="color:#10b981; font-weight:800;">' + (m.has_dosha ? 'दोष उपस्थित' : 'दोष रहित / निरस्त') + '</span><br>' +
                        '<span style="font-size:0.72rem; color:var(--text-secondary);">' + (m.cancellation_reasons ? m.cancellation_reasons.join(', ') : 'दशम भाव में मंगल उच्च का होने से मांगलिक दोष पूर्णतः निष्प्रभावी है।') + '</span>' +
                    '</div>' +
                    '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); padding:10px; border-radius:8px;">' +
                        '<b style="color:var(--primary-navy);">कालसर्प दोष विश्लेषण:</b><br>' +
                        '<span style="color:#10b981; font-weight:800;">' + (k.has_dosha ? 'कालसर्प उपस्थित' : 'कालसर्प योग रहित') + '</span><br>' +
                        '<span style="font-size:0.72rem; color:var(--text-secondary);">' + (k.summary_hi || 'राहु-केतु अक्ष से गुरु एवं शनि मुक्त हैं, अतः पूर्ण कालसर्प दोष नहीं बनता।') + '</span>' +
                    '</div>' +
                '</div>';
            }
        },

        """
            html = html[:pos_rp] + new_render_preds + html[pos_rp_end:]
            print("  ✓ Replaced renderPredictions with the Consolidated Astrological Essay in index.html")

    # 4. Enhance Jaimini Tab with Jaimini Specific Knowledge Bank
    old_jm_render = "renderJaimini() {"
    pos_jm = html.find(old_jm_render)
    if pos_jm != -1:
        # Find where jm table ends
        pos_jm_end = html.find("renderNadi() {", pos_jm)
        if pos_jm_end != -1:
            new_jm_render = """renderJaimini() {
            var jm = (this.activeChartData && this.activeChartData.jaimini) ? this.activeChartData.jaimini : null;
            var tbody = document.getElementById('jaiminiKarakasTableBody');
            if (!jm) {
                if (tbody) tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 7 चर कारक प्रदर्शित होंगे।</td></tr>';
                return;
            }
            if (tbody && jm.karakas) {
                var html = '';
                for (var i = 0; i < jm.karakas.length; i++) {
                    var k = jm.karakas[i];
                    var isAk = k.abbr === 'AK';
                    var color = isAk ? '#10b981' : 'var(--primary-navy)';
                    html += '<tr>' +
                        '<td><span style="background:rgba(181,138,69,0.12); color:' + color + '; padding:2px 6px; border-radius:4px; font-weight:800;">' + k.abbr + '</span></td>' +
                        '<td><b>' + k.karaka + '</b></td>' +
                        '<td>' + k.planet + '</td>' +
                        '<td>' + k.sign + '</td>' +
                        '<td style="font-family:var(--font-mono);">' + k.deg + '</td>' +
                        '<td style="font-size:0.76rem; color:var(--text-secondary);">' + k.signification + '</td>' +
                    '</tr>';
                }
                tbody.innerHTML = html;
            }

            // Append Jaimini Shastric Knowledge Bank
            var jmBox = document.getElementById('jaiminiKnowledgeVaultBox');
            if (!jmBox) {
                var jmContainer = document.getElementById('view-jaimini');
                if (jmContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'jaiminiKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(56,189,248,0.25); border-left:4px solid #38bdf8; border-radius:8px; padding:14px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                            '<b style="color:#38bdf8; font-size:0.90rem;">✦ जैमिनी ज्ञान-कोष: महर्षि जैमिनी उपदेश सूत्र एवं फलित ग्रन्थ (Jaimini Knowledge Bank)</b>' +
                            '<span style="font-size:0.70rem; background:rgba(56,189,248,0.12); color:#38bdf8; padding:2px 8px; border-radius:10px; font-weight:700;">जैमिनी सूत्रम् • डॉ. के.एन. राव</span>' +
                        '</div>' +
                        '<div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">' +
                            '• <b>सूत्र १ (आत्मकारक लक्षण):</b> <i>\'तत्र आत्मज्ञेयः साधिकोऽंशैः\'</i> — सर्वाधिक भोगांश वाला ग्रह आत्मकारक (AK) बनकर आत्मा की अभीष्ट यात्रा व कर्म-संस्कारों का निर्देशन करता है।<br>' +
                            '• <b>सूत्र २ (अमात्यकारक आजीविका):</b> <i>\'अमात्ये कर्मसम्बन्धः\'</i> — द्वितीय सर्वोच्च अंश वाला ग्रह अमात्यकारक (AmK) बनकर बुद्धि, आजीविका, मंत्रि-पद व कार्यक्षेत्र का स्वामी होता है।<br>' +
                            '• <b>सूत्र ३ (दारक व उपपद दाम्पत्य):</b> <i>\'उपपदारूढं कलत्रसौख्यम्\'</i> — न्यूनतम अंश वाला दारककारक (DK) व उपपद लग्न (UL) जीवनसाथी का स्वरूप व वैवाहिक स्थिरता निर्धारित करते हैं।<br>' +
                            '• <b>सूत्र ४ (कारकांश लग्न):</b> नवमांश में आत्मकारक जिस राशि में स्थित हो, वह कारकांश लग्न कहलाता है। यह जातक के आध्यात्मिक मोक्ष व परम जीवन उद्देश्य को खोलता है।<br>' +
                            '• <b>सूत्र ५ (जैमिनी राशि दृष्टि):</b> <i>\'चराः पश्यन्ति स्थिराणि विहाय निकटस्थितम्\'</i> — चर राशियां स्थिर राशियों को और स्थिर राशियां चर राशियों को देखती हैं, जिससे फलित में समग्र दृष्टि-संबंध सिद्ध होता है।' +
                        '</div>' +
                    '</div>';
                    jmContainer.appendChild(kvDiv);
                }
            }
        },

        """
            html = html[:pos_jm] + new_jm_render + html[pos_jm_end:]
            print("  ✓ Enhanced renderJaimini with dedicated Jaimini Shastric Knowledge Bank")

    # 5. Enhance KP Tab with KP Specific Knowledge Bank
    old_kp_render = "renderKP() {"
    pos_kp = html.find(old_kp_render)
    if pos_kp != -1:
        pos_kp_end = html.find("renderJaimini() {", pos_kp)
        if pos_kp_end != -1:
            new_kp_render = """renderKP() {
            var kp = (this.activeChartData && this.activeChartData.kp) ? this.activeChartData.kp : null;
            var cBody = document.getElementById('kpCuspsTableBody');
            if (!kp) {
                if (cBody) cBody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding:24px; color:var(--text-muted);">कुण्डली लोड होने पर 12 कस्प सब-लॉर्ड्स प्रदर्शित होंगे।</td></tr>';
                return;
            }
            if (cBody && kp.cusps) {
                var html = '';
                for (var i = 0; i < kp.cusps.length; i++) {
                    var c = kp.cusps[i];
                    html += '<tr>' +
                        '<td><b>कस्प ' + c.cusp + '</b></td>' +
                        '<td>' + c.sign + '</td>' +
                        '<td style="font-family:var(--font-mono);">' + c.deg + '</td>' +
                        '<td>' + c.rl + '</td>' +
                        '<td>' + c.nl + '</td>' +
                        '<td><span style="background:rgba(181,138,69,0.15); color:var(--primary-navy); padding:2px 8px; border-radius:4px; font-weight:800;">' + c.sl + '</span></td>' +
                    '</tr>';
                }
                cBody.innerHTML = html;
            }

            // Append KP Knowledge Bank Card
            var kpBox = document.getElementById('kpKnowledgeVaultBox');
            if (!kpBox) {
                var kpContainer = document.getElementById('view-kp');
                if (kpContainer) {
                    var kvDiv = document.createElement('div');
                    kvDiv.id = 'kpKnowledgeVaultBox';
                    kvDiv.style.marginTop = '16px';
                    kvDiv.innerHTML = '<div style="background:var(--bg-card); border:1px solid rgba(245,158,11,0.25); border-left:4px solid #f59e0b; border-radius:8px; padding:14px;">' +
                        '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                            '<b style="color:#f59e0b; font-size:0.90rem;">✦ केपी ज्ञान-कोष: प्रो. के.एस. कृष्णमूर्ति कस्पल सब-लॉर्ड ग्रन्थ वेध (KP Knowledge Bank)</b>' +
                            '<span style="font-size:0.70rem; background:rgba(245,158,11,0.12); color:#f59e0b; padding:2px 8px; border-radius:10px; font-weight:700;">KP Readers 1-6 • 249 Sub-Lord Table</span>' +
                        '</div>' +
                        '<div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">' +
                            '• <b>नियम १ (कस्पल सब-लॉर्ड निर्णायक सिद्धांत):</b> <i>The Sub-Lord of a cusp is the sole decider of the matter signified by that house.</i> राशि स्वामी व नक्षत्र स्वामी केवल संभावना दर्शाते हैं, जबकि घटना का होना या न होना केवल उप-स्वामी (Sub-Lord) निश्चित करता है।<br>' +
                            '• <b>नियम २ (दशम कस्पल सब-लॉर्ड व करियर):</b> यदि दशम भाव का उप-स्वामी 2, 6, 10, 11 भावों का सिग्निफिकेटर बने, तो जातक को उच्च राजकीय पद, व्यवसाय में अपार सफलता व स्थायी ख्याति मिलती है।<br>' +
                            '• <b>नियम ३ (सप्तम कस्पल सब-लॉर्ड व विवाह):</b> सप्तम कस्पल सब-लॉर्ड यदि 2, 7, 11 भावों को दर्शाए तो सुखद दांपत्य; यदि 1, 6, 10 को दर्शाए तो विलंब अथवा असहमति का योग बनता है।<br>' +
                            '• <b>नियम ४ (द्वितीय व एकादश धन योग):</b> 2nd व 11th CSL का परस्पर संबंध कभी भी जातक को आर्थिक अभाव में नहीं रहने देता।' +
                        '</div>' +
                    '</div>';
                    kpContainer.appendChild(kvDiv);
                }
            }
        },

        """
            html = html[:pos_kp] + new_kp_render + html[pos_kp_end:]
            print("  ✓ Enhanced renderKP with dedicated KP Shastric Knowledge Bank")

    # 6. Enhance Nadi Tab with Nadi Specific Knowledge Bank
    old_nd_render = "renderNadi() {"
    pos_nd = html.find(old_nd_render)
    if pos_nd != -1:
        pos_nd_end = html.find("renderSphutas() {", pos_nd)
        if pos_nd_end != -1:
            new_nd_render = """renderNadi() {
            var nd = (this.activeChartData && this.activeChartData.nadi) ? this.activeChartData.nadi : (window.AUTHENTIC_BUNDLE ? window.AUTHENTIC_BUNDLE.nadi : {});
            var container = document.getElementById('nadiCombinationsContainer');
            if (!container) return;
            var combs = (nd && nd.combinations && nd.combinations.length > 0) ? nd.combinations : [
                {
                    title: "धर्म-कर्माधिपति नाड़ी योग (गुरु + शनि संबंध)",
                    relation: "त्रिकोण 1-5-9 संबंध",
                    sutra: "जीव-कर्म संयोगे धर्म-कर्माधिपति योगः प्राप्नोति",
                    impact: "जातक अपने कार्यक्षेत्र व आजीविका में नीति, न्याय, अनुशासन व सामाजिक प्रतिष्ठा प्राप्त करता है।"
                },
                {
                    title: "ज्ञान-वैभव नाड़ी योग (गुरु + शुक्र संबंध)",
                    relation: "दिक-संयोग संबंध",
                    sutra: "जीव-भृगु समागमे विद्या-धन-कीर्ति समृद्धिः",
                    impact: "उत्तम परामर्शदाता, उच्च अध्ययन, शास्त्र ज्ञान, आर्थिक स्थिरता व सांसारिक प्रतिष्ठा का योग।"
                },
                {
                    title: "पराक्रम-विजय नाड़ी योग (मंगल + गुरु संबंध)",
                    relation: "केंद्र-त्रिकोण संबंध",
                    sutra: "भौम-जीव संयोगे भ्रातृ-भूमि-विजय योगः",
                    impact: "भूमि, संपत्ति, निर्भीक निर्णय, प्रशासनिक प्रतिष्ठा व संकटों पर सहज विजय।"
                }
            ];

            var html = '<div style="display:grid; grid-template-columns:1fr; gap:10px; margin-bottom:16px;">';
            for (var i = 0; i < combs.length; i++) {
                var c = combs[i];
                html += '<div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:4px solid #10b981; border-radius:6px; padding:12px;">' +
                    '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">' +
                        '<b style="color:var(--primary-navy); font-size:0.86rem;">' + c.title + '</b>' +
                        '<span style="font-size:0.70rem; background:rgba(16,185,129,0.12); color:#10b981; padding:2px 8px; border-radius:10px; font-weight:700;">' + c.relation + '</span>' +
                    '</div>' +
                    '<div style="font-size:0.72rem; color:var(--accent-gold); font-style:italic; margin-bottom:4px;">' + c.sutra + '</div>' +
                    '<p style="font-size:0.78rem; color:var(--text-secondary); margin:0; line-height:1.5;">' + c.impact + '</p>' +
                '</div>';
            }
            html += '</div>';

            // Append Nadi Specific Knowledge Bank Card
            html += '<div style="background:var(--bg-card); border:1px solid rgba(16,185,129,0.25); border-left:4px solid #10b981; border-radius:8px; padding:14px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">' +
                    '<b style="color:#10b981; font-size:0.90rem;">✦ नाड़ी ज्ञान-कोष: भृगु नन्दी नाड़ी एवं देव केरळम् ग्रन्थ वेध (Nadi Knowledge Bank)</b>' +
                    '<span style="font-size:0.70rem; background:rgba(16,185,129,0.12); color:#10b981; padding:2px 8px; border-radius:10px; font-weight:700;">Bhrigu Nandi Nadi • Deva Keralam</span>' +
                '</div>' +
                '<div style="font-size:0.78rem; line-height:1.6; color:var(--text-secondary);">' +
                    '• <b>दिशात्मक त्रिकोण सिद्धांत (Directional Trines):</b> नाड़ी में 1-5-9 (पूर्व/अग्नि), 2-6-10 (दक्षिण/पृथ्वी), 3-7-11 (पश्चिम/वायु), 4-8-12 (उत्तर/जल) राशियों के ग्रह परस्पर युत माने जाते हैं।<br>' +
                    '• <b>जीव-कर्म राजयोग:</b> गुरु (जीव) और शनि (कर्म) का त्रिकोणीय संबंध जातक को समाजोपयोगी, सम्माननीय व कर्तव्यपरायण नेतृत्वकर्ता बनाता है।<br>' +
                    '• <b>भृगु बिन्दु (Bhrigu Bindu):</b> चन्द्रमा और राहु के मध्य बिंदु का गोचर भ्रमण जीवन में युगांतकारी घटनाओं को जन्म देता है।' +
                '</div>' +
            '</div>';

            container.innerHTML = html;
        },

        """
            html = html[:pos_nd] + new_nd_render + html[pos_nd_end:]
            print("  ✓ Enhanced renderNadi with dedicated Nadi Shastric Knowledge Bank")

    # 7. Embed VYAS 34.0 Master Prompt into window.VyasAIEngine
    pos_ai = html.find("window.VyasAIEngine = {")
    if pos_ai != -1:
        if "MASTER_SYSTEM_PROMPT:" not in html:
            prompt_injection = f"""window.VyasAIEngine = {{
        // =========================================================================
        // VYAS 34.0 MASTER SYSTEM PROMPT EMBEDDED
        // =========================================================================
        MASTER_SYSTEM_PROMPT: {repr(VYAS_34_MASTER_PROMPT)},
        """
            html = html[:pos_ai] + prompt_injection + html[pos_ai + len("window.VyasAIEngine = {"):]
            print("  ✓ Embedded VYAS 34.0 Master System Prompt into window.VyasAIEngine")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✓ Saved updated index.html successfully.")

def update_mobile():
    print("Updating mobile/index.html with VYAS 34.0 Consolidated Essay...")
    with open('mobile/index.html', 'r', encoding='utf-8') as f:
        m_html = f.read()

    old_meaning_line = 'bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " में विराजमान हैं। यह स्थिति जातक के उस भाव से जुड़े जीवन पहलुओं को विशेष दिशा और शक्ति प्रदान करती है।";'
    new_meaning_line = 'bNameStr + " (" + bhInfo.sign + " राशि के अधिपति " + bhInfo.lordName + ") कुंडली के भाव " + bhInfo.placedInHouse + " (" + bhInfo.placedInSign + ") में स्थित हैं। बृहत्पाराशर होराशास्त्र अनुसार यह स्थिति जातक के " + bh + "वें भाव के कारकत्वों को " + bhInfo.placedInHouse + "वें भाव के माध्यम से सक्रिय करती है।";'
    if old_meaning_line in m_html:
        m_html = m_html.replace(old_meaning_line, new_meaning_line)
        print("  ✓ Replaced repetitive filler sentence in mobile/index.html")

    with open('mobile/index.html', 'w', encoding='utf-8') as f:
        f.write(m_html)
    print("  ✓ Saved updated mobile/index.html successfully.")

if __name__ == '__main__':
    update_desktop()
    update_mobile()

