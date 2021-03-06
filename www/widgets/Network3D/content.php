<div class='row-fluid'>
		<div class="span10" >
			<span id="<?= $id ?>-alert"></span>
			<div id="<?= $id ?>"></div>
		</div>
		<div class='network3D-table'>
			<h2>Informations</h2>
			<div id='<?= $id ?>-table-container'>
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
<?php if(NDOP::$app['debug']){ ?>

	<script src="lib/three.min.js"></script>
    <script src="lib/OrbitControls.js"></script>

	<script src="script/network3D/Ray.js"></script>
    <script src="script/network3D/Scene3D.js"></script>
    <script src="script/network3D/Satellite3D.js"></script>
    <script src="script/network3D/InformationsDisplay.js"></script>


<?php }else{ ?>
	
	<script src="minify/3d.min.js"></script>

<?php } ?>

<script type="text/javascript">

	Network3DMaskList = [<?= $params['mask_customize'] ?>];

</script>

<script type="text/javascript">
$(function(){
	var scene3D = new Scene3D('<?= $id ?>', <?= $params['quality'] ?>);
	scene3D.animate();
	scene3D.connect(dispatcher, 'local_communication');
});
</script>

<link rel="stylesheet" type="text/css" href="widgets/Network3D/style.css">


