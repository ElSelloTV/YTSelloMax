import requests
import os

client_id = '4p7co79ke3c09hydlf071ouvy8coa1'
access_token = 'tu_token_de_acceso'

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
        token = json_response.get('data', {}).get('playbackAccessToken', {}).get('value')
        sig = json_response.get('data', {}).get('playbackAccessToken', {}).get('signature')
        if token and sig:
            m3u8_url = f"https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8?client_id={client_id}&token={token}&sig={sig}&allow_audio_only=true&allow_source=true&type=any"
            return m3u8_url
    else:
        print(f"Error: La API de Twitch retornó el código de estado {response.status_code}")
        return None

def main():
    # Ajusta las rutas relativas para acceder a la raíz del proyecto desde la subcarpeta Script
    path_to_ipnoticias_txt = os.path.join(os.path.dirname(__file__), '..', 'ipnoticias.txt')
    path_to_ipnoticias_m3u8 = os.path.join(os.path.dirname(__file__), '..', 'ipnoticias.m3u8')

    with open(path_to_ipnoticias_m3u8, 'w') as m3u8_file:
        m3u8_file.write('#EXTM3U\n')
        with open(path_to_ipnoticias_txt) as f:
            for line in f:
                line = line.strip()
                if 'twitch.tv' in line:
                    m3u8_link = grab_twitch(line)
                    if m3u8_link:
                        m3u8_file.write(f'#EXTINF:-1, {line}\n')
                        m3u8_file.write(f'{m3u8_link}\n')

if __name__ == "__main__":
    main()
