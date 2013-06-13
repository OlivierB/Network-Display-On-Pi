
// load the alert table once to begin from BASE (Snort GUI with ACID)
$("#content-table").load("/base/perso/base_stat_alerts.php?caller=&sort_order=last_d");

// refresh every 5 seconds
setInterval(
	function(){
		$("#content-table").load("/base/perso/base_stat_alerts.php?caller=&sort_order=last_d");
	}, 	
	5000
); 


	