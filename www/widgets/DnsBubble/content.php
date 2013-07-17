<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>

<script type="text/javascript">
	var display = new DnsDisplayerCanvas("<?= $id ?>");
	display.connect(dispatcher, 'dns');
</script>

