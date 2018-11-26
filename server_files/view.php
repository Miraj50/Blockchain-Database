<?php 
	session_start();

	if(isset($_SESSION['logged_in'])){
		if($_SESSION['student'] === '1'){ // student
			$servername = "localhost";
			$username = "root";
			$password = "Hack@hack1";
			$dbname = "student";
			try {
				$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
				$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

				$s = "SELECT grades.uid id, name, course, grade FROM grades, creds WHERE grades.uid=creds.uid AND grades.uid = :uname";
				$stmt = $conn->prepare($s);
				$stmt->bindValue(':uname', $_SESSION['logged_in']);
				$stmt->execute();

				while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
					echo $row['id'] . ' ' . $row['name'] . ' ' . $row['course'] . ' ' . $row['grade'] . '&';
				}
			}
			catch(PDOException $e){
				echo "D";
			}
			$conn = null;
		}
		else if($_SESSION['student'] === '0'){ // instructor
			$servername = "localhost";
			$username = "root";
			$password = "Hack@hack1";
			$dbname = "student";
			try {
				$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
				$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

				$s = "SELECT grades.uid id, name, course, grade FROM grades, creds WHERE grades.uid=creds.uid ORDER BY id";
				$stmt = $conn->prepare($s);
				$stmt->execute();

				while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
					echo $row['id'] . '%' . $row['name'] . '%' . $row['course'] . '%' . $row['grade'] . '&';
				}
			}
			catch(PDOException $e){
				echo "D";
			}
			$conn = null;
		}
	}
?>