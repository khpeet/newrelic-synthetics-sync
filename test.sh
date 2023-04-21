#!/bin/bash

# file="ABC I&O: https://cooperost.icsconnect.com/.js"
#
# filename=$(basename $file)
# filename=${filename%.*}
# echo $filename
# jsname=${filename//[ &:/\\\.]/_}
#
# echo $jsname


# echo "[\"scripts/New Runtime Example.js\",\"scripts/runtime2.js\"]" | jq -r '.[]'
changed_files=$(echo "[\"scripts/New Runtime Example.js\",\"scripts/runtime2.js\"]" | jq -r '.[]')
echo $changed_files
filenames=()
for file in $changed_files; do
  monitorName=$(echo basename ${f%.*} | sed "s/.*\///")
  echo $monitorName
  filenames+=("$monitorName")
done
echo $filenames
