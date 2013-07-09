<?php
$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$insert_widget = "INSERT INTO `widget` (`folder_name`, `name`, `description`, `updated`) VALUES (:folder_name, :name, :description, TRUE) ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description), updated=TRUE;";
$prep_insert_widget = $this['database']->prepare($insert_widget);


$select_id_widget = "SELECT `id` FROM `widget` WHERE `folder_name` = :folder_name;";
$prep_select_id_widget = $this['database']->prepare($select_id_widget);


$insert_default_set = "INSERT IGNORE INTO `widget_parameter_set` (`name`, `id_widget`) VALUES (:name, :id_widget);";
$prep_insert_default_set = $this['database']->prepare($insert_default_set);


$select_id_set = "SELECT `id` FROM `widget_parameter_set` WHERE `id_widget` = :id_widget AND `name` = :name ;";
$prep_select_id_set = $this['database']->prepare($select_id_set);


$insert_param_widget = "INSERT INTO `widget_parameter_design` (`id_widget`, `name`, `type`, `description`, `updated`) VALUES (:id_widget, :name, :type, :description, TRUE) ON DUPLICATE KEY UPDATE description=VALUES(description), updated=TRUE, type=VALUES(type) ;";
$prep_insert_param_widget = $this['database']->prepare($insert_param_widget);


$select_id_param = "SELECT `id` FROM `widget_parameter_design` WHERE `name` = :name AND `id_widget` = :id_widget ;";
$prep_select_id_param = $this['database']->prepare($select_id_param);


$insert_default_param = "INSERT  INTO `widget_parameter_value` (`id_set`, `id_param`, `value`) VALUES (:id_set, :id_param, :value);";
$prep_insert_default_param = $this['database']->prepare($insert_default_param);

$sql = 'UPDATE `widget` SET `updated`=FALSE;';
$this['database']->exec($sql);

$dir = opendir('../widgets') or die('Erreur');
while($entry = @readdir($dir)) {
	if($entry != '.' && $entry != '..'){

		$ini_data_widget = @parse_ini_file('../widgets/'.$entry.'/widget.ini',true);
		if($ini_data_widget){
			
			if(isset($ini_data_widget['INFOS']) && 
				isset($ini_data_widget['INFOS']['name']) && 
				isset($ini_data_widget['INFOS']['description']))
			{
				
				// insert the new widget (or update)
				$prep_insert_widget->execute(array( 
					'folder_name' 	=> $entry, 
					'name' 			=> $ini_data_widget['INFOS']['name'],
					'description' 	=> $ini_data_widget['INFOS']['description']
				));
				
				// get the id of the current widget
				$prep_select_id_widget->execute(array(
					'folder_name' => $entry
				));
				$id_widget = $prep_select_id_widget->fetch(PDO::FETCH_ASSOC)['id'];

				// insert the default set of paraneters for this widget
				$prep_insert_default_set->execute(array(
					'name' 		=> 'default',
					'id_widget' => $id_widget
				));

				// get the id of the current set
				$prep_select_id_set->execute(array(
					'id_widget' => $id_widget,
					'name' 		=> 'default'
				));
				$id_set = $prep_select_id_set->fetch(PDO::FETCH_ASSOC)['id'];
				

				$ini_data_params = @parse_ini_file('../widgets/'.$entry.'/params.ini',true);
				if($ini_data_params){
					foreach ($ini_data_params as $variable_name => $var) {
						
						// insert the design of each parameters for the current widget
						$prep_insert_param_widget->execute(array(
							'id_widget' 	=> $id_widget,
							'name' 			=> $variable_name,
							'type' 			=> $var['type'],
							'description'	=> $var['description']
						));

						// get the id of the current parameter
						$prep_select_id_param->execute(array(
							'name' 		=> $variable_name,
							'id_widget'	=> $id_widget,
						));
						$id_param = $prep_select_id_param->fetch(PDO::FETCH_ASSOC)['id'];
						
						echo $id_param.'<br>';
						// insert the default value
						$prep_insert_default_param->execute(array(
							'id_set' 		=> $id_set,
							'id_param' 		=> $id_param,
							'value' 		=> $var['default']
						));
					}
				}
			}	
		}

			
	}
}
closedir($dir);

$sql = "DELETE FROM `widget` WHERE `updated`=FALSE";
$this['database']->exec($sql);

// $this->redirect('widgets');
