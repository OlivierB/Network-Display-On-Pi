#!/bin/sh


FILES=""
FILES=$FILES" ../style/slide.css"
FILES=$FILES" ../style/main.css"
FILES=$FILES" ../style/chart.css"
FILES=$FILES" ../style/resize.css"

cat $FILES > tmp.css
java -jar yuicompressor.jar tmp.css > ../minify/style.min.css
rm tmp.css