
<link rel="stylesheet" href="/lib/leaflet/leaflet.css" />
<script src="/lib/leaflet/leaflet.js"></script>

<link rel="stylesheet" href="/modules/mapOffline/style/map.css" />
<script type="text/javascript" src="/script/map/IpLocationMap.js"></script>
<script type="text/javascript" src="/script/map/IpLocationMapOnline.js"></script>
<script type="text/javascript" src="/script/map/IpLocationMapOffline.js"></script>


<?php header_display('Visited IPs around the world'); ?>

<div class='slide-div'>
	<span id="map-offline-alert"></span>
	<div class='height-full' id="map-offline"></div>
</div>

<script type="text/javascript" src="/modules/mapOffline/script/map-loader.js"></script>
