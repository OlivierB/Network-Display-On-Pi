function PercentBarChart(id, id_data) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');



	this.id = id;
	this.id_data = id_data;

	this.data = [];

	this.chart = new CanvasJS.Chart(this.id, {

		title: {
			text: "Division of traffic",

		},
		axisX: {
			interval: 1,
			gridThickness: 0,
			labelFontSize: 10,
			labelFontStyle: "normal",
			labelFontWeight: "normal",
			labelFontFamily: "Lucida Sans Unicode",

		},

		data: [{
				type: "bar",
				name: "protocol",				
				dataPoints: this.data
			},

		]
	});


	this.chart.render();
}

// inheritance from WebSocketManager
PercentBarChart.prototype = Object.create(WebSocketManager.prototype);


PercentBarChart.prototype.updateChart = function(array) {
	this.data.length = 0;

	for (var i = 0; i < array.length; i++) {
		this.data.push({
			y: array[i][1],
			label: array[i][0]
		});
	}



	this.chart.render();
}

PercentBarChart.prototype.dataManager = function(obj) {
	this.updateChart(obj[this.id_data]);
}