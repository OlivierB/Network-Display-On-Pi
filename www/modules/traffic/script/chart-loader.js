
var chart = new BandwidthChartWebsocket("bandwidth-chart");
chart.connect(dispatcher, 'bandwidth');

var chart = new BandwidthTextWebsocket("bandwidth-text");
chart.connect(dispatcher, 'bandwidth');



var protocolChart = new BarChartWebsocket('protocol-ethernet', 'ethernet');
protocolChart.connect(dispatcher, 'protocols');

var protocolChart = new BarChartWebsocket('protocol-ip', 'ip');
protocolChart.connect(dispatcher, 'protocols');