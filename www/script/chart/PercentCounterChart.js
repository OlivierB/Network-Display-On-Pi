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
		var that = this;

		this.address = address || App.serverAddress || 'localhost';
		this.prot = protocol || App.ServerStatProtocol || 'server_stat';


		this.connection = new WebSocket(this.address, this.prot);

		// When the connection is open, send some data to the server
		this.connection.onopen = function () {
		  that.connection.send('Ping'); // Send the message 'Ping' to the server
		  that.alertContainer.html('');
		};

		// Log errors
		this.connection.onerror = function (error) {
			console.log('WebSocket Error ' + error);
			that.alertContainer.text(error);
		};

		// Log messages from the server
		this.connection.onmessage = function (e) {
			// console.log('Server: ' + e.data);

			var obj = JSON.parse(e.data);

			that.updateChart(obj[that.id_data]);
			

		};

		this.connection.onclose = function (e) {
			// console.log('Deconnexion tentative de reconnexion dans 5 sec !');
			that.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(function(){that.connect(that.address, that.prot);}, 5000);
		};
	}
}










