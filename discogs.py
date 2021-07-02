import requests
import config
from ratelimit import limits

if __name__ == '__main__':
    getAlbumCover(seach_string)

# no more than 60 calls in a 1 minute period
@limits(calls=60,period=60)
def getAlbumCover(seach_string):
    url = "https://api.discogs.com/database/search"

    querystring = {
        "key":config.discogs_key,
        "secret":config.discogs_secret,
        "q":seach_string
    }

    response = requests.request("GET", url, params=querystring)

    dict = {}

    if response.json()['results'][0]['type']=='master' and response.status_code == 200:
        dict['album_cover_url'] = response.json()['results'][0]['cover_image']
        dict['album_year'] = response.json()['results'][0]['year']
        return dict
    else:
        return None
