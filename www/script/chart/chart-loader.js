
var chart = new BandwidthChart("bandwidth");
chart.connect(App.serverAddress, App.bandwidtProtocol);



var procChart = new PercentCounterChart('proc', 'proc_load', 100);
procChart.connect(App.serverAddress, App.serverStatProtocol);

var procChart = new PercentCounterChart('memory', 'mem_load', 100);
procChart.connect(App.serverAddress, App.serverStatProtocol);

var procChart = new PercentCounterChart('stuff', 'swap_load', 100);
procChart.connect(App.serverAddress, App.serverStatProtocol);

