with open('api/ai_chat.php', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update isLordQuery
old_lord = "$isLordQuery = preg_match('/स्वामी|मालिक|अधिपति|भावेश|लॉर्ड|lord|ruler|governs|master/u', $q);"
new_lord = "$isLordQuery = preg_match('/स्वामी|मालिक|अधिपति|भावेश|लॉर्ड|swami|malik|adhipati|lord|ruler|governs|master/ui', $q);"
if old_lord in code:
    code = code.replace(old_lord, new_lord, 1)
    print("✓ Replaced isLordQuery")

# 2. Update rashis
old_rashis = """    // 2. 12 RASHI LORDS (12 राशियां एवं उनके अधिपति)
    $rashis = [
        ['patterns' => ['मिथुन', 'gemini'], 'name' => 'मिथुन राशि (Gemini)', 'lord' => 'बुधदेव (Mercury)', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'भौमशुक्रबुधेंद्वर्कसौम्यशुक्रावनीसुताः। जीवेन्दुपूज्यावकीनां क्षेत्राणि क्रमशः स्मृताः॥', 'details' => 'त्रिकाल सत्य: **मिथुन राशि के अधिपति केवल और केवल बुधदेव (Mercury) हैं** (कदापि शुक्र नहीं)। कालपुरुष चक्र में मिथुन तृतीय भाव (पराक्रम, संवाद व मेधा) का प्रतिनिधित्व करती है।'],
        ['patterns' => ['मेष', 'aries'], 'name' => 'मेष राशि (Aries)', 'lord' => 'मंगलदेव (Mars)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'चर (Movable)', 'shloka' => 'कुजस्य क्षेत्रं प्रथमं मेषसंज्ञम्।', 'details' => 'मेष राशि के अधिपति ग्रह **मंगलदेव (Mars)** हैं। कालपुरुष के प्रथम भाव (तनु) की यह राशि साहस, ऊर्जा व नेतृत्व की प्रतीक है।'],
        ['patterns' => ['वृषभ', 'वृष', 'taurus'], 'name' => 'वृषभ राशि (Taurus)', 'lord' => 'शुक्रदेव (Venus)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'शुक्रस्य भवनं वृषः।', 'details' => 'वृषभ राशि के अधिपति ग्रह **शुक्रदेव (Venus)** हैं। यह स्थिर पृथ्वी तत्त्व की राशि धन, वाणी, कुटुंब व सौंदर्य की प्रतीक है।'],
        ['patterns' => ['कर्क', 'cancer'], 'name' => 'कर्क राशि (Cancer)', 'lord' => 'चन्द्रदेव (Moon)', 'element' => 'जल तत्त्व (Water)', 'nature' => 'चर (Movable)', 'shloka' => 'कर्कस्य चन्द्रमाः स्वामी।', 'details' => 'कर्क राशि के अधिपति ग्रह **चन्द्रदेव (Moon)** हैं। कालपुरुष के चतुर्थ भाव (मातृ व सुख) की यह राशि भावना व संवेदनशीलता का केंद्र है।'],
        ['patterns' => ['सिंह', 'leo'], 'name' => 'सिंह राशि (Leo)', 'lord' => 'सूर्यदेव (Sun)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'सिंहस्य स्वामी दिनकृत्।', 'details' => 'सिंह राशि के अधिपति ग्रह **भगवान सूर्यदेव (Sun)** हैं। कालपुरुष के पंचम भाव (बुद्धि व तेज) की यह राशि आत्मगौरव, पराक्रम व तेज की प्रतीक है।'],
        ['patterns' => ['कन्या', 'virgo'], 'name' => 'कन्या राशि (Virgo)', 'lord' => 'बुधदेव (Mercury)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'कन्याया अपि बुधः स्वामी।', 'details' => 'कन्या राशि के अधिपति ग्रह **बुधदेव (Mercury)** हैं। बुधदेव इस राशि में उच्च के भी होते हैं (15° तक)। यह राशि विश्लेषण, कौशल, सेवा व शुचिता की प्रतीक है।'],
        ['patterns' => ['तुला', 'libra'], 'name' => 'तुला राशि (Libra)', 'lord' => 'शुक्रदेव (Venus)', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'चर (Movable)', 'shloka' => 'तुलाया भार्गवः स्वामी।', 'details' => 'तुला राशि के अधिपति ग्रह **शुक्रदेव (Venus)** हैं। कालपुरुष के सप्तम भाव (साझेदारी, व्यापार व सामंजस्य) की यह राशि न्याय व संतुलन की प्रतीक है।'],
        ['patterns' => ['वृश्चिक', 'scorpio'], 'name' => 'वृश्चिक राशि (Scorpio)', 'lord' => 'मंगलदेव (Mars) [सह-स्वामी: केतु]', 'element' => 'जल तत्त्व (Water)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'वृश्चिकस्य कुजः स्वामी।', 'details' => 'वृश्चिक राशि के प्रधान अधिपति ग्रह **मंगलदेव (Mars)** हैं (केतु सह-स्वामी माने जाते हैं)। कालपुरुष के अष्टम भाव की यह राशि गूढ़ ज्ञान, शोध व रूपांतरण की प्रतीक है।'],
        ['patterns' => ['धनु', 'sagittarius'], 'name' => 'धनु राशि (Sagittarius)', 'lord' => 'देवगुरु बृहस्पति (Jupiter)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'धनुषो गुरुनायकः।', 'details' => 'धनु राशि के अधिपति ग्रह **देवगुरु बृहस्पति (Jupiter)** हैं। कालपुरुष के नवम भाव (धर्म, भाग्य व दर्शन) की यह राशि सात्विक विवेक की प्रतीक है।'],
        ['patterns' => ['मकर', 'capricorn'], 'name' => 'मकर राशि (Capricorn)', 'lord' => 'शनिदेव (Saturn)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'चर (Movable)', 'shloka' => 'मकरस्य प्रभुर्मन्दः।', 'details' => 'मकर राशि के अधिपति ग्रह **शनिदेव (Saturn)** हैं। कालपुरुष के दशम भाव (कर्म, पद व आजीविका) की यह राशि अनुशासन, श्रम व दायित्व की प्रतीक है।'],
        ['patterns' => ['कुंभ', 'कुम्भ', 'aquarius'], 'name' => 'कुम्भ राशि (Aquarius)', 'lord' => 'शनिदेव (Saturn) [सह-स्वामी: राहु]', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'कुम्भस्य मन्दनायकः।', 'details' => 'कुम्भ राशि के प्रधान अधिपति ग्रह **शनिदेव (Saturn)** हैं (राहु सह-स्वामी हैं)। कालपुरुष के एकादश भाव (लाभ, विस्तार व लोकहित) की यह राशि उच्च दार्शनिक चेतना की प्रतीक है।'],
        ['patterns' => ['मीन', 'pisces'], 'name' => 'मीन राशि (Pisces)', 'lord' => 'देवगुरु बृहस्पति (Jupiter)', 'element' => 'जल तत्त्व (Water)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'मीनस्य च गुरुः स्वामी।', 'details' => 'मीन राशि के अधिपति ग्रह **देवगुरु बृहस्पति (Jupiter)** हैं। कालपुरुष के द्वादश भाव (मोक्ष, अंतर्ज्ञान व त्याग) की यह राशि आध्यात्मिक पूर्णता की प्रतीक है।']
    ];"""

new_rashis = """    // 2. 12 RASHI LORDS (12 राशियां एवं उनके अधिपति)
    $rashis = [
        ['patterns' => ['मिथुन', 'gemini', 'mithun', 'mithuna'], 'name' => 'मिथुन राशि (Gemini)', 'lord' => 'बुधदेव (Mercury)', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'भौमशुक्रबुधेंद्वर्कसौम्यशुक्रावनीसुताः। जीवेन्दुपूज्यावकीनां क्षेत्राणि क्रमशः स्मृताः॥', 'details' => 'त्रिकाल सत्य: **मिथुन राशि के अधिपति केवल और केवल बुधदेव (Mercury) हैं** (कदापि शुक्र नहीं)। कालपुरुष चक्र में मिथुन तृतीय भाव (पराक्रम, संवाद व मेधा) का प्रतिनिधित्व करती है।'],
        ['patterns' => ['मेष', 'aries', 'mesh', 'mesha'], 'name' => 'मेष राशि (Aries)', 'lord' => 'मंगलदेव (Mars)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'चर (Movable)', 'shloka' => 'कुजस्य क्षेत्रं प्रथमं मेषसंज्ञम्।', 'details' => 'मेष राशि के अधिपति ग्रह **मंगलदेव (Mars)** हैं। कालपुरुष के प्रथम भाव (तनु) की यह राशि साहस, ऊर्जा व नेतृत्व की प्रतीक है।'],
        ['patterns' => ['वृषभ', 'वृष', 'taurus', 'vrishabh', 'vrishabha', 'vrish'], 'name' => 'वृषभ राशि (Taurus)', 'lord' => 'शुक्रदेव (Venus)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'शुक्रस्य भवनं वृषः।', 'details' => 'वृषभ राशि के अधिपति ग्रह **शुक्रदेव (Venus)** हैं। यह स्थिर पृथ्वी तत्त्व की राशि धन, वाणी, कुटुंब व सौंदर्य की प्रतीक है।'],
        ['patterns' => ['कर्क', 'cancer', 'kark', 'karka'], 'name' => 'कर्क राशि (Cancer)', 'lord' => 'चन्द्रदेव (Moon)', 'element' => 'जल तत्त्व (Water)', 'nature' => 'चर (Movable)', 'shloka' => 'कर्कस्य चन्द्रमाः स्वामी।', 'details' => 'कर्क राशि के अधिपति ग्रह **चन्द्रदेव (Moon)** हैं। कालपुरुष के चतुर्थ भाव (मातृ व सुख) की यह राशि भावना व संवेदनशीलता का केंद्र है।'],
        ['patterns' => ['सिंह', 'leo', 'singh', 'simha'], 'name' => 'सिंह राशि (Leo)', 'lord' => 'सूर्यदेव (Sun)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'सिंहस्य स्वामी दिनकृत्।', 'details' => 'सिंह राशि के अधिपति ग्रह **भगवान सूर्यदेव (Sun)** हैं। कालपुरुष के पंचम भाव (बुद्धि व तेज) की यह राशि आत्मगौरव, पराक्रम व तेज की प्रतीक है।'],
        ['patterns' => ['कन्या', 'virgo', 'kanya'], 'name' => 'कन्या राशि (Virgo)', 'lord' => 'बुधदेव (Mercury)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'कन्याया अपि बुधः स्वामी।', 'details' => 'कन्या राशि के अधिपति ग्रह **बुधदेव (Mercury)** हैं। बुधदेव इस राशि में उच्च के भी होते हैं (15° तक)। यह राशि विश्लेषण, कौशल, सेवा व शुचिता की प्रतीक है।'],
        ['patterns' => ['तुला', 'libra', 'tula'], 'name' => 'तुला राशि (Libra)', 'lord' => 'शुक्रदेव (Venus)', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'चर (Movable)', 'shloka' => 'तुलाया भार्गवः स्वामी।', 'details' => 'तुला राशि के अधिपति ग्रह **शुक्रदेव (Venus)** हैं। कालपुरुष के सप्तम भाव (साझेदारी, व्यापार व सामंजस्य) की यह राशि न्याय व संतुलन की प्रतीक है।'],
        ['patterns' => ['वृश्चिक', 'scorpio', 'vrishchik', 'vrischika'], 'name' => 'वृश्चिक राशि (Scorpio)', 'lord' => 'मंगलदेव (Mars) [सह-स्वामी: केतु]', 'element' => 'जल तत्त्व (Water)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'वृश्चिकस्य कुजः स्वामी।', 'details' => 'वृश्चिक राशि के प्रधान अधिपति ग्रह **मंगलदेव (Mars)** हैं (केतु सह-स्वामी माने जाते हैं)। कालपुरुष के अष्टम भाव की यह राशि गूढ़ ज्ञान, शोध व रूपांतरण की प्रतीक है।'],
        ['patterns' => ['धनु', 'sagittarius', 'dhanu'], 'name' => 'धनु राशि (Sagittarius)', 'lord' => 'देवगुरु बृहस्पति (Jupiter)', 'element' => 'अग्नि तत्त्व (Fire)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'धनुषो गुरुनायकः।', 'details' => 'धनु राशि के अधिपति ग्रह **देवगुरु बृहस्पति (Jupiter)** हैं। कालपुरुष के नवम भाव (धर्म, भाग्य व दर्शन) की यह राशि सात्विक विवेक की प्रतीक है।'],
        ['patterns' => ['मकर', 'capricorn', 'makar', 'makara'], 'name' => 'मकर राशि (Capricorn)', 'lord' => 'शनिदेव (Saturn)', 'element' => 'पृथ्वी तत्त्व (Earth)', 'nature' => 'चर (Movable)', 'shloka' => 'मकरस्य प्रभुर्मन्दः।', 'details' => 'मकर राशि के अधिपति ग्रह **शनिदेव (Saturn)** हैं। कालपुरुष के दशम भाव (कर्म, पद व आजीविका) की यह राशि अनुशासन, श्रम व दायित्व की प्रतीक है।'],
        ['patterns' => ['कुंभ', 'कुम्भ', 'aquarius', 'kumbh', 'kumbha'], 'name' => 'कुम्भ राशि (Aquarius)', 'lord' => 'शनिदेव (Saturn) [सह-स्वामी: राहु]', 'element' => 'वायु तत्त्व (Air)', 'nature' => 'स्थिर (Fixed)', 'shloka' => 'कुम्भस्य मन्दनायकः।', 'details' => 'कुम्भ राशि के प्रधान अधिपति ग्रह **शनिदेव (Saturn)** हैं (राहु सह-स्वामी हैं)। कालपुरुष के एकादश भाव (लाभ, विस्तार व लोकहित) की यह राशि उच्च दार्शनिक चेतना की प्रतीक है।'],
        ['patterns' => ['मीन', 'pisces', 'meen', 'meena'], 'name' => 'मीन राशि (Pisces)', 'lord' => 'देवगुरु बृहस्पति (Jupiter)', 'element' => 'जल तत्त्व (Water)', 'nature' => 'द्विस्वभाव (Dual)', 'shloka' => 'मीनस्य च गुरुः स्वामी।', 'details' => 'मीन राशि के अधिपति ग्रह **देवगुरु बृहस्पति (Jupiter)** हैं। कालपुरुष के द्वादश भाव (मोक्ष, अंतर्ज्ञान व त्याग) की यह राशि आध्यात्मिक पूर्णता की प्रतीक है।']
    ];"""

if old_rashis in code:
    code = code.replace(old_rashis, new_rashis, 1)
    print("✓ Replaced rashis")

# 3. Update Drishtis
old_drishti = "if (preg_match('/दृष्टि|aspect/u', $q) && preg_match('/शनि|मंगल|गुरु|सूर्य|चन्द्र|बुध|शुक्र|राहु|केतु/u', $q)) {"
new_drishti = "if (preg_match('/दृष्टि|aspect|drishti|dristi/ui', $q) && preg_match('/शनि|मंगल|गुरु|सूर्य|चन्द्र|बुध|शुक्र|राहु|केतु|shani|saturn|mangal|mars|guru|jupiter|brihaspati|surya|sun|chandra|moon|budh|mercury|shukra|venus|rahu|ketu/ui', $q)) {"
if old_drishti in code:
    code = code.replace(old_drishti, new_drishti, 1)
    print("✓ Replaced drishti")

old_shani = "if (mb_strpos($q, 'शनि', 0, 'UTF-8') !== false) {"
new_shani = "if (mb_strpos($q, 'शनि', 0, 'UTF-8') !== false || strpos($q, 'shani') !== false || strpos($q, 'saturn') !== false) {"
if old_shani in code:
    code = code.replace(old_shani, new_shani, 1)
    print("✓ Replaced shani")

old_mangal = "if (mb_strpos($q, 'मंगल', 0, 'UTF-8') !== false) {"
new_mangal = "if (mb_strpos($q, 'मंगल', 0, 'UTF-8') !== false || strpos($q, 'mangal') !== false || strpos($q, 'mars') !== false) {"
if old_mangal in code:
    code = code.replace(old_mangal, new_mangal, 1)
    print("✓ Replaced mangal")

old_guru = "if (mb_strpos($q, 'गुरु', 0, 'UTF-8') !== false || mb_strpos($q, 'बृहस्पति', 0, 'UTF-8') !== false) {"
new_guru = "if (mb_strpos($q, 'गुरु', 0, 'UTF-8') !== false || mb_strpos($q, 'बृहस्पति', 0, 'UTF-8') !== false || strpos($q, 'guru') !== false || strpos($q, 'jupiter') !== false || strpos($q, 'brihaspati') !== false) {"
if old_guru in code:
    code = code.replace(old_guru, new_guru, 1)
    print("✓ Replaced guru")

old_rahu = "if (mb_strpos($q, 'राहु', 0, 'UTF-8') !== false || mb_strpos($q, 'केतु', 0, 'UTF-8') !== false) {"
new_rahu = "if (mb_strpos($q, 'राहु', 0, 'UTF-8') !== false || mb_strpos($q, 'केतु', 0, 'UTF-8') !== false || strpos($q, 'rahu') !== false || strpos($q, 'ketu') !== false) {"
if old_rahu in code:
    code = code.replace(old_rahu, new_rahu, 1)
    print("✓ Replaced rahu")

# 4. Update Ekadashi and Panchang
old_eka = "if (preg_match('/एकादशी|ekadashi|द्वादशी|पारण|प्रबोधिनी|देवउठनी|देवप्रबोधिनी|तुलसी विवाह|tulsi vivah/u', $q)) {"
new_eka = "if (preg_match('/एकादशी|ekadashi|द्वादशी|पारण|parana|प्रबोधिनी|देवउठनी|देवप्रबोधिनी|तुलसी विवाह|tulsi vivah/ui', $q)) {"
if old_eka in code:
    code = code.replace(old_eka, new_eka, 1)
    print("✓ Replaced eka")

old_panch = "if (preg_match('/आज का पंचांग|कल का पंचांग|पंचांग|tithi|तिथि क्या है/u', $q)) {"
new_panch = "if (preg_match('/आज का पंचांग|कल का पंचांग|पंचांग|panchang|panchangam|tithi|तिथि|muhurat|मुहूर्त/ui', $q)) {"
if old_panch in code:
    code = code.replace(old_panch, new_panch, 1)
    print("✓ Replaced panch")

with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: api/ai_chat.php patched completely!")

