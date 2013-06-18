function BandwidthChart(id) {

	// inheritance from WebSocketManager
	WebSocketManager.call(this, id + '-alert');

	this.id = id;
	// this.alertContainer = $('#' + this.id + '-alert');
	this.yVal = 100;
	this.yVal2 = 100;
	this.updateInterval = 1000;
	this.dataLength = 100; // number of dataPoints visible at any point
	this.xVal = this.dataLength;

	this.local_network = []; // dataPoints
	this.incoming = []; // dataPoints
	this.outcoming = []; // dataPoints
	this.global = []; // dataPoints


	// initializes arrays to begin the display of new points at the right part of the chart
	iter = this.dataLength;
	while (iter--) {
		this.incoming.push({
			x: this.dataLength - iter,
			y: 0,
		});
		this.outcoming.push({
			x: this.dataLength - iter,
			y: 0,
		});

		this.local_network.push({
			x: this.dataLength - iter,
			y: 0,
		});
		this.global.push({
			x: this.dataLength - iter,
			y: 0,
		});

	}
	this.dataLength = this.xVal;



	this.chart = new CanvasJS.Chart(this.id, {
		title: {
			text: "Current traffic",
			fontFamily: "Champ"
		},
		data: [{
				type: "line",
				name: "Local Network",
				dataPoints: this.local_network,
				showInLegend: true
			}, {
				type: "line",
				name: "Incoming",
				showInLegend: true,
				dataPoints: this.incoming
			}, {
				type: "line",
				name: "Outcoming",
				showInLegend: true,
				dataPoints: this.outcoming
			}, {
				type: "line",
				name: "Global",
				showInLegend: true,
				dataPoints: this.global
			}
		],
		axisY: {
			title: "kB/s",
			titleFontFamily: "Champ",
			titleFontWeight: "bold"
		}
	});

	this.chart.render();
}

// inheritance from WebSocketManager
BandwidthChart.prototype = Object.create(WebSocketManager.prototype);


BandwidthChart.prototype.updateChart = function(local_, inp_, outp_, global_) {

	yVal1 = local_;
	this.local_network.push({
		x: this.xVal,
		y: yVal1,
	});

	yVal2 = inp_;
	this.incoming.push({
		x: this.xVal,
		y: yVal2,
	});

	yVal3 = outp_;
	this.outcoming.push({
		x: this.xVal,
		y: yVal3,
	});

	yVal4 = global_;
	this.global.push({
		x: this.xVal,
		y: yVal4,
	});

	this.xVal++;

	if (this.outcoming.length > this.dataLength) {
		this.local_network.shift();
		this.incoming.shift();
		this.outcoming.shift();
		this.global.shift();
	}

	this.chart.render();

}

BandwidthChart.prototype.dataManager = function(obj) {
	this.updateChart(obj.loc_Ko, obj.in_Ko , obj.out_Ko,obj.Ko);
}


