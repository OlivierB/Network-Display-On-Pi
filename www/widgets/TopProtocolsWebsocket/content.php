<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>"></div>



<script type="text/javascript">
$(function(){
	var chart = new TopProtocolsWebsocket("<?= $id ?>");
	chart.connect(dispatcher, 'protocols');
});
</script>