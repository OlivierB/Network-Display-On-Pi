#!/bin/sh


FILES=""

# Network manager
FILES=$FILES" ../script/network/AjaxManager.js"
FILES=$FILES" ../script/network/WebSocketManager.js"

FILES=$FILES" ../script/network/DataDispatcher.js"
FILES=$FILES" ../script/network/loader.js"

# Tools classes
FILES=$FILES" ../script/text/TextFormatter.js"

# Resize class
FILES=$FILES" ../script/resize/resize.js"

# Widget classes
FILES=$FILES" ../script/chart/BandwidthChart.js"
FILES=$FILES" ../script/chart/BandwidthChartAjax.js"

FILES=$FILES" ../script/text/BandwidthText.js"
FILES=$FILES" ../script/text/BandwidthTextAjax.js"


FILES=$FILES" ../script/snort/BaseAlert.js"

FILES=$FILES" ../script/chart/StackedColumnChart.js"
FILES=$FILES" ../script/chart/StackedColumnChartAjax.js"

FILES=$FILES" ../script/dns/DnsDisplayer.js"
FILES=$FILES" ../script/dns/DnsDisplayerText.js"
FILES=$FILES" ../script/dns/BubbleDns.js"
FILES=$FILES" ../script/dns/DnsDisplayerCanvas.js"

FILES=$FILES" ../script/map/IpLocationMap.js"
FILES=$FILES" ../script/map/IpLocationMapOffline.js"
FILES=$FILES" ../script/map/IpLocationMapOnline.js"

# FILES=$FILES" ../script/network3D/Ray.js"
# FILES=$FILES" ../script/network3D/Scene3D.js"
# FILES=$FILES" ../script/network3D/Satellite3D.js"
# FILES=$FILES" ../script/network3D/InformationsDisplay.js"

FILES=$FILES" ../script/chart/PercentCounterChart.js"
FILES=$FILES" ../script/chart/ServerStat.js"

FILES=$FILES" ../script/chart/SummaryCanvas.js"

FILES=$FILES" ../script/chart/BandwidthChartWebsocket.js"
FILES=$FILES" ../script/text/BandwidthTextWebsocket.js"

FILES=$FILES" ../script/chart/BarChart.js"
FILES=$FILES" ../script/chart/BarChartWebsocket.js"


# minify JS
uglifyjs $FILES --output ../minify/script.min.js --mangle --compress

