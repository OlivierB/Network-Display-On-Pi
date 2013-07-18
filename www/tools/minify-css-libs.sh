#!/bin/sh


FILES=""
FILES=$FILES" ../lib/leaflet/leaflet.css"


cat $FILES > tmp.css
java -jar yuicompressor.jar tmp.css > ../minify/libs.min.css
rm tmp.css