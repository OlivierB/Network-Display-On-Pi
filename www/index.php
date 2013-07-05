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

	<script src='/script/network/DataDispatcher.js'></script>
	<script src='/script/network/loader.js'></script>
	
	<script src='/script/slide/slide-conf.js'></script>
	<script src="/script/network/WebSocketManager.js"></script>
	<script src="/script/network/AjaxManager.js"></script>
	<script src="/script/text/TextFormatter.js"></script>
	<script src="/script/resize/resize.js"></script>


</head>

<body>
	<!-- All pages are included here, slideJS handle the animation -->

	
	
	<div id="slides" >

		<?php
		$app = parse_ini_file('ndop.conf.ini');

		if( isset($app['database_address']) && 
			isset($app['database_login']) && 
			isset($app['database_password']) )
		{
			try {
				$db = new PDO("mysql:host=".$app['database_address'].";dbname=NDOP_GUI", $app['database_login'], $app['database_password']);


				$sql = "SELECT folder_name FROM  `layout` JOIN modules ON id_module = id";
				$results = $db->query($sql);
				$pages = $results->fetchAll(PDO::FETCH_ASSOC);

				foreach ($pages as $key => $value) {
					echo "<div>";
					include "modules/".$value['folder_name']."/index.php";
					echo "</div>";
				}
			}
			catch(PDOException $e)
			{
				echo $e->getMessage();
			}
		}
		?>

		

	</div>
	
	

</body>
</html>
