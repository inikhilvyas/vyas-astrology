<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — WEB PUSH SUBSCRIPTION ENDPOINT
// Stores subscriber endpoints for daily panchang, festival & horoscope alerts
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true);

if (!$input || empty($input['endpoint'])) {
    http_response_code(400);
    echo json_encode(["success" => false, "error" => "Invalid subscription payload"]);
    exit();
}

$subscribersFile = __DIR__ . '/../data/push_subscribers.json';
$subscribers = [];

if (file_exists($subscribersFile)) {
    $existing = json_decode(file_get_contents($subscribersFile), true);
    if (is_array($existing)) {
        $subscribers = $existing;
    }
}

// Check if endpoint already registered
$endpoint = $input['endpoint'];
$found = false;
foreach ($subscribers as &$sub) {
    if (isset($sub['endpoint']) && $sub['endpoint'] === $endpoint) {
        $sub['updated_at'] = date("c");
        $sub['rashi'] = isset($input['rashi']) ? $input['rashi'] : ($sub['rashi'] ?? 'all');
        $found = true;
        break;
    }
}

if (!$found) {
    $subscribers[] = [
        "endpoint" => $endpoint,
        "keys" => $input['keys'] ?? null,
        "rashi" => $input['rashi'] ?? 'all',
        "created_at" => date("c"),
        "user_agent" => $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown'
    ];
}

// Keep directory safe and write atomic
if (!is_dir(__DIR__ . '/../data')) {
    mkdir(__DIR__ . '/../data', 0755, true);
}
file_put_contents($subscribersFile, json_encode($subscribers, JSON_PRETTY_PRINT));

echo json_encode([
    "success" => true,
    "total_subscribers" => count($subscribers),
    "message" => "दैनिक पंचांग, शुभ मुहूर्त एवं पावन पर्वों की सूचनाएं सफलतापूर्वक सक्रिय हो गई हैं।"
]);
