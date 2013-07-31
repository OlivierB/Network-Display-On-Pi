/**
 * WebsocketManager
 * Abstract class, the inheritant class must implement a dataManager function
 * which will handle the incoming message in a JSon format.
 * @author Matrat Erwan
 **/

function WebSocketManager(id_alert_container) {
    this.alertContainer = $('#' + id_alert_container);
}


WebSocketManager.prototype.connect = function(dataDispatcher, protocol) {
    dataDispatcher.register(this, protocol);
};

// When the connection is open, send some data to the server
WebSocketManager.prototype.onopen = function() {
    this.alertContainer.html('');
};

// Log errors
WebSocketManager.prototype.onerror = function(error) {
};

// dispatch messages from the server
WebSocketManager.prototype.onmessage = function(obj) {
    this.dataManager(obj);
};

WebSocketManager.prototype.onclose = function() {
    if (this.protocolNotSupported) {
        this.alertContainer.html('<span class="alert">Disconnected from server. Protocol not supported.</span>');
    } else {
        this.alertContainer.html('<span class="alert">Disconnected from server. Next try in 5 seconds.</span>');
    }
};