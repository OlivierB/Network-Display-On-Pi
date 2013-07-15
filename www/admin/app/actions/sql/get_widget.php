<?php
Atomik::disableLayout();
if(isset($_GET['id'])){
	$select_widget = "SELECT *, `widget`.`name` as `widget_name`, `widget_parameter_set`.`id` as `set_id`, `widget_parameter_set`.`name` as `set_name` FROM  `widget` LEFT OUTER JOIN  `widget_parameter_set` ON  `widget`.`id` =  `widget_parameter_set`.`id_widget` WHERE  `widget`.`id` = :id_widget;";
	$prep_select_widget = $this['database']->prepare($select_widget);
	$prep_select_widget->execute(array(
		'id_widget' => $_GET['id']
		));
	$widget = $prep_select_widget->fetchAll(PDO::FETCH_ASSOC);

	echo json_encode($widget);
}