<?php
	$this['layout_page'] = 'active';

	$sql = "SELECT * FROM  `modules` ORDER BY name";

	$results = $this['database']->query($sql);
	$modules = $results->fetchAll(PDO::FETCH_ASSOC);

	$sql = "SELECT id, folder_name, name FROM  `layout` JOIN modules ON id_module = id";

	$results = $this['database']->query($sql);
	$pages = $results->fetchAll(PDO::FETCH_ASSOC);