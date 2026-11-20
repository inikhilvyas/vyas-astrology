import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -----------------------------------------------------------------------------
# 1. Add lookupDirectAstrologicalTruth to VyasAIEngine in index.html
# -----------------------------------------------------------------------------
truth_js = '''
        lookupDirectAstrologicalTruth: function(query) {
            if (!query) return null;
            var q = query.toLowerCase().trim();

            var isLordQuery = /(स्वामी|मालिक|अधिपति|भावेश|लॉर्ड|lord|ruler|governs|master)/.test(q);
            var isNakshatraQuery = /(नक्षत्र|nakshatra)/.test(q);

            // 1. 27 Nakshatras
            var nakshatras = [
                { pats: ['अनुराधा', 'anuradha'], name: 'अनुराधा (Anuradha)', lord: 'शनिदेव (Saturn)', group: 'पुष्य, अनुराधा, उत्तराभाद्रपद', deity: 'मित्र देव', shloka: 'अनुराधायाः स्वामी शनैश्चरः स्मृतः।', details: 'विंशोत्तरी दशा नियमानुसार अनुराधा नक्षत्र के अधिपति ग्रह <b>शनिदेव (Saturn)</b> हैं। इस नक्षत्र पर शनि की 19 वर्षीय महादशा का आधिपत्य होता है।' },
                { pats: ['अश्विनी', 'ashwini'], name: 'अश्विनी (Ashwini)', lord: 'केतु (Ketu)', group: 'अश्विनी, मघा, मूल', deity: 'अश्विनी कुमार', shloka: 'अश्विनीशः शिखी ज्ञेयः।', details: 'विंशोत्तरी दशा नियमानुसार अश्विनी नक्षत्र के स्वामी <b>केतुदेव</b> हैं।' },
                { pats: ['भरणी', 'bharani'], name: 'भरणी (Bharani)', lord: 'शुक्रदेव (Venus)', group: 'भरणी, पूर्वाफाल्गुनी, पूर्वाषाढ़ा', deity: 'यमराज', shloka: 'भरण्यां भृगुजः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार भरणी नक्षत्र के स्वामी <b>शुक्रदेव (Venus)</b> हैं।' },
                { pats: ['कृत्तिका', 'कृतिका', 'krittika'], name: 'कृत्तिका (Krittika)', lord: 'सूर्यदेव (Sun)', group: 'कृत्तिका, उत्तराफाल्गुनी, उत्तराषाढ़ा', deity: 'अग्नि देव', shloka: 'कृत्तिकाया रविः स्वामी।', details: 'विंशोत्तरी दशा नियमानुसार कृत्तिका नक्षत्र के स्वामी <b>सूर्यदेव (Sun)</b> हैं।' },
                { pats: ['रोहिणी', 'rohini'], name: 'रोहिणी (Rohini)', lord: 'चन्द्रदेव (Moon)', group: 'रोहिणी, हस्त, श्रवण', deity: 'प्रजापति ब्रह्मा', shloka: 'रोहिण्याः शशिनायकः।', details: 'विंशोत्तरी दशा नियमानुसार रोहिणी नक्षत्र के स्वामी <b>चन्द्रदेव (Moon)</b> हैं।' },
                { pats: ['मृगशिरा', 'मृगशीर्ष', 'mrigashira'], name: 'मृगशिरा (Mrigashira)', lord: 'मंगलदेव (Mars)', group: 'मृगशिरा, चित्रा, धनिष्ठा', deity: 'सोम (चन्द्र)', shloka: 'मृगे भौमः प्रभुः स्मृतः।', details: 'विंशोत्तरी दशा नियमानुसार मृगशिरा नक्षत्र के स्वामी <b>मंगलदेव (Mars)</b> हैं।' },
                { pats: ['आर्द्रा', 'आद्रा', 'ardra'], name: 'आर्द्रा (Ardra)', lord: 'राहु (Rahu)', group: 'आर्द्रा, स्वाति, शतभिषा', deity: 'रुद्र (शिव)', shloka: 'आर्द्राया राहुनायकः।', details: 'विंशोत्तरी दशा नियमानुसार आर्द्रा नक्षत्र के स्वामी <b>राहुदेव (Rahu)</b> हैं।' },
                { pats: ['पुनर्वसु', 'punarvasu'], name: 'पुनर्वसु (Punarvasu)', lord: 'देवगुरु बृहस्पति (Jupiter)', group: 'पुनर्वसु, विशाखा, पूर्वाभाद्रपद', deity: 'अदिति', shloka: 'पुनर्वसौ गुरुः स्वामी।', details: 'विंशोत्तरी दशा नियमानुसार पुनर्वसु नक्षत्र के स्वामी <b>देवगुरु बृहस्पति (Jupiter)</b> हैं।' },
                { pats: ['पुष्य', 'तिष्य', 'pushya'], name: 'पुष्य (Pushya)', lord: 'शनिदेव (Saturn)', group: 'पुष्य, अनुराधा, उत्तराभाद्रपद', deity: 'बृहस्पति', shloka: 'पुष्ये मन्दः प्रभुः सदा।', details: 'विंशोत्तरी दशा नियमानुसार पुष्य नक्षत्र के स्वामी <b>शनिदेव (Saturn)</b> हैं।' },
                { pats: ['आश्लेषा', 'अश्लेषा', 'ashlesha'], name: 'आश्लेषा (Ashlesha)', lord: 'बुधदेव (Mercury)', group: 'आश्लेषा, ज्येष्ठा, रेवती', deity: 'सर्प (नाग)', shloka: 'आश्लेषाया बुधो नाथः।', details: 'विंशोत्तरी दशा नियमानुसार आश्लेषा नक्षत्र के स्वामी <b>बुधदेव (Mercury)</b> हैं।' },
                { pats: ['मघा', 'magha'], name: 'मघा (Magha)', lord: 'केतु (Ketu)', group: 'अश्विनी, मघा, मूल', deity: 'पितर', shloka: 'मघायाः शिखिनायकः।', details: 'विंशोत्तरी दशा नियमानुसार मघा नक्षत्र के स्वामी <b>केतुदेव</b> हैं।' },
                { pats: ['पूर्वाफाल्गुनी', 'पूर्वा फाल्गुनी', 'purva phalguni'], name: 'पूर्वाफाल्गुनी (Purva Phalguni)', lord: 'शुक्रदेव (Venus)', group: 'भरणी, पूर्वाफाल्गुनी, पूर्वाषाढ़ा', deity: 'भग', shloka: 'पूर्वाफाल्गुन्यां भार्गवः।', details: 'विंशोत्तरी दशा नियमानुसार पूर्वाफाल्गुनी नक्षत्र के स्वामी <b>शुक्रदेव (Venus)</b> हैं।' },
                { pats: ['उत्तराफाल्गुनी', 'उत्तरा फाल्गुनी', 'uttara phalguni'], name: 'उत्तराफाल्गुनी (Uttara Phalguni)', lord: 'सूर्यदेव (Sun)', group: 'कृत्तिका, उत्तराफाल्गुनी, उत्तराषाढ़ा', deity: 'अर्यमा', shloka: 'उत्तराया रविरधिपः।', details: 'विंशोत्तरी दशा नियमानुसार उत्तराफाल्गुनी नक्षत्र के स्वामी <b>सूर्यदेव (Sun)</b> हैं।' },
                { pats: ['हस्त', 'hasta'], name: 'हस्त (Hasta)', lord: 'चन्द्रदेव (Moon)', group: 'रोहिणी, हस्त, श्रवण', deity: 'सूर्य (सविता)', shloka: 'हस्ते चन्द्रः प्रभुः स्मृतः।', details: 'विंशोत्तरी दशा नियमानुसार हस्त नक्षत्र के स्वामी <b>चन्द्रदेव (Moon)</b> हैं।' },
                { pats: ['चित्रा', 'chitra'], name: 'चित्रा (Chitra)', lord: 'मंगलदेव (Mars)', group: 'मृगशिरा, चित्रा, धनिष्ठा', deity: 'त्वष्टा (विश्वकर्मा)', shloka: 'चित्राया भौमनायकः।', details: 'विंशोत्तरी दशा नियमानुसार चित्रा नक्षत्र के स्वामी <b>मंगलदेव (Mars)</b> हैं।' },
                { pats: ['स्वाति', 'स्वाती', 'swati'], name: 'स्वाति (Swati)', lord: 'राहु (Rahu)', group: 'आर्द्रा, स्वाति, शतभिषा', deity: 'वायु देव', shloka: 'स्वात्यां राहुः प्रभुः सदा।', details: 'विंशोत्तरी दशा नियमानुसार स्वाति नक्षत्र के स्वामी <b>राहुदेव (Rahu)</b> हैं।' },
                { pats: ['विशाखा', 'vishakha'], name: 'विशाखा (Vishakha)', lord: 'देवगुरु बृहस्पति (Jupiter)', group: 'पुनर्वसु, विशाखा, पूर्वाभाद्रपद', deity: 'इन्द्राग्नि', shloka: 'विशाखाया गुरुः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार विशाखा नक्षत्र के स्वामी <b>देवगुरु बृहस्पति (Jupiter)</b> हैं।' },
                { pats: ['ज्येष्ठा', 'jyeshtha'], name: 'ज्येष्ठा (Jyeshtha)', lord: 'बुधदेव (Mercury)', group: 'आश्लेषा, ज्येष्ठा, रेवती', deity: 'इन्द्र', shloka: 'ज्येष्ठाया बुधनायकः।', details: 'विंशोत्तरी दशा नियमानुसार ज्येष्ठा नक्षत्र के स्वामी <b>बुधदेव (Mercury)</b> हैं।' },
                { pats: ['मूल', 'moola', 'mula'], name: 'मूल (Moola)', lord: 'केतु (Ketu)', group: 'अश्विनी, मघा, मूल', deity: 'निरृति', shloka: 'मूले केतुः प्रभुः स्मृतः।', details: 'विंशोत्तरी दशा नियमानुसार मूल नक्षत्र के स्वामी <b>केतुदेव</b> हैं।' },
                { pats: ['पूर्वाषाढ़ा', 'पूर्वाषाढा', 'purva ashadha'], name: 'पूर्वाषाढ़ा (Purva Ashadha)', lord: 'शुक्रदेव (Venus)', group: 'भरणी, पूर्वाफाल्गुनी, पूर्वाषाढ़ा', deity: 'जल (आपः)', shloka: 'पूर्वाषाढायां शुक्रः।', details: 'विंशोत्तरी दशा नियमानुसार पूर्वाषाढ़ा नक्षत्र के स्वामी <b>शुक्रदेव (Venus)</b> हैं।' },
                { pats: ['उत्तराषाढ़ा', 'उत्तराषाढा', 'uttara ashadha'], name: 'उत्तराषाढ़ा (Uttara Ashadha)', lord: 'सूर्यदेव (Sun)', group: 'कृत्तिका, उत्तराफाल्गुनी, उत्तराषाढ़ा', deity: 'विश्वेदेव', shloka: 'उत्तराषाढायां रविः।', details: 'विंशोत्तरी दशा नियमानुसार उत्तराषाढ़ा नक्षत्र के स्वामी <b>सूर्यदेव (Sun)</b> हैं।' },
                { pats: ['श्रवण', 'shravana'], name: 'श्रवण (Shravana)', lord: 'चन्द्रदेव (Moon)', group: 'रोहिणी, हस्त, श्रवण', deity: 'भगवान विष्णु', shloka: 'श्रवणे चन्द्रमाः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार श्रवण नक्षत्र के स्वामी <b>चन्द्रदेव (Moon)</b> हैं।' },
                { pats: ['धनिष्ठा', 'dhanishta'], name: 'धनिष्ठा (Dhanishta)', lord: 'मंगलदेव (Mars)', group: 'मृगशिरा, चित्रा, धनिष्ठा', deity: 'अष्ट वसु', shloka: 'धनिष्ठाया कुजः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार धनिष्ठा नक्षत्र के स्वामी <b>मंगलदेव (Mars)</b> हैं।' },
                { pats: ['शतभिषा', 'शततारका', 'shatabhisha'], name: 'शतभिषा (Shatabhisha)', lord: 'राहु (Rahu)', group: 'आर्द्रा, स्वाति, शतभिषा', deity: 'वरुण देव', shloka: 'शतभिषायां राहुः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार शतभिषा नक्षत्र के स्वामी <b>राहुदेव (Rahu)</b> हैं।' },
                { pats: ['पूर्वाभाद्रपद', 'purva bhadrapada'], name: 'पूर्वाभाद्रपद (Purva Bhadrapada)', lord: 'देवगुरु बृहस्पति (Jupiter)', group: 'पुनर्वसु, विशाखा, पूर्वाभाद्रपद', deity: 'अजैकपाद', shloka: 'पूर्वाभाद्रे गुरुः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार पूर्वाभाद्रपद नक्षत्र के स्वामी <b>देवगुरु बृहस्पति (Jupiter)</b> हैं।' },
                { pats: ['उत्तराभाद्रपद', 'uttara bhadrapada'], name: 'उत्तराभाद्रपद (Uttara Bhadrapada)', lord: 'शनिदेव (Saturn)', group: 'पुष्य, अनुराधा, उत्तराभाद्रपद', deity: 'अहिर्बुध्न्य', shloka: 'उत्तराभाद्रे मन्दः प्रभुः।', details: 'विंशोत्तरी दशा नियमानुसार उत्तराभाद्रपद नक्षत्र के स्वामी <b>शनिदेव (Saturn)</b> हैं।' },
                { pats: ['रेवती', 'revati'], name: 'रेवती (Revati)', lord: 'बुधदेव (Mercury)', group: 'आश्लेषा, ज्येष्ठा, रेवती', deity: 'पूषा देव', shloka: 'रेवत्यां ज्ञः प्रभुः स्मृतः।', details: 'विंशोत्तरी दशा नियमानुसार रेवती नक्षत्र के स्वामी <b>बुधदेव (Mercury)</b> हैं।' }
            ];

            for (var i = 0; i < nakshatras.length; i++) {
                var nak = nakshatras[i];
                var m = nak.pats.some(function(p) { return q.indexOf(p) !== -1; });
                if (m && (isLordQuery || isNakshatraQuery)) {
                    return "<b>सादर प्रणाम। प्रामाणिक वैदिक ज्योतिषीय सिद्धांत प्रमाण:</b><br><br>" +
                           "✦ <b>नक्षत्र:</b> " + nak.name + "<br>" +
                           "✦ <b>विंशोत्तरी दशाधिपति (स्वामी):</b> <span style='color:#d4af37; font-size:1.05rem; font-weight:700;'>" + nak.lord + "</span><br>" +
                           "✦ <b>अधिष्ठाता देवता:</b> " + nak.deity + "<br>" +
                           "✦ <b>समान दशाधिपति नक्षत्र समूह:</b> " + nak.group + "<br><br>" +
                           "<b>शास्त्रीय प्रमाण (बृहत्पाराशर होराशास्त्र / फलदीपिका):</b><br>" +
                           "<i>\"" + nak.shloka + "\"</i><br>" +
                           nak.details + "<br><br>" +
                           "<small style='color:#94a3b8;'>✓ व्यास अस्त्र प्रामाणिक सिद्धान्त: यह गणना महर्षि पाराशर प्रणीत विंशोत्तरी महादशा पद्धति के 100% गणितीय नियमों पर आधारित है।</small>";
                }
            }

            // 2. 12 Rashis
            var rashis = [
                { pats: ['मिथुन', 'gemini'], name: 'मिथुन राशि (Gemini)', lord: 'बुधदेव (Mercury)', element: 'वायु तत्त्व (Air)', nature: 'द्विस्वभाव (Dual)', shloka: 'भौमशुक्रबुधेंद्वर्कसौम्यशुक्रावनीसुताः। जीवेन्दुपूज्यावकीनां क्षेत्राणि क्रमशः स्मृताः॥', details: 'त्रिकाल सत्य: <b>मिथुन राशि के अधिपति केवल और केवल बुधदेव (Mercury) हैं</b> (कदापि शुक्र नहीं)। कालपुरुष चक्र में मिथुन तृतीय भाव (पराक्रम, संवाद व मेधा) का प्रतिनिधित्व करती है।' },
                { pats: ['मेष', 'aries'], name: 'मेष राशि (Aries)', lord: 'मंगलदेव (Mars)', element: 'अग्नि तत्त्व (Fire)', nature: 'चर (Movable)', shloka: 'कुजस्य क्षेत्रं प्रथमं मेषसंज्ञम्।', details: 'मेष राशि के अधिपति ग्रह <b>मंगलदेव (Mars)</b> हैं। कालपुरुष के प्रथम भाव की यह राशि साहस, ऊर्जा व नेतृत्व की प्रतीक है।' },
                { pats: ['वृषभ', 'वृष', 'taurus'], name: 'वृषभ राशि (Taurus)', lord: 'शुक्रदेव (Venus)', element: 'पृथ्वी तत्त्व (Earth)', nature: 'स्थिर (Fixed)', shloka: 'शुक्रस्य भवनं वृषः।', details: 'वृषभ राशि के अधिपति ग्रह <b>शुक्रदेव (Venus)</b> हैं। यह स्थिर पृथ्वी तत्त्व की राशि धन, वाणी, कुटुंब व सौंदर्य की प्रतीक है।' },
                { pats: ['कर्क', 'cancer'], name: 'कर्क राशि (Cancer)', lord: 'चन्द्रदेव (Moon)', element: 'जल तत्त्व (Water)', nature: 'चर (Movable)', shloka: 'कर्कस्य चन्द्रमाः स्वामी।', details: 'कर्क राशि के अधिपति ग्रह <b>चन्द्रदेव (Moon)</b> हैं। कालपुरुष के चतुर्थ भाव की यह राशि भावना व संवेदनशीलता का केंद्र है।' },
                { pats: ['सिंह', 'leo'], name: 'सिंह राशि (Leo)', lord: 'सूर्यदेव (Sun)', element: 'अग्नि तत्त्व (Fire)', nature: 'स्थिर (Fixed)', shloka: 'सिंहस्य स्वामी दिनकृत्।', details: 'सिंह राशि के अधिपति ग्रह <b>भगवान सूर्यदेव (Sun)</b> हैं। कालपुरुष के पंचम भाव की यह राशि आत्मगौरव, पराक्रम व तेज की प्रतीक है।' },
                { pats: ['कन्या', 'virgo'], name: 'कन्या राशि (Virgo)', lord: 'बुधदेव (Mercury)', element: 'पृथ्वी तत्त्व (Earth)', nature: 'द्विस्वभाव (Dual)', shloka: 'कन्याया अपि बुधः स्वामी।', details: 'कन्या राशि के अधिपति ग्रह <b>बुधदेव (Mercury)</b> हैं। बुधदेव इस राशि में उच्च के भी होते हैं (15° तक)। यह राशि विश्लेषण व कौशल की प्रतीक है।' },
                { pats: ['तुला', 'libra'], name: 'तुला राशि (Libra)', lord: 'शुक्रदेव (Venus)', element: 'वायु तत्त्व (Air)', nature: 'चर (Movable)', shloka: 'तुलाया भार्गवः स्वामी।', details: 'तुला राशि के अधिपति ग्रह <b>शुक्रदेव (Venus)</b> हैं। कालपुरुष के सप्तम भाव (साझेदारी व संतुलन) की यह राशि न्याय व संतुलन की प्रतीक है।' },
                { pats: ['वृश्चिक', 'scorpio'], name: 'वृश्चिक राशि (Scorpio)', lord: 'मंगलदेव (Mars) [सह-स्वामी: केतु]', element: 'जल तत्त्व (Water)', nature: 'स्थिर (Fixed)', shloka: 'वृश्चिकस्य कुजः स्वामी।', details: 'वृश्चिक राशि के प्रधान अधिपति ग्रह <b>मंगलदेव (Mars)</b> हैं (केतु सह-स्वामी माने जाते हैं)। कालपुरुष के अष्टम भाव की यह राशि गूढ़ ज्ञान व शोध की प्रतीक है।' },
                { pats: ['धनु', 'sagittarius'], name: 'धनु राशि (Sagittarius)', lord: 'देवगुरु बृहस्पति (Jupiter)', element: 'अग्नि तत्त्व (Fire)', nature: 'द्विस्वभाव (Dual)', shloka: 'धनुषो गुरुनायकः।', details: 'धनु राशि के अधिपति ग्रह <b>देवगुरु बृहस्पति (Jupiter)</b> हैं। कालपुरुष के नवम भाव (धर्म, भाग्य व दर्शन) की यह राशि सात्विक विवेक की प्रतीक है।' },
                { pats: ['मकर', 'capricorn'], name: 'मकर राशि (Capricorn)', lord: 'शनिदेव (Saturn)', element: 'पृथ्वी तत्त्व (Earth)', nature: 'चर (Movable)', shloka: 'मकरस्य प्रभुर्मन्दः।', details: 'मकर राशि के अधिपति ग्रह <b>शनिदेव (Saturn)</b> हैं। कालपुरुष के दशम भाव (कर्म व आजीविका) की यह राशि अनुशासन व दायित्व की प्रतीक है।' },
                { pats: ['कुंभ', 'कुम्भ', 'aquarius'], name: 'कुम्भ राशि (Aquarius)', lord: 'शनिदेव (Saturn) [सह-स्वामी: राहु]', element: 'वायु तत्त्व (Air)', nature: 'स्थिर (Fixed)', shloka: 'कुम्भस्य मन्दनायकः।', details: 'कुम्भ राशि के प्रधान अधिपति ग्रह <b>शनिदेव (Saturn)</b> हैं (राहु सह-स्वामी हैं)। कालपुरुष के एकादश भाव की यह राशि उच्च दार्शनिक चेतना की प्रतीक है।' },
                { pats: ['मीन', 'pisces'], name: 'मीन राशि (Pisces)', lord: 'देवगुरु बृहस्पति (Jupiter)', element: 'जल तत्त्व (Water)', nature: 'द्विस्वभाव (Dual)', shloka: 'मीनस्य च गुरुः स्वामी।', details: 'मीन राशि के अधिपति ग्रह <b>देवगुरु बृहस्पति (Jupiter)</b> हैं। कालपुरुष के द्वादश भाव (मोक्ष व अंतर्ज्ञान) की यह राशि आध्यात्मिक पूर्णता की प्रतीक है।' }
            ];

            for (var j = 0; j < rashis.length; j++) {
                var ras = rashis[j];
                var mr = ras.pats.some(function(p) { return q.indexOf(p) !== -1; });
                if (mr && isLordQuery) {
                    return "<b>सादर प्रणाम। प्रामाणिक वैदिक ज्योतिषीय सिद्धांत प्रमाण:</b><br><br>" +
                           "✦ <b>राशि:</b> " + ras.name + "<br>" +
                           "✦ <b>राश्याधिपति (स्वामी / भावेश):</b> <span style='color:#d4af37; font-size:1.05rem; font-weight:700;'>" + ras.lord + "</span><br>" +
                           "✦ <b>तत्त्व एवं स्वभाव:</b> " + ras.element + " • " + ras.nature + "<br><br>" +
                           "<b>शास्त्रीय संहिता प्रमाण (बृहत्पाराशर होराशास्त्र, अध्याय 3):</b><br>" +
                           "<i>\"" + ras.shloka + "\"</i><br>" +
                           ras.details + "<br><br>" +
                           "<small style='color:#94a3b8;'>✓ व्यास अस्त्र प्रामाणिक सिद्धान्त: 12 राशियों के स्वामियों का यह नियम महर्षि पाराशर द्वारा प्रतिपादित अखंड सिद्धांत है।</small>";
                }
            }

            // 3. Exaltation & Debilitation
            if (/(उच्च|नीच|exalted|debilitated)/.test(q) && /(सूर्य|चन्द्र|मंगल|बुध|गुरु|शुक्र|शनि|राहु|केतु|sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu)/.test(q)) {
                var dignities = {
                    'सूर्य': { name: 'सूर्यदेव', exalt: 'मेष (10° परम उच्च)', deb: 'तुला (10° परम नीच)', own: 'सिंह' },
                    'चन्द्र': { name: 'चन्द्रदेव', exalt: 'वृषभ (3° परम उच्च)', deb: 'वृश्चिक (3° परम नीच)', own: 'कर्क' },
                    'मंगल': { name: 'मंगलदेव', exalt: 'मकर (28° परम उच्च)', deb: 'कर्क (28° परम नीच)', own: 'मेष, वृश्चिक' },
                    'बुध': { name: 'बुधदेव', exalt: 'कन्या (15° परम उच्च)', deb: 'मीन (15° परम नीच)', own: 'मिथुन, कन्या' },
                    'गुरु': { name: 'देवगुरु बृहस्पति', exalt: 'कर्क (5° परम उच्च)', deb: 'मकर (5° परम नीच)', own: 'धनु, मीन' },
                    'शुक्र': { name: 'शुक्रदेव', exalt: 'मीन (27° परम उच्च)', deb: 'कन्या (27° परम नीच)', own: 'वृषभ, तुला' },
                    'शनि': { name: 'शनिदेव', exalt: 'तुला (20° परम उच्च)', deb: 'मेष (20° परम नीच)', own: 'मकर, कुंभ' }
                };
                for (var pk in dignities) {
                    if (q.indexOf(pk) !== -1) {
                        var info = dignities[pk];
                        return "<b>सादर प्रणाम। शास्त्रीय उच्च-नीच ग्रह स्थिति प्रमाण (बृहत्पाराशर होराशास्त्र):</b><br><br>" +
                               "✦ <b>ग्रह:</b> " + info.name + "<br>" +
                               "✦ <b>उच्च राशि:</b> <span style='color:#10b981; font-weight:700;'>" + info.exalt + "</span><br>" +
                               "✦ <b>नीच राशि:</b> <span style='color:#ef4444; font-weight:700;'>" + info.deb + "</span><br>" +
                               "✦ <b>स्वराशि:</b> " + info.own + "<br><br>" +
                               "<small style='color:#94a3b8;'>✓ व्यास अस्त्र शुद्ध खगोलीय व वैदिक होरा प्रमाण।</small>";
                    }
                }
            }

            // 4. Drishti
            if (/(दृष्टि|aspect)/.test(q)) {
                if (q.indexOf('शनि') !== -1) {
                    return "<b>सादर प्रणाम। शनिदेव की शास्त्रीय दृष्टियों का अखंड नियम:</b><br><br>" +
                           "✦ <b>शनिदेव की पूर्ण दृष्टियां:</b> <span style='color:#d4af37; font-weight:700;'>3री, 7वीं एवं 10वीं</span> भाव पर पूर्ण दृष्टि होती है।<br>" +
                           "<i>\"पश्यन्ति त्रिदशं मन्दः...\" (बृहत्पाराशर होराशास्त्र)</i><br>" +
                           "विशेष निर्देश: शनिदेव की 5वीं अथवा 9वीं दृष्टि कदापि नहीं होती।";
                }
                if (q.indexOf('मंगल') !== -1) {
                    return "<b>सादर प्रणाम। मंगलदेव की शास्त्रीय दृष्टियों का अखंड नियम:</b><br><br>" +
                           "✦ <b>मंगलदेव की पूर्ण दृष्टियां:</b> <span style='color:#d4af37; font-weight:700;'>4थी, 7वीं एवं 8वीं</span> भाव पर पूर्ण दृष्टि होती है।<br>" +
                           "<i>\"चतुर्थमष्टमं भौमः...\" (बृहत्पाराशर होराशास्त्र)</i>";
                }
                if (q.indexOf('गुरु') !== -1 || q.indexOf('बृहस्पति') !== -1) {
                    return "<b>सादर प्रणाम। देवगुरु बृहस्पति की शास्त्रीय दृष्टियों का अखंड नियम:</b><br><br>" +
                           "✦ <b>देवगुरु बृहस्पति की पूर्ण दृष्टियां:</b> <span style='color:#d4af37; font-weight:700;'>5वीं, 7वीं एवं 9वीं (त्रिकोण दृष्टि)</span> अमृतमय दृष्टि होती है।<br>" +
                           "<i>\"त्रिकोणं च गुरोः स्मृतम्...\" (बृहत्पाराशर होराशास्त्र)</i>";
                }
            }

            return null;
        },
'''

