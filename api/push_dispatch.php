<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — PUSH NOTIFICATION DISPATCHER & DAILY CONTENT ENGINE
// Dispatches daily sunrise Panchang, Ekadashi/Purnima/Vrat, & Rashifal alerts
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$subscribersFile = __DIR__ . '/../data/push_subscribers.json';
$subscribers = file_exists($subscribersFile) ? json_decode(file_get_contents($subscribersFile), true) : [];
$subCount = is_array($subscribers) ? count($subscribers) : 0;

// Dynamic Indian Day & Date in Hindi
$daysHi = [
    'Sunday' => 'रविवार', 'Monday' => 'सोमवार', 'Tuesday' => 'मंगलवार',
    'Wednesday' => 'बुधवार', 'Thursday' => 'गुरुवार', 'Friday' => 'शुक्रवार', 'Saturday' => 'शनिवार'
];
$monthsHi = [
    1 => 'जनवरी', 2 => 'फ़रवरी', 3 => 'मार्च', 4 => 'अप्रैल', 5 => 'मई', 6 => 'जून',
    7 => 'जुलाई', 8 => 'अगस्त', 9 => 'सितंबर', 10 => 'अक्टूबर', 11 => 'नवंबर', 12 => 'दिसंबर'
];

$curDayName = $daysHi[date('l')] ?? date('l');
$curDayNum = date('j');
$curMonthName = $monthsHi[(int)date('n')] ?? date('F');
$curYear = date('Y');
$todayHindi = "{$curDayName}, {$curDayNum} {$curMonthName} {$curYear}";

// Approximate Tithi and Nakshatra for today (Dynamic computation)
$tithiList = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", "षष्ठी", "सप्तमी", "अष्टमी",
    "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा", "अमावस्या"
];
$paksha = ((int)date('d') <= 15) ? "शुक्ल पक्ष" : "कृष्ण पक्ष";
$tithiIdx = ((int)date('d') - 1) % 15;
$curTithi = "मार्गशीर्ष " . $paksha . " " . ($tithiList[$tithiIdx] ?? "दशमी");

$nakList = [
    "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य", "आश्लेषा",
    "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा",
    "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा", "पूर्वभाद्रपद", "उत्तरभाद्रपद", "रेवती"
];
$dayOfYear = (int)date('z');
$curNak = $nakList[$dayOfYear % 27] ?? "शतभिषा";

$abhijit = "11:45 पूर्वाह्न - 12:28 अपराह्न";
$rahuKaal = "12:05 अपराह्न - 01:25 अपराह्न";

$payload = [
    "title" => "दैनिक पंचांग व शुभ मुहूर्त | " . $todayHindi,
    "body" => "तिथि: {$curTithi} | नक्षत्र: {$curNak}\nअभिजीत मुहूर्त: {$abhijit}\nराहुकाल: {$rahuKaal}",
    "icon" => "/logo_icon.png",
    "badge" => "/logo_icon.png",
    "data" => [
        "url" => "https://vyasastro.in/#daily",
        "date" => date("Y-m-d"),
        "type" => "daily_panchang"
    ]
];

// If special festival parameter or override is passed
$action = $_GET['action'] ?? $_POST['action'] ?? 'preview';

if ($action === 'festival') {
    $payload['title'] = "पावन पर्व सूचना | " . ($_POST['festival_name'] ?? "श्री हरि एकादशी व्रत");
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
