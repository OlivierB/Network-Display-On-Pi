<?php
	Atomik::disableLayout();
	$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	

		$sql = "UPDATE `slide_configuration` SET update_id=update_id+1;";
		$this['database']->exec($sql);
	
	
	$this->redirect('slide_config');