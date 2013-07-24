<?php
require "app/tools/image.php";

	$this['modules_page'] = 'active';

	
	$sql = "SELECT * FROM  `module` ORDER BY name";

	$results = $this['database']->query($sql);
	$modules = $results->fetchAll(PDO::FETCH_ASSOC);
	

	Thumbnail::check_thumbnails_existence($modules, $this['database']);