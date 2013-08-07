/**
 * Handle the connection with the server programm and dispatch the data to each module
 * which subscribes to the corresponding protocol.
 *
 * @author Matrat Erwan
 **/

function DataDispatcher(serverAddress) {
    this.websocketManagers = [];
    this.connections = [];
    this.serverAddress = serverAddress;
}

/**
 * Register a module (which inherits from WebsocketManager) with the protocol it requires.
 * When this protocol will receive a data, this data will be sent to this module.
 * If the protocol has never been suscribed at, a new connection to the server will be
 * attempted using the protocol.
 **/
DataDispatcher.prototype.register = function(websocketManager, protocol) {
    if (!(protocol in this.websocketManagers)) {
        this.websocketManagers[protocol] = [];
        this.connectToProt(this.serverAddress, protocol);
    }

    this.websocketManagers[protocol].push(websocketManager);
};


/**
 * Try to connect to the server and construct callbacks which will handle the differents
 * scenarii and dispatch the data to the suscribing modules.
 **/
DataDispatcher.prototype.connectToProt = function(serverAddress, prot) {

    var connection = new WebSocket(serverAddress, prot);

    // When the connection is open, informs all the modules
    connection.onopen = function() {
        if(connection.protocol == prot){
            console.log("Main connexion");
            this.protocolNotSupported = false;
            var i = 0,
                length = this.websocketManagers[prot].length;

            for (; i < length; i++) {
                this.websocketManagers[prot][i].onopen();
            }
            this.connections.push(connection);
        }else{
            // if the protocol is not supported, we close the connection with
            // the "protocolNotSupported" flag
            var i = 0,
                length = this.websocketManagers[prot].length;

            for (; i < length; i++) {
                this.websocketManagers[prot][i].protocolNotSupported = true;
                this.protocolNotSupported = true;
            }
            connection.close();
        }
    }.bind(this);

    // Log errors
    connection.onerror = function(error) {
        var i = 0,
            length = this.websocketManagers[prot].length;

        for (; i < length; i++) {
            this.websocketManagers[prot][i].onerror(error);
        }
        
    }.bind(this);

    // dispatch messages from the server to the corresponding modules
    connection.onmessage = function(e) {
        var obj = JSON.parse(e.data);
        var i = 0,
            length = this.websocketManagers[prot].length;

        for (; i < length; i++) {
            this.websocketManagers[prot][i].onmessage(obj);
        }
    }.bind(this);

    connection.onclose = function(e) {
        var i = 0,
            length = this.websocketManagers[prot].length;
        for (; i < length; i++) {
            this.websocketManagers[prot][i].onclose(e);
        }

        if (this.protocolNotSupported) {
            console.log('Protocol Not Supported : ' + prot);
        } else {
            setTimeout(function() {
                this.connectToProt(serverAddress, prot);
            }.bind(this), 5000);
        }
    }.bind(this);

};

