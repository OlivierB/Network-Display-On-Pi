<?php

	Atomik::disableLayout();

	$sql = "SELECT * FROM  `layout` ";

	$results = $this['database']->query($sql);
	$layout = $results->fetch(PDO::FETCH_ASSOC);
	echo json_encode($layout);