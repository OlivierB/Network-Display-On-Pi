/**
* BandwidthTextWebsocket class displaying bandwidth informations in a text format.
* Data come from the websocket connected to the NDOP program.
* @author Matrat Erwan
**/

function BandwidthTextWebsocket(id, font_size) {

 // inheritance from BandwidthText
 BandwidthText.call(this, id, font_size);

 // inheritance from WebSocketManager
 WebSocketManager.call(this, id + '-alert');
}


// inheritance from WebSocketManager
BandwidthTextWebsocket.prototype = Object.create(WebSocketManager.prototype);

// inheritance from BandwidthText
BandwidthTextWebsocket.prototype.dataManager = BandwidthText.prototype.dataManager;