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
string="new_runteimt_a-fun.js"

# remove any leading or trailing spaces
string=$(echo "$string" | xargs)

# extract characters before .js
filename=${string%%.js}

echo $filename
