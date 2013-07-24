<?php
require "app/tools/image.php";
	$this['layout_page'] = 'active';

	$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);


	$select_modules = "SELECT * FROM  `module` ORDER BY name";

	$results = $this['database']->query($select_modules);
	$modules = $results->fetchAll(PDO::FETCH_ASSOC);

	$select_layout = "SELECT id, name FROM  `layout` JOIN `module` ON id_module = id";

	$results = $this['database']->query($select_layout);
	$pages = $results->fetchAll(PDO::FETCH_ASSOC);

	$nb_page =  count($pages);
	
	Thumbnail::check_thumbnails_existence($modules, $this['database']);