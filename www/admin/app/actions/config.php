<?php
$this['config_page'] = 'active';

// will be true if some connection infomations exist in the ndop.config.ini file.
$database_info = false;
// will be true if the connection to the database works
$database_connection = false;
$database_login = '';
$database_password = '';
$database_address='';
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


		try{
			// if we can't reach the database, we try to create it
	        $db_tmp = new PDO("mysql:host=".NDOP::$app['database_address'].";", NDOP::$app['database_login'], NDOP::$app['database_password'],array(PDO::ATTR_TIMEOUT => "1"));
	        
	        $request = file_get_contents("../BDD/NDOP_GUI.sql");
			$db_tmp->exec($request);

			$dbh = new PDO("mysql:host=".NDOP::$app['database_address'].";dbname=NDOP_GUI", NDOP::$app['database_login'], NDOP::$app['database_password'],array(PDO::ATTR_TIMEOUT => "1"));

			Atomik::set('database', $dbh);
			$database_connection = true;
			$database_state = 'alert-success';
		}catch(PDOException $e)
	    {
	    	// if an exception occured, it means we can't reach mysql or the user can't create the database
	        $database_state = 'alert-block';
	    }
		
	}
	
}else{
	// no informations in the ndop.conf.php file
	$database_state = 'alert-error';
	
	$database_address = '';
	$database_login = '';
	$database_password = '';
}

// *******************************************************

// will be true if some connection infomations exist in the database.
$ndop_database_info = false;
// will be true if the connection to the server works
$ndop_database_connection = false;

if($database_connection){
	$sql = "SELECT * FROM server_information WHERE  `name` =  'ndop_database'";
	$results = $this['database']->query($sql);
	$data_server_infos = $results->fetch();

	if(isset($data_server_infos['ip']) && $data_server_infos['port']){
		$ndop_database_address = $data_server_infos['ip'];
		$ndop_database_port = $data_server_infos['port'];
		$ndop_database_login = $data_server_infos['login'];
		$ndop_database_password = $data_server_infos['password'];
		$ndop_database_info = true;

		try{
			$db_tmp =  new PDO("mysql:host=".$ndop_database_address.';port='.$ndop_database_port.";", $ndop_database_login, $ndop_database_password,array(PDO::ATTR_TIMEOUT => "1"));
		
			$ndop_database_connection = true;
			$ndop_database_state = 'alert-success';
		}catch(PDOException $e)
	    {
	    	$ndop_database_state = 'alert-block';
	    }

		
		


	}else{
		$ndop_database_state = 'alert-error';
		$ndop_database_address = '';
		$ndop_database_port = '';
		$ndop_database_login = '';
		$ndop_database_password = '';
	}
	
}else{
	$ndop_database_state = 'alert-error';
	$ndop_database_address = '';
	$ndop_database_port = '';
	$ndop_database_login = '';
	$ndop_database_password = '';
}



// ************************************************



// check the NDOP data server connection

// will be true if some connection infomations exist in the database.
$data_server_info = false;
// will be true if the connection to the server works
$data_server_connection = false;

if($database_connection){
	$sql = "SELECT * FROM server_information WHERE  `name` =  'data_server'";
	$results = $this['database']->query($sql);
	$data_server_infos = $results->fetch();

	if(isset($data_server_infos['ip']) && $data_server_infos['port']){
		$data_server_address = $data_server_infos['ip'];
		$data_server_port = $data_server_infos['port'];
		$data_server_info = true;

		$url = 'http://'.$data_server_address.':'.$data_server_port.'/online';
		$ctx = stream_context_create(array('http'=>array('timeout' => 2 )));
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
	
}else{
	$data_server_state = 'alert-error';
	$data_server_address = '';
	$data_server_port = '';
}

// check the freegeoip server connection

// will be true if some connection infomations exist in the database.
$freegeoip_server_info = false;
// will be true if the connection to the server works
$freegeoip_server_connection = false;

if($database_connection){
	$sql = "SELECT * FROM server_information WHERE  `name` =  'freegeoip_server'";
	$results = $this['database']->query($sql);
	$freegeoip_server_infos = $results->fetch();

	if(isset($freegeoip_server_infos['ip']) && isset($freegeoip_server_infos['port'])){
		$freegeoip_server_address = $freegeoip_server_infos['ip'];
		$freegeoip_server_port = $freegeoip_server_infos['port'];
		$freegeoip_server_info = true;

		$url = 'http://'.$freegeoip_server_address.':'.$freegeoip_server_port.'/csv/255.255.255.255';
		$ctx = stream_context_create(array('http'=>array('timeout' => 2 )));
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
	
}else{
	$freegeoip_server_state = 'alert-error';
	$freegeoip_server_address = '';
	$freegeoip_server_port = '';
}