# Check if lookupDirectAstrologicalTruth already exists in index.html
if 'lookupDirectAstrologicalTruth' not in html:
    pos_ask = html.find('async askSage(query, activeChart) {')
    assert pos_ask != -1, 'askSage not found'
    html = html[:pos_ask] + truth_js + '\n        ' + html[pos_ask:]
    print("Injected lookupDirectAstrologicalTruth into VyasAIEngine.")

# In askSage, call lookupDirectAstrologicalTruth at top:
ask_intercept = '''            // 0. Deterministic Astrological Axiom Interceptor (Zero Hallucination Gate)
            var directAxiomReply = this.lookupDirectAstrologicalTruth(query);
            if (directAxiomReply) {
                if (window.VyasAIEngine && window.VyasAIEngine.chatHistory) {
                    window.VyasAIEngine.chatHistory.push({ role: "user", content: query });
                    window.VyasAIEngine.chatHistory.push({ role: "assistant", content: directAxiomReply });
                }
                return directAxiomReply;
            }
'''
if '0. Deterministic Astrological Axiom Interceptor' not in html:
    pos_proxy = html.find('// 1. Try PHP Backend Proxy First')
    assert pos_proxy != -1, 'proxy anchor not found'
    html = html[:pos_proxy] + ask_intercept + '\n            ' + html[pos_proxy:]
    print("Injected client-side axiom intercept into askSage.")

