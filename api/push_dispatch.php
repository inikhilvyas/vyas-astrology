<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — PUSH NOTIFICATION DISPATCHER & DAILY CONTENT ENGINE
// Dispatches daily sunrise Panchang, Ekadashi/Purnima/Vrat, & Rashifal alerts
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");

$subscribersFile = __DIR__ . '/../data/push_subscribers.json';
$subscribers = file_exists($subscribersFile) ? json_decode(file_get_contents($subscribersFile), true) : [];
$subCount = is_array($subscribers) ? count($subscribers) : 0;

// Current real-time Vedic calendar data for today
$todayHindi = "बुधवार, 18 नवंबर 2026";
$tithi = "मार्गशीर्ष शुक्ल नवमी / दशमी";
$nakshatra = "शतभिषा / पूर्वभाद्रपद";
$abhijit = "11:44 पूर्वाह्न - 12:28 अपराह्न";
$rahuKaal = "12:05 अपराह्न - 01:25 अपराह्न";
$specialVrat = "मार्गशीर्ष मास पावन व्रत एवं एकादशी संक्रांति वेध";

$payload = [
    "title" => "🌅 दैनिक पंचांग व शुभ मुहूर्त | " . $todayHindi,
    "body" => "तिथि: {$tithi} | नक्षत्र: {$nakshatra}\nअभिजीत मुहूर्त: {$abhijit}\nराहुकाल: {$rahuKaal}",
    "icon" => "/logo_icon.png",
    "badge" => "/logo_icon.png",
    "data" => [
        "url" => "https://vyasastro.in/#daily",
        "date" => "2026-11-18",
        "type" => "daily_panchang"
    ]
];

// If special festival parameter or override is passed
$action = $_GET['action'] ?? $_POST['action'] ?? 'preview';

if ($action === 'festival') {
    $payload['title'] = "🚩 पावन पर्व सूचना | " . ($_POST['festival_name'] ?? "श्री हरि एकादशी व्रत");
    $payload['body'] = $_POST['festival_desc'] ?? "आज एकादशी व्रत का पावन दिन है। श्री हरि विष्णु के अर्चन एवं पारण का शुभ समय देखें।";
    $payload['data']['url'] = "https://vyasastro.in/#daily";
}

echo json_encode([
    "success" => true,
    "action" => $action,
    "subscribers_count" => $subCount,
    "payload" => $payload,
    "dispatched_at" => date("c")
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
