<?php
	Atomik::disableLayout();
	$this['database']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	if(isset($_POST['interval']) && isset($_POST['update_check_interval'])){


		$sql = 'UPDATE `slide_configuration` SET `interval`=:interval, `auto_start`=:auto_start, `pause_on_hover`=:pause_on_hover, `update_check_interval`=:update_check_interval, `background_color`=:background_color;';

		$prep_insert = $this['database']->prepare($sql);

		$prep_insert->execute(array(
				'interval' 				=> $_POST['interval'],
				'auto_start' 			=> isset($_POST['auto_start']),
				'pause_on_hover' 		=> isset($_POST['pause_on_hover']),
				'update_check_interval' => $_POST['update_check_interval'],
				'background_color'		=> $_POST['background_color']
			));		
	}
	
	$this->redirect('slide_config');