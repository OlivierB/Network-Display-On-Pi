<?php
	$this['layout_page'] = 'active';

	$sql = "SELECT * FROM  `module` ORDER BY name";

	$results = $this['database']->query($sql);
	$modules = $results->fetchAll(PDO::FETCH_ASSOC);

	$sql = "SELECT id, folder_name, name FROM  `layout` JOIN `module` ON id_module = id";

	$results = $this['database']->query($sql);
	$pages = $results->fetchAll(PDO::FETCH_ASSOC);

	$nb_page =  count($pages);
	// if($nb_page < 0)
	// 	$nb_page = 0;