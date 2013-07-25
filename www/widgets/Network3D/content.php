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

<script src="widgets/Network3D/Network3D.conf.js"></script>

<script type="text/javascript">
$(function(){
	var scene3D = new Scene3D('<?= $id ?>', <?= $params['quality'] ?>);
	scene3D.animate();
	scene3D.connect(dispatcher, 'local_communication');
});
</script>

<link rel="stylesheet" type="text/css" href="widgets/Network3D/style.css">


