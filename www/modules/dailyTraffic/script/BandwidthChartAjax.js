function BandwidthChartAjax(id){

	// inheritance from BandwidthChart
	BandwidthChart.call(this, id, false, -1);


}


// inheritance from WebSocketManager
BandwidthChartAjax.prototype = Object.create(BandwidthChart.prototype);



BandwidthChartAjax.prototype.connect = function(address, ip, path) {

	this.address = address;
	this.ip = ip;
	this.path = path;

	this.load();
	

};

BandwidthChartAjax.prototype.load = function() {
	$.ajax({
		type: "GET",
		url: "http://" + this.address + this.path ,
		async: true,
		success: function(data) {
			data = $.parseJSON(data);
			for(var i = 0; (i < data.length) ; i++){
				var tmp = data[i];
				this.updateChart(parseInt(tmp.local), parseInt(tmp.incoming), parseInt(tmp.outcoming), parseInt(tmp.global), (tmp.date));
			}
			setTimeout(this.load.bind(this), 10000);
		}.bind(this),

		error: function() {
			var msg = '<span class="alert">Cannot reach the page.</span>';
			$("#" + this.id + "-alert").html(msg);
		}.bind(this)
	});
	// setTimeout(this.connect.bind(this), 90000);
		
}