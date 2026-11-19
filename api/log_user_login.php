<?php
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$dataFile = __DIR__ . '/../data/user_logins.json';
if (!is_dir(__DIR__ . '/../data')) {
    mkdir(__DIR__ . '/../data', 0755, true);
}

// 1. GET Request: Return summary of logged in users for Admin Dashboard
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $users = [];
    if (file_exists($dataFile)) {
        $raw = file_get_contents($dataFile);
        $users = json_decode($raw, true) ?: [];
    }
    
    // Sort by last_login descending
    usort($users, function($a, $b) {
        return strtotime($b['last_login'] ?? '2000-01-01') - strtotime($a['last_login'] ?? '2000-01-01');
    });

    echo json_encode([
        'ok' => true,
        'total_unique_users' => count($users),
        'users' => $users,
        'privacy_guarantee' => 'No horoscope or birth chart data is stored on this server.'
    ], JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
    exit;
}

// 2. POST Request: Record user login event (Zero Kundli Data transmitted or stored)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input || empty($input['email'])) {
        echo json_encode(['ok' => false, 'error' => 'Email required']);
        exit;
    }

    $email = strtolower(trim($input['email']));
    $name = trim($input['name'] ?? 'जातक');
    $picture = trim($input['picture'] ?? '');
    $now = date('c');

    $users = [];
    if (file_exists($dataFile)) {
        $raw = file_get_contents($dataFile);
        $users = json_decode($raw, true) ?: [];
    }

    $foundIndex = -1;
    for ($i = 0; $i < count($users); $i++) {
        if (strtolower($users[$i]['email']) === $email) {
            $foundIndex = $i;
            break;
        }
    }

    if ($foundIndex !== -1) {
        $users[$foundIndex]['name'] = $name;
        if (!empty($picture)) $users[$foundIndex]['picture'] = $picture;
        $users[$foundIndex]['last_login'] = $now;
        $users[$foundIndex]['login_count'] = ($users[$foundIndex]['login_count'] ?? 1) + 1;
    } else {
        $users[] = [
            'id' => 'usr_' . substr(md5($email), 0, 8),
            'name' => $name,
            'email' => $email,
            'picture' => $picture,
            'first_login' => $now,
            'last_login' => $now,
            'login_count' => 1
        ];
    }

    file_put_contents($dataFile, json_encode($users, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));

    echo json_encode([
        'ok' => true,
        'total_unique_users' => count($users),
        'message' => 'Login recorded securely. Zero personal astrological data saved on server.'
    ]);
    exit;
}

