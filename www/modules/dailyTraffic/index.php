<script type="text/javascript" src="/script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChart.js"></script>
<script type="text/javascript" src="/script/chart/BandwidthChartAjax.js"></script>
<script type="text/javascript" src="/script/chart/TotalBandwidthTextAjax.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChartAjax.js"></script>

<?php header_display('Informations of the day'); ?>

<div class='slide-div'>
		<div class='row-fluid height-half'>
			<div class="span8" >
				<span id="daily-bandwidth-chart-alert"></span>
				<div  id="daily-bandwidth-chart" ></div>
			</div>
			<div class="span4">
				<span id="daily-total-bandwidth-text-alert"></span>
				<div class='bandwith-table' id="daily-total-bandwidth-text" ></div>
			</div>
		</div>

		<div class='row-fluid height-half'>
			<div class="span6" >
				<span id="daily-protocol-use-chart-alert"></span>
				<div id="daily-protocol-use-chart" ></div>
			</div>
			<div class="span6" >
				<span id="daily-subprotocol-ipv4-use-chart-alert"></span>
				<div  id="daily-subprotocol-ipv4-use-chart" ></div>
			</div>
		</div>		
</div>


<script type="text/javascript" src="/modules/dailyTraffic/script/chart-loader.js"></script>