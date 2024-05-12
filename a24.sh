#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/scripts/

python3 a24.py > ../a24.m3u8

echo m3u8 grabbed
