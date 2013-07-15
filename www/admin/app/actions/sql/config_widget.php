<?php
$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

// if this is an update
if(isset($_POST['id_param_set'])){

	$select_parameter_set = "SELECT id_param FROM `widget_parameter_set` LEFT OUTER JOIN `widget_parameter_value` ON `widget_parameter_set`.`id` = `widget_parameter_value`.`id_set` WHERE `widget_parameter_set`.`id`=:id_set;";
	$prep_select_parameter_set = $this['database']->prepare($select_parameter_set);


	




	$id_set = $_POST['id_param_set'];

	$prep_select_parameter_set->execute(array(
		'id_set' => $_POST['id_param_set']
		));
	$params = $prep_select_parameter_set->fetchAll(PDO::FETCH_ASSOC);
	


// if this is a new set
}elseif(isset($_POST['id_widget']) ){

	$insert_new_set = "INSERT INTO `widget_parameter_set`(`id`, `name`, `id_widget`) VALUES (NULL, :name_set, :id_widget);";
	$prep_insert_new_set = $this['database']->prepare($insert_new_set);


	$select_parameter_module = "SELECT `widget_parameter_design`.`id` as `id_param` FROM `widget` LEFT OUTER JOIN `widget_parameter_design` ON `widget`.`id` = `widget_parameter_design`.`id_widget` WHERE `widget`.`id` = :id_widget;";
	$prep_select_parameter_module = $this['database']->prepare($select_parameter_module);



	$prep_insert_new_set->execute(array(
		'name_set' 	=> $_POST['name_set'],
		'id_widget' 	=> $_POST['id_widget']
		));
	$id_set = $this['database']->lastInsertId('id');

	$prep_select_parameter_module->execute(array(
		'id_widget' => $_POST['id_widget']
		));
	$params = $prep_select_parameter_module->fetchAll(PDO::FETCH_ASSOC);

	
}else{
	$this->trigger404();
}

$insert_parameter_value = "INSERT INTO `widget_parameter_value`(`id_set`, `id_param`, `value`) VALUES (:id_set, :id_param, :value) ON DUPLICATE KEY UPDATE `value`=VALUES(value);";
$prep_insert_parameter_value = $this['database']->prepare($insert_parameter_value);


foreach ($params as $index => $entry) {
		// var_dump($entry);
	$prep_insert_parameter_value->execute(array(
		'id_set' 	=> $id_set,
		'id_param' 	=> $entry['id_param'],
		'value' 	=> $_POST[$entry['id_param']]
		));
}
$this->redirect('widgets/editor/'.$_POST['id_widget']);