# -----------------------------------------------------------------------------
# 2. Update init() to synchronously restore googleUser before loadStoredProfile
# -----------------------------------------------------------------------------
old_init = '''        init() {
            this.loadStoredProfile();
            this.initGoogleAuth();'''

new_init = '''        init() {
            // STEP 0: Synchronously restore authenticated googleUser from localStorage FIRST!
            try {
                var savedGoogle = localStorage.getItem('vyas_google_user');
                if (savedGoogle) {
                    var parsedG = JSON.parse(savedGoogle);
                    if (parsedG && parsedG.email && parsedG.isVerified && parsedG.email !== 'user@gmail.com') {
                        this.googleUser = parsedG;
                    }
                }
            } catch(e) {}

            // STEP 1: Load stored profile (with this.googleUser populated, so vault can be retrieved!)
            this.loadStoredProfile();

            // STEP 2: Initialize Google Identity Services & Auth listeners
            this.initGoogleAuth();'''

if old_init in html:
    html = html.replace(old_init, new_init)
    print("Updated VyasDesktop.init() to synchronously restore googleUser.")

# Also in init(), call restoreSageChat() at the end
old_init_end = '''            this.initPanchangClock();
        },'''

new_init_end = '''            this.initPanchangClock();
            
            // STEP 4: Restore previous AI Chat history in Cockpit
            if (typeof this.restoreSageChat === 'function') {
                this.restoreSageChat();
            }
        },'''

