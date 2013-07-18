<script type="text/javascript" src="/script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChart.js"></script>
<script type="text/javascript" src="/script/chart/BandwidthChartAjax.js"></script>
<script type="text/javascript" src="/script/chart/TotalBandwidthTextAjax.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChartAjax.js"></script>

<?php header_display('Informations of the month'); ?>

<div class='slide-div'>
		<div class='row-fluid'>
			<div class="span8 height-half" >
				<span id="monthly-bandwidth-chart-alert"></span>
				<div  id="monthly-bandwidth-chart" ></div>
			</div>
			<div class="span4">
				<span id="monthly-total-bandwidth-text-alert"></span>
				<div class='bandwith-table' id="monthly-total-bandwidth-text" ></div>
			</div>
		</div>

		<div class='row-fluid'>
			<div class="span6 height-half" >
				<span id="monthly-protocol-use-chart-alert"></span>
				<div  id="monthly-protocol-use-chart" ></div>
			</div>
			<div class="span6" >
				<span id="monthly-subprotocol-ipv4-use-chart-alert"></span>
				<div  id="monthly-subprotocol-ipv4-use-chart" ></div>
			</div>
		</div>		
</div>


<script type="text/javascript" src="/modules/monthlyTraffic/script/chart-loader.js"></script>