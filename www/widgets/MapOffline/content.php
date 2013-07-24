<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>

<script type="text/javascript">
$(function(){
	var IpMap = new IpLocationMapOffline("<?= $id ?>", <?= $params['dither'] ?>, <?= $params['opacity'] ?>);
	IpMap.connect(dispatcher, 'iplist');
});
</script>

