#! /usr/bin/python3

import requests
import re
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

# Esta función intentará encontrar la URL del stream .m3u8 en una página de ok.ru
def grab_okru(url):
    response = requests.get(url, timeout=15).text

    # Expresión regular para buscar la URL del .m3u8 dentro del contenido de la página
    # Esta expresión regular es un ejemplo y puede necesitar ser ajustada
    m3u8_urls = re.findall(r'https://[^\s"]+\.m3u8[^\s"]*', response)
    
    if m3u8_urls:
        # Si se encuentran URLs, asumimos la primera como la correcta
        print('#EXTM3U')
        print('#EXT-X-VERSION:3')
        print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
        print(m3u8_urls[0])
    else:
        # En caso de no encontrar el enlace .m3u8, imprimir un enlace predeterminado o manejar el error
        print('No se encontró el stream .m3u8')

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
with open('../deportes1.txt') as f:
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
            # Llamar a la función específica para ok.ru
            grab_okru(line)

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')

