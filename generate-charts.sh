#!/bin/bash

set -euo pipefail

shopt -s nullglob
for fit in archive/*.fit; do
    basefit=$(basename "$fit")
    outpng="charts/${basefit%.fit}.png"
    if [ ! -f "$outpng" ]; then
        python app.py "$fit" "$outpng"
    fi
done


