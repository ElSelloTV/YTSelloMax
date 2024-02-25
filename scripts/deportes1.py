#! /usr/bin/python3

import requests
import re
import os
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab_okru(url):
    # Intentaremos imitar la solicitud que se hace desde el navegador para obtener la URL del .m3u8
    headers = {
        'Referer': 'https://ok.ru/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # Suponiendo que la URL del .m3u8 se pueda encontrar directamente en el contenido de la página
        m3u8_urls = re.findall(r'https://[^\s"]+\.m3u8[^\s"]*', response.text)
        if m3u8_urls:
            # Imprime la URL del .m3u8 encontrado
            print('#EXTM3U')
            print('#EXT-X-VERSION:3')
            print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
            print(m3u8_urls[0])
        else:
            # Manejo en caso de no encontrar la URL del .m3u8
            print('No se encontró el stream .m3u8 o no se pudo acceder a él')
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
with open('../deportes1.txt') as f:  # Asegúrate de ajustar la ruta del archivo según sea necesario
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
            grab_okru(line)

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')

