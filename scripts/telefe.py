#! /usr/bin/python3

import os
import sys
import requests
import re

windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    response = requests.get(url).text
    m3u8_match = re.search(r'(https?://[^\s]+\.m3u8)', response)

    if m3u8_match:
        stream_url = m3u8_match.group(1)
        print(stream_url)
    else:
        print(f"No se encontró enlace .m3u8 para {url}")

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

with open('../telefe.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            line = line.split('|')
            ch_name = line[0].strip()
            grp_title = line[1].strip().title()
            tvg_logo = line[2].strip()
            tvg_id = line[3].strip()
        else:
            grab(line)