if old_init_end in html:
    html = html.replace(old_init_end, new_init_end)
    print("Added restoreSageChat() to VyasDesktop.init().")

# -----------------------------------------------------------------------------
# 3. Harden loadStoredProfile() to auto-restore active Kundli on reload
# -----------------------------------------------------------------------------
old_load_profile_block = '''            var hasStored = false;
            this.activeChartData = null; // Always clear RAM first

            // Check if current authenticated user is Nikhil
            var isCurrentGoogleNikhil = (this.googleUser && (
                (this.googleUser.email && this.googleUser.email.toLowerCase().indexOf('nikhil') !== -1) ||
                (this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1)
            ));'''

new_load_profile_block = '''            var hasStored = false;
            this.activeChartData = null; // Always clear RAM first

            var email = (this.googleUser && this.googleUser.email) ? this.googleUser.email.trim().toLowerCase() : '';
            var isCurrentGoogleNikhil = (email.indexOf('nikhil') !== -1) ||
                (this.googleUser && this.googleUser.name && this.googleUser.name.toUpperCase().indexOf('NIKHIL') !== -1);'''

if old_load_profile_block in html:
    html = html.replace(old_load_profile_block, new_load_profile_block)
    print("Updated email and isCurrentGoogleNikhil calculation in loadStoredProfile.")

