#!/bin/bash

changed_files=$(echo "[\"scripts/New Runtime Example.js\"]" | jq -r '.[]')
