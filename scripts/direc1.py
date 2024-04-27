import requests
import os

def grab(url):
    s = requests.Session()
    response = s.get(url, timeout=15).text
    if '.m3u8' not in response:
        print('No se encontró M3U8 válido en la respuesta.')
        return  # Si no se encuentra ningún archivo m3u8, termina la función

    end = response.find('.m3u8') + 5
    tuner = 100
    while True:
        if 'https://' in response[end-tuner:end]:
            link = response[end-tuner:end]
            start = link.find('https://')
            end = link.find('.m3u8') + 5
            return link[start:end]
        else:
            tuner += 5
            if tuner > len(response):  # Previene un bucle infinito si no se encuentra el enlace
                print('No se pudo localizar el enlace M3U8.')
                return

def main():
    # Leer el enlace m3u8 del archivo 'ruta.txt'
    with open("ruta.txt", "r") as file:
        m3u8_url = file.readline().strip()
    
    if m3u8_url:
        final_link = grab(m3u8_url)
        if final_link:
            # Escribir la estructura M3U8 en 'direc1.m3u8'
            with open("direc1.m3u8", "w") as m3u8_file:
                m3u8_file.write("#EXTM3U\n")
                m3u8_file.write("#EXT-X-VERSION:3\n")
                m3u8_file.write("#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n")
                m3u8_file.write(final_link + "\n")
            print(f"Archivo M3U8 creado con éxito: {final_link}")
    else:
        print("No se encontró URL M3U8 en 'ruta.txt'.")

if __name__ == "__main__":
    main()

