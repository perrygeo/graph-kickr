#!/bin/bash

shopt -s nullglob
for fit in *.fit; do
    mv "$fit" archive/
done
