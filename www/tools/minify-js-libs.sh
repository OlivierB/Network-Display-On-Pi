#!/bin/sh


# minify libs JS
FILES=""

FILES=$FILES" ../lib/canvasjs.min.js"
FILES=$FILES" ../lib/jquery-2.0.2.min.js"
FILES=$FILES" ../lib/jquery.slides.min.js"
FILES=$FILES" ../lib/rendro-easy-pie/jquery.easy-pie-chart.js"
FILES=$FILES" ../lib/jquery-number.js"
FILES=$FILES" ../lib/bootstrap/js/bootstrap.min.js"
FILES=$FILES" ../lib/leaflet/leaflet.js"




# minify JS LIBS
uglifyjs $FILES --output ../minify/libs.min.js --mangle --compress 



