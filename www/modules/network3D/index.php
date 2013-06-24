<script src="/lib/three.min.js"></script>
<script src="/lib/OrbitControls.js"></script>


<link rel="stylesheet" type="text/css" href="/modules/network3D/style/canvas-3d.css">

<?php header_display('3D viewer'); ?>

<div class='slide-div'>
	<div class='row-fluid'>
		<div class="span10" >
			<span id="content-canvas-alert"></span>
			<div id="content-canvas"></div>
		</div>
		<div id='network3D-table'>
			<h2>Informations</h2>
			<!-- <ul>
				<li>Sous reseaux 192.168.1 <span style="background-color: black; width: 15px;" ></span></li>


			</ul> -->
			<div id='network3D-table-container'>
				<table class="table">
					<thead>
						<tr>
							<th>Network / IP</th>
							<th>Number</th>
						</tr>
					</thead>
					
				</table>
			</div>

		</div>
	</div>
</div>

<script type="text/javascript" src='/modules/network3D/res/Network3D.conf.js'></script>

<script type="text/javascript" src='/modules/network3D/script/InformationsDisplay.js'></script>
<script type="text/javascript" src='/modules/network3D/script/Ray.js'></script>
<script type="text/javascript" src='/modules/network3D/script/Satellite3D.js'></script>
<script type="text/javascript" src='/modules/network3D/script/Scene3D.js'></script>
<script type="text/javascript" src='/modules/network3D/script/canvas-loader.js'></script>
