
function PaquetLossChartWebsocket(id){
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	// inheritance from PaquetLossChart
	PaquetLossChart.call(this, id, true, 100);
}


// inheritance from WebSocketManager
PaquetLossChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the PaquetLossChartWebsocket inheritance works
PaquetLossChartWebsocket.prototype.dataManager = function(obj) {
	this.updateChart(parseInt(obj.packet_received), parseInt(obj.packet_handled));
	this.refresh();
}

// inheritance from PaquetLossChart
PaquetLossChartWebsocket.prototype.updateChart = PaquetLossChart.prototype.updateChart;
PaquetLossChartWebsocket.prototype.refresh = PaquetLossChart.prototype.refresh;