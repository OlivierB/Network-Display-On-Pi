<?php
$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$select_widget = "SELECT * FROM `widget`";
$prep_select_widget = $this['database']->prepare($select_widget);
$prep_select_widget->execute();
$widgets = $prep_select_widget->fetchAll();

if($this['request.module'] != ''){
	// echo $this['request.module'];
	$sql = "SELECT * ,  `module`.`name` AS module_name,  `module`.`description` AS module_description FROM  `module` LEFT OUTER JOIN  `module_composition_widget` ON  `module`.`id` =  `module_composition_widget`.`id_module` LEFT OUTER JOIN  `widget` ON  `module_composition_widget`.`id_widget` =  `widget`.`id` LEFT OUTER JOIN  `widget_parameter_design` ON  `widget`.`id` =  `widget_parameter_design`.`id_widget` LEFT OUTER JOIN  `widget_parameter_value` ON  `widget_parameter_design`.`id` =  `widget_parameter_value`.`id_param` LEFT OUTER JOIN  `widget_parameter_set` ON  `widget_parameter_set`.`id` =  `module_composition_widget`.`id_widget_parameter_set` WHERE  `module`.`id` = :id_module";
	$prep_select_id_module = $this['database']->prepare($sql);

	$prep_select_id_module->execute(array(
		'id_module' => $this['request.module']
		));
	$module = $prep_select_id_module->fetch(PDO::FETCH_ASSOC);
	// print_r($module);
}else{
	// echo 'default';
	$module = array();
	$module['module_name'] = '';
	$module['module_description'] = '';
}