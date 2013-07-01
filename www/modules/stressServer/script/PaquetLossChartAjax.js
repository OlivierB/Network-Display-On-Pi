
function PaquetLossChartAjax(id){
	// inheritance from AjaxManager
	AjaxManager.call(this, id + '-alert');

	// inheritance from PaquetLossChart
	PaquetLossChart.call(this, id, false, -1);
}


// inheritance from AjaxManager
PaquetLossChartAjax.prototype = Object.create(AjaxManager.prototype);

// method needed to make the PaquetLossChartAjax inheritance works
PaquetLossChartAjax.prototype.dataManager = function(obj) {
	
	
	for (var i = 0; i < obj.length; i++) {
		var tmp = obj[i];
		console.log(tmp)
		var percent_loss = ((parseInt(tmp.packet_received) - parseInt(tmp.packet_handled))/parseInt(tmp.packet_received))*100;
		this.updateChart(parseInt(tmp.packet_received), percent_loss, (tmp.date));
	}
	this.refresh();
	this.clean();
}

// inheritance from PaquetLossChart
PaquetLossChartAjax.prototype.updateChart = PaquetLossChart.prototype.updateChart;
PaquetLossChartAjax.prototype.refresh = PaquetLossChart.prototype.refresh;
PaquetLossChartAjax.prototype.clean = PaquetLossChart.prototype.clean;