<!-- 
This project demonstrates detection of insider attacks on databases using Blockchain
Copyright (C) 2018  Rishabh Raj
This code is licensed under GNU GPLv3 license. See LICENSE for details
-->

<?php 

	require __DIR__ . '/vendor/autoload.php';
	use be\kunstmaan\multichain\MultichainClient as MultichainClient;

	$servername = "localhost";
	$dbname = "credential";
	$username = "root";
	$password = "Hack@hack1";

	$uname = $_POST['uid'];
	$pass = $_POST['pass'];
	$pubkey = $_POST['pubkey'];

	$salt = bin2hex(random_bytes(32));

	$hash = hash_pbkdf2("sha256", $pass, $salt, 100000);

	try {
	    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
	    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        $s = "SELECT * from instructor WHERE uid = :uname";
    	$stmt = $conn->prepare($s);
    	$stmt->bindValue(':uname', $uname);
    	$stmt->execute();
    	$result = $stmt->fetchAll();
		if(sizeof($result) > 0){
			echo "M";
		}
		else{
		    $s = "INSERT INTO instructor VALUES (:uname, :salt, :hash)";
			$stmt = $conn->prepare($s);
			$stmt->bindValue(':uname', $uname);
			$stmt->bindValue(':salt', $salt);
			$stmt->bindValue(':hash', $hash);
			
			if($stmt->execute()){
				$client = new MultichainClient("http://127.0.0.1:6472", "multichainrpc", "ANVEmUWRZxYs3GS8GkrBtjKt14vNTtKWgSLNqETg9FY6", 3);
				$client->publishStreamItem('pubkey', $uname, $pubkey);
				echo "S";
			}
		}
	}
	catch(PDOException $e){
		echo "N";
	}
	$conn = null;
?>