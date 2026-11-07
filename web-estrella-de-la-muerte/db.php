<?php
//$conn = new mysqli("localhost", "root", "", "deathstar");
$conn = new mysqli("db1", "root", getenv('DB_PASSWORD'), "deathstar");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
