var chart = new BandwidthChartAjax("daily-bandwidth-chart");
chart.connect(App.webServerAddress, "/modules/dailyTraffic/sql/daily_bandwidth.php", 1000);

var text = new TotalBandwidthText('total-bandwidth-text');
text.connect(App.webServerAddress, "/modules/dailyTraffic/sql/total_daily_bandwidth.php", 60000);