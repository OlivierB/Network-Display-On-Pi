<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new BandwidthChartAjax("<?= $id ?>", "<?= $params['style_line'] ?>");
	chart.connect(App.webServerAddress, "app/sql_request.php?request=bandwidth&day_before_begin=<?= $params['nb_day'] ?>&day_before_end=0&group=<?= $params['group_by'] ?>", <?= $params['refresh_time'] ?>);	
});
</script>