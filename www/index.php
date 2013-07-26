<?php
require 'ndop.conf.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>NDOP</title>
    

    <!-- Load js IPs address configuration from the database -->
    <script language="javascript" type="text/javascript" >
        <?= NDOP::load_JS_conf(); ?>
    </script>
    
<?php if(NDOP::$app['debug']){ ?>

    <!-- library CSS -->
    <link rel="stylesheet" href="lib/rendro-easy-pie/jquery.easy-pie-chart.css">
    <link rel="stylesheet" href="lib/bootstrap/css/bootstrap.css">
    <link rel="stylesheet" href="lib/leaflet/leaflet.css" />
   

    <!-- Personnal CSS -->
    <link rel="stylesheet" href="style/slide.css">
    <link rel="stylesheet" href="style/main.css">
    <link rel="stylesheet" href="style/chart.css">
    <link rel="stylesheet" href="style/resize.css">



    <!-- library JS -->
    <script src="lib/canvasjs.min.js"></script>
    <script src="lib/jquery-2.0.2.min.js"></script>
    <script src="lib/jquery.slides.min.js"></script>
    <script src="lib/rendro-easy-pie/jquery.easy-pie-chart.js"></script>
    <script src='lib/jquery-number.js'></script>
    <script src='lib/bootstrap/js/bootstrap.min.js'></script>
    <script src="lib/leaflet/leaflet.js"></script>
    


    <!-- Personnal JS -->
    <script src="script/resize/resize.js"></script>
    <script src='script/slide/slide-conf.js'></script>

    <script src="script/network/AjaxManager.js"></script>
    <script src="script/network/WebSocketManager.js"></script>

    <script src='script/network/DataDispatcher.js'></script>
    <script src='script/network/loader.js'></script>

    <script src="script/text/TextFormatter.js"></script>

    
    <script src="script/chart/BandwidthChart.js"></script>
    <script src="script/chart/BandwidthChartAjax.js"></script>
    <script src="script/snort/BaseAlert.js"></script>

    <script src="script/snort/BaseAlert.js"></script>

    <script src="script/text/BandwidthText.js"></script>
    <script src="script/text/BandwidthTextAjax.js"></script>

    <script src="script/chart/StackedColumnChart.js"></script>
    <script src="script/chart/StackedColumnChartAjax.js"></script>

    <script src="script/dns/DnsDisplayer.js"></script>
    <script src="script/dns/DnsDisplayerText.js"></script>
    <script src="script/dns/BubbleDns.js"></script>
    <script src="script/dns/DnsDisplayerCanvas.js"></script>

    <script src="script/map/IpLocationMap.js"></script>
    <script src="script/map/IpLocationMapOffline.js"></script>
    <script src="script/map/IpLocationMapOnline.js"></script>

    <script src="script/chart/PercentCounterChart.js"></script>
    <script src="script/chart/ServerStat.js"></script>

    <script src="script/chart/SummaryCanvas.js"></script>

    <script src="script/chart/BandwidthChartWebsocket.js"></script>
    <script src="script/text/BandwidthTextWebsocket.js"></script>

    <script src="script/chart/BarChart.js"></script>
    <script src="script/chart/BarChartWebsocket.js"></script>


    

<?php }else{ ?>
    <!-- Minified CSS -->
    <link rel="stylesheet" href="minify/libs.min.css">
    <link rel="stylesheet" href="minify/style.min.css">

    <!-- Minified JS -->
    <script src="minify/libs.min.js"></script>
    <script src="minify/script.min.js"></script>

<?php } ?>


</head>

<body>
    <!-- All pages are included here, slideJS handle the animation -->

    
    
    <div id="slides" >
        <?php NDOP::display_modules(); ?>
    </div>
</body>
</html>
