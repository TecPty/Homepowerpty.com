<?php
// Unified form handler for contact and careers
// Clean rewrite with CSRF, rate limit, and optional test mode

session_start();

header('Content-Type: application/json; charset=UTF-8');
header('Access-Control-Allow-Methods: POST');

// Allow CORS for production and safe local testing
$allowed_origins = [
    'https://www.homepowerpty.com',
    'http://localhost',
    'http://127.0.0.1',
    'http://127.0.0.1:5500'
];
if (isset($_SERVER['HTTP_ORIGIN']) && in_array($_SERVER['HTTP_ORIGIN'], $allowed_origins, true)) {
    header('Access-Control-Allow-Origin: ' . $_SERVER['HTTP_ORIGIN']);
}

// Test mode: when true, write emails to /logs instead of sending
define('HP_TEST_MODE', false);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode('method_not_allowed');
    exit;
}

// CSRF check
if (!isset($_POST['csrf_token']) || !isset($_SESSION['csrf_token']) || !hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    http_response_code(403);
    echo json_encode('csrf_error');
    exit;
}

// Rate limit (60s per IP)
$rate_key = 'form_submission_' . ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
if (isset($_SESSION[$rate_key]) && time() - $_SESSION[$rate_key] < 60) {
    http_response_code(429);
    echo json_encode('rate_limit');
    exit;
}
$_SESSION[$rate_key] = time();

function valid_phone($s) {
    return (bool)preg_match('/^[\d\s\+\-\(\)]{7,}$/', $s);
}

function send_mail_or_log($to, $subject, $html, $headers) {
    if (HP_TEST_MODE) {
        $logDir = __DIR__ . '/../logs';
        if (!is_dir($logDir)) {
            @mkdir($logDir, 0755, true);
        }
        $fn = $logDir . '/mail_' . date('Ymd_His') . '_' . uniqid() . '.html';
        file_put_contents($fn, "Subject: $subject\nTo: $to\n\n" . $html);
        return true;
    }
    return mail($to, $subject, $html, implode("\r\n", $headers));
}

$form_type = filter_input(INPUT_POST, 'form_type', FILTER_SANITIZE_FULL_SPECIAL_CHARS) ?: 'contact';
$to = 'josephharari@homepowerpty.com, davidazran@homepowerpty.com, soporte@tecpty.com';

