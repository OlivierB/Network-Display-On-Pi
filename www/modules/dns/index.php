<link rel="stylesheet" href="/modules/dns/style/dns.css">

<?php header_display('Live DNS request'); ?>

<div class='slide-div'>
	<div class='row-fluid'>
		<div class="span12" >
			<span id="dns-display-alert"></span>
			<div class='height-full' id="dns-display" >

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
		</div>

	</div>

	
</div>

<script type="text/javascript" src="/modules/dns/script/DnsDisplayer.js"></script>
<script type="text/javascript" src="/modules/dns/script/loader.js"></script>