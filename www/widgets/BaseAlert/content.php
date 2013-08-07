
<?php 
	if($file = fopen('./widgets/BaseAlert//base/base.conf.ini', 'w')){
	
		$str = 'address='.$params['address'].PHP_EOL.
				'port='.$params['port'].PHP_EOL.
				'login='.$params['login'].PHP_EOL.
				'name='.$params['name'].PHP_EOL.
				'type='.$params['type'].PHP_EOL.
				'password='.$params['password'];

		fwrite($file, $str);
	}else{
		echo 'Cannot write in the file <strong>base.conf.ini</strong>. The owner of the NDOP www/ folder need to be www-data (or the user who run the web server program).';
	}





 ?>
<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>


<script type="text/javascript">
$(function(){
	var base = new BaseAlert('<?= $id ?>', <?= $params['font_size'] ?>);
	base.connect(App.webServerAddress, "./widgets/BaseAlert/base/perso/base_stat_alerts.php?caller=&sort_order=last_d", <?= $params['refresh_time'] ?>);
});
</script>

<link rel="stylesheet" href="widgets/BaseAlert/style.css">