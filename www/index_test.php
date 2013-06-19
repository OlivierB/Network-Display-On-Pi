<?php
	include 'pages/common.php';
?>
<a href=""></a>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>NDOP</title>
	
	<!-- library CSS-->
	<link rel="stylesheet" href="/lib/font-awesome/css/font-awesome.min.css">
	<link rel="stylesheet" href="/lib/rendro-easy-pie/jquery.easy-pie-chart.css">
	<link rel="stylesheet" href="/lib/bootstrap/css/bootstrap.css">

	
	<!-- library JS -->
	<script src="/lib/canvasjs.min.js"></script>
	<script src="/lib/jquery-2.0.2.min.js"></script>
	<script src="/lib/jquery.slides.min.js"></script>
	<script src="/lib/rendro-easy-pie/jquery.easy-pie-chart.js"></script>
	<script src='/lib/jquery-number.js'></script>
	<script src='/lib/bootstrap/js/bootstrap.min.js'></script>

	<!-- Personnal CSS -->
	<link rel="stylesheet" href="/style/slide.css">
	<link rel="stylesheet" href="/style/main.css">
	<link rel="stylesheet" href="/style/chart.css">
	<link rel="stylesheet" href="/style/resize.css">

	<!-- Personnal JS -->
	<script src="/ndop.conf.js"></script>
	<script src='/script/slide/slide-conf.js'></script>
	<script src="/script/network/WebSocketManager.js"></script>
	<script src="/script/resize/resize.js"></script>

</head>

<body>
	<!-- All pages are included here, slideJS handle the animation -->
	<div><?php include "pages/3d_view.php" ?></div>

</body>
</html>

