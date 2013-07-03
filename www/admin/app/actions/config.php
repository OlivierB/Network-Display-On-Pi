<?php
$this['config_page'] = 'active';

require_once '../ndop.conf.php';

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
		$database_connection = false;
		$database_state = 'alert-block';
	}
	
}else{
	// no informations in the ndop.conf.php file
	$database_state = 'alert-error';
	$database_info = false;
	$database_connection = false;

	$database_address = '';
	$database_login = '';
	$database_password = '';

}
