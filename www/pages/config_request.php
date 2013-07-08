<?php

function appConfig(){
	require_once '../ndop.conf.php';
	$obj = array();

	NDOP::$app['db'] = new PDO("mysql:host=192.168.1.144;dbname=NDOP_GUI", 'ndop', 'ndop');


	$sql = "SELECT * FROM  `server_informations` WHERE name='data_server' ;";
	$results = NDOP::$app['db']->query($sql);
	$address = $results->fetch(PDO::FETCH_ASSOC);

	if(isset($address['ip']) && isset($address['port'])){
		$obj['NDOPAddress'] = 'ws://'.$address['ip'].':'.$address['port'];
	}

	$sql = "SELECT * FROM  `server_informations` WHERE name='freegeoip_server' ;";
	$results = NDOP::$app['db']->query($sql);
	$address = $results->fetch(PDO::FETCH_ASSOC);

	if(isset($address['ip']) && isset($address['port'])){
		$obj['freeGeoIpAdress'] = $address['ip'].':'.$address['port'];
	}

	$obj['webServerAddress'] = $_SERVER['SERVER_ADDR'];

	$app = array();
	// $app['App'] = $obj;

	return 'var App = '.json_encode($obj).';';
}
