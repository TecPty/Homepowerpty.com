<?php
header('Content-Type: application/json');
error_log("=== TEST PHP ===");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['full_name'])) {
        error_log("CARRERAS: " . $_POST['full_name']);
        echo json_encode('success');
    } elseif (isset($_POST['name'])) {
        error_log("CONTACTO: " . $_POST['name']);
        echo json_encode('success');
    } else {
        echo json_encode('invalid_data');
    }
} else {
    echo json_encode('error');
}
?>