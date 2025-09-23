<?php
session_start();

// Configuración de seguridad
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://www.homepowerpty.com'); // Restringir CORS
header('Access-Control-Allow-Methods: POST');

// Validar CSRF
if (!isset($_POST['csrf_token']) || !hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    http_response_code(403);
    echo json_encode('csrf_error');
    exit;
}

// Rate limiting
$rate_limit_key = 'form_submission_' . $_SERVER['REMOTE_ADDR'];
if (isset($_SESSION[$rate_limit_key]) && time() - $_SESSION[$rate_limit_key] < 60) {
    http_response_code(429);
    echo json_encode('rate_limit');
    exit;
}
$_SESSION[$rate_limit_key] = time();

// Sanitizar y validar datos
$name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
$number = filter_input(INPUT_POST, 'number', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
$message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_FULL_SPECIAL_CHARS);

if (empty($name) || empty($number) || empty($message)) {
    echo json_encode('empty');
    exit;
}

// Validación adicional
if (strlen($name) < 2 || strlen($message) < 10) {
    echo json_encode('empty');
    exit;
}

// Configurar emails (ambos destinatarios)
$to = 'jharari@hgroupcapital.com, duduazran@gmail.com';
$subject = 'Nuevo mensaje desde HomePowerPty - ' . $name;
$headers = [
    'From: noreply@homepowerpty.com',
    'Reply-To: noreply@homepowerpty.com',
    'Content-Type: text/html; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion()
];

$email_body = "
<html>
<head>
    <meta charset='UTF-8'>
    <titsle>Nuevo mensaje de contacto</titsle>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333;'>
    <div style='max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;'>
        <h2 style='color: #faaa01; text-align: center;'>Nuevo mensaje desde HomePowerPty</h2>
        
        <div style='background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 20px 0;'>
            <p><strong>Nombre:</strong> " . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . "</p>
            <p><strong>Teléfono:</strong> " . htmlspecialchars($number, ENT_QUOTES, 'UTF-8') . "</p>
            <p><strong>Mensaje:</strong></p>
            <div style='background: white; padding: 10px; border-left: 4px solid #faaa01;'>
                " . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . "
            </div>
        </div>
        
        <hr style='border: 1px solid #eee; margin: 20px 0;'>
        <p style='font-size: 12px; color: #666; text-align: center;'>
            Enviado desde: " . htmlspecialchars($_SERVER['HTTP_HOST'], ENT_QUOTES, 'UTF-8') . " 
            el " . date('d/m/Y H:i:s') . "
        </p>
    </div>
</body>
</html>";

// Enviar email
if (mail($to, $subject, $email_body, implode("\r\n", $headers))) {
    echo json_encode('success');
} else {
    error_log('Error enviando email desde HomePowerPty: ' . error_get_last()['message']);
    echo json_encode('error');
}
?>