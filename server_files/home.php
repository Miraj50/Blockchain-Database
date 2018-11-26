<?php 
	session_start();
	if(!isset($_SESSION['logged_in'])){
		header("location:index.php");
	}
?>

<!DOCTYPE html>
<html>
<style>
	a{
		padding: 8px 16px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		font-size: 16px;
		margin: 4px 2px;
		transition-duration: 0.4s;
		cursor: pointer;
		background-color: #660033; 
		color: white;
		border: none;
	}
	a:hover {
		background-color: black;
		color: white;
	}
</style>
<head>
	<title>Home</title>
</head>
<body>
	<a href="logout.php">Logout</a>
</body>
</html>