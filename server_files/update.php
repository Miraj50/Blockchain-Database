<!-- 
This project is a demonstration of detecting insider attacks on databases using Blockchain
Copyright (C) 2018  Rishabh Raj
This code is licensed under GNU GPLv3 license. See LICENSE for details
-->

<?php
	session_start();

	if(isset($_SESSION['logged_in'])){
		if($_SESSION['student'] === '0'){ // instructor
			try {
				require __DIR__ . "/check.php"; 
			}
			catch (Exception $e){
				echo "D";
				die();
			}

			$uid = $_POST['uid'];
			$course = $_POST['course'];
			$grade = $_POST['grade'];
			$sig = $_POST['sig'];
			$identifier = $_POST['identifier'];

			try {
				$sig = pack("H*", $sig);

				$p_key = $client->listStreamKeyItems('pubkey', $identifier);
				$p_key = pack("H*", $p_key[0]['data']);
				$ok = openssl_verify($uid . $course . $grade, $sig, $p_key, OPENSSL_ALGO_SHA256);
				if ($ok != 1) {
					echo "D";
					die();
				}

				$s = "UPDATE grades SET grade = :grd, txid = :tid WHERE uid = :uname AND course = :cors";
				$utmt = $conn->prepare($s);

				$q = "SELECT txid, uid, course, grade, identifier from grades WHERE uid = :uid AND course = :cors";
				$stmt = $conn->prepare($q);

				$stmt->bindValue(':uid', $uid);
				$stmt->bindValue(':cors', $course);
				
				$stmt->execute();

				$row = $stmt->fetch(PDO::FETCH_ASSOC);

				$old_row_data = $row['txid'] . $row['uid'] . $row['course'] . $row['grade'] . $row['identifier'];
				$cur_db = array_diff($cur_db, [$old_row_data]);

				$cur_data = $row['uid'] . $row['course'] . $grade . $row['identifier'];
				$cur_db_hash = hash('sha256', implode("", $cur_db));
				$stream_data = hash('sha256', $cur_db_hash . $cur_data);
				$new_txid = $client->publishStreamItem('stream1', $uid . $course, $stream_data);
				$cur_db[] = $new_txid . $cur_data . $identifier;
				// sort($cur_db);

				$utmt->bindValue(':grd', $grade);
				$utmt->bindValue(':tid', $new_txid);
				$utmt->bindValue(':uname', $uid);
				$utmt->bindValue(':cors', $course);
				$utmt->execute();
				
			}
			catch(PDOException $e){
				echo "D";
				die();
			}
			echo "S";
			$conn = null;
		}
	}
?>