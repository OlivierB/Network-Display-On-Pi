function DataDispatcher() {
	this.websocketManagers = [];
	this.connections = [];
}

DataDispatcher.prototype.register = function(websocketManager, protocol) {
	if (this.websocketManagers[protocol] == null)
		this.websocketManagers[protocol] = [];

	this.websocketManagers[protocol].push(websocketManager)
}


DataDispatcher.prototype.connect = function(serverAddress) {
	for (var prot in this.websocketManagers) {
		this.connectToProt(serverAddress, prot);
	}

}

DataDispatcher.prototype.connectToProt = function(serverAddress, prot) {

	var connection = new WebSocket(serverAddress, prot);

	// When the connection is open, send some data to the server
	connection.onopen = function() {
		console.log("Main connexion");
		for (var i = 0; i < this.websocketManagers[prot].length; i++) {
			this.websocketManagers[prot][i].onopen();
		}
		this.connections.push(connection);
	}.bind(this);

	// Log errors
	connection.onerror = function(error) {
		console.log('WebSocket Error ' + error);
		for (var i = 0; i < this.websocketManagers[prot].length; i++) {
			this.websocketManagers[prot][i].onerror(error);
		}
		this.protocolNotSupported = true;
	}.bind(this);

	// dispatch messages from the server
	connection.onmessage = function(e) {
		var obj = JSON.parse(e.data);
		for (var i = 0; i < this.websocketManagers[prot].length; i++) {
			this.websocketManagers[prot][i].onmessage(obj);
		}
	}.bind(this);

	connection.onclose = function(e) {
		for (var i = 0; i < this.websocketManagers[prot].length; i++) {
			this.websocketManagers[prot][i].onclose(e);
		}

		if (this.protocolNotSupported) {
			console.log('protocolNotSupported');
		} else {
			setTimeout(function() {
				this.connectToProt(serverAddress, prot)
			}.bind(this), 5000);
		}
	}.bind(this);

}