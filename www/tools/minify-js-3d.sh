#!/bin/sh

# 3D script are minified in a separate file because it's 
# better not to to include it for smaller configuration

# minify 3D libs
FILES=""

FILES=$FILES" ../lib/three.min.js"
FILES=$FILES" ../lib/OrbitControls.js"

# minify 3D personnal script
FILES=$FILES" ../script/network3D/Ray.js"
FILES=$FILES" ../script/network3D/Scene3D.js"
FILES=$FILES" ../script/network3D/Satellite3D.js"
FILES=$FILES" ../script/network3D/InformationsDisplay.js"

uglifyjs $FILES --output ../minify/3d.min.js --mangle --compress 