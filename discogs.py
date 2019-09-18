import requests
import json
import urllib

from discogs_client import Client

from config import *
from access_tokens import *


class DiscogsWrapper:
    """
    An OAuth athentication wrapper for discogs API
    """
    def __init__ (self):
        self.consumer_key = 'pDGCsGkOvnpeoypQDyMp'
        self.consumer_secret = 'MXrkZgMMofvlTBVMWwGIYIgdfjXWXhvM'


        self.client = Client('AlbumCoverSearch/1.0', user_token=access_token)
        self.header = {'User-Agent': 'AlbumCoverSearch/1.0'}

    def search(self, params):
        # takes params as dict and return search results as json
        url = 'https://api.discogs.com/database/search?'
        for key, value in params.items():
            url += key + '=' + value + '&'

        # url += 'token=' + self.user_token
        # TODO: Setup OAUth so we can use token
        url += 'key=' + consumer_key
        url += '&secret=' + consumer_secret
    
        print(url)
        response = requests.get(url, headers=self.header).text
        data = json.loads(response)
        try:
            item = data['results'][0]
            cover_url = item['cover_image']
            cover_id = str(item['id']) 
            request = urllib.request.Request(url, headers=self.header)
            response = urllib.request.urlopen(request)
            return response, cover_id
        except IndexError:
            print(f"Nothing found for {params['artist']}")


        




# a = DiscogsSearch('qjraMiiuJBJJIBPFfNFFHsoyItSMLKveQaSiRWoK')
# results = a.search({'title': 'Revolver', 'artist': 'Beatles', 'format': 'album'})
# image_url, image_id = get_image_url(results)
# print(image_url, image_id)
# response = a.get_image(image_url)
# binary_str = response.read()
# file_obj = open('images/' + image_id + '.jpg', 'wb')
# file_obj.write(binary_str)
# file_obj.close()
