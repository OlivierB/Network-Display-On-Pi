<script type="text/javascript" src="/script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChart.js"></script>
<script type="text/javascript" src="/script/chart/BandwidthChartAjax.js"></script>
<script type="text/javascript" src="/script/chart/TotalBandwidthTextAjax.js"></script>
<script type="text/javascript" src="/script/chart/StackedColumnChartAjax.js"></script>

<?php header_display('Informations of the week'); ?>

<div class='slide-div'>
		<div class='row-fluid'>
			<div class="span8" >
				<span id="weekly-bandwidth-chart-alert"></span>
				<div class='height-half' id="weekly-bandwidth-chart" ></div>
			</div>
			<div class="span4">
				<span id="weekly-total-bandwidth-text-alert"></span>
				<div class='height-half bandwith-table' id="weekly-total-bandwidth-text" ></div>
			</div>
		</div>

		<div class='row-fluid'>
			<div class="span6" >
				<span id="weekly-protocol-use-chart-alert"></span>
				<div class='height-half' id="weekly-protocol-use-chart" ></div>
			</div>
			<div class="span6" >
				<span id="weekly-subprotocol-ipv4-use-chart-alert"></span>
				<div class='height-half' id="weekly-subprotocol-ipv4-use-chart" ></div>
			</div>
		</div>		
</div>


<script type="text/javascript" src="/modules/weeklyTraffic/script/chart-loader.js"></script>