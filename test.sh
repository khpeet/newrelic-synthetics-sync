#!/bin/bash

files=$(echo "["scripts/New Runtime Example.js","scripts/runtime2.js"]" | tr '\n' ',' | sed 's/.$//')
echo $files

for f in files; do
  script=$(cat "$f")
  echo $script
done


# ["scripts/New Runtime Example.js","scripts/runtime2.js"]
#
#
# echo "["scripts/New Runtime Example.js","scripts/runtime2.js"]" | tr '\n' ',' | sed 's/.$//' > files.txt
