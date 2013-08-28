<?php
/**
 * Called by the config page to save the database id to the ndop.conf.ini file.
 **/

if($file = @fopen('../ndop.conf.ini', 'w')){
	if( isset($_POST['database_address']) && 
		isset($_POST['database_login']) && 
		isset($_POST['database_password']) &&
		isset($_POST['database_name']))
	{
		if($_POST['database_port'] == ''){
			$_POST['database_port'] = '3306';
		}
		if($_POST['database_name'] == ''){
			$_POST['database_name'] = 'NDOP_GUI';
		}
		$str = 'database_address='.$_POST['database_address'].PHP_EOL.
				'database_port='.$_POST['database_port'].PHP_EOL.
				'database_login='.$_POST['database_login'].PHP_EOL.
				'database_password='.$_POST['database_password'].PHP_EOL.
				'database_name='.$_POST['database_name'];

		fwrite($file, $str);

		$this->redirect('config');
	}else{
		echo 'An error occured';
	}
		
}else{
	echo 'Cannot write in the file <strong>ndop.conf.ini</strong>. The owner of the NDOP www/ folder need to be www-data (or the user who run the web server program).';
}


