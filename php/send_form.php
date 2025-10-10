<?php
/**
 * Sistema de envío de formularios - HomePowerPty
 * Maneja formularios de contacto y carreras
 * 
 * @version 2.0
 * @author NetWeb
 */

session_start();

// ============================================
// CONFIGURACIÓN DE SEGURIDAD
// ============================================
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://www.homepowerpty.com');
header('Access-Control-Allow-Methods: POST');

// Validar CSRF Token
if (!isset($_POST['csrf_token']) || !isset($_SESSION['csrf_token'])) {
    http_response_code(403);
    echo json_encode('csrf_error');
    exit;
}

if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    http_response_code(403);
    echo json_encode('csrf_error');
    exit;
}

// ============================================
// RATE LIMITING (Prevenir spam)
// ============================================
$rate_limit_key = 'form_submission_' . $_SERVER['REMOTE_ADDR'];
if (isset($_SESSION[$rate_limit_key]) && time() - $_SESSION[$rate_limit_key] < 60) {
    http_response_code(429);
    echo json_encode('rate_limit');
    exit;
}
$_SESSION[$rate_limit_key] = time();

// ============================================
// CONFIGURACIÓN DE EMAIL
// ============================================
$email_config = [
    'to' => 'josephharari@homepowerpty.com, davidazran@homepowerpty.com',
    'from_email' => 'admin@homepowerpty.com',
    'from_name' => 'HomePowerPty - Formulario Web',
    'reply_to' => 'admin@homepowerpty.com'
];

// ============================================
// DETERMINAR TIPO DE FORMULARIO
// ============================================
$form_type = filter_input(INPUT_POST, 'form_type', FILTER_SANITIZE_FULL_SPECIAL_CHARS);

// Variables para el email
$subject = '';
$email_body = '';
$valid = false;

// ============================================
// PROCESAMIENTO SEGÚN TIPO DE FORMULARIO
// ============================================

