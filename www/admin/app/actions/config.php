<?php
$this['config_page'] = 'active';

require_once '../ndop.conf.php';

if( NDOP::$app['database_address'] != null && 
	NDOP::$app['database_login'] != null && 
	NDOP::$app['database_password'] != null)
{
	$database_info = true;

	if($this['db']){
		$database_connection = true;
		$database_state = 'alert-success';
	}else{
		$database_state = 'alert-block';
	}
	
}else{
	$database_state = 'alert-error';
}
