#!/bin/bash

# file="ABC I&O: https://cooperost.icsconnect.com/.js"
#
# filename=$(basename $file)
# filename=${filename%.*}
# echo $filename
# jsname=${filename//[ &:/\\\.]/_}
#
# echo $jsname


# FILES=/Users/kpeet/newrelic-synthetics-sync/scripts/*
#
# for f in $FILES; do
#   echo $f
# done
string="scripts/ABC I&O: https://cooperost.icsconnect.com/.js scripts/runtime2.js"

# split string into an array
IFS=' ' read -ra files <<< "$string"

# extract only file names and add to array
js_files=()
for file in "${files[@]}"; do
  filename=$(basename "$file")
  monitorName=$(echo basename ${f%.*} | sed "s/.*\///")
  echo $monitorName
  # filename=$(echo "$filename" | xargs)
  # jsname=${filename%%.js}
  monitors+=("$jsname")
done

echo "${monitors[@]}"
