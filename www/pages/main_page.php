<script type="text/javascript" src="./script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="./script/chart/PercentCounterChart.js"></script>


<?php header_display('Main page'); ?>



<div id="bandwidth"><span id="bandwidth-alert"></span></div>

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
		<span id="stuff-alert"></span>
		<div class='percent-chart-loader' id="stuff" data-percent="0"><span>0</span></div>
		<h3>Swap load</h3>
	</div>

</div>

<script type="text/javascript" src="./script/chart/chart-loader.js"></script>