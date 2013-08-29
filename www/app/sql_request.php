<?php
require_once "NDOP.php";
NDOP::init('../ndop.conf.ini');

require 'sql_function.php';
try {
	// we retrieve the data we need to connect to the NDOP database
	$select_ndop_database = "SELECT * FROM `server_information` WHERE `name` = 'ndop_database'";
	$ndop_db_information = NDOP::$app['db']->query($select_ndop_database)->fetch();

	if(isset($ndop_db_information['ip']) 
		&& isset($ndop_db_information['port'])
		&& isset($ndop_db_information['login'])
		&& isset($ndop_db_information['password'])
		&& isset($ndop_db_information['database_name'])
	)
	{

		// we use these data to connect
		$dns = 'mysql:host='.$ndop_db_information['ip'].';port='.$ndop_db_information['port'].';dbname='.$ndop_db_information['database_name'];
		$user = $ndop_db_information['login'];
		$password = $ndop_db_information['password'];
		$connection = new PDO( $dns, $user, $password, array(PDO::ATTR_TIMEOUT => "1") );


		if(isset($_GET['request'])){
			if($_GET['request'] == 'update_id'){
				$sql = "SELECT `update_id`  FROM  `slide_configuration` ;";
				$results = NDOP::$app['db']->query($sql);
				$update_id = $results->fetch(PDO::FETCH_ASSOC);
				echo json_encode($update_id);
			}else{

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
					echo json_encode(getBandwidth($connection, $date_begin, $date_end, $group) );
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

		}
	}
} catch ( Exception $e ) {
	echo $e->getMessage();
	die();
}