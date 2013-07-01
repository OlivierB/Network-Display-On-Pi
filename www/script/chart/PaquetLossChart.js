function PaquetLossChart(id, initializes, dataLength) {

	this.id = id;

	this.number_paquets_total = [];
	this.number_paquets_loss = [];
	this.dataLength = dataLength; // number of dataPoints visible at any point

	if (initializes) {
		var currentDate = new Date();
		var currentMilli = currentDate.getTime() - (this.dataLength * 1000);

		// initializes arrays to begin the display of new points at the right part of the chart
		iter = this.dataLength;
		while (iter--) {
			currentDate.setTime(currentMilli);
			this.updateChart(0, 0, currentDate);
			currentMilli += 1000;
		}
	}



	this.chart = new CanvasJS.Chart(this.id, {
		title: {
			text: "Paquet Loss",
			titleFontFamily: "ChampWoff",
		},
		axisY2: {
			title: "% Paquet loss",
			minimum: 0,
			maximum: 100,
			titleFontFamily: "ChampWoff",
			titleFontWeight: "bold",
		},
		axisY: {
			title: "Global flow (MB/s)",
			titleFontFamily: "ChampWoff",
			titleFontWeight: "bold",
		},
		legend: {
			verticalAlign: "bottom",
		},
		data: [{
				type: "spline",
				showInLegend: true,
				legendText: "Global flow (MB/s)",
				dataPoints: this.number_paquets_total
			}, {
				type: "spline",
				axisYType: "secondary",
				showInLegend: true,
				legendText: "% Paquet loss",
				dataPoints: this.number_paquets_loss

			}

		]
	});

	this.chart.render();
}



PaquetLossChart.prototype.updateChart = function(total_, loss_, time_) {

	if (time_){
		this.xVal = new Date(time_);
		console.log('p '+this.xVal)
	}
	else
		this.xVal = new Date();


	yVal1 = total_;
	this.number_paquets_total.push({
		x: this.xVal,
		y: yVal1,
	});

	yVal2 = loss_;
	this.number_paquets_loss.push({
		x: this.xVal,
		y: yVal2,
	});



	this.xVal++;
	if (this.number_paquets_total.length > this.dataLength && this.dataLength > 0) {
		this.number_paquets_total.shift();
		this.number_paquets_loss.shift();
	}

}


PaquetLossChart.prototype.clean = function() {
	this.number_paquets_total.length = 0;
	this.number_paquets_loss.length = 0;
}

PaquetLossChart.prototype.refresh = function() {
	this.chart.render();
}