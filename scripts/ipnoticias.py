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
        print(m3u8_url)
    else:
        print("Error fetching Twitch M3U8 link")

def main():
    print('#EXTM3U')
    print('#EXT-X-VERSION:3')
    print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')
    with open('../ipnoticias.txt') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('~~'):
                continue
            elif 'twitch.tv' in line:
                channel_name = line.split('/')[-1]  # Asume que la URL es del formato twitch.tv/nombre_del_canal
                grab_twitch(channel_name)

if __name__ == "__main__":
    main()

if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
