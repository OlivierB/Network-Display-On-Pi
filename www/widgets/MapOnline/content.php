<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>

<script type="text/javascript">
	var IpMap = new IpLocationMapOnline("<?= $id ?>");
	IpMap.connect(dispatcher, 'iplist');
</script>

