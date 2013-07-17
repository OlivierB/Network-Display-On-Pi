<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
	var chart = new BandwidthChartWebsocket("<?= $id ?>");
	chart.connect(dispatcher, 'bandwidth');
</script>