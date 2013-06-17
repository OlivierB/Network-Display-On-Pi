function BandwidthChart(id){

	this.id = id;
	this.alertContainer = $('#' + this.id + '-alert');
	this.yVal = 100;	
	this.yVal2 = 100;	
	this.updateInterval = 1000;
	this.dataLength = 100; // number of dataPoints visible at any point
	this.xVal = this.dataLength;

	this.local_network = []; // dataPoints
	this.incoming = []; // dataPoints
	this.outcoming = []; // dataPoints
	this.global = []; // dataPoints
	

	iter = this.dataLength;
	while(iter--)
	{
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


	

	this.chart = new CanvasJS.Chart(this.id,{
		title :{
			text: "Current traffic",
			fontFamily: "Champ"
		},			
		data: [{
			type: "line",
			name: "Local Network",
			dataPoints: this.local_network,
			showInLegend: true 
		},{
			type: "line",
			name: "Incoming",
			showInLegend: true,
			dataPoints: this.incoming 
		},
		{
			type: "line",
			name: "Outcoming",
			showInLegend: true,
			dataPoints: this.outcoming 
		},
		{
			type: "line",
			name: "Global",
			showInLegend: true,
			dataPoints: this.global 
		}],
		axisY: {						
			title: "kB/s",
			titleFontFamily: "Champ",
			titleFontWeight: "bold"
		}
	});
	
	this.chart.render();
	console.log('constructor');
}


BandwidthChart.prototype = {
	constructor: BandwidthChart,
	updateChart: function (local_, inp_, outp_, global_) {

		
		
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
		
		if (this.outcoming.length > this.dataLength)
		{
			this.local_network.shift();
			this.incoming.shift();
			this.outcoming.shift();		
			this.global.shift();		
		}
		
		this.chart.render();		

	},
	connect : function (address, protocol){
		// console.log('tentative de connexion live ' + App.serverAddress + '/' + App.bandwidtProtocol);

		this.address = address || App.serverAddress || 'localhost';
		this.prot = protocol || App.bandwidtProtocol || 'bandwidth';


		this.connection = new WebSocket(this.address, this.prot);

		// this.animate.bind(this)
		// When the connection is open, send some data to the server
		this.connection.onopen = function () {
			console.log("connexion");
			this.alertContainer.html('');
		  	this.connection.send('Ping'); // Send the message 'Ping' to the server

		  }.bind(this);

		// Log errors
		this.connection.onerror = function (error) {
			console.log('WebSocket Error ' + error);
			this.alertContainer.text('Connection error : ' + error);
		}.bind(this);

		// Log messages from the server
		this.connection.onmessage = function (e) {
			var obj = JSON.parse(e.data);
			this.updateChart(obj.loc_Ko, obj.in_Ko , obj.out_Ko,obj.Ko);
		}.bind(this);

		this.connection.onclose = function (e) {
			// console.log('Deconnexion tentative de reconnexion dans 5 sec ' + App.serverAddress + '/' + App.bandwidtProtocol);
			this.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(function(){this.connect(this.address, this.prot);}, 5000);
		}.bind(this);

	}

}





