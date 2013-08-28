<?php
/**
 * Called by the config page to save the data server infos to the database file.
 **/
if(isset($_POST['data_server_address']) && isset($_POST['data_server_port'])){
	if($_POST['data_server_port'] == ''){
			$_POST['data_server_port'] = '9005';
	}
	$sql = "INSERT INTO  `server_information` (`id` ,`name` ,`ip` ,`port`)
		VALUES (1 ,  'data_server',  '".
			$_POST['data_server_address']."',  '".
			$_POST['data_server_port']."')  
			ON DUPLICATE KEY UPDATE `port`=VALUES(`port`), `ip`=VALUES(`ip`);";
// echo $sql;
	$this['database']->exec($sql);
	$this->redirect('config');
	
}



