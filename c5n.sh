#!/bin/bash

echo $(dirname $0)

python3 -m pip install requests

cd $(dirname $0)/scripts/

python3 c5n.py > ../c5n.m3u8

echo m3u8 grabbed
