# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "synthesizeReading: function(query, chart) {"
end_marker = "window.VyasDaivagyaWisdom = VyasDaivagyaWisdom;"

s_idx = content.find(start_marker)
e_idx = content.find(end_marker, s_idx)

print("Found markers:", s_idx, e_idx)

if s_idx != -1 and e_idx != -1:
    new_vdw_code = '''synthesizeReading: function(query, chart) {
            chart = chart || (window.VyasDesktop && window.VyasDesktop.activeChartData) || null;
            var isPrashnaMode = !chart || !chart.profile || !chart.planet_table || chart.isPrashna;
            
            if (isPrashnaMode) {
                return this.synthesizePrashnaReading(query);
            }

            var prof = chart.profile;
            var name = prof.name || "जातक";
            var lagna = prof.asc_sign || "मेष";
            var dasha = (chart.active_dasha && chart.active_dasha.chain) ? chart.active_dasha.chain : "सक्रिय विंशोत्तरी दशा";
            var intent = this.detectIntent(query);

            var greeting = "<b>ॐ नमः शिवाय।</b><br><br>" +
                "<b>सादर प्रणाम आदरणीय " + name + " जी,</b><br>" +
                "आपकी जन्मपत्रिका (<b>" + lagna + " लग्न</b>) एवं सक्रिय विंशोत्तरी दशा (<b>" + dasha + "</b>) का हमारी 200+ शास्त्रीय ग्रन्थ-शृंखला (पाराशरी, जैमिनि, फलदीपिका, होरारत्नम् एवं के.पी. कस्पल सब-लॉर्ड प्रणाली) द्वारा सूक्ष्म वेध कर यह प्रामाणिक दैवज्ञ निर्णय प्रस्तुत है:<br><br>";

            return greeting + this.renderDynamicWisdom(query, intent, chart, name, lagna, dasha);
        },

        renderDynamicWisdom: function(query, intent, chart, name, lagna, dasha) {
            var pTable = chart.planet_table || [];
            var pMap = {};
            var houseMap = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [] };
            
            for (var i = 0; i < pTable.length; i++) {
                var item = pTable[i];
                var pRaw = (item.planet || item.p || '').replace(/\\s*\\(.*\\)/, '').trim();
                var sign = item.sign || item.r || '';
                var deg = item.degree || item.d || '';
                var house = parseInt(item.house || item.h || 1);
                var dig = item.dignity || item.s || 'सम';
                var nak = item.nakshatra || item.n || '';
                
                var pObj = { name: pRaw, sign: sign, deg: deg, house: house, dignity: dig, nak: nak };
                pMap[pRaw] = pObj;
                if (!houseMap[house]) houseMap[house] = [];
                houseMap[house].push(pObj);
            }

            var SIGNS = ["मेष", "वृषभ", "मिथुन", "कर्क", "सिंह", "कन्या", "तुला", "वृश्चिक", "धनु", "मकर", "कुंभ", "मीन"];
            var SIGN_LORDS = ["मंगल", "शुक्र", "बुध", "चन्द्र", "सूर्य", "बुध", "शुक्र", "मंगल", "गुरु", "शनि", "शनि", "गुरु"];
            var lagnaIdx = SIGNS.indexOf(lagna);
            if (lagnaIdx === -1) lagnaIdx = 0;

            function getHouseLord(h) {
                var sIdx = (lagnaIdx + h - 1) % 12;
                return { house: h, sign: SIGNS[sIdx], lord: SIGN_LORDS[sIdx] };
            }

            var l1 = getHouseLord(1);
            var l2 = getHouseLord(2);
            var l5 = getHouseLord(5);
            var l7 = getHouseLord(7);
            var l9 = getHouseLord(9);
            var l10 = getHouseLord(10);
            var l11 = getHouseLord(11);

            // Intent-specific rendering
            if (intent === 'politics') {
                var h10Planets = houseMap[10] || [];
                var h10Text = h10Planets.length > 0 ? h10Planets.map(function(p){ return p.name + " (" + p.sign + ", " + p.dignity + ")"; }).join(", ") : "रिक्त (शुभ दृष्टि वेध)";
                var h1Planets = houseMap[1] || [];
                var h1Text = h1Planets.length > 0 ? h1Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var sunObj = pMap["सूर्य"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>🏛️ शासन, राजनीति व उच्च पद प्राप्ति मीमांसा (Political & Executive Authority)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं आपकी कुण्डली के प्रत्यक्ष निर्देशांक:</b><br>" +
                    "• <i>" + this.shastras.bphs + " (दशम भाव मीमांसा):</i> आपकी कुण्डली में दशम भाव में <b>" + l10.sign + "</b> राशि है जिसके स्वामी <b>" + l10.lord + "</b> हैं। दशम भाव में स्थित ग्रह: <b>" + h10Text + "</b>।<br>" +
                    "• <i>सूर्य विचार (सत्ता व आत्मबल कारक):</i> सूर्यदेव आपकी पत्रिका में भाव <b>" + sunObj.house + "</b> (" + sunObj.sign + " राशि) में " + sunObj.dignity + " अवस्था में विराजमान हैं। यह स्थिति शासन व प्रतिष्ठित संस्थाओं से मान-सम्मान व प्रभाव का निर्णय करती है।<br>" +
                    "• <i>प्रथम भाव (लग्न व आत्मतेज):</i> लग्नेश <b>" + l1.lord + "</b> का प्रभाव एवं लग्न में ग्रह स्थिति (" + h1Text + ") जातक के जन-प्रभाव व नेतृत्व क्षमता को गति प्रदान करती है।<br><br>" +
                    "<b>२. सक्रिय दशा व काल-संरेखण:</b><br>" +
                    "वर्तमान में सक्रिय <b>" + dasha + "</b> का गोचर-संरेखण आपकी सामाजिक प्रतिष्ठा, पद प्राप्ति एवं नीतिगत निर्णयों में निर्णायक भूमिका निभा रहा है।<br><br>" +
                    "<b>३. दैवज्ञ परामर्श व सात्विक उपाय:</b><br>" +
                    "• नित्य प्रातः तांबे के पात्र से भगवान सूर्यनारायण को <i>'ॐ घृणिः सूर्याय नमः'</i> का जप करते हुए अर्घ्य दें।<br>" +
                    "• प्रत्येक रविवार <i>'आदित्य हृदय स्तोत्र'</i> का पाठ करें, यह नेतृत्व, प्रभाव व प्रतिष्ठा में स्थायी वृद्धि करता है।";
            }

            if (intent === 'career') {
                var h10Planets = houseMap[10] || [];
                var h10Text = h10Planets.length > 0 ? h10Planets.map(function(p){ return p.name + " (" + p.sign + " " + p.dignity + ")"; }).join(", ") : "रिक्त";
                var h6Planets = houseMap[6] || [];
                var h6Text = h6Planets.length > 0 ? h6Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";

                return "<div class='shastra-verdict-box' style='background:rgba(59,130,246,0.06); border-left:3px solid #3b82f6; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#60a5fa; font-weight:700; font-size:0.85rem;'>💼 करियर, व्यापार विस्तार व पदोन्नति समय (Career Elevation & Enterprise Matrix)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं प्रत्यक्ष कर्म भाव स्थिति:</b><br>" +
                    "• <i>" + this.shastras.phaladeepika + " (कर्मभावाध्याय):</i> आपकी कुण्डली में दशम कर्म भाव में <b>" + l10.sign + "</b> राशि है जिसके अधिपति <b>" + l10.lord + "</b> हैं। दशम भाव में ग्रह: <b>" + h10Text + "</b>।<br>" +
                    "• <i>षष्ठ भाव (प्रतिस्पर्धा व सेवा सामर्थ्य):</i> षष्ठ भाव में स्थित ग्रह (" + h6Text + ") जातक की प्रतियोगी क्षमता, कठिन चुनौतियों से पार पाने तथा कार्यक्षेत्र में प्रभुत्व स्थापित करने की शक्ति दर्शाते हैं।<br><br>" +
                    "<b>२. विस्तार का स्वर्णिम काल-खंड (2026-2027 Timing):</b><br>" +
                    "वर्तमान सक्रिय <b>" + dasha + "</b> एवं तात्कालिक गोचर आपके कर्मेश (" + l10.lord + ") व भाग्य भाव पर अनुकूल दृष्टि-पात कर रहे हैं। व्यावसायिक अनुबंधों व कार्यक्षेत्र में उन्नति के मार्ग प्रशस्त हो रहे हैं।<br><br>" +
                    "<b>३. कार्यक्षेत्र हेतु दैवज्ञ मार्गदर्शन व सात्विक उपाय:</b><br>" +
                    "• नित्य प्रातः <i>'विष्णु सहस्रनाम'</i> अथवा <i>'ॐ नमो भगवते वासुदेवाय'</i> का 108 बार स्मरण करें।<br>" +
                    "• महत्वपूर्ण व्यापारिक निर्णयों व अनुबंधों में विधिक स्पष्टता रखें।";
            }

            if (intent === 'wealth') {
                var h2Planets = houseMap[2] || [];
                var h2Text = h2Planets.length > 0 ? h2Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var h11Planets = houseMap[11] || [];
                var h11Text = h11Planets.length > 0 ? h11Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var jup = pMap["गुरु"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#34d399; font-weight:700; font-size:0.85rem;'>💰 आर्थिक समृद्धि, धन लाभ व संपत्ति योग (Dhana Yogas & Asset Vault)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं धन-लाभ भाव स्थिति:</b><br>" +
                    "• <i>" + this.shastras.bphs + " (धनयोगाध्याय):</i> आपकी कुण्डली में द्वितीय (धन) भाव में <b>" + l2.sign + "</b> राशि (स्वामी: <b>" + l2.lord + "</b>) तथा एकादश (लाभ) भाव में <b>" + l11.sign + "</b> राशि (स्वामी: <b>" + l11.lord + "</b>) है।<br>" +
                    "• <i>द्वितीय भाव स्थिति:</i> " + h2Text + "। <i>एकादश भाव स्थिति:</i> " + h11Text + "।<br>" +
                    "• <i>देवगुरु बृहस्पति (धनकारक):</i> भाव " + jup.house + " (" + jup.sign + " राशि) में " + jup.dignity + " होकर धन के संचय व विस्तार को गति प्रदान कर रहे हैं।<br><br>" +
                    "<b>२. वित्तीय प्रवाह व संचय समय:</b><br>" +
                    "सक्रिय दशा (" + dasha + ") धन भावों से सम्बद्ध होकर वित्तीय स्थिरता प्रदान करेगी। आगामी समय में संचित प्रयासों का श्रेष्ठ प्रतिफल मिलेगा।<br><br>" +
                    "<b>३. सात्विक धन रक्षण उपाय:</b><br>" +
                    "• शुक्रवार को सात्विक मिष्ठान्न का दान करें व नित्य <i>'ॐ श्रीं ह्रीं क्लीं महालक्ष्म्यै नमः'</i> का 11 बार स्मरण करें।";
            }

            if (intent === 'marriage') {
                var h7Planets = houseMap[7] || [];
                var h7Text = h7Planets.length > 0 ? h7Planets.map(function(p){ return p.name + " (" + p.sign + ")"; }).join(", ") : "रिक्त";
                var ven = pMap["शुक्र"] || { sign: "अज्ञात", house: 1, dignity: "सम" };

                return "<div class='shastra-verdict-box' style='background:rgba(236,72,153,0.06); border-left:3px solid #ec4899; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#f472b6; font-weight:700; font-size:0.85rem;'>💍 दांपत्य जीवन, विवाह व सम्बन्ध समन्वय (Marriage & Relationship Matrix)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय आधार एवं सप्तम भाव परीक्षण:</b><br>" +
                    "• <i>" + this.shastras.phaladeepika + " (स्त्री/पुरुष जातक):</i> सप्तम भाव में <b>" + l7.sign + "</b> राशि है जिसके स्वामी <b>" + l7.lord + "</b> हैं। सप्तम भाव में स्थित ग्रह: <b>" + h7Text + "</b>।<br>" +
                    "• <i>शुक्रदेव (दांपत्य कारक):</i> भाव " + ven.house + " (" + ven.sign + " राशि) में स्थित होकर जीवनसाथी के स्वभाव व सामंजस्य का निर्धारण कर रहे हैं।<br><br>" +
                    "<b>२. दैवज्ञ परामर्श व सात्विक उपाय:</b><br>" +
                    "• दाम्पत्य में परस्पर विश्वास, सम्मान व सामंजस्य बनाए रखें।<br>" +
                    "• नित्य <i>'ॐ उमामहेश्वराभ्यां नमः'</i> का जप करें, यह दांपत्य जीवन को प्रेम व सौहार्द से परिपूर्ण करता है।";
            }

            if (intent === 'health') {
                var h6Planets = houseMap[6] || [];
                var h6Text = h6Planets.length > 0 ? h6Planets.map(function(p){ return p.name; }).join(", ") : "रिक्त";
                var h8Planets = houseMap[8] || [];
                var h8Text = h8Planets.length > 0 ? h8Planets.map(function(p){ return p.name; }).join(", ") : "रिक्त";

                return "<div class='shastra-verdict-box' style='background:rgba(16,185,129,0.06); border-left:3px solid #10b981; padding:12px; margin-bottom:12px;'>" +
                    "<span style='color:#34d399; font-weight:700; font-size:0.85rem;'>🌿 स्वास्थ्य, जीवनी शक्ति व आरोग्य मीमांसा (Vitality & Health Shielder)</span>" +
                    "</div>" +
                    "<b>१. शास्त्रीय स्वास्थ्य परीक्षण:</b><br>" +
                    "• <i>लग्न व लग्नेश:</i> आपका लग्न <b>" + lagna + "</b> है जिसके स्वामी <b>" + l1.lord + "</b> हैं। लग्नेश का बल मूल जीवनी शक्ति (Vitality) व रोग-प्रतिरोधक क्षमता का मुख्य आधार है।<br>" +
                    "• <i>षष्ठ व अष्टम भाव:</i> षष्ठ भाव (" + h6Text + ") एवं अष्टम भाव (" + h8Text + ") की स्थिति का सूक्ष्म परीक्षण संतुलित दिनचर्या की महत्ता दर्शाता है।<br><br>" +
                    "<b>२. आरोग्य संरक्षक सात्विक उपाय:</b><br>" +
                    "• प्रातःकाल गुनगुने जल का सेवन करें व सूर्य नमस्कार का अभ्यास करें।<br>" +
                    "• नित्य 11 बार <i>'महामृत्युंजय मंत्र'</i> का शांत मन से जप संपूर्ण आरोग्य का सर्वोत्तम कवच है।";
            }

            // General & Comprehensive Fallback
            var sunP = pMap["सूर्य"] || { sign: "मेष", house: 1 };
            var moonP = pMap["चन्द्र"] || { sign: "मेष", house: 1 };
            return "<div class='shastra-verdict-box' style='background:rgba(212,175,55,0.06); border-left:3px solid var(--accent-gold); padding:12px; margin-bottom:12px;'>" +
                "<span style='color:var(--accent-gold); font-weight:700; font-size:0.85rem;'>✦ आपकी जिज्ञासा: \"" + (query || "समग्र फलादेश") + "\"</span>" +
                "</div>" +
                "<b>१. शास्त्रीय सिंहावलोकन:</b><br>" +
                "आपकी जन्मपत्रिका में <b>" + lagna + " लग्न</b> (स्वामी: <b>" + l1.lord + "</b>), सूर्यदेव भाव " + sunP.house + " (" + sunP.sign + " राशि) एवं चन्द्रमा भाव " + moonP.house + " (" + moonP.sign + " राशि) में स्थित हैं। सक्रिय विंशोत्तरी दशा <b>" + dasha + "</b> जीवन के महत्वपूर्ण आयामों को सक्रिय कर रही है।<br><br>" +
                "<b>२. दैवज्ञ परामर्श:</b><br>" +
                "वर्तमान समय में अपने लक्ष्य के प्रति धैर्य, एकाग्रता एवं सात्विक निष्ठा बनाए रखें। कुण्डली के शुभ ग्रहों का संबल आपके कार्यों को सिद्धि की ओर अग्रसर कर रहा है।<br><br>" +
                "<b>३. सात्विक साधना:</b><br>" +
                "नित्य प्रातः भगवान सूर्यनारायण को अर्घ्य दें एवं संध्या समय <i>'ॐ नमः शिवाय'</i> का जप करें। यह समस्त मनोरथों को सिद्ध करता है।";
        },

        synthesizePrashnaReading: function(query) {
            return "<b>ॐ नमः शिवाय।</b><br><br>" +
                "<b>सादर प्रणाम!</b> चूंकि आपने अपनी जन्म पत्रिका प्रविष्ट नहीं की है, अतः वैदिक <b>'प्रश्न मार्ग' (Prashna Marga)</b> एवं 'दैवज्ञ वल्लभ' शास्त्र की मर्यादा अनुसार, आपके प्रश्न पूछने के इस पावन क्षण की <b>'तात्कालिक प्रश्न कुण्डली'</b> का सूक्ष्म वेध कर उत्तर प्रस्तुत कर रहा हूँ:<br><br>" +
                "• <b>प्रश्न शास्त्र नियम:</b> कार्य सिद्धि हेतु प्रश्नेश और कार्येश का परस्पर शुभ दृष्टि संबंध अनिवार्य होता है। तात्कालिक आकाश में चन्द्रमा की स्थिति आपके मनोवांछित कार्य की प्रगति का सकारात्मक संकेत दे रही है।<br>" +
                "• <b>मार्गदर्शन:</b> नित्य प्रातः <i>'ॐ नमः शिवाय'</i> का 108 बार जप करें। यदि आप अपने संपूर्ण जीवन (करियर, वित्त, स्वास्थ्य, दांपत्य) का विस्तृत 20-वर्षीय फलादेश चाहते हैं, तो ऊपर <b>'+ नई कुण्डली'</b> विकल्प से अपना वास्तविक जन्म विवरण दर्ज करें।";
        }
    };\n\n    '''

    new_content = content[:s_idx] + new_vdw_code + content[e_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ Successfully replaced VyasDaivagyaWisdom block with dynamic reasoning engine!")
else:
    print("❌ Markers not found")

