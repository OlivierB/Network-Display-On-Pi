<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var protocolChart = new BarChartWebsocket('<?= $id ?>', 'ip',  "Division of IPV4 traffic");
	protocolChart.connect(dispatcher, 'protocols');
});
</script>