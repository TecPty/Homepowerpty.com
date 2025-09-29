<?php
// Configuración de seguridad básica
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *'); // Permitir cualquier origen para pruebas
header('Access-Control-Allow-Methods: POST');

// Rate limiting simple
session_start();
$rate_limit_key = 'form_submission_' . $_SERVER['REMOTE_ADDR'];
if (isset($_SESSION[$rate_limit_key]) && time() - $_SESSION[$rate_limit_key] < 30) {
    http_response_code(429);
    echo json_encode('rate_limit');
    exit;
}
$_SESSION[$rate_limit_key] = time();

// Configurar direcciones de email
$to = 'josephharari@homepowerpty.com, davidazran@homepowerpty.com';

// Validar método POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode('method_not_allowed');
    exit;
}

// Obtener y validar datos del formulario
$name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
$number = filter_input(INPUT_POST, 'number', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
$message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_FULL_SPECIAL_CHARS);

// Validaciones básicas
if (empty($name) || empty($number) || empty($message)) {
    echo json_encode('empty');
    exit;
}

if (strlen($name) < 2 || strlen($message) < 10) {
    echo json_encode('invalid_data');
    exit;
}

// Validar número de teléfono
if (!preg_match('/^[\d\s\+\-\(\)]{7,}$/', $number)) {
    echo json_encode('invalid_phone');
    exit;
}

// Preparar el email
$subject = 'Nuevo mensaje desde homepowerpty.com - ' . $name;
$email_body = "
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Nuevo Mensaje - Home Power PTY</title>
</head>
<body style='font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5;'>
    <div style='max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        
        <!-- Header -->
        <div style='background: linear-gradient(135deg, #FF9F1C 0%, #e8890b 100%); padding: 30px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 24px; font-weight: bold;'>
                📧 Nuevo Mensaje de Contacto
            </h1>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 14px;'>
                homepowerpty.com
            </p>
        </div>
        
        <!-- Contenido -->
        <div style='padding: 30px;'>
            
            <!-- Información del cliente -->
            <div style='background-color: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 25px;'>
                <h2 style='color: #333; margin: 0 0 15px 0; font-size: 18px; border-bottom: 2px solid #FF9F1C; padding-bottom: 8px;'>
                    👤 Información del Cliente
                </h2>
                <p style='margin: 8px 0; color: #555; font-size: 14px;'>
                    <strong style='color: #333;'>Nombre:</strong> " . htmlspecialchars($name) . "
                </p>
                <p style='margin: 8px 0; color: #555; font-size: 14px;'>
                    <strong style='color: #333;'>Teléfono:</strong> " . htmlspecialchars($number) . "
                </p>
                <p style='margin: 8px 0; color: #555; font-size: 14px;'>
                    <strong style='color: #333;'>Fecha:</strong> " . date('d/m/Y H:i:s') . "
                </p>
            </div>
            
            <!-- Mensaje -->
            <div style='background-color: #fff; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px;'>
                <h2 style='color: #333; margin: 0 0 15px 0; font-size: 18px; border-bottom: 2px solid #4CAF50; padding-bottom: 8px;'>
                    💬 Mensaje
                </h2>
                <div style='background-color: #f8f9fa; border-left: 4px solid #4CAF50; padding: 15px; border-radius: 0 4px 4px 0;'>
                    <p style='margin: 0; color: #333; line-height: 1.6; font-size: 14px;'>
                        " . nl2br(htmlspecialchars($message)) . "
                    </p>
                </div>
            </div>
            
            <!-- Instrucciones de respuesta -->
            <div style='background-color: #e3f2fd; border-radius: 8px; padding: 20px; margin-top: 25px; border-left: 4px solid #2196F3;'>
                <h3 style='color: #1565C0; margin: 0 0 10px 0; font-size: 16px;'>
                    📋 Acciones Recomendadas
                </h3>
                <ul style='margin: 0; padding-left: 20px; color: #333;'>
                    <li style='margin-bottom: 5px; font-size: 14px;'>Responder vía WhatsApp al: " . htmlspecialchars($number) . "</li>
                    <li style='margin-bottom: 5px; font-size: 14px;'>Tiempo de respuesta objetivo: 24 horas</li>
                    <li style='margin-bottom: 5px; font-size: 14px;'>Categorizar lead según el mensaje recibido</li>
                </ul>
            </div>
            
        </div>
        
        <!-- Footer -->
        <div style='background-color: #333; padding: 20px; text-align: center;'>
            <p style='color: #ccc; margin: 0; font-size: 12px;'>
                Este mensaje fue enviado automáticamente desde 
                <strong style='color: #FF9F1C;'>homepowerpty.com</strong>
            </p>
            <p style='color: #888; margin: 5px 0 0 0; font-size: 11px;'>
                Sistema de notificaciones - Home Power PTY
            </p>
        </div>
        
    </div>
</body>
</html>
";

// Headers del email
$headers = array(
    'MIME-Version: 1.0',
    'Content-type: text/html; charset=UTF-8',
    'From: Home Power PTY <noreply@homepowerpty.com>',
    'Reply-To: ' . $name . ' <noreply@homepowerpty.com>',
    'X-Mailer: PHP/' . phpversion(),
    'X-Priority: 1',
    'X-MSMail-Priority: High'
);

// Intentar enviar el email
try {
    $mail_sent = mail($to, $subject, $email_body, implode("\r\n", $headers));
    
    if ($mail_sent) {
        // Log exitoso (opcional)
        error_log("[FORM SUCCESS] Mensaje enviado desde: $name ($number) a las " . date('Y-m-d H:i:s'));
        echo json_encode('success');
    } else {
        // Log de error
        error_log("[FORM ERROR] Falló el envío desde: $name ($number) a las " . date('Y-m-d H:i:s'));
        echo json_encode('error');
    }
} catch (Exception $e) {
    // Log de excepción
    error_log("[FORM EXCEPTION] Error: " . $e->getMessage() . " desde: $name ($number)");
    echo json_encode('error');
}
?>