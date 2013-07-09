<script type="text/javascript" src="/script/chart/PacketLossChart.js"></script>


<?php header_display('Server stress'); ?>

<div class='slide-div'>
		<div class='row-fluid height-half'>
			<div class="span12" >
				<span id="packet-loss-live-chart-alert"></span>
				<div  id="packet-loss-live-chart" ></div>
			</div>			
		</div>

		<div class='row-fluid height-half'>
			<div class="span12" >
				<span id="packet-loss-day-chart-alert"></span>
				<div  id="packet-loss-day-chart"></div>
			</div>

			
		</div>
</div>

<script type="text/javascript" src="/modules/stressServer/script/PacketLossChartWebsocket.js"></script>
<script type="text/javascript" src="/modules/stressServer/script/PacketLossChartAjax.js"></script>
<script type="text/javascript" src="/modules/stressServer/script/loader.js"></script>