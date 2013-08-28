/**
 * TopProtocolsWebsocket, displays the top used protocol.
 * Receive the data via websocket by the NDOP program.
 * @author Matrat Erwan
 **/


function TopProtocolsWebsocket(id){
    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');

    // inheritance from BandwidthChart
    // BandwidthChart.call(this, id, true, 100);
}


// inheritance from WebSocketManager
TopProtocolsWebsocket.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the TopProtocolsWebsocket inheritance works
TopProtocolsWebsocket.prototype.dataManager = function(obj) {
    console.log(obj);
};

// inheritance from BandwidthChart
// TopProtocolsWebsocket.prototype.updateChart = BandwidthChart.prototype.updateChart;
// TopProtocolsWebsocket.prototype.refresh = BandwidthChart.prototype.refresh;