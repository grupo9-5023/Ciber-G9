<?php
$conn = new mysqli("db3", "root", getenv('DB_PASSWORD'), "enterprise");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
