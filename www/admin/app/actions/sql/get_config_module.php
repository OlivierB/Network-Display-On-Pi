<?php
Atomik::disableLayout();
if(isset($_GET['id'])){
	$select_module = "SELECT *, `widget`.`name` as `widget_name` FROM  `module` LEFT OUTER JOIN  `module_composition_widget` ON  `module`.`id` =  `module_composition_widget`.`id_module` LEFT OUTER JOIN  `widget` ON  `module_composition_widget`.`id_widget` =  `widget`.`id` WHERE  `module`.`id` = :id_module ORDER BY y, x";
	$prep_select_module = $this['database']->prepare($select_module);
	$prep_select_module->execute(array(
		'id_module' => $_GET['id']
		));
	$widgets = $prep_select_module->fetchAll(PDO::FETCH_ASSOC);

	echo json_encode($widgets);
}