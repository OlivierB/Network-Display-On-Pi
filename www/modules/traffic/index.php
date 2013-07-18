<script type="text/javascript" src="/script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="/script/chart/BarChart.js"></script>


<?php header_display('Main page'); ?>

<div class='slide-div'>
		<div class='row-fluid height-half'>
			<div class="span8" >
				<span id="bandwidth-chart-alert"></span>
				<div  id="bandwidth-chart" ></div>
			</div>

			<div class="span4">
				<span id="bandwidth-text-alert"></span>
				<div class='bandwith-table' id="bandwidth-text" ></div>
			</div>
			
		</div>

		<div class='row-fluid height-half'>
			<div class="span6" >
				<div id="protocol-ethernet"><span id="protocol-ethernet-alert"></span></div>
			</div>

			<div class="span6">
				<div  id="protocol-ip"><span id="protocol-ip-alert"></span></div>
			</div>
		</div>
</div>

<script type="text/javascript" src="/modules/traffic/script/BarChartWebsocket.js"></script>
<script type="text/javascript" src="/modules/traffic/script/BandwidthChartWebsocket.js"></script>
<script type="text/javascript" src="/modules/traffic/script/BandwidthTextWebsocket.js"></script>
<script type="text/javascript" src="/modules/traffic/script/chart-loader.js"></script>