<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — AI COPILOT HIGH SPEED PROXY (GROQ MULTI-KEY FAILOVER)
// STORE-READY RESILIENT FULL-DIALOGUE CHAT ENGINE
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
$models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"];

$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true);
$query = isset($input['query']) ? trim($input['query']) : '';
$systemPrompt = isset($input['systemPrompt']) ? trim($input['systemPrompt']) : '';
$chatHistory = (isset($input['chatHistory']) && is_array($input['chatHistory'])) ? $input['chatHistory'] : [];

if (empty($query)) {
    echo json_encode(["error" => "Empty query"]);
    exit();
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
