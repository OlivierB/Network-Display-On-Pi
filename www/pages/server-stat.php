<script type="text/javascript" src="/script/chart/PercentCounterChart.js"></script>

<?php header_display('Server statistics'); ?>

<div id='server-stat'>
	<h2>Server statistics</h2>
	<div>
		<span id="proc-alert"></span>
		<div class='percent-chart-loader' id="proc" data-percent="0"><span>0</span></div>
		<h3>Processor load</h3>
	</div>

	
	<div>
		<span id="memory-alert"></span>
		<div class='percent-chart-loader' id="memory" data-percent="0"><span>0</span></div>
		<h3>Memory load</h3>
	</div>


	<div>
		<span id="swap-alert"></span>
		<div class='percent-chart-loader' id="swap" data-percent="0"><span>0</span></div>
		<h3>Swap load</h3>
	</div>

</div>

<script src="/script/chart/server-stat-loader.js"></script>