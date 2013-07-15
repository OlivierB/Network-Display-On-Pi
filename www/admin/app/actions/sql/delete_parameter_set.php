<?php
if(isset($_POST['id_set'])){
	$delete_set = "DELETE FROM `widget_parameter_set` WHERE `id` = :id_set;";
	$prep_delete_set = $this['database']->prepare($delete_set);

	$prep_delete_set->execute(array(
			'id_set' => $_POST['id_set']
		));

	$this->redirect('widgets/editor/'.$_POST['id_widget']);
}else{
	$this->trigger404();
}