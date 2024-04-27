import requests
import os
import sys

def grab(url):
    s = requests.Session()
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        response = requests.get(url).text
        if '.m3u8' not in response:
            print('No se encontró M3U8 válido en la respuesta.')
            return  # Si no se encuentra ningún archivo m3u8, termina la función

    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner : end]:
            link = response[end-tuner : end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            break
        else:
            tuner += 5
            if tuner > len(response):  # Previene un bucle infinito si no se encuentra el enlace
                print('No se pudo localizar el enlace M3U8.')
                return

    streams = s.get(link[start:end]).text.split('#EXT')
    hd = streams[-1].strip()
    st = hd.find('http')
    print(hd[st:].strip())

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

# Leer el enlace m3u8 del archivo 'ruta.txt'
with open("main/ruta.txt", "r") as file:
    m3u8_url = file.readline().strip()
    if m3u8_url:
        grab(m3u8_url)

# Limpieza de archivos temporales si existen
if 'temp.txt' in os.listdir():
    os.remove('temp.txt')
