<?php

	$this['widgets_page'] = 'active';

	// if(!isset($this['request.folder'])){
		$sql = "SELECT * FROM  `widget` ORDER BY name";

		$results = $this['database']->query($sql);
		$widgets = $results->fetchAll(PDO::FETCH_ASSOC);
	// } else {
	// 	Atomik::setView('module');

	// 	$sql = "SELECT *, `widgets`.`name` as widget_name, `widgets_parameters`.`name` as param_name FROM `widgets` LEFT OUTER JOIN `widgets_parameters`
	// 		on `widgets`.`id` = `id_widgets` WHERE `folder_name`='".$this['request.folder']."'";
	// 	$results = $this['database']->query($sql);
	// 	$module = $results->fetch(PDO::FETCH_ASSOC);

	// 	// print_r($module);

	// 	if(!isset($module)){
	// 		$this->trigger404();
	// 	}
	// }

	

