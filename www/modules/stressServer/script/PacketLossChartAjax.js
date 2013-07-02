
function PacketLossChartAjax(id){
	// inheritance from AjaxManager
	AjaxManager.call(this, id + '-alert');

	// inheritance from PacketLossChart
	PacketLossChart.call(this, id, false, -1);
}


// inheritance from AjaxManager
PacketLossChartAjax.prototype = Object.create(AjaxManager.prototype);

// method needed to make the AjaxManager inheritance works
PacketLossChartAjax.prototype.dataManager = function(obj) {
	
	
	for (var i = 0; i < obj.length; i++) {
		var tmp = obj[i];
		this.updateChart(parseInt(tmp.packet_received), parseInt(tmp.packet_handled), (tmp.date));
	}
	this.refresh();
	this.clean();
}

// inheritance from PacketLossChart
PacketLossChartAjax.prototype.updateChart = PacketLossChart.prototype.updateChart;
PacketLossChartAjax.prototype.refresh = PacketLossChart.prototype.refresh;
PacketLossChartAjax.prototype.clean = PacketLossChart.prototype.clean;