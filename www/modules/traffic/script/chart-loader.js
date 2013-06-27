
// var chart = new BandwidthChart("bandwidth-chart");

var chart = new BandwidthChartWebsocket("bandwidth-chart");
chart.connect(App.serverAddress, App.bandwidtProtocol);

var chart = new BandwidthTextWebsocket("bandwidth-text");
chart.connect(App.serverAddress, App.bandwidtProtocol);



var protocolChart = new BarChartWebsocket('protocol-ethernet', 'ethernet');
protocolChart.connect(App.serverAddress, App.protocolUseProtocol);

var protocolChart = new BarChartWebsocket('protocol-ip', 'ip');
protocolChart.connect(App.serverAddress, App.protocolUseProtocol);