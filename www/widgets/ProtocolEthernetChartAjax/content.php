<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new StackedColumnChartAjax("<?= $id ?>", "<?= $params['title'] ?>");
	chart.connect(App.webServerAddress, "/pages/sql_request.php?request=protocol_ethernet&day_before_begin=<?= $params['nb_day'] ?>&day_before_end=0&group=<?= $params['group_by'] ?>", <?= $params['refresh_time'] ?>);
});
</script>