<script type="text/javascript" src="/script/chart/PercentCounterChart.js"></script>
<script type="text/javascript" src="/modules/serverStat/script/ServerStat.js"></script>

<?php header_display('Server statistics'); ?>

<div class='server-stat rows server-stat-legend'>
	<h2>Server statistics</h2>

	<span id="server-stat-alert"></span>

	<div class='span4'>
		<div class='percent-chart-loader' id="proc" data-percent="0"><span>0</span></div>
		<h3>Processor load</h3>
	</div>

	
	<div class='span4'>
		<div class='percent-chart-loader' id="memory" data-percent="0"><span>0</span></div>
		<h3>Memory load</h3>
	</div>


	<div class='span4'>
		<div class='percent-chart-loader' id="swap" data-percent="0"><span>0</span></div>
		<h3>Swap load</h3>
	</div>





</div>

<script src="/modules/serverStat/script/server-stat-loader.js"></script>