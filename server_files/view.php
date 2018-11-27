<?php 
	session_start();

	if(isset($_SESSION['logged_in'])){
		if($_SESSION['student'] === '1'){ // student
			try {
				require __DIR__ . "/check.php"; 
			}
			catch (Exception $e){
				echo "D";
				die();
			}

			try {
				$s = "SELECT grades.uid id, name, course, grade FROM grades, creds WHERE grades.uid=creds.uid AND grades.uid = :uname";
				$stmt = $conn->prepare($s);
				$stmt->bindValue(':uname', $_SESSION['logged_in']);
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
		else if($_SESSION['student'] === '0'){ // instructor
			
			try {
				require __DIR__ . "/check.php"; 
			}
			catch (Exception $e){
				echo "D";
				die();
			}

			try {
				// 
				$course_list = $client->listStreamKeyItems('instructor', '<instructor_identifier>');
				$courses = array();
				foreach ($course_list as $key => $value) {
					$courses[] = $value['data'];
				}

				$s = "SELECT grades.uid id, name, course, grade FROM grades, creds WHERE grades.uid=creds.uid";
				foreach($courses as $key => $value) {
					// strval -> integer to string
					$s = $s . " AND course = :course" . strval($key);
				}
				// $s = "SELECT grades.uid id, name, course, grade FROM grades, creds WHERE grades.uid=creds.uid AND ORDER BY id";
				$stmt = $conn->prepare($s);
				foreach($courses as $key => $value) {
					// strval -> integer to string
					$stmt->bindValue(':course' . strval($key), $value);
				}
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