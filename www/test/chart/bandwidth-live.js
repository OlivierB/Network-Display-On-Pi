function current_global_bandwidth_line(id) {

	
	
	var yVal = 100;	
	var yVal2 = 100;	
	var updateInterval = 1000;
	var dataLength = 100; // number of dataPoints visible at any point
	var xVal = dataLength;

	var local_network = []; // dataPoints
	var incoming = []; // dataPoints
	var outcoming = []; // dataPoints
	var global = []; // dataPoints
	

	var iter = dataLength;
	while(iter--)
	{
		incoming.push({
			x: dataLength - iter,
			y: 0,
		});
		outcoming.push({
			x: dataLength - iter,
			y: 0,
		});

		local_network.push({
			x: dataLength - iter,
			y: 0,
		});
		global.push({
			x: dataLength - iter,
			y: 0,
		});
		
	} 
	dataLength = xVal;


	

	var chart = new CanvasJS.Chart(id,{
		title :{
			text: "Current traffic",
			fontFamily: "Champ"
		},			
		data: [{
			type: "line",
			name: "Local Network",
			dataPoints: local_network,
			showInLegend: true 
		},{
			type: "line",
			name: "Incoming",
			showInLegend: true,
			dataPoints: incoming 
		},
		{
			type: "line",
			name: "Outcoming",
			showInLegend: true,
			dataPoints: outcoming 
		},
		{
			type: "line",
			name: "Global",
			showInLegend: true,
			dataPoints: global 
		}],
		axisY: {						
			title: "kB/s",
			titleFontFamily: "Champ",
			titleFontWeight: "bold"
		}
	});
	
	chart.render();



	
	var updateChart = function (local_, inp_, outp_, global_) {

		
		
		yVal1 = local_;
		local_network.push({
			x: xVal,
			y: yVal1,
		});

		yVal2 = inp_;
		incoming.push({
			x: xVal,
			y: yVal2,
		});

		yVal3 = outp_;
		outcoming.push({
			x: xVal,
			y: yVal3,
		});

		yVal4 = global_;
		global.push({
			x: xVal,
			y: yVal4,
		});

		xVal++;
		
		if (outcoming.length > dataLength)
		{
			local_network.shift();
			incoming.shift();
			outcoming.shift();		
			global.shift();		
		}
		
		chart.render();		

	};

	var connect = function (){

		console.log('tentative de connexion live');
		var connection = new WebSocket(App.serverAddress, App.bandwidtProtocol);

		// When the connection is open, send some data to the server
		connection.onopen = function () {
			console.log("connexion");
			$('#alert-bandwidth').html('');
		  	connection.send('Ping'); // Send the message 'Ping' to the server
		  
		};

		// Log errors
		connection.onerror = function (error) {
			console.log('WebSocket Error ' + error);
			$('#alert-bandwidth').text('Connection error : ' + error);
		};

		// Log messages from the server
		connection.onmessage = function (e) {
			// console.log('Server: ' + e.data);

			var obj = JSON.parse(e.data);
			updateChart(obj.loc_Ko, obj.in_Ko , obj.out_Ko,obj.Ko);
		};

		connection.onclose = function (e) {
			console.log('Deconnexion tentative de reconnexion dans 5 sec');
			$('#alert-bandwidth').html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(connect, 5000);
		};

	}
	
	connect();



}

