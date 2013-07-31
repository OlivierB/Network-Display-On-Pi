<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var canvas = new SummaryCanvas('<?= $id ?>');
	canvas.connect(App.webServerAddress, "./app/sql_request.php?request=total_bandwidth", <?= $params['refresh_time'] ?>);
});
</script>