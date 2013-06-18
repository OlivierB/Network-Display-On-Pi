function PercentBarChart(id, id_data) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');



	this.id = id;
	this.id_data = id_data;

	this.data = [];


	// this.chart = new CanvasJS.Chart(this.id,
	// 	{
	// 		animationEnabled: false,
	// 		title:{
	// 			text: "Division of traffic",
	// 			verticalAlign: 'top',
	// 			horizontalAlign: 'left'
	// 		},
	// 		data: [
	// 		{        
	// 			type: "pie",
	// 			startAngle:20,
	// 			showInLegend: false,
	// 			indexLabelFontColor: "rgba(0,0,0,0)",
	// 			indexLabelLineColor: "rgba(0,0,0,0)",
	// 			dataPoints: this.data
	// 		}
	// 		]
	// 	});

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
				// axisYType: "secondary",
				// color: "#014D65",				
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

	// var sortable = [];
	// for (var obj in array)
	// 	sortable.push([obj, array[obj]])

	// sortable.sort(function(a, b) {
	// 	a = a[1];
	// 	b = b[1];

	// 	return a < b ? -1 : (a > b ? 1 : 0);
	// });

	for (var i = 0; i < array.length; i++) {
		this.data.push({
			y: array[i][1],
			label: array[i][0]
		});
		// console.log(value);
	}

	// for (var value in array) {
	// 	this.data.push({
	// 		y: array[value],
	// 		label: value
	// 	});
	// 	console.log(value);
	// }



	this.chart.render();
}

PercentBarChart.prototype.dataManager = function(obj) {
	// console.log(obj[this.id_data]);
	this.updateChart(obj[this.id_data]);
}