<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var protocolChart = new BarChartWebsocket('<?= $id ?>', 'ports',  "Ports use");
	protocolChart.connect(dispatcher, 'protocols');
});
</script>