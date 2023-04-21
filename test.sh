#!/bin/bash

# file="ABC I&O: https://cooperost.icsconnect.com/.js"
#
# filename=$(basename $file)
# filename=${filename%.*}
# echo $filename
# jsname=${filename//[ &:/\\\.]/_}
#
# echo $jsname


# string="ABC I&O: https://cooperost.icsconnect.com/.js"
string="Fun yes here.js"

# remove any leading or trailing spaces
string=$(echo "$string" | xargs)

# extract characters before .js
filename=${string%%.js}

echo $filename
