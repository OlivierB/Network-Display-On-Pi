function BandwidthChartAjax(id){

	// inheritance from BandwidthChart
	BandwidthChart.call(this, id, false);


}


// inheritance from WebSocketManager
BandwidthChartAjax.prototype = Object.create(BandwidthChart.prototype);



BandwidthChartAjax.prototype.connect = function(address, ip, path) {

	this.address = address;
	this.ip = ip;
	$.ajax({
		type: "GET",
		url: "http://" + this.address +path ,
		async: true,
		success: function(data) {
			data = $.parseJSON(data);
			console.log('ready ' + data.length);
			for(var i = 0; (i < data.length) ; i++){
				var tmp = data[i];
				this.updateChart(parseInt(tmp.global), parseInt(tmp.local), parseInt(tmp.incoming), parseInt(tmp.outcoming), (tmp.date));
			}
			console.log('done ' + data.length);
			
		}.bind(this)
	});


};