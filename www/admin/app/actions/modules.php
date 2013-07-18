<?php

	$this['modules_page'] = 'active';

	if(!isset($this['request.folder'])){
		$sql = "SELECT * FROM  `module` ORDER BY name";

		$results = $this['database']->query($sql);
		$modules = $results->fetchAll(PDO::FETCH_ASSOC);
	} else {
		Atomik::setView('module');

		$sql = "SELECT *, `module`.`name` as module_name FROM `module` WHERE `folder_name`='".$this['request.folder']."'";
		$results = $this['database']->query($sql);
		$module = $results->fetch(PDO::FETCH_ASSOC);

		// print_r($module);

		if(!isset($module)){
			$this->trigger404();
		}
	}

	

