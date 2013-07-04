<?php

	$this['modules_page'] = 'active';

	$sql = "SELECT * FROM  `modules` ORDER BY name";

	$results = $this['database']->query($sql);
	$modules = $results->fetchAll(PDO::FETCH_ASSOC);