# -----------------------------------------------------------------------------
# 4. Add restoreSageChat, clearSageChat, and getAIChatStorageKey to VyasDesktop
# -----------------------------------------------------------------------------
chat_methods = '''
        getAIChatStorageKey: function() {
            try {
                var u = (this.googleUser && this.googleUser.email) ? this.googleUser.email.trim().toLowerCase() : 'guest';
                return 'vyas_ai_chat_' + u;
            } catch(e) { return 'vyas_ai_chat_guest'; }
        },

        restoreSageChat: function() {
            var container = document.getElementById('sageChatMessages');
            if (!container) return;
            var key = this.getAIChatStorageKey();
            var saved = [];
            try {
                var s = localStorage.getItem(key);
                if (s) saved = JSON.parse(s);
            } catch(e) {}

            var welcomeHtml = '<div class="chat-bubble sage" style="background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.25); border-radius:8px; padding:12px; margin-bottom:10px;">' +
                '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">' +
                    '<b style="color:#d4af37;">✦ आचार्य व्यास (परम दैवज्ञ):</b>' +
                    '<button onclick="VyasDesktop.clearSageChat()" class="header-btn" style="font-size:0.7rem; padding:2px 8px; border:1px solid rgba(212,175,55,0.4);" title="चैट साफ़ करें">🗑️ नई चर्चा</button>' +
                '</div>' +
                'सादर प्रणाम! आपकी जन्मपत्रिका, 16 वर्ग चक्र, अष्टकवर्ग, विंशोत्तरी दशा एवं गोचर वेध का संपूर्ण डेटा मेरे सम्मुख सक्रिय है। करियर, धन, विवाह, स्वास्थ्य अथवा किसी भी गूढ़ प्रश्न का प्रामाणिक शास्त्रीय मार्गदर्शन प्राप्त करें।' +
            '</div>';

            if (saved && saved.length > 0) {
                var historyHtml = '';
                for (var i = 0; i < saved.length; i++) {
                    var m = saved[i];
                    if (m.role === 'user') {
                        historyHtml += '<div class="chat-bubble user" style="margin-bottom:8px;">' + m.content + '</div>';
                    } else {
                        historyHtml += '<div class="chat-bubble sage" style="margin-bottom:8px;">' + m.content + '</div>';
                    }
                }
                container.innerHTML = welcomeHtml + historyHtml;
                if (window.VyasAIEngine) {
                    window.VyasAIEngine.chatHistory = saved.slice(-10);
                }
            } else {
                container.innerHTML = welcomeHtml;
            }
            container.scrollTop = container.scrollHeight;
        },

        clearSageChat: function() {
            if (!confirm("क्या आप इस चैट इतिहास को साफ़ करके नई चर्चा शुरू करना चाहते हैं?")) return;
            try {
                localStorage.removeItem(this.getAIChatStorageKey());
                if (window.VyasAIEngine) window.VyasAIEngine.chatHistory = [];
            } catch(e) {}
            this.restoreSageChat();
        },
'''

