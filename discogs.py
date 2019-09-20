import requests
import json
import os
import time

from discogs_client import Client


USER_AGENT = 'AlbumCoverSearch/1.0'


class Discogs:
    """
    OAuth authentication wrapper for discogs API with 'search' method to 
    search for cover images.
    """
    def __init__(self):
        self.consumer_key = 'pDGCsGkOvnpeoypQDyMp'
        self.consumer_secret = 'MXrkZgMMofvlTBVMWwGIYIgdfjXWXhvM'

        if self.is_authenticated():
            from access_tokens import access_token, access_secret

            self.discogs = Client(USER_AGENT, consumer_key=self.consumer_key,
                                  consumer_secret=self.consumer_secret,
                                  token=access_token,
                                  secret=access_secret)
        # If user does not have access token and secret we need to use OAuth
        else: 
            self.discogs = Client(USER_AGENT)
            self.get_request_token()

    def get_request_token(self):
        self.discogs.get_consumer_key(self.consumer_key, self.consumer_secret)
        token, secret, url = self.discogs.get_authorize_url()

        auth = False
        while not auth:
            print('in order to access your access images from discogs you')
            print('need to verify your Discogs account using OAuth.')
            print(f'please visit {url} and accept the authentication request')
            oauth_code = input('Verification code: ')

            try:
                token, secret = self.discogs.get_access_token(oauth_code)
            except Exception as e:
                print(f'Unable to authenticate, please try again. error="{e}"')
                continue

            if token:
                auth = True
        with open('access_tokens.py', 'w') as f:
            f.write('access token: {token}')
            f.write('access secret: {secret}')

    def is_authenticated(self):
        """
        Returns True if token exists in local file
        """
        if os.path.isfile('access_tokens.py'):
            return True

    def search(self, params):
        """
        takes search params as param, col dict and returns image & image id
        """
        url = 'https://api.discogs.com/database/search?'
        for key, value in params.items():
            url += key + '=' + value + '&'

        url += 'key=' + self.consumer_key
        url += '&secret=' + self.consumer_secret

        response = requests.get(url).text
        data = json.loads(response)
        try:
            item = data['results'][0]
        except IndexError:
            print(f"Nothing found for {params['artist']}")
            return None

        time.sleep(1.1)
        cover_url = item['cover_image']
        cover_id = str(item['id'])
        response = requests.get(cover_url, stream=True)
        if response.status_code == 200:
            print(f"Downloaded image for {params['artist']}, id:{cover_id}")
            return response, cover_id
        else:
            print(f"Error getting {params['artist']}: {response.status_code}")
