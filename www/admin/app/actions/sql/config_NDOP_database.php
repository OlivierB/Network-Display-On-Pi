<?php
/**
 * Called by the config page to save the NDOP database info to the database file.
 **/
if(isset($_POST['ndop_database_address'])  
	&& isset($_POST['ndop_database_login']) 
	&& isset($_POST['ndop_database_password']))
{
	if($_POST['ndop_database_port'] == ''){
			$_POST['ndop_database_port'] = '3306';
	}
	// $ndop_database_name = $data_server_infos['database_name'];
	if($_POST['ndop_database_name'] == ''){
			$_POST['ndop_database_name'] = 'NDOP';
	}
	
	$sql = "INSERT INTO  `server_information` (`id` ,`name` ,`ip` ,`port`, `login`, `password`, `database_name`)
		VALUES (3 ,  'ndop_database',  '".
			$_POST['ndop_database_address']."', '".
			$_POST['ndop_database_port']."', '".
			$_POST['ndop_database_login']."', '".
			$_POST['ndop_database_password']."', '".
			$_POST['ndop_database_name']."' )  
			ON DUPLICATE KEY UPDATE `port`=VALUES(`port`), `ip`=VALUES(`ip`), `login`=VALUES(`login`), `password`=VALUES(`password`), `database_name`=VALUES(`database_name`);";

	$this['database']->exec($sql);
	$this->redirect('config');
	
}



