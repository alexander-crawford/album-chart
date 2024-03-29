import requests
import config
from ratelimit import limits, sleep_and_retry

if __name__ == '__main__':
    getAlbumInfo(seach_string)

# no more than 60 calls in a 1 minute period
@sleep_and_retry
@limits(calls=60,period=60)
def getAlbumInfo(seach_string):
    url = "https://api.discogs.com/database/search"

    querystring = {
        "key":config.discogs_key,
        "secret":config.discogs_secret,
        "q":seach_string
    }

    response = requests.request("GET", url, params=querystring)

    dict = {}

    if response.status_code == 200:
        if (response.json()['pagination']['items'] > 0 and
            (response.json()['results'][0]['type']=='release' or
            response.json()['results'][0]['type']=='master')):

            dict['album_cover_url'] = response.json()['results'][0].get('cover_image')
            dict['album_year'] = response.json()['results'][0].get('year')

            return dict
        else:
            return None

    else:
        print('Discogs api FAIL')
        exit()
