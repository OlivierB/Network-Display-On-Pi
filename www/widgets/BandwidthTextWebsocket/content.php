<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
	var chart = new BandwidthTextWebsocket("<?= $id ?>", <?= $params['font_size'] ?>);
	chart.connect(dispatcher, 'bandwidth');
</script>