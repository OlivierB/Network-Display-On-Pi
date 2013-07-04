<?php


	$sql = 'UPDATE `modules` SET `updated`=FALSE;';
	$this['database']->exec($sql);

$dir = opendir('../modules') or die('Erreur');
while($entry = @readdir($dir)) {
	if($entry != '.' && $entry != '..'){
		// echo '<br>'.PHP_EOL.$entry.' ';
		// echo '../modules/'.$entry.'/module.ini<br>';
		$ini_data = @parse_ini_file('../modules/'.$entry.'/module.ini',true);
		if($ini_data){
			// echo $entry;
			// print_r($ini_data); 
			if(isset($ini_data['INFOS']) && 
				isset($ini_data['INFOS']['name']) && 
				isset($ini_data['INFOS']['description']))
			{
				$sql = "INSERT INTO `modules` (`id`, `folder_name`, `name`, `description`, `updated`) 
					VALUES (NULL, '".$entry."', '".$ini_data['INFOS']['name']."', '".
						$ini_data['INFOS']['description']."', TRUE) ON DUPLICATE KEY UPDATE ".
						"folder_name=VALUES(folder_name), description=VALUES(description), updated=TRUE;";

				$this['database']->exec($sql);
			}

			
		}
	}	
}
closedir($dir);

$sql = "DELETE FROM `modules` WHERE `updated`=FALSE";
$this['database']->exec($sql);

$this->redirect('modules');
