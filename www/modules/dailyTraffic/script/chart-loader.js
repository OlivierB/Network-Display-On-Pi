var chart = new BandwidthChartAjax("daily-bandwidth-chart");
chart.connect(App.webServerAddress, App.webServerPort, "/modules/dailyTraffic/sql/daily_bandwidth.php");