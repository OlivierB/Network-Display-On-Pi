<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
	var protocolChart = new BarChartWebsocket('<?= $id ?>', 'ethernet',  "Division of ethernet traffic");
	protocolChart.connect(dispatcher, 'protocols');
</script>