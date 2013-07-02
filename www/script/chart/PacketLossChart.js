function PacketLossChart(id, initializes, dataLength) {

	this.id = id;

	this.number_packets_total = [];
	this.number_packets_loss = [];
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
			text: "Packet Loss",
			titleFontFamily: "ChampWoff",
		},
		axisY2: {
			title: "% Packet loss",
			minimum: 0,
			maximum: 100,
			titleFontFamily: "ChampWoff",
			titleFontWeight: "bold",
		},
		axisY: {
			title: "Packets received (unity)",
			titleFontFamily: "ChampWoff",
			titleFontWeight: "bold",
		},
		legend: {
			verticalAlign: "bottom",
		},
		data: [{
				type: "spline",
				showInLegend: true,
				legendText: "Number of packets received",
				dataPoints: this.number_packets_total
			}, {
				type: "spline",
				axisYType: "secondary",
				showInLegend: true,
				legendText: "% Packet loss",
				dataPoints: this.number_packets_loss

			}

		]
	});

	this.chart.render();
}



PacketLossChart.prototype.updateChart = function(total_, handled_, time_) {

	if (time_){
		this.xVal = new Date(time_);
		// console.log('p '+this.xVal)
	}
	else
		this.xVal = new Date();
	if(total_ != 0)
		var percent_loss = ((total_ - handled_)/total_)*100;
	else
		var percent_loss = 0;
	
	yVal1 = total_;
	this.number_packets_total.push({
		x: this.xVal,
		y: yVal1,
	});

	yVal2 = percent_loss;
	this.number_packets_loss.push({
		x: this.xVal,
		y: yVal2,
	});



	this.xVal++;
	if (this.number_packets_total.length > this.dataLength && this.dataLength > 0) {
		this.number_packets_total.shift();
		this.number_packets_loss.shift();
	}

}


PacketLossChart.prototype.clean = function() {
	this.number_packets_total.length = 0;
	this.number_packets_loss.length = 0;
}

PacketLossChart.prototype.refresh = function() {
	this.chart.render();
}