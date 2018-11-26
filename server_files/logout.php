<?php
    session_start();
    // echo session_status() === PHP_SESSION_ACTIVE ? 1 : 0;
    unset($_SESSION['logged_in']);
	session_destroy();
?>
