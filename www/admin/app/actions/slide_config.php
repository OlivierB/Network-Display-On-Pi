<?php
$this['slide_config_page'] = 'active';

$sql = "SELECT * FROM  `slide_configuration`;";

$results = $this['database']->query($sql);
$conf = $results->fetch(PDO::FETCH_ASSOC);

if(isset($conf['interval'])){
	$interval = $conf['interval'];
}else{
	$interval = 15000;
}

if(isset($conf['auto_start'])){
	if($conf['auto_start']){
		$auto_start = 'checked';
	}else{
		$auto_start = '';
	}
}else{
	$auto_start = '';
}

if(isset($conf['pause_on_hover'])){
	if($conf['pause_on_hover']){
		$pause_on_hover = 'checked';
	}else{
		$pause_on_hover = '';
	}
}else{
	$pause_on_hover = '';
}

if(isset($conf['update_check_interval'])){
	$update_check_interval = $conf['update_check_interval'];
}else{
	$update_check_interval = 900000;
}