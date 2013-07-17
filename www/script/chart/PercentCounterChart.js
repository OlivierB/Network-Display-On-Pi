/**
 * PercentCounterChart, chart showing a percent value as a counter.
 * Use easyPieChart http://rendro.github.io/easy-pie-chart/
 * @author Matrat Erwan
 **/

function PercentCounterChart(id, id_data, speed) {

	this.speed = speed | 100;

	this.id = id;
	this.id_data = id_data;

	this.chart = $('#' + id);

	this.chart.easyPieChart({
		animate: this.speed
	});

	this.container = $('#' + this.id + " span");
}


PercentCounterChart.prototype.updateChart = function(percent) {
	this.chart.data('easyPieChart').update(percent);
	this.container.text(percent.toFixed(2) + "%");
};


