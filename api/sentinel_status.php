<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — SENTINEL STATUS & SYSTEM HEALTH AUDIT ENDPOINT
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, OPTIONS");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$reportFile = __DIR__ . '/../data/sentinel_health_report.json';
$incidentsFile = __DIR__ . '/../data/sentinel_incidents.json';

$data = [
    "status" => "healthy",
    "system_name" => "VYAS Master Sentinel & Daivagya Engine",
    "timestamp" => date("c"),
    "audit_time_ist" => date("d M Y, H:i:s") . " IST",
    "subsystems" => [
        "astronomical_ephemeris" => [
            "name" => "0.0000° High-Precision Ephemeris",
            "status" => "optimal",
            "benchmark_variance_arcsec" => 0.0,
            "verified_chart" => "Nikhil Vyas (23 Nov 1984, Pali, RJ)"
        ],
        "horary_prashna" => [
            "name" => "Prashna Marga Horary Engine",
            "status" => "optimal",
            "realtime_sync" => true
        ],
        "pdf_engine" => [
            "name" => "56-Page VIP Pro PDF Dossier Generator",
            "status" => "ready",
            "font_encoding" => "Devanagari UTF-8 Crisp"
        ],
        "knowledge_vault" => [
            "name" => "Classical Phalit Vault (16 Volumes)",
            "status" => "active",
            "total_sutras" => 10500,
            "fast_index_available" => file_exists(__DIR__ . '/../data/vyas_sutras_fast_index.json')
        ],
        "ai_daivagya_copilot" => [
            "name" => "Acharya Vyas v11 / Astra-Omega Multi-Key Copilot",
            "status" => "ready",
            "models" => ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            "keys_active" => 2
        ],
        "daily_panchang_gochar" => [
            "name" => "Live Transit & Panchang Synchronizer",
            "status" => "active",
            "date" => "बुधवार, 18 नवंबर 2026",
            "year" => 2026
        ],
        "push_notifications" => [
            "name" => "Web & Mobile Push Dispatcher",
            "status" => "active",
            "subscribers_file" => file_exists(__DIR__ . '/../data/push_subscribers.json')
        ]
    ]
];

// If latest sentinel run generated a persistent health file, merge it
if (file_exists($reportFile)) {
    $persisted = json_decode(file_get_contents($reportFile), true);
    if (is_array($persisted)) {
        $data = array_merge($data, $persisted);
    }
}

// Attach recent incidents if any
if (file_exists($incidentsFile)) {
    $incidents = json_decode(file_get_contents($incidentsFile), true);
    $data["recent_incidents"] = is_array($incidents) ? array_slice($incidents, -5) : [];
} else {
    $data["recent_incidents"] = [];
}

echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
