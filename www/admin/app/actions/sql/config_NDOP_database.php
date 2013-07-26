<?php
/**
 * Called by the config page to save the NDOP database info to the database file.
 **/
if(isset($_POST['ndop_database_address']) 
	&& isset($_POST['ndop_database_port']) 
	&& isset($_POST['ndop_database_login']) 
	&& isset($_POST['ndop_database_password']))
{
	
	$sql = "INSERT INTO  `server_information` (`id` ,`name` ,`ip` ,`port`, `login`, `password`)
		VALUES (3 ,  'ndop_database',  '".
			$_POST['ndop_database_address']."', '".
			$_POST['ndop_database_port']."', '".
			$_POST['ndop_database_login']."', '".
			$_POST['ndop_database_password']."' )  
			ON DUPLICATE KEY UPDATE `port`=VALUES(`port`), `ip`=VALUES(`ip`), `login`=VALUES(`login`), `password`=VALUES(`password`);";
// echo $sql;
	$this['database']->exec($sql);
	$this->redirect('config');
	
}else{
	echo 45;
}