if 'restoreSageChat: function' not in html:
    pos_send = html.find('sendSageQuery: async function() {')
    assert pos_send != -1, 'sendSageQuery not found'
    html = html[:pos_send] + chat_methods + '\n        ' + html[pos_send:]
    print("Injected restoreSageChat and clearSageChat into VyasDesktop.")

# -----------------------------------------------------------------------------
# 5. Update sendSageQuery to persist conversation to user's chat history
# -----------------------------------------------------------------------------
old_sage_send = '''            try {
                var reply = await window.VyasAIEngine.askSage(q, chart);
                var thinkEl = document.getElementById(thinkId);
                if (thinkEl) {
                    thinkEl.innerHTML = reply;
                } else {
                    container.innerHTML += '<div class="chat-bubble sage">' + reply + '</div>';
                }
            } catch (err) {'''

new_sage_send = '''            try {
                var reply = await window.VyasAIEngine.askSage(q, chart);
                var thinkEl = document.getElementById(thinkId);
                if (thinkEl) {
                    thinkEl.innerHTML = reply;
                } else {
                    container.innerHTML += '<div class="chat-bubble sage" style="margin-bottom:8px;">' + reply + '</div>';
                }

                // Persist conversation to user vault in localStorage
                try {
                    var cKey = this.getAIChatStorageKey ? this.getAIChatStorageKey() : 'vyas_ai_chat_guest';
                    var cSaved = JSON.parse(localStorage.getItem(cKey) || '[]');
                    cSaved.push({ role: 'user', content: q });
                    cSaved.push({ role: 'assistant', content: reply });
                    if (cSaved.length > 30) cSaved = cSaved.slice(-30);
                    localStorage.setItem(cKey, JSON.stringify(cSaved));
                } catch(e) {}
            } catch (err) {'''

