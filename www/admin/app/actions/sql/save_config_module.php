<?php
require "app/tools/image.php";

	Atomik::disableLayout();
	$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


	$insert_module = 'INSERT INTO `module` (`id` ,`name` ,`description`)VALUES (:id,  :name,  :description) ON DUPLICATE KEY UPDATE `name`=VALUES(name), `description`=VALUES(description);';
	$prep_insert_module = $this['database']->prepare($insert_module);

	$suppr_composition = "DELETE FROM `module_composition_widget` WHERE `id_module` = :id_module;";
	$prep_suppr_composition = $this['database']->prepare($suppr_composition);

	$insert_widget_composition = "INSERT INTO `module_composition_widget` (`id`, `id_module`, `id_widget`, `x`, `y`, `width`, `height`, `id_widget_parameter_set`) VALUES (NULL, :id_module, :id_widget, :x, :y, :width, :height, :id_widget_parameter_set);";
	$prep_insert_widget_composition = $this['database']->prepare($insert_widget_composition);




	if( isset($_POST['id']) ){
		$id = $_POST['id'];
	}else{
		$id = NULL;
	}

	// insert or update the module
	$prep_insert_module->execute(array(
			'id' 			=> $id,
			'name'			=> $_POST['name'],
			'description'	=> $_POST['description']
		));

	if(!isset($_POST['id'])){
		$id = $this['database']->lastInsertId('id');
	}


	if(isset($_POST['id'])){
		// suppr the previous composition
		$prep_suppr_composition->execute(array(
			'id_module' => $_POST['id']
		));
	}



	if(isset($_POST['module'])){
		$module = json_decode($_POST['module'] );
		$thumbnail = new Thumbnail($id);
		// var_dump($module);
		foreach ($module as $index => $widget) {
			if($widget != NULL){
				// echo($widget->current_id_parameter_set);

				$prep_insert_widget_composition->execute(array(
					'id_module' => $_POST['id'],
					'id_widget' => $widget->db_id,
					'x' => $widget->x,
					'y' => $widget->y,
					'width' => $widget->width,
					'height' => $widget->height,
					'id_widget_parameter_set' => $widget->current_id_parameter_set,
				));
				$thumbnail->add_widget($widget->x, $widget->y, $widget->width, $widget->height, $widget->folder_name, $widget->db_id);
			}
		}
		$thumbnail->save();
	}
	
	echo $id;
