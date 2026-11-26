<?php
// ----------------------------------------------------------------------
// VYAS ASTRA — SERVER-SIDE CLOUD KUNDLI VAULT API
// Persists each Google user's saved Kundlis on Hostinger so charts NEVER
// disappear across browsers, devices, cache clears, or logins.
// ----------------------------------------------------------------------
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$vaultDir = __DIR__ . '/../data/user_vaults';
if (!is_dir($vaultDir)) {
    mkdir($vaultDir, 0755, true);
}

$rawInput = file_get_contents('php://input');
$input = json_decode($rawInput, true) ?: [];
$email = strtolower(trim($_GET['email'] ?? $input['email'] ?? ''));

if (!$email || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(["success" => false, "error" => "Valid email required"]);
    exit();
}

$hash = md5($email);
$vaultFile = $vaultDir . '/' . $hash . '.json';
$existing = file_exists($vaultFile) ? json_decode(file_get_contents($vaultFile), true) : null;
if (!is_array($existing)) {
    $existing = ["email" => $email, "profiles" => [], "updated_at" => date("c")];
}

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo json_encode([
        "success" => true,
        "email" => $email,
        "profiles" => $existing['profiles'] ?? [],
        "updated_at" => $existing['updated_at'] ?? null
    ], JSON_UNESCAPED_UNICODE);
    exit();
}

// POST: merge or replace profiles
$action = $input['action'] ?? 'merge';
$incoming = $input['profiles'] ?? [];
if (!is_array($incoming)) {
    $incoming = [];
}

if ($action === 'delete' && isset($input['name'], $input['dob'])) {
    $delName = trim($input['name']);
    $delDob = trim($input['dob']);
    $existing['profiles'] = array_values(array_filter($existing['profiles'], function ($p) use ($delName, $delDob) {
        return !(trim($p['name'] ?? '') === $delName && trim($p['dob'] ?? '') === $delDob);
    }));
} else {
    // Merge incoming profiles with existing (deduplicate by name + dob)
    $merged = $existing['profiles'];
    foreach ($incoming as $inc) {
        if (!is_array($inc) || empty($inc['name']) || empty($inc['dob'])) continue;
        $found = false;
        foreach ($merged as &$m) {
            if (trim($m['name'] ?? '') === trim($inc['name']) && trim($m['dob'] ?? '') === trim($inc['dob'])) {
                $m = array_merge($m, $inc);
                $found = true;
                break;
            }
        }
        if (!$found) {
            array_unshift($merged, [
                "name" => $inc['name'],
                "dob" => $inc['dob'],
                "tob" => $inc['tob'] ?? '12:00',
                "city" => $inc['city'] ?? 'Pali, Rajasthan',
                "gender" => $inc['gender'] ?? 'Male',
                "asc_sign" => $inc['asc_sign'] ?? '',
                "lat" => $inc['lat'] ?? null,
                "lon" => $inc['lon'] ?? null,
                "tz" => $inc['tz'] ?? 5.5
            ]);
        }
    }
    $existing['profiles'] = array_slice($merged, 0, 100);
}

$existing['updated_at'] = date("c");
file_put_contents($vaultFile, json_encode($existing, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

echo json_encode([
    "success" => true,
    "email" => $email,
    "count" => count($existing['profiles']),
    "profiles" => $existing['profiles'],
    "updated_at" => $existing['updated_at']
], JSON_UNESCAPED_UNICODE);
