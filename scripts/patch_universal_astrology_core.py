import os, sys, re, json

def patch_ai_chat():
    path = "api/ai_chat.php"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replacement for lookupClassicalSutras and directives
    old_fn_start = content.find("function lookupClassicalSutras($query, $systemPrompt) {")
    old_fn_end = content.find("// Check for continuation intent", old_fn_start)
    if old_fn_start == -1 or old_fn_end == -1:
        print("ERROR: Could not find lookupClassicalSutras in api/ai_chat.php")
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
    }

    $fastIndexPath = __DIR__ . '/../data/vyas_sutras_fast_index.json';
    $selectedSutras = [];

    // Parse native's actual chart tokens from systemPrompt for authentic matching
    $chartSigns = [];
    $chartHouses = [];
    $chartPlanets = ['सूर्य', 'चन्द्र', 'मंगल', 'बुध', 'गुरु', 'शुक्र', 'शनि', 'राहु', 'केतु'];
    $rashiList = ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या', 'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुंभ', 'मीन'];
    
    foreach ($chartPlanets as $pl) {
        if (preg_match('/' . $pl . '[^:]*:\s*([^\s\d]+)\s*[\d°\']*\s*\(.*?भाव\s*(\d+)/u', $systemPrompt, $m)) {
            $chartSigns[$pl] = trim($m[1]);
            $chartHouses[$pl] = intval($m[2]);
        }
    }

    if (file_exists($fastIndexPath)) {
        $indexData = json_decode(file_get_contents($fastIndexPath), true);
        if (isset($indexData['domains'][$domain]) && !empty($indexData['domains'][$domain])) {
            $pool = $indexData['domains'][$domain];
            
            // STRICT CONDITION-FILTER: Only select sutras whose planetary condition matches this native's chart!
            foreach ($pool as $item) {
                $cond = $item['cond_hi'] ?? '';
                $factor = $item['factor'] ?? '';
                $matched = false;

                // Check planetary condition against native's chart
                foreach ($chartPlanets as $pl) {
                    if (mb_strpos($cond, $pl, 0, 'UTF-8') !== false || mb_strpos($cond, $factor, 0, 'UTF-8') !== false) {
                        $pSign = $chartSigns[$pl] ?? '';
                        $pHouse = $chartHouses[$pl] ?? 0;

                        // If sutra specifies a sign, verify native has that planet in that sign
                        if (!empty($pSign) && mb_strpos($cond, $pSign, 0, 'UTF-8') !== false) {
                            $matched = true;
                        }
                        // If sutra specifies a house, verify native has that planet in that house
                        if ($pHouse > 0) {
                            $houseOrdinals = [1=>'प्रथम|लग्न', 2=>'द्वितीय', 3=>'तृतीय', 4=>'चतुर्थ', 5=>'पंचम', 6=>'षष्ठ', 7=>'सप्तम', 8=>'अष्टम', 9=>'नवम', 10=>'दशम', 11=>'एकादश', 12=>'द्वादश'];
                            if (isset($houseOrdinals[$pHouse]) && preg_match('/(' . $houseOrdinals[$pHouse] . ')\s*भाव/u', $cond)) {
                                $matched = true;
                            }
                        }
                    }
                }

                if ($matched) {
                    $selectedSutras[] = $item;
                    if (count($selectedSutras) >= 3) break;
                }
            }
        }
    }

    $contextLines = [
        "\\n[अपरिहार्य दैवज्ञ शास्त्रीय संहिता प्रमाण — Shastric Context Lock]",
        "⚠️ अति-महत्वपूर्ण शास्त्रीय निर्देश: केवल वही शास्त्रीय सूत्र लागू करें जो जातक की जन्म कुण्डली में प्रत्यक्ष उपस्थित हों। किसी भी अप्रासंगिक, काल्पनिक या अन्य ग्रह योग का उल्लेख सर्वथा वर्जित है।"
    ];

    if (!empty($selectedSutras)) {
        $contextLines[] = "जातक की कुण्डली पर प्रत्यक्ष घटित होने वाले प्रामाणिक शास्त्र सूत्र:";
        foreach ($selectedSutras as $s) {
            $src = htmlspecialchars_decode($s['src'] ?? 'बृहत्पाराशर होराशास्त्र / फलदीपिका');
            $cond = htmlspecialchars_decode($s['cond_hi'] ?? '');
            $pred = htmlspecialchars_decode($s['pred_hi'] ?? '');
            $contextLines[] = "• शास्त्र प्रमाण ({$src}): जब '{$cond}' की स्थिति बनती है, तो शास्त्र सम्मत फल — {$pred}";
        }
    } else {
        // Fallback to classical house lord & karaka principles without asserting false placements
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
    content = content[:old_fn_start] + new_fn + content[old_fn_end:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Patched api/ai_chat.php with chart-aware classical sutra filtering and strict aspect rules.")
    return True

if __name__ == "__main__":
    patch_ai_chat()
