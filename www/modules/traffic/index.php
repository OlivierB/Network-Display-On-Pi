<script type="text/javascript" src="/script/chart/BandwidthChart.js"></script>
<script type="text/javascript" src="/script/text/BandwidthText.js"></script>
<script type="text/javascript" src="/script/chart/PercentBarChart.js"></script>


<?php header_display('Main page'); ?>

<div class='slide-div'>
		<div class='row-fluid'>
			<div class="span8" >
				<span id="bandwidth-chart-alert"></span>
				<div class='height-half' id="bandwidth-chart" ></div>
			</div>

			<div class="span4">
				<span id="bandwidth-text-alert"></span>
				<div class='height-half' id="bandwidth-text" ></div>
			</div>
			
		</div>

		<div class='row-fluid'>
			<div class="span6" >
				<div class='height-half' id="protocol-ethernet"><span id="protocol-ethernet-alert"></span></div>
			</div>

			<div class="span6">
				<div class='height-half' id="protocol-ip"><span id="protocol-ip-alert"></span></div>
			</div>
		</div>
</div>

<script type="text/javascript" src="/modules/traffic/script/chart-loader.js"></script>