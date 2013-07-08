var chart = new PacketLossChartWebsocket("packet-loss-live-chart");
chart.connect(dispatcher, 'packet_loss');

var chart = new PacketLossChartAjax("packet-loss-day-chart");
chart.connect(App.webServerAddress, "/pages/sql_request.php?request=packet_loss&day_before_begin=7&day_before_end=0", 60000);
