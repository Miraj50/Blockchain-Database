<?php 

	session_start();

	// if(isset($_SESSION['logged_in'])){
		// if($_SESSION['student'] === '0'){ // instructor

			$servername = "localhost";
			$username = "root";
			$password = "Hack@hack1";
			$dbname = "student";

			$data = file_get_contents("php://input");

			$json = json_decode($data, true);
			$check = 1;

			foreach ($json['data'] as $i) {
				if(count($i) != 3 || strlen($i['uid']) > 128 || strlen($i['course']) > 10 || strlen($i['grade']) != 2){
					echo "N";
					$check = 0;
					break;
				}
			}

			if($check == 1){
				$count = 0;

				$s = "INSERT INTO grades VALUES (:uname, :course, :grade)";

				try {
					$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
					$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

					foreach ($json['data'] as $i) {
						$stmt = $conn->prepare($s);
						$stmt->bindValue(':uname', $i['uid']);
						$stmt->bindValue(':course', $i['course']);
						$stmt->bindValue(':grade', $i['grade']);
						
						if($stmt->execute()){
							$count = $count + 1;
						}
					}
					echo "S";
				}
				catch(PDOException $e){
					echo "D" . $count;
					die();
				}
			}

		// }
	// }
?>