if ($form_type === 'careers') {
    // ========================================
    // FORMULARIO DE CARRERAS/EMPLEO
    // ========================================
    
    // Sanitizar datos
    $full_name = filter_input(INPUT_POST, 'full_name', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $phone = filter_input(INPUT_POST, 'phone', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $position = filter_input(INPUT_POST, 'position', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $experience = filter_input(INPUT_POST, 'experience', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $motivation = filter_input(INPUT_POST, 'motivation', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    
    // Validación básica - campos obligatorios
    if (empty($full_name) || empty($email) || empty($phone) || 
        empty($position) || empty($motivation)) {
        echo json_encode('empty');
        exit;
    }
    
    // Validaciones específicas
    if (strlen($full_name) < 2) {
        echo json_encode('invalid');
        exit;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode('invalid');
        exit;
    }
    
    if (strlen($motivation) < 20) {
        echo json_encode('invalid');
        exit;
    }
    
    // Si llegamos aquí, los datos son válidos
    $valid = true;
    
    // Preparar asunto
    $subject = 'Solicitud de Empleo - HomePowerPty - ' . $full_name;
    
    // Preparar cuerpo del email (HTML)
    $email_body = "<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Solicitud de Empleo</title>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 0;'>
    <div style='max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        
        <!-- Header -->
        <div style='background: linear-gradient(135deg, #faaa01 0%, #ff9f1c 100%); padding: 30px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 24px; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                Nueva Solicitud de Empleo
            </h1>
        </div>
        
        <!-- Content -->
        <div style='padding: 30px;'>
            <div style='background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #faaa01;'>
                
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr>
                        <td style='padding: 10px 0; font-weight: bold; color: #555; width: 40%;'>Nombre Completo:</td>
                        <td style='padding: 10px 0; color: #333;'>" . htmlspecialchars($full_name, ENT_QUOTES, 'UTF-8') . "</td>
                    </tr>
                    <tr style='border-top: 1px solid #eee;'>
                        <td style='padding: 10px 0; font-weight: bold; color: #555;'>Email:</td>
                        <td style='padding: 10px 0;'><a href='mailto:" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "' style='color: #faaa01; text-decoration: none;'>" . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . "</a></td>
                    </tr>
                    <tr style='border-top: 1px solid #eee;'>
                        <td style='padding: 10px 0; font-weight: bold; color: #555;'>Teléfono:</td>
                        <td style='padding: 10px 0; color: #333;'>" . htmlspecialchars($phone, ENT_QUOTES, 'UTF-8') . "</td>
                    </tr>
                    <tr style='border-top: 1px solid #eee;'>
                        <td style='padding: 10px 0; font-weight: bold; color: #555;'>Posición de Interés:</td>
                        <td style='padding: 10px 0; color: #333;'><strong>" . htmlspecialchars($position, ENT_QUOTES, 'UTF-8') . "</strong></td>
                    </tr>
                </table>
                
            </div>
            
            <!-- Experiencia -->
            <div style='margin-bottom: 20px;'>
                <h3 style='color: #faaa01; margin-bottom: 10px; font-size: 16px;'>Experiencia Laboral:</h3>
                <div style='background: white; padding: 15px; border: 1px solid #e0e0e0; border-radius: 6px; white-space: pre-wrap;'>" . htmlspecialchars($experience, ENT_QUOTES, 'UTF-8') . "</div>
            </div>
            
            <!-- Motivación -->
            <div style='margin-bottom: 20px;'>
                <h3 style='color: #faaa01; margin-bottom: 10px; font-size: 16px;'>¿Por qué quiere trabajar con nosotros?</h3>
                <div style='background: #fff9e6; padding: 15px; border-left: 4px solid #faaa01; border-radius: 6px; white-space: pre-wrap;'>" . nl2br(htmlspecialchars($motivation, ENT_QUOTES, 'UTF-8')) . "</div>
            </div>
            
        </div>
        
        <!-- Footer -->
        <div style='background: #f4f4f4; padding: 20px; text-align: center; border-top: 1px solid #e0e0e0;'>
            <p style='margin: 0; color: #666; font-size: 12px;'>
                Enviado desde: <strong>" . htmlspecialchars($_SERVER['HTTP_HOST'], ENT_QUOTES, 'UTF-8') . "</strong><br>
                Fecha y hora: <strong>" . date('d/m/Y H:i:s') . "</strong>
            </p>
        </div>
        
    </div>
</body>
</html>";

} else {
    // ========================================
    // FORMULARIO DE CONTACTO
    // ========================================
    
    // Sanitizar datos
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $number = filter_input(INPUT_POST, 'number', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    
    // Validación básica - campos obligatorios
    if (empty($name) || empty($number) || empty($message)) {
        echo json_encode('empty');
        exit;
    }
    
    // Validaciones específicas
    if (strlen($name) < 2 || strlen($message) < 10) {
        echo json_encode('empty');
        exit;
    }
    
    // Si llegamos aquí, los datos son válidos
    $valid = true;
    
    // Preparar asunto
    $subject = 'Nuevo Mensaje de Contacto - HomePowerPty - ' . $name;
    
    // Preparar cuerpo del email (HTML)
    $email_body = "<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Mensaje de Contacto</title>
</head>
<body style='font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 0;'>
    <div style='max-width: 600px; margin: 20px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        
        <!-- Header -->
        <div style='background: linear-gradient(135deg, #faaa01 0%, #ff9f1c 100%); padding: 30px; text-align: center;'>
            <h1 style='color: white; margin: 0; font-size: 24px; text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                Nuevo Mensaje de Contacto
            </h1>
        </div>
        
        <!-- Content -->
        <div style='padding: 30px;'>
            <div style='background: #f9f9f9; padding: 20px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #faaa01;'>
                
                <table style='width: 100%; border-collapse: collapse;'>
                    <tr>
                        <td style='padding: 10px 0; font-weight: bold; color: #555; width: 30%;'>Nombre:</td>
                        <td style='padding: 10px 0; color: #333;'>" . htmlspecialchars($name, ENT_QUOTES, 'UTF-8') . "</td>
                    </tr>
                    <tr style='border-top: 1px solid #eee;'>
                        <td style='padding: 10px 0; font-weight: bold; color: #555;'>Teléfono:</td>
                        <td style='padding: 10px 0;'><a href='tel:" . htmlspecialchars($number, ENT_QUOTES, 'UTF-8') . "' style='color: #faaa01; text-decoration: none;'>" . htmlspecialchars($number, ENT_QUOTES, 'UTF-8') . "</a></td>
                    </tr>
                </table>
                
            </div>
            
            <!-- Mensaje -->
            <div style='margin-bottom: 20px;'>
                <h3 style='color: #faaa01; margin-bottom: 10px; font-size: 16px;'>Mensaje:</h3>
                <div style='background: #fff9e6; padding: 15px; border-left: 4px solid #faaa01; border-radius: 6px; white-space: pre-wrap;'>" . nl2br(htmlspecialchars($message, ENT_QUOTES, 'UTF-8')) . "</div>
            </div>
            
        </div>
        
        <!-- Footer -->
        <div style='background: #f4f4f4; padding: 20px; text-align: center; border-top: 1px solid #e0e0e0;'>
            <p style='margin: 0; color: #666; font-size: 12px;'>
                Enviado desde: <strong>" . htmlspecialchars($_SERVER['HTTP_HOST'], ENT_QUOTES, 'UTF-8') . "</strong><br>
                Fecha y hora: <strong>" . date('d/m/Y H:i:s') . "</strong>
            </p>
        </div>
        
    </div>
</body>
</html>";
}

// ============================================
// ENVÍO DEL EMAIL (si los datos son válidos)
// ============================================

if (!$valid) {
    echo json_encode('error');
    exit;
}

// Configurar headers del email
$headers = [
    'From: ' . $email_config['from_name'] . ' <' . $email_config['from_email'] . '>',
    'Reply-To: ' . $email_config['reply_to'],
    'Content-Type: text/html; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
    'MIME-Version: 1.0',
    'Return-Path: ' . $email_config['from_email'],
    'X-Priority: 3',
    'X-MSMail-Priority: Normal'
];

// Parámetros adicionales para sendmail (importante para tu configuración)
$additional_params = '-f ' . $email_config['from_email'];

// Intentar enviar el email
$mail_sent = @mail(
    $email_config['to'],
    $subject,
    $email_body,
    implode("\r\n", $headers),
    $additional_params
);

// ============================================
// RESPUESTA AL CLIENTE
// ============================================

if ($mail_sent) {
    // Log exitoso (opcional)
    error_log("Email enviado exitosamente - Tipo: $form_type - Fecha: " . date('Y-m-d H:i:s'));
    echo json_encode('success');
} else {
    // Log del error
    $error = error_get_last();
    error_log("Error enviando email - Tipo: $form_type - Error: " . ($error ? $error['message'] : 'Unknown error'));
    echo json_encode('error');
}
?>