<?php
/**
 * Script de diagnóstico de correo electrónico
 * IMPORTANTE: Elimina este archivo después de usarlo por seguridad
 */

// Verificar si la función mail está disponible
if (!function_exists('mail')) {
    die('❌ La función mail() no está disponible en este servidor');
}

echo "<h2>🔍 Diagnóstico de Correo Electrónico</h2>";

// Test 1: Información del servidor
echo "<h3>1. Información del Servidor</h3>";
echo "<ul>";
echo "<li><strong>PHP Version:</strong> " . phpversion() . "</li>";
echo "<li><strong>Servidor:</strong> " . $_SERVER['SERVER_SOFTWARE'] . "</li>";
echo "<li><strong>Sistema Operativo:</strong> " . PHP_OS . "</li>";
echo "</ul>";

// Test 2: Configuración SMTP
echo "<h3>2. Configuración SMTP de PHP</h3>";
echo "<ul>";
echo "<li><strong>SMTP:</strong> " . ini_get('SMTP') . "</li>";
echo "<li><strong>smtp_port:</strong> " . ini_get('smtp_port') . "</li>";
echo "<li><strong>sendmail_from:</strong> " . ini_get('sendmail_from') . "</li>";
echo "<li><strong>sendmail_path:</strong> " . ini_get('sendmail_path') . "</li>";
echo "</ul>";

// Test 3: Envío de correo de prueba
echo "<h3>3. Envío de Correo de Prueba</h3>";

$test_email = 'josephharari@homepowerpty.com';
$subject = 'Test desde HomePowerPty - ' . date('Y-m-d H:i:s');
$message = '
<html>
<head>
    <meta charset="UTF-8">
    <title>Test de Email</title>
</head>
<body>
    <h2>Este es un correo de prueba</h2>
    <p>Si recibes este mensaje, el sistema de correo está funcionando correctamente.</p>
    <p><strong>Hora de envío:</strong> ' . date('d/m/Y H:i:s') . '</p>
    <p><strong>Servidor:</strong> ' . $_SERVER['HTTP_HOST'] . '</p>
</body>
</html>
';

$headers = [
    'From: HomePowerPty <admin@homepowerpty.com>',
    'Reply-To: admin@homepowerpty.com',
    'Content-Type: text/html; charset=UTF-8',
    'X-Mailer: PHP/' . phpversion(),
    'MIME-Version: 1.0'
];

$result = mail($test_email, $subject, $message, implode("\r\n", $headers));

if ($result) {
    echo "<p style='color: green;'>✅ <strong>Éxito:</strong> El correo se envió correctamente a $test_email</p>";
    echo "<p>Revisa tu bandeja de entrada (y spam) en los próximos minutos.</p>";
} else {
    echo "<p style='color: red;'>❌ <strong>Error:</strong> No se pudo enviar el correo</p>";
    
    $error = error_get_last();
    if ($error) {
        echo "<p><strong>Detalle del error:</strong> " . $error['message'] . "</p>";
    }
    
    echo "<h4>Posibles soluciones:</h4>";
    echo "<ol>";
    echo "<li>Verifica que tu hosting tenga habilitada la función mail()</li>";
    echo "<li>Contacta a tu proveedor de hosting (Hostinger) para configurar SMTP</li>";
    echo "<li>Considera usar PHPMailer o una API de email (SendGrid, Mailgun, etc.)</li>";
    echo "</ol>";
}

// Test 4: Alternativas recomendadas
echo "<h3>4. Alternativas Recomendadas</h3>";
echo "<p>Si la función mail() no funciona, considera estas opciones:</p>";
echo "<ul>";
echo "<li><strong>PHPMailer:</strong> Librería robusta para envío de emails con SMTP</li>";
echo "<li><strong>SendGrid:</strong> API de email con plan gratuito (100 emails/día)</li>";
echo "<li><strong>Mailgun:</strong> Similar a SendGrid, muy confiable</li>";
echo "<li><strong>SMTP de Gmail:</strong> Usar Gmail como servidor SMTP</li>";
echo "</ul>";

echo "<hr>";
echo "<p style='color: red;'><strong>⚠️ IMPORTANTE:</strong> Elimina este archivo (test_email.php) después de usarlo por razones de seguridad.</p>";
?>