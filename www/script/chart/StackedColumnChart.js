/**
 * StackedColumnChart, interface displaying in a stacked Column chart a list of data.
 * @author Matrat Erwan
 **/

function StackedColumnChart(id, title) {

	this.id = id;

	this.data = [];

	this.chart = new CanvasJS.Chart(this.id, {
		title: {
			text: title
		},
		axisY: {
			title: "Packet percentage"
		},
		data: this.data
	});


	this.chart.render();
}


/**
 * The obj parameter should contain a list of label (obj['listProt'] = ['label1', 'label2'])
 * the data should be listed as couple 
 * obj['listValue']=[
 *  {"date":"2013-07-25 16:30:04","value":{"label1":"2709","label2":"169728"}},
 *  {"date":"2013-07-25 17:00:03","value":{"label1":"2444"}}
 * ]
 **/
StackedColumnChart.prototype.updateChart = function(obj) {
	this.data.length = 0;
	var listProt = obj.listProt;
	for (var j = 0; j < listProt.length; j++) {
		var prot = listProt[j];
		dataProt = [];
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

};