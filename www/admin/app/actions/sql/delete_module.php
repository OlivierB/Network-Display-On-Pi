<?php
	if(isset($_POST['id'])){
		$delete_module = "DELETE FROM `module` WHERE `id` = :id_module";
		$prep_delete_module = $this['database']->prepare($delete_module);

		$prep_delete_module->execute(array('id_module' => $_POST['id']));
	}