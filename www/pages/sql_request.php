<?php
require "../ndop.conf.php";
require 'sql_function.php';
try {
	// server connection
	$dns = 'mysql:host='.NDOP::$app['database_address'].';dbname=NDOP';
	$user = NDOP::$app['database_login'];
	$password = NDOP::$app['database_password'];
	$connection = new PDO( $dns, $user, $password );



	if(isset($_GET['request'])){

		if(!isset($_GET['day_before_begin']) && !isset($_GET['day_before_end'])){
			$date_begin = '';
			$date_end = '';
		}else{
			
			if(isset($_GET['day_before_begin'])){
				$date_begin = 'NOW( ) - INTERVAL '.$_GET['day_before_begin'].' DAY';
			}else{
				$date_begin = 'NOW( ) - INTERVAL 1 DAY';
			}

			if(isset($_GET['day_before_end'])){
				$date_end = 'NOW( ) - INTERVAL '.$_GET['day_before_end'].' DAY';
			}else{
				$date_end = 'NOW( )';
			}

		}

		if(isset($_GET['group'])){

			$group = $_GET['group'];
		}else{
			$group = "";
		}

		

		if ($_GET['request'] == 'subprotocol_ipv4')
		{
			echo json_encode(getSubProtocolIpv4($connection, $date_begin, $date_end, $group) );
		}
		elseif($_GET['request'] == 'protocol_ethernet')
		{
			echo json_encode(getProtocolEthernet($connection, $date_begin, $date_end, $group) );
		}
		elseif ($_GET['request'] == 'bandwidth') 
		{
			echo json_encode(getBandwidth($connection, $date_begin, $date_end) );
		}
		elseif ($_GET['request'] == 'total_bandwidth') 
		{
			echo json_encode(getTotalBandwidth($connection, $date_begin, $date_end) );
		}
		elseif ($_GET['request'] == 'packet_loss') 
		{
			echo json_encode(getPacketLoss($connection, $date_begin, $date_end) );
		}

	}
	

	

	



	

} catch ( Exception $e ) {
	echo "Connection à MySQL impossible : ", $e->getMessage();
	die();
}

?>