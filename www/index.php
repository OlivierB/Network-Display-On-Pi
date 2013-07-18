<?php
include 'ndop.conf.php';
include 'pages/common.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>NDOP</title>
    
    <!-- library CSS-->
    <link rel="stylesheet" href="/lib/font-awesome/css/font-awesome.min.css">
    <link rel="stylesheet" href="/lib/rendro-easy-pie/jquery.easy-pie-chart.css">
    <link rel="stylesheet" href="/lib/bootstrap/css/bootstrap.css">
    <link rel="stylesheet" href="/lib/leaflet/leaflet.css" />

    

    <!-- Load js IPs address configuration from the database -->
    <script language="javascript" type="text/javascript" src="/pages/load_conf.php"></script>
    
<?php if(NDOP::$app['debug']){ ?>


    <!-- Personnal CSS -->
    <link rel="stylesheet" href="/style/slide.css">
    <link rel="stylesheet" href="/style/main.css">
    <link rel="stylesheet" href="/style/chart.css">
    <link rel="stylesheet" href="/style/resize.css">



    <!-- library JS -->
    <script src="/lib/canvasjs.min.js"></script>
    <script src="/lib/jquery-2.0.2.min.js"></script>
    <script src="/lib/jquery.slides.min.js"></script>
    <script src="/lib/rendro-easy-pie/jquery.easy-pie-chart.js"></script>
    <script src='/lib/jquery-number.js'></script>
    <script src='/lib/bootstrap/js/bootstrap.min.js'></script>
    <script src="/lib/leaflet/leaflet.js"></script>
    <script src="/lib/three.min.js"></script>
    <script src="/lib/OrbitControls.js"></script>


    <!-- Personnal JS -->
    <script src="/script/resize/resize.js"></script>
    <script src='/script/slide/slide-conf.js'></script>

    <script src="/script/network/AjaxManager.js"></script>
    <script src="/script/network/WebSocketManager.js"></script>

    <script src='/script/network/DataDispatcher.js'></script>
    <script src='/script/network/loader.js'></script>

    <script src="/script/text/TextFormatter.js"></script>

    



    <script src="/script/chart/BandwidthChart.js"></script>
    <script src="/script/chart/BandwidthChartAjax.js"></script>
    <script src="/script/snort/BaseAlert.js"></script>

    <script src="/script/snort/BaseAlert.js"></script>

    <script src="/script/text/BandwidthText.js"></script>
    <script src="/script/text/BandwidthTextAjax.js"></script>

    <script src="/script/chart/StackedColumnChart.js"></script>
    <script src="/script/chart/StackedColumnChartAjax.js"></script>

    <script src="/script/dns/DnsDisplayer.js"></script>
    <script src="/script/dns/DnsDisplayerText.js"></script>
    <script src="/script/dns/BubbleDns.js"></script>
    <script src="/script/dns/DnsDisplayerCanvas.js"></script>

    <script src="/script/map/IpLocationMap.js"></script>
    <script src="/script/map/IpLocationMapOffline.js"></script>
    <script src="/script/map/IpLocationMapOnline.js"></script>

    <script src="/script/network3D/Ray.js"></script>
    <script src="/script/network3D/Scene3D.js"></script>
    <script src="/script/network3D/Satellite3D.js"></script>
    <script src="/script/network3D/InformationsDisplay.js"></script>

    <script src="/script/chart/PercentCounterChart.js"></script>
    <script src="/script/chart/ServerStat.js"></script>

    <script src="/script/chart/SummaryCanvas.js"></script>

    <script src="/script/chart/BandwidthChartWebsocket.js"></script>
    <script src="/script/text/BandwidthTextWebsocket.js"></script>

    <script src="/script/chart/BarChart.js"></script>
    <script src="/script/chart/BarChartWebsocket.js"></script>


    

<?php }else{ ?>
    <!-- Minified CSS -->
    <link rel="stylesheet" href="/minify/libs.min.css">
    <link rel="stylesheet" href="/minify/style.min.css">

    <!-- Minified JS -->
    <script src="/minify/libs.3d.min.js"></script>
    <script src="/minify/libs.min.js"></script>
    <script src="/minify/script.min.js"></script>

<?php } ?>


</head>

<body>
    <!-- All pages are included here, slideJS handle the animation -->

    
    
    <div id="slides" >

        <?php
        
        NDOP::$app = parse_ini_file('ndop.conf.ini');

        if( isset(NDOP::$app['database_address']) && 
            isset(NDOP::$app['database_login']) && 
            isset(NDOP::$app['database_password']) )
        {
            try {
                NDOP::$app['db'] = new PDO("mysql:host=".NDOP::$app['database_address'].";dbname=NDOP_GUI", NDOP::$app['database_login'], NDOP::$app['database_password']);
                NDOP::$app['db']->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                $sql = "SELECT `module`.`name`, `module`.`id` FROM `layout` JOIN `module` ON `layout`.`id_module` = `module`.`id` GROUP BY `layout`.`page`";
                $results = NDOP::$app['db']->query($sql);
                $pages = $results->fetchAll(PDO::FETCH_ASSOC);

                foreach ($pages as $key => $value) {
                    echo "<div>";
                    display_module($value['name'], $value['id']);
                    echo "</div>";
                }
            }
            catch(PDOException $e)
            {
                echo "<div>";
                include "modules/introduction/index.php";
                echo "</div>";
            }
        }
        ?>
    </div>
</body>
</html>
