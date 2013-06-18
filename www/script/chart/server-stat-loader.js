

var procChart = new PercentCounterChart('proc', 'proc_load', 100);
procChart.connect(App.serverAddress, App.serverStatProtocol);

var memChartChart = new PercentCounterChart('memory', 'mem_load', 100);
memChartChart.connect(App.serverAddress, App.serverStatProtocol);

var swapChart = new PercentCounterChart('swap', 'swap_load', 100);
swapChart.connect(App.serverAddress, App.serverStatProtocol);