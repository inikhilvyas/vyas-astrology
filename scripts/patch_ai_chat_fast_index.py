import os, sys

def update_ai_chat_with_indexed_lookup():
    path = "api/ai_chat.php"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    fn_start = content.find("function lookupClassicalSutras($query, $systemPrompt) {")
    fn_end = content.find("// Check for continuation intent", fn_start)
    if fn_start == -1 or fn_end == -1:
        print("ERROR: lookupClassicalSutras not found")
        return False

    new_fn = """function lookupClassicalSutras($query, $systemPrompt) {
    $text = mb_strtolower($query . ' ' . $systemPrompt, 'UTF-8');
    $domain = 'general';
    
    if (preg_match('/करियर|नौकरी|व्यापार|व्यवसाय|काम|प्रोजेक्ट|आजीविका|कैरियर|दशम|job|career|business/u', $text)) {
        $domain = 'career';
    } elseif (preg_match('/धन|रुपया|पैसा|लाभ|आय|सम्पत्ति|कर्ज|ऋण|आर्थिक|wealth|money|finance/u', $text)) {
        $domain = 'wealth';
    } elseif (preg_match('/विवाह|शादी|सप्तम|जीवनसाथी|पत्नी|पति|प्रेम|संबंध|marriage|spouse/u', $text)) {
        $domain = 'marriage';
    } elseif (preg_match('/स्वास्थ्य|रोग|कष्ट|बीमारी|आयु|मानसिक|दवा|health|disease/u', $text)) {
        $domain = 'health';
    } elseif (preg_match('/संतान|पुत्र|संतानहीन|बुद्धि|पढ़ाई|विद्या|ज्ञान|children|education/u', $text)) {
        $domain = 'mind';
    } elseif (preg_match('/धर्म|अध्यात्म|उपासना|गुरु|मंत्र|साधना|spiritual/u', $text)) {
        $domain = 'spirituality';
    }

    $fastIndexPath = __DIR__ . '/../data/vyas_sutras_fast_index.json';
    $selectedSutras = [];

    // Parse native's actual chart tokens from systemPrompt for authentic matching
    $chartSigns = [];
    $chartHouses = [];
    $chartDignities = [];
    $chartPlanets = [
        'सूर्य' => 'Sun', 'चन्द्र' => 'Moon', 'मंगल' => 'Mars',
        'बुध' => 'Mercury', 'गुरु' => 'Jupiter', 'शुक्र' => 'Venus',
        'शनि' => 'Saturn', 'राहु' => 'Rahu', 'केतु' => 'Ketu'
    ];
    $signEngMap = [
        'मेष' => 'Aries', 'वृषभ' => 'Taurus', 'मिथुन' => 'Gemini', 'कर्क' => 'Cancer',
        'सिंह' => 'Leo', 'कन्या' => 'Virgo', 'तुला' => 'Libra', 'वृश्चिक' => 'Scorpio',
        'धनु' => 'Sagittarius', 'मकर' => 'Capricorn', 'कुंभ' => 'Aquarius', 'मीन' => 'Pisces'
    ];

    foreach ($chartPlanets as $plHi => $plEn) {
        if (preg_match('/' . $plHi . '[^:]*:\s*([^\s\d]+)\s*[\d°\']*\s*\(.*?भाव\s*(\d+).*?स्थिति:\s*([^\)]+)\)/u', $systemPrompt, $m)) {
            $rashiHi = trim($m[1]);
            $chartSigns[$plEn] = $signEngMap[$rashiHi] ?? $rashiHi;
            $chartHouses[$plEn] = intval($m[2]);
            $stateHi = trim($m[3]);
            if (mb_strpos($stateHi, 'उच्च', 0, 'UTF-8') !== false) {
                $chartDignities[$plEn] = 'Exalted';
            } elseif (mb_strpos($stateHi, 'नीच', 0, 'UTF-8') !== false) {
                $chartDignities[$plEn] = 'Debilitated';
            } elseif (mb_strpos($stateHi, 'स्वक्षेत्र', 0, 'UTF-8') !== false || mb_strpos($stateHi, 'मूलत्रिकोण', 0, 'UTF-8') !== false) {
                $chartDignities[$plEn] = 'Own';
            }
        }
    }

    if (file_exists($fastIndexPath)) {
        $indexData = json_decode(file_get_contents($fastIndexPath), true);
        if ($indexData) {
            $candidateKeys = [];

            // 1. Keys based on relevant planets for the domain
            $priorityPlanets = ['Saturn', 'Jupiter'];
            if ($domain === 'career') {
                $priorityPlanets = ['Mars', 'Saturn', 'Sun'];
            } elseif ($domain === 'wealth') {
                $priorityPlanets = ['Jupiter', 'Mercury', 'Venus'];
            } elseif ($domain === 'marriage') {
                $priorityPlanets = ['Venus', 'Jupiter', 'Saturn'];
            } elseif ($domain === 'health') {
                $priorityPlanets = ['Sun', 'Moon', 'Saturn'];
            }

            // Collect exact keys that match THIS native's chart
            foreach ($priorityPlanets as $pl) {
                if (isset($chartSigns[$pl])) {
                    $candidateKeys[] = ['planet_signs', "{$pl}_{$chartSigns[$pl]}"];
                }
                if (isset($chartHouses[$pl])) {
                    $candidateKeys[] = ['planet_houses', "{$pl}_{$chartHouses[$pl]}"];
                }
                if (isset($chartDignities[$pl])) {
                    $candidateKeys[] = ['dignities', "{$pl}_{$chartDignities[$pl]}"];
                }
            }

            // Check Yutis (conjunctions) present in native's chart
            $houseToPlanets = [];
            foreach ($chartHouses as $pl => $h) {
                $houseToPlanets[$h][] = $pl;
            }
            foreach ($houseToPlanets as $h => $pList) {
                if (count($pList) >= 2) {
                    sort($pList);
                    for ($i = 0; $i < count($pList); $i++) {
                        for ($j = $i + 1; $j < count($pList); $j++) {
                            $candidateKeys[] = ['yutis', "{$pList[$i]}_{$pList[$j]}"];
                        }
                    }
                }
            }

            // Retrieve only matching sutras from index
            foreach ($candidateKeys as $ck) {
                $cat = $ck[0];
                $k = $ck[1];
                if (isset($indexData[$cat][$k]) && !empty($indexData[$cat][$k])) {
                    foreach ($indexData[$cat][$k] as $sutra) {
                        $selectedSutras[$sutra['id']] = $sutra;
                        if (count($selectedSutras) >= 4) break 2;
                    }
                }
            }

            // If empty, look up general placement keys
            if (empty($selectedSutras)) {
                foreach ($chartPlanets as $plEn) {
                    if (isset($chartSigns[$plEn])) {
                        $k = "{$plEn}_{$chartSigns[$plEn]}";
                        if (isset($indexData['planet_signs'][$k]) && !empty($indexData['planet_signs'][$k])) {
                            $selectedSutras[$indexData['planet_signs'][$k][0]['id']] = $indexData['planet_signs'][$k][0];
                            if (count($selectedSutras) >= 3) break;
                        }
                    }
                }
            }
        }
    }

    $contextLines = [
        "\\n[अपरिहार्य दैवज्ञ शास्त्रीय संहिता प्रमाण — Shastric Context Lock]",
        "⚠️ अति-महत्वपूर्ण शास्त्रीय निर्देश: केवल वही शास्त्रीय सूत्र लागू करें जो जातक की जन्म कुण्डली में प्रत्यक्ष उपस्थित हों। किसी भी अप्रासंगिक, काल्पनिक या अन्य ग्रह योग का उल्लेख सर्वथा वर्जित है।"
    ];

    if (!empty($selectedSutras)) {
        $contextLines[] = "जातक की कुण्डली पर प्रत्यक्ष घटित होने वाले प्रामाणिक शास्त्र सूत्र (Authentic Matched Sutras):";
        foreach ($selectedSutras as $s) {
            $src = htmlspecialchars_decode($s['src'] ?? 'बृहत्पाराशर होराशास्त्र / फलदीपिका');
            $cond = htmlspecialchars_decode($s['cond_hi'] ?? '');
            $pred = htmlspecialchars_decode($s['pred_hi'] ?? '');
            $contextLines[] = "• शास्त्र प्रमाण ({$src}): जब '{$cond}' की स्थिति बनती है, तो शास्त्र सम्मत फल — {$pred}";
        }
    } else {
        $contextLines[] = "• शास्त्र प्रमाण (बृहत्पाराशर होराशास्त्र): फलित निर्णय सदा संबंधित भाव, भावेश, कारक ग्रह की स्थिति, उनकी वास्तविक दृष्टि एवं वर्तमान विंशोत्तरी दशा के अनुसार ही करें।";
    }

    // Append Inviolable Drishti (Aspect) Invariants
    $contextLines[] = "\\n[अपरिवर्तनीय शास्त्रीय दृष्टि नियम — INVIOLABLE ASPECT INVARIANTS]:";
    $contextLines[] = "1. शनिदेव की केवल 3री, 7वीं एवं 10वीं पूर्ण दृष्टि होती है। शनिदेव की 5वीं या 9वीं दृष्टि कभी नहीं होती (मिथुन पर शनि की दृष्टि का दावा सर्वथा असत्य व वर्जित है)।";
    $contextLines[] = "2. मंगलदेव की केवल 4थी, 7वीं एवं 8वीं दृष्टि होती है।";
    $contextLines[] = "3. देवगुरु बृहस्पति, राहु एवं केतु की केवल 5वीं, 7वीं एवं 9वीं दृष्टि होती है।";
    $contextLines[] = "4. सूर्य, चन्द्र, बुध, शुक्र की केवल 7वीं दृष्टि होती है।";
    $contextLines[] = "5. फलादेश में केवल वही दृष्टियां उद्धृत करें जो ऊपर दिए गए 'दृष्टि चक्र' में साक्षात प्रमाणित हैं।";

    return implode("\\n", $contextLines);
}
"""

    content = content[:fn_start] + new_fn + content[fn_end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Updated api/ai_chat.php with direct multi-dimensional indexed lookup.")
    return True

if __name__ == '__main__':
    update_ai_chat_with_indexed_lookup()

