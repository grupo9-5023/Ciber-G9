<?php
//$conn = new mysqli("localhost", "root", "", "mordor");
$conn = new mysqli("db2", "root", getenv('DB_PASSWORD'), "mordor");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
