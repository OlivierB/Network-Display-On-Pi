<?php

	$this['widgets_page'] = 'active';

	$sql = "SELECT * FROM  `widget` ORDER BY name";

	$results = $this['database']->query($sql);
	$widgets = $results->fetchAll(PDO::FETCH_ASSOC);

	

