function PercentCounterChart(id, id_data, speed){
	this.speed = speed | 100;

	this.id = id;
	this.id_data = id_data;

	this.chart = $('#' + id);
	this.alertContainer = $('#' + id + '-alert');
	this.chart.easyPieChart({
		animate: this.speed
	});
}


PercentCounterChart.prototype = {
	constructor: PercentCounterChart,

	updateChart : function (percent) {
		this.chart.data('easyPieChart').update(percent);
		$('#' + this.id + " span").text(percent + "%");
		
	},

	connect : function (address, protocol){

		this.address = address || App.serverAddress || 'localhost';
		this.prot = protocol || App.ServerStatProtocol || 'server_stat';


		this.connection = new WebSocket(this.address, this.prot);

		// When the connection is open, send some data to the server
		this.connection.onopen = function () {
		  this.connection.send('Ping'); // Send the message 'Ping' to the server
		  this.alertContainer.html('');
		}.bind(this);

		// Log errors
		this.connection.onerror = function (error) {
			console.log('WebSocket Error ' + error);
			this.alertContainer.text(error);
		}.bind(this);

		// Log messages from the server
		this.connection.onmessage = function (e) {
			// console.log('Server: ' + e.data);

			var obj = JSON.parse(e.data);

			this.updateChart(obj[this.id_data]);
			

		}.bind(this);

		this.connection.onclose = function (e) {
			// console.log('Deconnexion tentative de reconnexion dans 5 sec !');
			this.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(function(){this.connect(this.address, this.prot);}, 5000);
		}.bind(this);
	}
}










