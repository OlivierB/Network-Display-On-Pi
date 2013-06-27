function AjaxManager(id_alert_container) {
	this.alertContainer = $('#' + id_alert_container);
}

AjaxManager.prototype.connect = function(address, path, time) {

	this.address = address;
	this.path = path;
	this.time = time;

	this.load();


};

AjaxManager.prototype.load = function() {

	$.ajax({
		type: "GET",
		url: "http://" + this.address + this.path,
		async: true,
		success: function(data) {


			data = $.parseJSON(data);
			this.dataManager(data);
			setTimeout(this.load.bind(this), this.time);
		}.bind(this),

		error: function() {
			var msg = '<span class="alert">Cannot reach the page.</span>';
			this.alertContainer.html(msg);
		}.bind(this)
	});
	// setTimeout(this.connect.bind(this), 90000);

}