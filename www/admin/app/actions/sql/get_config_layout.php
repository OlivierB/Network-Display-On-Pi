<?php

	Atomik::disableLayout();

	$sql = "SELECT * FROM  `layout` ORDER BY `page`";

	$results = $this['database']->query($sql);
	$layout = $results->fetchAll(PDO::FETCH_ASSOC);
	echo json_encode($layout);