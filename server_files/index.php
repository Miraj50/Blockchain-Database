<?php session_start();
	if(isset($_SESSION['logged_in'])){
		header("location:home.php");
	}
?>

<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta charset="UTF-8">
	<title>BC-D</title>
	<style>
	html {
		height: 100%;
		margin: 0;
		background-image: url("assets/background.png");
		height: 100%; 
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;
	}
	.welcome{
		/*position: absolute;*/
		text-align: center;
		/*left: 10%;*/
		/*top: 25%;*/
	}
	.button {
		padding: 12px 24px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		font-size: 16px;
		margin: 4px 2px;
		transition-duration: 0.4s;
		cursor: pointer;
		background-color: #660033; 
		color: white; 
	}
	.button:hover {
		background-color: black;
		color: white;
	}
	footer {
		position: absolute;
		bottom: 0;
		right: 0;
		background-color: black;
		color: white;
		text-align: center;
	}
	h1, h2{
		color: black;
	}

	input[type=submit]{
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
	input[type=submit]:hover {
		background-color: black;
		color: white;
	}

	/* Center the image and position the close button */
	.imgcontainer {
		text-align: center;
		padding-top: 3%;
		/*margin: 24px 12px 12px 12px;*/
		position: relative;
	}
	.container {
		text-align: center;
		padding: 16px;
	}

	.modal {
		display: none; /* Hidden by default */
		position: fixed; /* Stay in place */
		z-index: 1; /* Sit on top */
		left: 0;
		top: 0;
		width: 100%; /* Full width */
		height: 100%; /* Full height */
		overflow: auto; /* Enable scroll if needed */
		background-color: rgb(0,0,0); /* Fallback color */
		background-color: rgba(0,0,0,0.6); /* Black w/ opacity */
		padding-top: 60px;
	}
	.modal-content {
		background-color: #fefefe;
		margin: 5% auto 15% auto;
		border: 1px solid #888;
		width: 20%;
	}

	/* The Close Button (x) */
	.close {
		position: absolute;
		right: 1%;
		/*top: 0;*/
		color: #000;
		font-size: 20px;
		font-weight: bold;
	}

	.close:hover,.close:focus {
		color: red;
		cursor: pointer;
	}

	/* Add Zoom Animation */
	.animate {
		-webkit-animation: animatezoom 0.4s;
		animation: animatezoom 0.4s
	}

	@-webkit-keyframes animatezoom {
		from {-webkit-transform: scale(0)} 
		to {-webkit-transform: scale(1)}
	}

	@keyframes animatezoom {
		from {transform: scale(0)} 
		to {transform: scale(1)}
	}

	/* Change styles for span and cancel button on extra small screens */
	@media screen and (max-width: 300px) {
		span.psw {
			display: block;
			float: none;
		}
	}
	#error1, #error2{
		padding: 2px;
		font-size: 12px;
		margin-top: 5%;
		background: #ffccee;
	}
</style>
</head>

<body>
	<div class="welcome">
		<!-- <h2><i>Welcome</i></h2>
		<h1><i>Hope you had a Nice Day !</i></h1> -->
		<button onclick="document.getElementById('id02').style.display='block'" class="button" style="border: none;">Login</button>
		<button onclick="document.getElementById('id01').style.display='block'" class="button" style="border: none;">Sign Up</button>
	</div>

	<div id="id02" class="modal">

		<form id="loginform" method="post" class="modal-content animate">
			<div class="imgcontainer">
				<span onclick="document.getElementById('id02').style.display='none'" class="close" title="Close Modal">&times;</span>
				<h2 style="padding: 0px; margin: 0px">Login</h2>
			</div>
			<div class="container">
				<input type="text" id="name" name="uname" placeholder="Username..." required>
				<br><br>				
				<input type="password" id="psw" name="pass" placeholder="Password..." required>
				<br><br>
				<input type="submit" value="Login"><br>
				<div id="error1" style="display: none;">Incorrect Username or Password !</div>
			</div>
		</form>
	</div>
	<div id="id01" class="modal">

		<form id="signupform" method="post" class="modal-content animate">
			<div class="imgcontainer">
				<span onclick="document.getElementById('id01').style.display='none'" class="close" title="Close Modal">&times;</span>
				<h2 style="padding: 0px; margin: 0px">Sign Up</h2>
			</div>
			<div class="container">
				<input type="text" id="uname" name="uname" placeholder="Choose a Username..." required>
				<br><br>				
				<input type="password" id="pass" name="pass" placeholder="Choose a Password..." required>
				<br><br>
				<input type="submit" value="Sign Up">
				<div id="error2" style="display: none;">Some Error Occurred! Please Try Again</div>
			</div>
		</form>
	</div>

	<script>
		var modal = document.getElementById('id01');
		var modal1 = document.getElementById('id02');
		// When the user clicks anywhere outside of the modal, close it
		window.onclick = function(event) {
			if (event.target == modal) {
				modal.style.display = "none";
			}
			if (event.target == modal1) {
				modal1.style.display = "none";
			}
		}
	</script>
	<footer>&copy; 2018, Smoke 1337 Everyday!</footer>
</body>
<script src="assets/main.js"></script>
<script src="assets/OpenCrypto.js"></script>
<script src="assets/jquery.min.js"></script>
</html>

