BaseAlert = function(id) {
	this.url = "/base/perso/base_stat_alerts.php?caller=&sort_order=last_d";
	this.id = id;
}

BaseAlert.prototype.load = function() {

	$.ajax({
		type: "GET",
		url: "http://" + App.baseAdress + this.url,
		async: true,
		success: function(data) {
			$("#" + this.id).html(data);
			$("#" + this.id + "-alert").html('');
		}.bind(this),

		error: function() {
			var msg = '<span class="alert">Cannot reach the BASE page (Snort web page).</span>';
			$("#" + this.id + "-alert").html(msg);
		}.bind(this)
	});

	setTimeout(this.load.bind(this), 5000);
};

BaseAlert.prototype.launch = function() {
	// refresh every 5 seconds
	setInterval(this.load.bind(this), 5000);
};