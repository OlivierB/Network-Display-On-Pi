<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new BandwidthChartWebsocket("<?= $id ?>", "<?= $params['style_line'] ?>");
	chart.connect(dispatcher, 'bandwidth');
});
</script>