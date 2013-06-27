var chart = new BandwidthChartAjax("monthly-bandwidth-chart");
chart.connect(App.webServerAddress, "/pages/sql_request.php?request=bandwidth&day_before_begin=30&day_before_end=0", 60000);

var text = new TotalBandwidthText('monthly-total-bandwidth-text');
text.connect(App.webServerAddress, "/pages/sql_request.php?request=total_bandwidth&day_before_begin=30&day_before_end=0", 60000);

var chart = new StackedColumnChartAjax('monthly-protocol-use-chart', "Protocol use over the day");
chart.connect(App.webServerAddress, "/pages/sql_request.php?request=protocol_ethernet&day_before_begin=30&day_before_end=0", 60000);

var chart = new StackedColumnChartAjax('monthly-subprotocol-ipv4-use-chart', "Subprotocol IPV4 use over the day");
chart.connect(App.webServerAddress, "/pages/sql_request.php?request=subprotocol_ipv4&day_before_begin=30&day_before_end=0", 60000);