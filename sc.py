#!/usr/bin/python3

import json
import base64
import requests
from bs4 import BeautifulSoup

session = requests.session()
soundcloud_response = session.get('https://soundcloud.com/tomcr00se/it-was-called-the-cold-war-because-russia-is-cold')
soup = BeautifulSoup(soundcloud_response.content, 'html5lib')
scripts = soup.findAll('script')
for s in scripts:
	if 'webpackJsonp' in s.text:
		desired_script = s
scary_json = json.loads(desired_script.text.split('var c=')[1].split(',o=Date.now()')[0])
for container in scary_json:
	for data in container['data']:
		if 'waveform_url' in data.keys():
			waveform_url = data['waveform_url']

song_id = waveform_url.split('/')[-1].split('_m.json')[0]
media_url = f'https://cf-hls-media.sndcdn.com/media/1/9999999/{song_id}.128.mp3'
decoded_policy = '{"Statement":[{"Resource":"*://cf-hls-media.sndcdn.com/media/*/*/'+song_id+'.128.mp3","Condition":{"DateLessThan":{"AWS:EpochTime":1522817126}}}]}'
policy = base64.b64encode(decoded_policy.encode('ascii')).decode('utf-8')

# https://stackoverflow.com/questions/2573919/creating-signed-urls-for-amazon-cloudfront
# https://github.com/soundcloud/sc-gaws/blob/master/aws/cloudfront/signature.go#L53
query_params = {
	'Policy': policy,
	'Signature': 'sYNNDisn~HU8HSEQqGMjfZrfZepf3P-zsLZQRwNnKHZaPyfFME16pHBHxmgK9zfkcpAIniZpu4SOMal9hAXiHpjx9yX~iyz6eMsr0aBddRz1M7AAtM3nk-yOjBuKxPDbuRYdPplCCLWuqQefMGMPxcyA36AlluRaS2qNEATjS23Gg4VqrGfxRyxChNkPgP3dCLEkO-xXDqHLd2VxcpgiuNsPvgS9kMbNQYcGbqcZlD0Y3yFjjffCthEsnMvAbNofcVVPg3wfHf8PV4GQd4FaBbr2vwVYouSw5qUXj0V3xHVYfjywuqyGLZbyFbgxjDjOJ7QrHdzTQ64TZBTkLffkfg__',
	'Key-Pair-Id': 'APKAJAGZ7VMH2PFPW6UQ'
}
#print(session.get(media_url, params=query_params))




###############################
#### Let's do this instead ####
###############################
#sc_client_id = 'Iy5e1Ri4GTNgrafaXe4mLpmJLXbXEfBR'
sc_client_id = 'ZJqyxkmTPZPDW1ytOfwCvqzGRZEFqUf2'
track_id = soup.findAll('meta', {'property': 'twitter:app:url:iphone'})[0]['content'].split(':')[-1]
medias_url = f'https://api.soundcloud.com/i1/tracks/{track_id}/streams'
query_params = {
	'client_id': sc_client_id
}
response = requests.request('GET', medias_url, params=query_params).json()
# http_mp3_128_url
# hls_mp3_128_url
# hls_opus_64_url
# preview_mp3_128_url
mp3_url = response['http_mp3_128_url']
mp3_response = requests.get(mp3_url, stream=True)
with open(f'Downloads/{track_id}.mp3', 'wb') as file:
        for chunk in mp3_response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
