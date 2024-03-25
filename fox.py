import requests
import re

# La URL del script PHP que quieres acceder
url_php = 'http://pe.shortgod.com/volve24/tv11.php?id=77'

# Realizamos la petición a la URL
response = requests.get(url_php)

# Aquí deberías utilizar una expresión regular o algún método para extraer la URL final del contenido
# Este paso depende mucho de cómo se entrega el contenido. Aquí hay un ejemplo de cómo podrías buscar una URL dentro de la respuesta:
url_media = re.search("(http[s]?://[^\s]+\.m3u8)", response.text)

if url_media:
    url_media = url_media.group(0)
    # Crear el archivo M3U8
    with open("fox.m3u8", "w") as file:
        file.write("#EXTM3U\n")
        file.write("#EXT-X-VERSION:3\n")
        file.write("#EXTINF:-1, Canal\n")
        file.write(url_media + "\n")
    print("Archivo M3U8 creado con éxito.")
else:
    print("No se pudo encontrar la URL del contenido.")
