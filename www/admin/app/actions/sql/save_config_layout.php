<?php
	Atomik::disableLayout();
	

	$sql = 'DELETE FROM `layout`';

	$this['database']->exec($sql);

	if(isset($_POST['pages'])){

		foreach ($_POST['pages'] as $page => $module) {
			print_r(json_decode($module));
			$sql = "INSERT INTO `layout` (`page`, `id_module`) VALUES ('".$page."', '".$module."');";
			$this['database']->exec($sql);
		}
	}