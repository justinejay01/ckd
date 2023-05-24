<?php

$host = 'localhost';
$port = '3306';
$user = 'root';
$pass = '';

$db_name = "dietary";

$conn = mysqli_connect($host, $user, $pass, $db_name);

if (!$conn) {
	echo "Connection failed!";
}