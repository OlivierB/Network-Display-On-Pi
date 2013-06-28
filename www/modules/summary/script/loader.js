var canvas = new SummaryCanvas('canvas-summary-container');
canvas.connect(App.webServerAddress, "/pages/sql_request.php?request=total_bandwidth", 100000);