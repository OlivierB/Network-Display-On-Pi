
var chart = new BandwidthChartWebsocket("bandwidth-chart");
chart.connect(dispatcher, App.bandwidtProtocol);

var chart = new BandwidthTextWebsocket("bandwidth-text");
chart.connect(dispatcher, App.bandwidtProtocol);



var protocolChart = new BarChartWebsocket('protocol-ethernet', 'ethernet');
protocolChart.connect(dispatcher, App.protocolUseProtocol);

var protocolChart = new BarChartWebsocket('protocol-ip', 'ip');
protocolChart.connect(dispatcher, App.protocolUseProtocol);