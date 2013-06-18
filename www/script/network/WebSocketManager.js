/**
 * WebsocketManager
 * Abstract class, the inheritant class must implement a dataManager function
 * which will handle the incoming message in a JSon format.
 **/

WebSocketManager = function(id_alert_container) {
	this.alertContainer = $('#' + id_alert_container);
}


WebSocketManager.prototype.connect = function(address, protocol) {


	this.address = address || 'localhost';
	this.prot = protocol;

	this.connection = new WebSocket(this.address, this.prot);

	// When the connection is open, send some data to the server
	this.connection.onopen = function() {
		console.log("connexion");
		this.alertContainer.html('');
		this.connection.send('Ping'); // Send the message 'Ping' to the server

	}.bind(this);

	// Log errors
	this.connection.onerror = function(error) {
		console.log('WebSocket Error ' + error);
		this.protocolNotSupported = true;
	}.bind(this);

	// dispatch messages from the server
	this.connection.onmessage = function(e) {
		var obj = JSON.parse(e.data);
		this.dataManager(obj);
	}.bind(this);

	this.connection.onclose = function(e) {
		if (this.protocolNotSupported) {
			this.alertContainer.html('<span class="alert">Disconnected from server. Protocol not supported.</span>');
		}
		else{
			this.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
			setTimeout(
				this.connect(this.address, this.prot).bind(this), 50000);
		}
	}.bind(this);
}


