#!/bin/bash

echo [\"scripts/New Runtime Example.js\",\"scripts/runtime2.js\"]
changed_files=(${steps.changed-files.outputs.all_changed_files})
echo $changed_files

# ["scripts/New Runtime Example.js","scripts/runtime2.js"]
#
#
# echo "["scripts/New Runtime Example.js","scripts/runtime2.js"]" | tr '\n' ',' | sed 's/.$//' > files.txt
