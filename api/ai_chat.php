<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — AI COPILOT HIGH SPEED PROXY (GROQ MULTI-KEY FAILOVER)
// AUTONOMOUS DAIVAGYA AGENT CORE WITH CLASSICAL SUTRAS VAULT INTEGRATION
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$keys = [
    "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",
    "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"
];
$models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b"];

$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true);
$query = isset($input['query']) ? trim($input['query']) : '';
$systemPrompt = isset($input['systemPrompt']) ? trim($input['systemPrompt']) : '';
$chatHistory = (isset($input['chatHistory']) && is_array($input['chatHistory'])) ? $input['chatHistory'] : [];

if (empty($query)) {
    echo json_encode(["error" => "Empty query"]);
    exit();
}

// ----------------------------------------------------------------------
// 1. SHLASTRIC VAULT LOOKUP (10,500 Classical Sutras Silent Injection)
// ----------------------------------------------------------------------
function lookupClassicalSutras($query, $systemPrompt) {
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
        if (preg_match('/' . $plHi . '[^:]*:\s*([^\s\d]+)\s+[^()]*\(.*?भाव\s*(\d+).*?स्थिति:\s*([^\)]+)\)/u', $systemPrompt, $m)) {
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
        "\n[अपरिहार्य दैवज्ञ शास्त्रीय संहिता प्रमाण — Shastric Context Lock]",
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
    $contextLines[] = "\n[अपरिवर्तनीय शास्त्रीय दृष्टि नियम — INVIOLABLE ASPECT INVARIANTS]:";
    $contextLines[] = "1. शनिदेव की केवल 3री, 7वीं एवं 10वीं पूर्ण दृष्टि होती है। शनिदेव की 5वीं या 9वीं दृष्टि कभी नहीं होती।";
    $contextLines[] = "2. मंगलदेव की केवल 4थी, 7वीं एवं 8वीं दृष्टि होती है।";
    $contextLines[] = "3. देवगुरु बृहस्पति, राहु एवं केतु की केवल 5वीं, 7वीं एवं 9वीं दृष्टि होती है।";
    $contextLines[] = "4. सूर्य, चन्द्र, बुध, शुक्र की केवल 7वीं दृष्टि होती है।";
    $contextLines[] = "5. केवल जातक की प्रस्तुत कुण्डली के वास्तविक ग्रहों, भावों व दृष्टियों के आधार पर ही फलकथन करें। किसी भी अन्य कुण्डली या पूर्व डेटा के ग्रह (जैसे मकर में मंगल, तुला में शनि यदि जातक की कुण्डली में न हों) को कदापि लागू न करें।";

    return implode("\n", $contextLines);
}
// Check for continuation intent
$lowerQ = strtolower($query);
$isContinuation = (
    strpos($lowerQ, 'continue') !== false ||
    strpos($lowerQ, 'aage') !== false ||
    strpos($query, 'आगे') !== false ||
    strpos($query, 'जारी') !== false ||
    strpos($query, 'पूरा') !== false ||
    strpos($query, 'और बताएं') !== false
);

// Prepare messages payload
$messages = [];

// Inject strict real-time date and respect directives to ensure 0% past hallucination
$currentDateHindi = "बुधवार, 18 नवंबर 2026";
$currentYear = "2026";
$timeAndEtiquetteDirective = "\n\n[अपरिहार्य काल एवं शिष्टाचार नियम]\nआज का वास्तविक वर्तमान काल: {$currentDateHindi} (ईस्वी सन् {$currentYear}) है। भूलकर भी जनवरी 2025 या अतीत के किसी वर्ष को वर्तमान या भविष्य न कहें। जातक से सदा अत्यंत आदर से 'आप', 'आपका', 'सादर प्रणाम' कहकर बात करें। भूलकर भी जातक को 'पुत्र', 'वत्स', 'तुम', 'तुम्हारी' न कहें।";
$systemPrompt .= $timeAndEtiquetteDirective;

// Inject silent Shastric Classical Sutras
$sutraContext = lookupClassicalSutras($query, $systemPrompt);
if (!empty($sutraContext)) {
    $systemPrompt .= "\n\n" . $sutraContext;
}

// Inject 5-Part Authoritative Daivagya Structure Directive
$daivagyaStructureDirective = "\n\n[परम दैवज्ञ फलादेश संरचना नियम — MANDATORY 5-PART ARCHITECTURE]\n" .
    "किसी भी बनावटी चैट या सतही बुलेट-पॉइंट्स से बचें। आपका फलादेश एक सिद्ध दैवज्ञ की भांति इन 5 गंभीर व गरिमामय शीर्षकों में होना चाहिए:\n" .
    "I. दैवज्ञ पीठिका एवं कुण्डली दर्शन (लग्न, कस्प एवं ग्रह बल का सूक्ष्म समन्वय)\n" .
    "II. प्रामाणिक शास्त्रीय संहिता प्रमाण (बृहत्पाराशर, फलदीपिका या नाड़ी सूत्रों का प्रत्यक्ष उद्धरण)\n" .
    "III. अचूक काल-निर्णय (सक्रिय विंशोत्तरी दशा + 2026-2027 के शनि-गुरु गोचर वेध से निश्चित समय-सीमा)\n" .
    "IV. मनोवैज्ञानिक व व्यावहारिक स्वभाव दर्शन (ग्रहों से उत्पन्न वास्तविक आदतें एवं निर्णय प्रक्रिया)\n" .
    "V. सिद्ध सात्विक त्रिविध उपाय विधान (संज्ञानात्मक बोध + 40-दिवसीय सूक्ष्म आचरण + शास्त्रीय वैदिक बीज-मंत्र जप संख्या सहित)";
$systemPrompt .= $daivagyaStructureDirective;

$messages[] = ["role" => "system", "content" => $systemPrompt];

// Sanitize and append up to last 10 messages of history
$recentHistory = array_slice($chatHistory, -10);
foreach ($recentHistory as $msg) {
    if (isset($msg['role']) && isset($msg['content'])) {
        // Strip HTML tags for clean model context
        $cleanContent = strip_tags(str_replace(['<br>', '<br/>', '<br />'], "\n", $msg['content']));
        $messages[] = [
            "role" => ($msg['role'] === 'user') ? 'user' : 'assistant',
            "content" => $cleanContent
        ];
    }
}

// Format final query with continuation instruction if needed
$finalQuery = $query;
if ($isContinuation) {
    $finalQuery .= "\n\n(महत्वपूर्ण निर्देश: आपने पिछला कथन जहां अधूरा छोड़ा था, कृपया ठीक वहीं से बिना किसी औपचारिकता या पूर्व कथन को दोहराए, पूरे विस्तार, विद्वतापूर्ण शास्त्रीय सूत्रों, सटीक गोचर/दशा समय एवं अचूक उपायों के साथ वाक्य को पूर्ण करें।)";
}

$messages[] = ["role" => "user", "content" => $finalQuery];

// Perform failover across keys and models
foreach ($keys as $key) {
    foreach ($models as $model) {
        $ch = curl_init("https://api.groq.com/openai/v1/chat/completions");
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36");
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Authorization: Bearer " . $key,
            "Content-Type: application/json"
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            "model" => $model,
            "messages" => $messages,
            "temperature" => 0.65,
            "max_tokens" => 3800
        ]));
        curl_setopt($ch, CURLOPT_TIMEOUT, 28);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode === 200 && $response) {
            $data = json_decode($response, true);
            if (isset($data['choices'][0]['message']['content'])) {
                $rawText = $data['choices'][0]['message']['content'];
                $content = preg_replace('/\*\*(.*?)\*\*/', '<b>$1</b>', $rawText);
                $content = nl2br($content);
                echo json_encode([
                    "reply" => $content,
                    "rawText" => $rawText
                ]);
                exit();
            }
        }
    }
}

http_response_code(500);
echo json_encode(["error" => "AI model failover exhausted"]);
