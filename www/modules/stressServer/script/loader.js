var chart = new PaquetLossChartWebsocket("paquet-loss-live-chart");
chart.connect(dispatcher, App.packetLossProtocol);

var chart = new PaquetLossChartAjax("paquet-loss-day-chart");
chart.connect(App.webServerAddress, "/pages/sql_request.php?request=packet_loss&day_before_begin=7&day_before_end=0", 60000);
