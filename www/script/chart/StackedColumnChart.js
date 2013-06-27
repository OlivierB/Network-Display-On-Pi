function StackedColumnChart(id, title) {

	this.id = id;

	this.data = [];

	this.chart = new CanvasJS.Chart(this.id, {
		title: {
			text: title,
		},
		axisY: {
			title: "Number of packets",
		},
		data: this.data
	});


	this.chart.render();
}



StackedColumnChart.prototype.updateChart = function(obj) {
	console.log(obj);
	this.data.length = 0;

	var listProt = obj.listProt;
	for (var j = 0; j < listProt.length; j++) {
		var prot = listProt[j];
		dataProt = [];
		console.log(prot)
		var length = obj.listValue.length;

		for (i = 0; i < length; i++) {
			dataProt.push({
				y: parseInt(obj.listValue[i].value[prot]) || 0,
				label: obj.listValue[i].date
			});
		}

		this.data.push({
			type: "stackedColumn100",
			name: prot,
			showInLegend: "true",
			dataPoints: dataProt
		});
	}

	this.chart.render();

}