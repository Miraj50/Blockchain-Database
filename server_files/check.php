<?php

$servername = "localhost";
$username = "root";
$password = "Hack@hack1";
$dbname = "student";

try {
	$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $e){
	echo "V";
	die();
}
$conn = null;

