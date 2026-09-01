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

// --- NUEVA LÓGICA DE ENVÍO DE CORREO ---
$full_name = filter_input(INPUT_POST, 'full_name', FILTER_SANITIZE_SPECIAL_CHARS) ?: 'Postulante';
$email     = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL) ?: 'No proporcionado';
$phone     = filter_input(INPUT_POST, 'phone', FILTER_SANITIZE_SPECIAL_CHARS) ?: 'No proporcionado';
$position  = filter_input(INPUT_POST, 'position', FILTER_SANITIZE_SPECIAL_CHARS) ?: 'No especificada';
$experience= filter_input(INPUT_POST, 'experience', FILTER_SANITIZE_SPECIAL_CHARS) ?: 'No especificada';

$to = 'josephharari@homepowerpty.com, davidazran@homepowerpty.com, soporte@tecpty.com';
$subject = "Nueva Solicitud de Empleo: $full_name - $position";

$boundary = md5(time());
$headers = "From: Home Power PTY <noreply@homepowerpty.com>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: multipart/mixed; boundary=\"$boundary\"\r\n";

$message = "--$boundary\r\n";
$message .= "Content-Type: text/html; charset=UTF-8\r\n";
$message .= "Content-Transfer-Encoding: 7bit\r\n\r\n";
$message .= "<html><body style='font-family: Arial, sans-serif; color: #333;'>";
$message .= "<h2 style='color: #FF9F1C;'>Nueva Aplicación Laboral</h2>";
$message .= "<p><strong>Nombre:</strong> $full_name</p>";
$message .= "<p><strong>Email:</strong> $email</p>";
$message .= "<p><strong>Teléfono:</strong> $phone</p>";
$message .= "<p><strong>Posición:</strong> $position</p>";
$message .= "<p><strong>Experiencia:</strong><br>" . nl2br($experience) . "</p>";
$message .= "<p style='font-size: 12px; color: #999;'>El CV está adjunto a este correo.</p>";
$message .= "</body></html>\r\n\r\n";

$file_content = file_get_contents($dest);
$file_encoded = chunk_split(base64_encode($file_content));
$file_name = basename($dest);

$message .= "--$boundary\r\n";
$message .= "Content-Type: application/octet-stream; name=\"$file_name\"\r\n";
$message .= "Content-Description: $file_name\r\n";
$message .= "Content-Disposition: attachment; filename=\"$file_name\"; size=" . filesize($dest) . ";\r\n";
$message .= "Content-Transfer-Encoding: base64\r\n\r\n";
$message .= $file_encoded . "\r\n";
$message .= "--$boundary--";

mail($to, $subject, $message, $headers);
// ---------------------------------------

echo json_encode(['status'=>'success','filename'=>basename($dest)]);
?>
