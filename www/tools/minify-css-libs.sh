#!/bin/sh


FILES=""
FILES=$FILES" ../lib/leaflet/leaflet.css"
FILES=$FILES" ../lib/bootstrap/css/bootstrap.css"
FILES=$FILES" ../lib/rendro-easy-pie/jquery.easy-pie-chart.css"




cat $FILES > tmp.css
java -jar yuicompressor.jar tmp.css > ../minify/libs.min.css
rm tmp.css