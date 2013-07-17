

<div class='rows server-stat-legend' id="<?= $id ?>">
	<h2>Server statistics</h2>

	<span id="<?= $id ?>-alert"></span>

	<div class='span4'>
		<div class='percent-chart-loader' id="<?= $id ?>proc" data-percent="0"><span>0</span></div>
		<h3>Processor load</h3>
	</div>

	
	<div class='span4'>
		<div class='percent-chart-loader' id="<?= $id ?>memory" data-percent="0"><span>0</span></div>
		<h3>Memory load</h3>
	</div>


	<div class='span4'>
		<div class='percent-chart-loader' id="<?= $id ?>swap" data-percent="0"><span>0</span></div>
		<h3>Swap load</h3>
	</div>
</div>

<script type="text/javascript">
	var serverStat = new ServerStat('<?= $id ?>');
	serverStat.add('<?= $id ?>proc', 'proc_load', <?= $params['speed'] ?>);
	serverStat.add('<?= $id ?>memory', 'mem_load', <?= $params['speed'] ?>);
	serverStat.add('<?= $id ?>swap', 'swap_load', <?= $params['speed'] ?>);

	serverStat.connect(dispatcher, 'server_stat');
</script>