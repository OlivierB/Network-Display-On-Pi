<?php
$this['config_page'] = 'active';

require_once '../ndop.conf.php';

// will be true if some connection infomations exist in the ndop.config.ini file.
$database_info = false;
// will be true if the connection to the database works
$database_connection = false;

// check the database connection
if( isset(NDOP::$app['database_address']) && 
	isset(NDOP::$app['database_login']) && 
	isset(NDOP::$app['database_password']) )
{
	// at this point we know the databases informations exists
	$database_info = true;
	$database_address = NDOP::$app['database_address'];
	$database_login = NDOP::$app['database_login'];
	$database_password = NDOP::$app['database_password'];

	// we need to check if the connection went well
	if($this['database']){
		$database_connection = true;
		$database_state = 'alert-success';
	}else{
		$database_state = 'alert-block';
	}
	
}else{
	// no informations in the ndop.conf.php file
	$database_state = 'alert-error';
	
	$database_address = '';
	$database_login = '';
	$database_password = '';
}


// check the NDOP data server connection

// will be true if some connection infomations exist in the database.
$data_server_info = false;
// will be true if the connection to the server works
$data_server_connection = false;

if($database_connection){
	$sql = "SELECT * FROM server_informations WHERE  `name` =  'data_server'";
	$results = $this['database']->query($sql);
	$data_server_infos = $results->fetch();

	if(isset($data_server_infos['ip']) && $data_server_infos['port']){
		$data_server_address = $data_server_infos['ip'];
		$data_server_port = $data_server_infos['port'];
		$data_server_info = true;

		$url = 'http://'.$data_server_address.':'.$data_server_port.'/online';
		$ctx = stream_context_create(array('http'=>array('timeout' => 5 )));
		$content = @file_get_contents($url, false, $ctx);
		if($content === 'ndop'){
			$data_server_connection = true;
			$data_server_state = 'alert-success';
		}else{
			$data_server_state = 'alert-block';
		}
		
		


	}else{
		$data_server_state = 'alert-error';
		$data_server_address = '';
		$data_server_port = '';
	}
	
}

// check the freegeoip server connection

// will be true if some connection infomations exist in the database.
$freegeoip_server_info = false;
// will be true if the connection to the server works
$freegeoip_server_connection = false;

if($database_connection){
	$sql = "SELECT * FROM server_informations WHERE  `name` =  'freegeoip_server'";
	$results = $this['database']->query($sql);
	$freegeoip_server_infos = $results->fetch();

	if(isset($freegeoip_server_infos['ip']) && isset($freegeoip_server_infos['port'])){
		$freegeoip_server_address = $freegeoip_server_infos['ip'];
		$freegeoip_server_port = $freegeoip_server_infos['port'];
		$freegeoip_server_info = true;

		$url = 'http://'.$freegeoip_server_address.':'.$freegeoip_server_port.'/csv/255.255.255.255';
		$ctx = stream_context_create(array('http'=>array('timeout' => 5 )));
		$content = @file_get_contents($url, false, $ctx);

		if(explode(',', $content)[0] === '"255.255.255.255"'){
			$freegeoip_server_connection = true;
			$freegeoip_server_state = 'alert-success';
		}else{
			$freegeoip_server_state = 'alert-block';
		}
		
	}else{
		$freegeoip_server_state = 'alert-error';
		$freegeoip_server_address = '';
		$freegeoip_server_port = '';
	}
	
}
