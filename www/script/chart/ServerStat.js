/**
 * ServerStat, class receiving the NDOP server statistics via websocket
 * and displaying it in a PercentCounterChart.
 * @author Matrat Erwan
 **/

function ServerStat(id) {
	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.charts = [];
}

// inheritance from WebSocketManager
ServerStat.prototype = Object.create(WebSocketManager.prototype);

ServerStat.prototype.dataManager = function(obj) {

	var i = this.charts.length;
	for (; i--;) {
		var chart = this.charts[i];
		if (chart.id_data in obj) {
			chart.updateChart(obj[chart.id_data]);
		}
	}
};

ServerStat.prototype.add = function(id, id_data, speed) {
	this.charts.push(new PercentCounterChart(id, id_data, speed));
};