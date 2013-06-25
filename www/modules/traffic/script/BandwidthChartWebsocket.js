function BandwidthChartWebsocket(id){
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	// inheritance from BandwidthChart
	BandwidthChart.call(this, id, true);
}


// inheritance from WebSocketManager
BandwidthChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the BandwidthChartWebsocket inheritance works
BandwidthChartWebsocket.prototype.dataManager = function(obj) {
	this.updateChart(obj.loc_Ko, obj.in_Ko, obj.out_Ko, obj.Ko);
}

// inheritance from BandwidthChart
BandwidthChartWebsocket.prototype.updateChart = BandwidthChart.prototype.updateChart;