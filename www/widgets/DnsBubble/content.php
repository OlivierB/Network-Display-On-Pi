<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>

<script type="text/javascript">
$(function(){
	var display = new DnsDisplayerCanvas("<?= $id ?>", <?= $params['font_size'] ?>, <?= $params['draw_bubble'] ?>);
	display.connect(dispatcher, 'dns');
});
</script>