if old_sage_send in html:
    html = html.replace(old_sage_send, new_sage_send)
    print("Updated sendSageQuery to persist messages to localStorage.")

# -----------------------------------------------------------------------------
# 6. Update applyAuthenticatedGoogleUser to never purge Nikhil vault or set null
# -----------------------------------------------------------------------------
old_apply_auth = '''            if (isNikhil) {
                // Founder login: load founder vault or compute canonical chart
                var fromVault = this.loadFromUserVault();
                // Ensure founder vault does not contain stale Kanya Lagna
                if (fromVault && fromVault.profile && fromVault.profile.asc_sign === 'कन्या') {
                    fromVault = null;
                }
                if (fromVault && fromVault.profile && fromVault.profile.dob === '1984-11-23') {
                    this.activeChartData = fromVault;
                } else {
                    this.activeChartData = null;
                }
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(this.activeChartData)); } catch(e) {}
            }'''

new_apply_auth = '''            if (isNikhil) {
                // Founder login: load founder vault or compute canonical Mesha Lagna chart
                var fromVault = this.loadFromUserVault();
                if (!fromVault || !fromVault.profile || fromVault.profile.asc_sign === 'कन्या' || (fromVault.profile.asc_dms && fromVault.profile.asc_dms.indexOf("26°55") !== -1)) {
                    fromVault = this.computeMathematicalKundli('Nikhil Vyas', '1984-11-23', '16:51', 'Pali, Rajasthan', 'Male', 25.7711, 73.3234);
                    this.saveToUserVault(fromVault);
                }
                this.activeChartData = fromVault;
                try { localStorage.setItem('vyas_active_profile', JSON.stringify(fromVault)); } catch(e) {}
            }'''

if old_apply_auth in html:
    html = html.replace(old_apply_auth, new_apply_auth)
    print("Updated applyAuthenticatedGoogleUser for founder login.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully patched with stability, auto-restore, and truth engine!")

