import requests
import os

client_id = '4p7co79ke3c09hydlf071ouvy8coa1'
# Asegúrate de obtener y usar tu token de acceso de aplicación aquí.
access_token = '94a1h60airzvo0btb0rwv0xhb3zkcr'

def grab_twitch(channel_url):
    if "twitch.tv" in channel_url:
        channel_name = channel_url.split('/')[-1]
    else:
        print(f"URL no válida, omitiendo: {channel_url}")
        return None

    print(f"Procesando canal: {channel_name}")
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
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
        print(f"Error: La API de Twitch retornó el código de estado {response.status_code}")
        return None

# Ajusta la implementación de main() y otras funciones según sea necesario.