if ($form_type === 'careers') {
    $full_name = trim((string)filter_input(INPUT_POST, 'full_name', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $email     = trim((string)filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL));
    $phone     = trim((string)filter_input(INPUT_POST, 'phone', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $position  = trim((string)filter_input(INPUT_POST, 'position', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $experience= trim((string)filter_input(INPUT_POST, 'experience', FILTER_SANITIZE_FULL_SPECIAL_CHARS));

    if ($full_name === '' || $email === '' || $phone === '' || $position === '') {
        echo json_encode('empty');
        exit;
    }
    if (strlen($full_name) < 2 || !filter_var($email, FILTER_VALIDATE_EMAIL) || !valid_phone($phone) || strlen($position) < 2) {
        echo json_encode('invalid');
        exit;
    }

    $subject = 'Solicitud de Empleo - ' . $full_name . ' (' . htmlspecialchars($position, ENT_QUOTES, 'UTF-8') . ')';
    $email_body = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Solicitud de Empleo</title></head><body style='font-family:Arial,sans-serif;line-height:1.6;color:#333;'>" .
        "<div style='max-width:600px;margin:0 auto;padding:20px;border:1px solid #ddd;'>" .
        "<h2 style='color:#FF9F1C;text-align:center;'>Nueva Solicitud de Empleo</h2>" .
        "<div style='background:#f9f9f9;padding:15px;border-radius:5px;margin:20px 0;'>" .
        '<p><strong>Nombre Completo:</strong> ' . htmlspecialchars($full_name, ENT_QUOTES, 'UTF-8') . '</p>' .
        '<p><strong>Email:</strong> ' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</p>' .
        '<p><strong>Teléfono:</strong> ' . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . '</p>' .
        '<p><strong>Posición de Interés
        ($experience !== '' ? ('<p><strong>Experiencia:</strong></p><div style="background:#fff;padding:10px;border-left:4px solid #2196F3;">' . nl2br(htmlspecialchars($experience, ENT_QUOTES, 'UTF-8')) . '</div>') : '') .
        "</div><hr style='border:1px solid #eee;margin:20px 0;'><p style='font-size:12px;color:#666;text-align:center;'>Enviado desde: " . htmlspecialchars($_SERVER['HTTP_HOST'] ?? 'cli', ENT_QUOTES, 'UTF-8') . ' el ' . date('d/m/Y H:i:s') . "</p></div></body></html>";
} else {

    $name    = trim((string)filter_input(INPUT_POST, 'name', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $number  = trim((string)filter_input(INPUT_POST, 'number', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $email   = trim((string)filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL));
    $company = trim((string)filter_input(INPUT_POST, 'company', FILTER_SANITIZE_FULL_SPECIAL_CHARS));
    $message = trim((string)filter_input(INPUT_POST, 'message', FILTER_SANITIZE_FULL_SPECIAL_CHARS));

    if ($name === '' || $number === '' || $message === '') {
        echo json_encode('empty');
        exit;
    }
    if (strlen($name) < 2 || strlen($message) < 10 || !valid_phone($number)) {
        echo json_encode('invalid');
        exit;
    }

    $subject = 'Nuevo mensaje desde homepowerpty.com - ' . $name;
    $email_body = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Nuevo mensaje de contacto</title></head><body style='font-family:Arial,sans-serif;line-height:1.6;color:#333;'>" .
        "<div style='max-width:600px;margin:0 auto;padding:20px;border:1px solid #ddd;'>" .
        "<h2 style='color:#FF9F1C;text-align:center;'>Nuevo mensaje desde Home Power</h2>" .
        "<div style='background:#f9f9f9;padding:15px;border-radius:5px;margin:20px 0;'>" .
        '<p><strong>Nombre:</strong> ' . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . '</p>' .
        '<p><strong>Teléfono:</strong> ' . htmlspecialchars($number, ENT_QUOTES, 'UTF-8') . '</p>' .
        ($email !== '' ? ('<p><strong>Email:</strong> ' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</p>') : '') .
        ($company !== '' ? ('<p><strong>Empresa:</strong> ' . htmlspecialchars($company, ENT_QUOTES, 'UTF-8') . '</p>') : '') .
        '<p><strong>Mensaje:</strong></p><div style="background:#fff;padding:10px;border-left:4px solid #FF9F1C;">' . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . '</div>' .
        "</div><hr style='border:1px solid #eee;margin:20px 0;'><p style='font-size:12px;color:#666;text-align:center;'>Enviado desde: " . htmlspecialchars($_SERVER['HTTP_HOST'] ?? 'cli', ENT_QUOTES, 'UTF-8') . ' el ' . date('d/m/Y H:i:s') . "</p></div></body></html>";
}

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'From: Home Power PTY <noreply@homepowerpty.com>',
    'Reply-To: noreply@homepowerpty.com',
    'X-Mailer: PHP/' . phpversion()
];






// Build headers depending on attachment
$baseHeaders = [
    'MIME-Version: 1.0',
    'From: Home Power PTY <noreply@homepowerpty.com>',
    'Reply-To: noreply@homepowerpty.com',
    'X-Mailer: PHP/' . phpversion()
];

$hasFile = isset($_FILES['cv_file']) && is_array($_FILES['cv_file']) && $_FILES['cv_file']['error'] === UPLOAD_ERR_OK;
if ($hasFile) {
    $file = $_FILES['cv_file'];
    $allowed_types = ['application/pdf','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!in_array($file['type'], $allowed_types) || $file['size'] > 5 * 1024 * 1024) {
        $hasFile = false; // ignore invalid file silently
    }
}

if ($hasFile) {
    $separator = '==HPBOUNDARY_' . md5((string)time());
    $headers = $baseHeaders;
    $headers[] = 'Content-Type: multipart/mixed; boundary="' . $separator . '"';

    $body  = '--' . $separator . "\r\n";
    $body .= "Content-Type: text/html; charset=UTF-8\r\n";
    $body .= "Content-Transfer-Encoding: 7bit\r\n\r\n";
    $body .= $email_body . "\r\n";

    $filename = basename($file['name']);
    $filedata = chunk_split(base64_encode(file_get_contents($file['tmp_name'])));
    $body .= '--' . $separator . "\r\n";
    $body .= 'Content-Type: ' . $file['type'] . '; name="' . $filename . '"' . "\r\n";
    $body .= 'Content-Transfer-Encoding: base64' . "\r\n";
    $body .= 'Content-Disposition: attachment; filename="' . $filename . '"' . "\r\n\r\n";
    $body .= $filedata . "\r\n";
    $body .= '--' . $separator . '--';

    $ok = send_mail_or_log($to, $subject, $body, $headers);
} else {
    $headers = $baseHeaders;
    $headers[] = 'Content-Type: text/html; charset=UTF-8';
    $ok = send_mail_or_log($to, $subject, $email_body, $headers);
}

echo json_encode($ok ? 'success' : 'error');
exit;
?>



