function PercentCounterChart(id, id_data, speed) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');


	this.speed = speed | 100;

	this.id = id;
	this.id_data = id_data;

	this.chart = $('#' + id);

	this.chart.easyPieChart({
		animate: this.speed
	});
}

// inheritance from WebSocketManager
PercentCounterChart.prototype = Object.create(WebSocketManager.prototype);

PercentCounterChart.prototype.updateChart = function(percent) {
	this.chart.data('easyPieChart').update(percent);
	$('#' + this.id + " span").text(percent + "%");
}

PercentCounterChart.prototype.dataManager = function(obj) {
	this.updateChart(obj[this.id_data]);
}

