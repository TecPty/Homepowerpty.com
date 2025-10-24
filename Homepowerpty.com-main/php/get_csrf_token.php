<?php
session_start();

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://www.homepowerpty.com');
header('Access-Control-Allow-Methods: GET');

// Generar token CSRF si no existe
if (!isset($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

echo json_encode(['token' => $_SESSION['csrf_token']]);
?>