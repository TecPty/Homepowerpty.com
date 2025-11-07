<?php
session_start();
header('Content-Type: application/json; charset=UTF-8');
header('Access-Control-Allow-Methods: POST');

// CORS: producción y local
$allowed = ['https://www.homepowerpty.com','http://localhost','http://127.0.0.1','http://127.0.0.1:5500'];
if (isset($_SERVER['HTTP_ORIGIN']) && in_array($_SERVER['HTTP_ORIGIN'], $allowed, true)) {
    header('Access-Control-Allow-Origin: ' . $_SERVER['HTTP_ORIGIN']);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status'=>'method_not_allowed']);
    exit;
}

// Rate limit 30s
$key = 'cv_upload_' . ($_SERVER['REMOTE_ADDR'] ?? 'ip');
if (isset($_SESSION[$key]) && time() - $_SESSION[$key] < 30) {
    http_response_code(429);
    echo json_encode(['status'=>'rate_limit']);
    exit;
}
$_SESSION[$key] = time();

if (!isset($_FILES['cv_file']) || $_FILES['cv_file']['error'] !== UPLOAD_ERR_OK) {
    http_response_code(400);
    echo json_encode(['status'=>'no_file']);
    exit;
}

$file = $_FILES['cv_file'];
$allowed_types = ['application/pdf','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
if (!in_array($file['type'], $allowed_types)) {
    http_response_code(415);
    echo json_encode(['status'=>'invalid_type']);
    exit;
}
if ($file['size'] > 5 * 1024 * 1024) {
    http_response_code(413);
    echo json_encode(['status'=>'too_large']);
    exit;
}

$upload_dir = __DIR__ . '/../uploads/';
if (!is_dir($upload_dir)) {
    @mkdir($upload_dir, 0755, true);
}

$ext = pathinfo($file['name'], PATHINFO_EXTENSION);
$base = pathinfo($file['name'], PATHINFO_FILENAME);
$safe = preg_replace('/[^a-zA-Z0-9-_]/','_', $base);
$dest = $upload_dir . $safe . '_' . date('Ymd_His') . '.' . $ext;

if (!move_uploaded_file($file['tmp_name'], $dest)) {
    http_response_code(500);
    echo json_encode(['status'=>'upload_error']);
    exit;
}

echo json_encode(['status'=>'success','filename'=>basename($dest)]);
?>
