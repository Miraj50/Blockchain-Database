<?php 
	session_start();

	if(isset($_SESSION['logged_in'])){
		if($_SESSION['student'] === '0'){ // instructor
			try {
				require __DIR__ . "/check.php"; 
			}
			catch (Exception $e){
				echo "D" . "0";
				die();
			}

			$data = file_get_contents("php://input");

			$json = json_decode($data, true);
			$check = 1;
			$number = 0;

			foreach ($json['data'] as $i) {
				if(count($i) != 5 || strlen($i['uid']) > 128 || strlen($i['course']) > 10 || strlen($i['grade']) != 2){
					echo "N";
					$check = 0;
					break;
				}
				$number += 1;
			}

			if($check == 1){
				$count = 0;

				if(is_null($conn) || $number != $json['count']) {
					echo "D" . "0";
					die();
				}

				$s = "INSERT INTO grades VALUES (:uname, :course, :grade, :tid, :idfr)";
				$stmt = $conn->prepare($s);

				try {
					foreach ($json['data'] as $i) {
						$course_list = $client->listStreamKeyItems('instructor', $i['identifier'], false, 999999999);
						$isAllowed = false;
						foreach ($course_list as $value) {
							if($i['course'] === pack('H*', $value['data'])){
								$isAllowed = true;
								break;
							}
						}

						if(!$isAllowed){
							echo "D" . $count;
							die();
						}

						if(!(isset($i['sig']))){
							echo "D" . $count;
							die();
						}
						$sig = pack("H*", $i['sig']);

						$p_key = $client->listStreamKeyItems('pubkey', $i['identifier']);
						$p_key = pack("H*", $p_key[0]['data']);
						$ok = openssl_verify($i['uid'] . $i['course'] . $i['grade'], $sig, $p_key, OPENSSL_ALGO_SHA256);
						if ($ok != 1) {
							echo "D" . $count;
							die();
						}

						$primKey = $i['uid'] . $i['course'];
						if(in_array($primKey, $primkey_list)){
							echo "D" . $count;
							die();
						}
						else{
							sort($cur_db);
							$cur_data = $i['uid'] . $i['course'] . $i['grade'] . $i['identifier'];
							$cur_db_hash = hash('sha256', implode("", $cur_db));
							$stream_data = hash('sha256', $cur_db_hash . $cur_data);
							$new_txid = $client->publishStreamItem('stream1', $i['uid'] . $i['course'], $stream_data);
							$cur_db[] = $new_txid . $cur_data;
							$primkey_list[] = $primKey;

							$stmt->bindValue(':uname', $i['uid']);
							$stmt->bindValue(':course', $i['course']);
							$stmt->bindValue(':grade', $i['grade']);
							$stmt->bindValue(':tid', $new_txid);
							$stmt->bindValue(':idfr', $i['identifier']);
							
							if($stmt->execute()){
								$count = $count + 1;
							}
						}
					}
				}
				catch(PDOException $e){
					echo "D" . $count;
					die();
				}
				echo "S";
			}
		}
	}
?>