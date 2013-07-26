/**
 * StackedColumnChartAjax, class receiving data from ajax request
 * and displaying it in a StackedColumnChart.
 * @author Matrat Erwan
 **/


function StackedColumnChartAjax(id, title){
	// inheritance from AjaxManager
	AjaxManager.call(this, id + '-alert');

	// inheritance from StackedColumnChart
	StackedColumnChart.call(this, id, title);
}

// inheritance from AjaxManager
StackedColumnChartAjax.prototype = Object.create(AjaxManager.prototype);

// inheritance from StackedColumnChart
StackedColumnChartAjax.prototype.updateChart = StackedColumnChart.prototype.updateChart;



StackedColumnChartAjax.prototype.dataManager = function(obj) {
	this.updateChart(obj);
};