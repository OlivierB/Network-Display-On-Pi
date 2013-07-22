<?php
$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$select_params = "SELECT `widget`.`name` as widget_name, `widget_parameter_set`.*, GROUP_CONCAT(`widget_parameter_value`.`value`) as param_values, GROUP_CONCAT( `widget_parameter_value`.`id_param` ) as param_ids, GROUP_CONCAT( `widget_parameter_design`.`name` ) as param_names,  GROUP_CONCAT( `widget_parameter_design`.`description` ) as param_descriptions FROM `widget` LEFT  OUTER JOIN `widget_parameter_set` ON `widget`.`id` = `widget_parameter_set`.`id_widget` LEFT OUTER JOIN `widget_parameter_value` ON `widget_parameter_set`.`id` = `widget_parameter_value`.`id_set` LEFT OUTER JOIN `widget_parameter_design` ON `widget_parameter_value`.`id_param` = `widget_parameter_design`.`id` WHERE `widget`.`id` = :id_widget GROUP BY `widget_parameter_set`.`id`;";
$prep_select_params = $this['database']->prepare($select_params);
$prep_select_params->execute(array(
		'id_widget' => $this['request.widget']
	));
$params = $prep_select_params->fetchAll(PDO::FETCH_ASSOC);

