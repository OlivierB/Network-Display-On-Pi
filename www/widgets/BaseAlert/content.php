<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>


<script type="text/javascript">
	var base = new BaseAlert('<?= $id ?>');
	base.connect(App.webServerAddress, "/base/perso/base_stat_alerts.php?caller=&sort_order=last_d", <?= $params['refresh_time'] ?>);
</script>