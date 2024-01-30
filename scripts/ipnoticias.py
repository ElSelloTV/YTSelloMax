import requests
import os
import sys

CLIENT_ID = '4p7co79ke3c09hydlf071ouvy8coa1'
ACCESS_TOKEN = 'tl68n46w6vg343bfa6s5yxeb3x439w'

def get_twitch_stream_url(channel_name):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={channel_name}', headers=headers).json()
    
    # Procesar la respuesta para obtener la URL del stream en formato M3U8
    # Nota: Este código es un esquema básico y puede requerir ajustes
    if 'data' in response and len(response['data']) > 0:
        stream_info = response['data'][0]
        # Aquí se debe implementar la lógica para obtener la URL del stream en 360p si está disponible.
        # La API de Twitch no proporciona directamente la URL del stream en formato M3U8.
        # Puede ser necesario utilizar otros métodos o servicios para obtener esta URL.
        return stream_info.get('thumbnail_url')  # Placeholder para URL del stream
    else:
        return 'Stream no disponible'

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

with open('../ipnoticias.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if line.startswith('https://www.twitch.tv/'):
            channel_name = line.split('/')[-1]
            stream_url = get_twitch_stream_url(channel_name)
            print(stream_url)

# Limpieza de archivos temporales si existen
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
