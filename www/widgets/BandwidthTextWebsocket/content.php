<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new BandwidthTextWebsocket("<?= $id ?>", <?= $params['font_size'] ?>);
	chart.connect(dispatcher, 'bandwidth');
});
</script>