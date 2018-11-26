<?php

	// if(isset($_SESSION['logged_in'])){
		// if($_SESSION['student'] === '0'){ // instructor
			$servername = "localhost";
			$username = "root";
			$password = "Hack@hack1";
			$dbname = "student";

			$uid = $_POST['uid'];
			$course = $_POST['course'];
			$grade = $_POST['grade'];

			try {
				$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
				$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

				$s = "UPDATE grades SET grade = :grd WHERE uid = :uname AND course = :cors";

				$stmt = $conn->prepare($s);
				$stmt->bindValue(':grd', $grade);
				$stmt->bindValue(':uname', $uid);
				$stmt->bindValue(':cors', $course);
				
				if($stmt->execute()){
					echo "S";
				}
				else{
					echo "D";
				}
			}
			catch(PDOException $e){
				echo "D";
			}
			$conn = null;
	// }
// }
?>