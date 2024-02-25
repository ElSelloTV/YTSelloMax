#! /usr/bin/python3

import requests
import re
import os
import sys

# Asumiendo que estamos trabajando en un entorno similar al script original
windows = False
if 'win' in sys.platform:
    windows = True

def grab(url):
    try:
        response = requests.get(url, timeout=15)
        # Busca URLs que terminen en .m3u8 dentro del contenido de la respuesta
        m3u8_urls = re.findall(r'https://[^\s"]+\.m3u8[^\s"]*', response.text)
        
        if m3u8_urls:
            # Si encuentra alguna URL, imprime la primera
            print(m3u8_urls[0])
        else:
            # Manejo en caso de no encontrar la URL .m3u8
            if windows:
                print('https://raw.githubusercontent.com/ElSelloTV/YTSelloMax/main/assets/info.m3u8')
            else:
                print('No se encontró el stream .m3u8 segui intentando')
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")

# Inicia el script
if __name__ == "__main__":
    print('#EXTM3U')
    print('#EXT-X-VERSION:3')
    print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
    
    with open('deportes1.txt') as f:  # Asegúrate de tener la ruta correcta al archivo
        for line in f:
            line = line.strip()
            if not line or line.startswith('~~'):
                continue
            if line.startswith('https:'):
                grab(line)


