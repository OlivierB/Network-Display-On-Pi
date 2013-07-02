
function PacketLossChartWebsocket(id){
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	// inheritance from PacketLossChart
	PacketLossChart.call(this, id, true, 100);
}


// inheritance from WebSocketManager
PacketLossChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the PacketLossChartWebsocket inheritance works
PacketLossChartWebsocket.prototype.dataManager = function(obj) {
	this.updateChart(parseInt(obj.packet_received), parseInt(obj.packet_handled));
	this.refresh();
}

// inheritance from PacketLossChart
PacketLossChartWebsocket.prototype.updateChart = PacketLossChart.prototype.updateChart;
PacketLossChartWebsocket.prototype.refresh = PacketLossChart.prototype.refresh;