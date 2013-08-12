/**
 * BandwidthChartWebsocket, displays the current bandwidth in a chart.
 * Receive the data via websocket by the NDOP program.
 * @author Matrat Erwan
 **/


function BandwidthChartWebsocket(id, style_line){
    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');
    
    // inheritance from BandwidthChart
    BandwidthChart.call(this, id, true, 100, style_line);
}


// inheritance from WebSocketManager
BandwidthChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// method needed to make the BandwidthChartWebsocket inheritance works
BandwidthChartWebsocket.prototype.dataManager = function(obj) {
    this.updateChart(obj.loc_Ko, obj.in_Ko, obj.out_Ko, obj.Ko);
    this.refresh();
};

// inheritance from BandwidthChart
BandwidthChartWebsocket.prototype.updateChart = BandwidthChart.prototype.updateChart;
BandwidthChartWebsocket.prototype.refresh = BandwidthChart.prototype.refresh;