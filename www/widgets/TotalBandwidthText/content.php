<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
	var chart = new TotalBandwidthText("<?= $id ?>");
	chart.connect(App.webServerAddress, "/pages/sql_request.php?request=total_bandwidth&day_before_begin=<?= $params['nb_day'] ?>&day_before_end=0", <?= $params['refresh_time'] ?>);	
</script>