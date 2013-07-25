<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new BandwidthTextAjax("<?= $id ?>", <?= $params['font_size'] ?>);
	chart.connect(App.webServerAddress, "pages/sql_request.php?request=total_bandwidth&day_before_begin=<?= $params['nb_day'] ?>&day_before_end=0", <?= $params['refresh_time'] ?>);	
});
</script>