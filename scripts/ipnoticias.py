#! /usr/bin/python3

import requests
import os

client_id = '4p7co79ke3c09hydlf071ouvy8coa1'  # Tu Client-ID de Twitch

def grab_twitch(channel_name):
    headers = {
        'Client-ID': client_id,
        'Content-Type': 'application/json',
    }
    data = {
        'operationName': "PlaybackAccessToken_Template",
        'query': """
        query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, $isVod: Boolean!, $playerType: String!) {
          playbackAccessToken(login: $login, isLive: $isLive, vodID: $vodID, isVod: $isVod, playerType: $playerType) {
            value
            signature
            __typename
          }
        }""",
        'variables': {
            'isLive': True,
            'login': channel_name,
            'isVod': False,
            'vodID': '',
            'playerType': 'channel_home_live',
        }
    }
    response = requests.post('https://gql.twitch.tv/gql', headers=headers, json=data)
    if response.status_code == 200:
        json_response = response.json()
        token = json_response['data']['playbackAccessToken']['value']
        sig = json_response['data']['playbackAccessToken']['signature']
        m3u8_url = f"https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8?client_id={client_id}&token={token}&sig={sig}&allow_audio_only=true&allow_source=true&type=any"
        return m3u8_url
    else:
        print("Error fetching Twitch M3U8 link")
        return None

def main():
    with open('ipnoticias.m3u8', 'w') as m3u8_file:  # Ajusta la ruta si es necesario
        m3u8_file.write('#EXTM3U\n')
        m3u8_file.write('#EXT-X-VERSION:3\n')
        m3u8_file.write('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000\n')
        with open('ipnoticias.txt') as f:  # Ajusta la ruta si es necesario
            for line in f:
                line = line.strip()
                if not line or line.startswith('~~') or 'twitch.tv' not in line:
                    continue
                channel_name = line.split('/')[-1]
                m3u8_link = grab_twitch(channel_name)
                if m3u8_link:
                    m3u8_file.write(f'{m3u8_link}\n')

if __name__ == "__main__":
    main()

# Limpieza de archivos temporales, si existen
if 'temp.txt' in os.listdir('.'):
    os.system('rm temp.txt')
