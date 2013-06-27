BarChartWebsocket = function(id, id_data) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	// inheritance from WebSocketManager
	BarChart.call(this, id);

	this.id = id;
	this.id_data = id_data;
	this.container = $('#' + this.id);
}


// inheritance from WebSocketManager
BarChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// inheritance from BarChart
BarChartWebsocket.prototype.updateChart = BarChart.prototype.updateChart;

BarChartWebsocket.prototype.dataManager = function(obj) {
	this.updateChart(obj[this.id_data]);
}