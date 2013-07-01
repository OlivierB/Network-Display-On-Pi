<script type="text/javascript" src="/script/chart/PaquetLossChart.js"></script>


<?php header_display('Server stress'); ?>

<div class='slide-div'>
		<div class='row-fluid'>
			<div class="span12" >
				<span id="paquet-loss-live-chart-alert"></span>
				<div class='height-half' id="paquet-loss-live-chart" ></div>
			</div>			
		</div>

		<div class='row-fluid'>
			<div class="span12" >
				<span id="paquet-loss-day-chart-alert"></span>
				<div class='height-half' id="paquet-loss-day-chart"></div>
			</div>

			
		</div>
</div>

<script type="text/javascript" src="/modules/stressServer/script/PaquetLossChartWebsocket.js"></script>
<script type="text/javascript" src="/modules/stressServer/script/PaquetLossChartAjax.js"></script>
<script type="text/javascript" src="/modules/stressServer/script/loader.js"></script>