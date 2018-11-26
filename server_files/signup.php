<?php 
	// session_start();
	// if(isset($_SESSION['logged_in'])){
	// 	header("location:home.php");
	// }
	$servername = "localhost";
	$dbname = "pki";
	$username = "root";
	$password = "Hack@hack1";

	$uname = $_POST['uid'];
	$pass = $_POST['pass'];
	$salt = bin2hex(random_bytes(32));

	$hash = hash_pbkdf2("sha256", $pass, $salt, 100000);

	// echo $uname . ' ' . $pass . ' ' . $salt . ' ' . $hash;

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
				echo "S";
			}
			else{
				echo "N";
			}
		}
	}
	catch(PDOException $e){
		echo "N";
	}
	$conn = null;

?>