<?php
/**
 * Called by the config page to save the data server infos to the database file.
 **/
if(isset($_POST['freegeoip_server_address']) && isset($_POST['freegeoip_server_port'])){
	$sql = "INSERT INTO  `server_information` (`id` ,`name` ,`ip` ,`port`)
		VALUES (2 ,  'freegeoip_server',  '".
			$_POST['freegeoip_server_address']."',  '".
			$_POST['freegeoip_server_port']."')  
			ON DUPLICATE KEY UPDATE `port`=VALUES(`port`), `ip`=VALUES(`ip`);";
// echo $sql;
	$this['database']->exec($sql);
	$this->redirect('config');
	
}



