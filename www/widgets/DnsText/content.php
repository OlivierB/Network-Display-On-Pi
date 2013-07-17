<span id="<?= $id ?>-alert"></span>
<div  id="<?= $id ?>">

	<table class="big-table table table-striped" id='dns-table'>
		<thead>
			<tr>
				<th>Request on</th>
				<th>Number of request</th>
			</tr>
		</thead>
		<tbody>
			<!-- <tr><td></td><td></td></tr> -->

		</tbody>
	</table>
</div>

<script type="text/javascript">
	var display = new DnsDisplayerText("<?= $id ?>", <?= $params['nb_item'] ?>, <?= $params['font_size'] ?>);
	display.connect(dispatcher, 'dns');
</script>

<link rel="stylesheet" type="text/css" href="/widgets/DnsText/style.css">