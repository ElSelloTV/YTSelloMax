import os
import sys

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

with open('../ipnoticias.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        # Si la línea contiene la URL M3U8 específica, la procesa directamente
        if line.startswith('http://tv.teleclub.xyz/envivo/Cultura/DISCOVERY_CHANNEL/index.m3u8'):
            print(line)  # Imprime o procesa la URL M3U8 directamente

# Limpieza de archivos temporales si existen
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
