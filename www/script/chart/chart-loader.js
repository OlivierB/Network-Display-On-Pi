
var chart = new BandwidthChart("bandwidth-chart");
chart.connect(App.serverAddress, App.bandwidtProtocol);

var chart = new BandwidthText("bandwidth-text");
chart.connect(App.serverAddress, App.bandwidtProtocol);



var protocolChart = new PercentBarChart('protocol-ethernet', 'ethernet');
protocolChart.connect(App.serverAddress, App.protocolUseProtocol);

var protocolChart = new PercentBarChart('protocol-ip', 'ip');
protocolChart.connect(App.serverAddress, App.protocolUseProtocol);