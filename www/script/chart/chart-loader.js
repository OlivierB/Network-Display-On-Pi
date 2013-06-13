
var chart = new BandwidthChart("bandwidth");
chart.connect();

var procChart = new PercentCounterChart('proc', 'proc_load', 100);
procChart.connect();

var procChart = new PercentCounterChart('memory', 'mem_load', 100);
procChart.connect();

var procChart = new PercentCounterChart('stuff', 'swap_load', 100);
procChart.connect();

