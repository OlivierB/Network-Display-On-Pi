<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new BandwidthChartAjax("<?= $id ?>");
	chart.connect(App.webServerAddress, "pages/sql_request.php?request=bandwidth&day_before_begin=<?= $params['nb_day'] ?>&day_before_end=0", <?= $params['refresh_time'] ?>);	
});
</script>