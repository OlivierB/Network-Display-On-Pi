<?php
	include 'pages/common.php';
?>
<script src="http://192.168.1.144:35729/livereload.js?snipver=1"></script>

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
	<script src='/lib/bootstrap/js/bootstrap.min.js'></script>

	<!-- Personnal CSS -->
	<link rel="stylesheet" href="/style/slide.css">
	<link rel="stylesheet" href="/style/main.css">
	<link rel="stylesheet" href="/style/chart.css">

	<!-- Personnal JS -->
	<script src="/ndop.conf.js"></script>
	<script src='/script/slide/slide-conf.js'></script>

</head>

<body>
	<!-- All pages are included here, slideJS handle the animation -->
	<div id="slides">
		
		<div><?php include "pages/main_page.php" ?></div>
		<div><?php include "pages/alert_page.php" ?></div>
		<div><?php include "pages/map.php" ?></div>

		<div>
			<?php 
				include "pages/3d_view.php" 
			?>
		</div>

		
	</div>
	

</body>
</html>