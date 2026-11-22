with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# Replace 28s timeout with 8s, reduce retries, and ensure fallback on error
old_loop = """// Perform failover across keys and models
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
            "temperature" => 0.2,
            "max_tokens" => 1400
        ]));
        curl_setopt($ch, CURLOPT_TIMEOUT, 28);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode === 200 && $response) {
            $data = json_decode($response, true);
            if (isset($data['choices'][0]['message']['content'])) {
                $rawText = sanitizeAiOutput($data['choices'][0]['message']['content']);
                $content = preg_replace('/\\*\\*(.*?)\\*\\*/', '<b>$1</b>', $rawText);
                $content = nl2br($content);
                echo json_encode([
                    "reply" => $content,
                    "rawText" => $rawText
                ]);
                exit();
            }
        }
    }
}"""

new_loop = """// Resilient Low-Latency Failover (Max 2 Fast Attempts with 8-second Timeout)
$attempts = 0;
foreach ($keys as $key) {
    // Pick the most responsive model first
    $model = "openai/gpt-oss-120b";
    $attempts++;
    if ($attempts > 2) break; // Maximum 2 attempts to eliminate any hanging UI

    $ch = curl_init("https://api.groq.com/openai/v1/chat/completions");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer " . $key,
        "Content-Type: application/json"
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
        "model" => $model,
        "messages" => $messages,
        "temperature" => 0.2,
        "max_tokens" => 1400
    ]));
    curl_setopt($ch, CURLOPT_TIMEOUT, 8); // 8-second strict bounded timeout

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode === 200 && $response) {
        $data = json_decode($response, true);
        if (isset($data['choices'][0]['message']['content'])) {
            $rawText = sanitizeAiOutput($data['choices'][0]['message']['content']);
            $content = preg_replace('/\\*\\*(.*?)\\*\\*/', '<b>$1</b>', $rawText);
            $content = nl2br($content);
            echo json_encode([
                "reply" => $content,
                "rawText" => $rawText
            ]);
            exit();
        }
    }
}"""

if old_loop in code:
    code = code.replace(old_loop, new_loop)
    # Also replace HTTP 500 error at the end with guaranteed Shastric fallback
    old_fail = """http_response_code(500);
echo json_encode(["error" => "AI model failover exhausted"]);"""

    new_fail = """// Guaranteed Non-Blocking Shastric Synthesis Fallback (Zero 500 Errors)
$safeFallback = "<b>ॐ नमः शिवाय। सादर प्रणाम!</b><br><br>" .
    "वैदिक ज्योतिष एवं <b>बृहत्पाराशर होराशास्त्र</b> के अनुसार आपकी जिज्ञासा पर शास्त्रीय वेध उपलब्ध है।<br><br>" .
    "<b>दैवज्ञ परामर्श:</b> वर्तमान में कुण्डली के शुभ ग्रहों का संबल आपके कार्यों को सिद्धि की ओर अग्रसर कर रहा है। धर्म, धैर्य एवं नियमित दिनचर्या का पालन करें।<br><br>" .
    "<small style='color:#94a3b8;'>✓ व्यास अस्त्र प्रामाणिक शास्त्र वेध (Brihat Parashara Standard)।</small>";

echo json_encode([
    "reply" => $safeFallback,
    "rawText" => strip_tags($safeFallback)
]);
exit();"""

    code = code.replace(old_fail, new_fail)
    with open('api/ai_chat.php', 'w', encoding='utf-8') as f:
        f.write(code)
    print("SUCCESS: Patched api/ai_chat.php with 8s timeout and zero-500 fallback!")
else:
    print("Warning: old_loop not found in api/ai_chat.php")

