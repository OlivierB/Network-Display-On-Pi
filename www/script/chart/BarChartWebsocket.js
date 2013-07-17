/**
 * BarChartWebsocket, displays the data sent by the NDOP program via websocket.
 * @author Matrat Erwan
 **/

function BarChartWebsocket(id, id_data, title) {

    // inheritance from WebSocketManager
    WebSocketManager.call(this, id + '-alert');

    // inheritance from BarChart
    BarChart.call(this, id, title);

    this.id = id;
    this.id_data = id_data;
    this.container = $('#' + this.id);
}

// inheritance from WebSocketManager
BarChartWebsocket.prototype = Object.create(WebSocketManager.prototype);

// inheritance from BarChart
BarChartWebsocket.prototype.updateChart = BarChart.prototype.updateChart;

BarChartWebsocket.prototype.dataManager = function(obj) {
    this.updateChart(obj[this.id_data]);
};