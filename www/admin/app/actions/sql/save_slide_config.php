<?php
	Atomik::disableLayout();
	$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	var_dump($_POST);
	if(isset($_POST['interval']) ){

		$sql = "DELETE FROM `slide_configuration`;";
		$this['database']->exec($sql);

		$sql = 'INSERT INTO `slide_configuration` (`interval`, `auto_start`, `pause_on_hover`) VALUES (:interval, :auto_start, :pause_on_hover);';

		$prep_insert = $this['database']->prepare($sql);

		$prep_insert->execute(array(
				'interval' => $_POST['interval'],
				'auto_start' => isset($_POST['auto_start']),
				'pause_on_hover' => isset($_POST['pause_on_hover'])
			));
	}
	
	$this->redirect('slide_config');