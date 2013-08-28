<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>

<script type="text/javascript">
$(function(){
	var IpMap = new IpLocationMapOffline("<?= $id ?>", <?= $params['dither'] ?>, <?= $params['opacity'] ?>, "<?= $params['freegeoip_address'] ?>");
	IpMap.connect(dispatcher, 'iplist');
});
</script>

