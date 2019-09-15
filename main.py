import csv
import requests
import json
import time
import numpy as np
import cv2
import urllib

import discogs_client as dc 
from login_details import *
from search_params import Params

# hard coded while testing
input_file = 'AlbumsExport.csv'




def get_url(line):
	base_url = 'https://api.discogs.com/database/search?artist=' 
	url = base_url + artist + '&title=' + title + '&key=' + consumer_key + '&secret=' + consumer_secret
	headers = {'User-Agent': user_agent}
	response = requests.get(url, headers=headers).text
	data = json.loads(response)
	# print(json.dumps(data, indent=4, sort_keys=True))

	try:
		item = data['results'][0]
	except IndexError:
		print(f"Nothing found for {artist}-{title}")
		with open('output.csv', 'a', encoding='utf-8') as output:
			output_csv = csv.writer(output)
			output_csv.writerow([artist, title, 'Null'])
		return None

	cover_url = item['cover_image']
	image_id = str(item['id'])

	time.sleep(1.1)
	try:
		request = urllib.request.Request(cover_url, headers=headers)
		response = urllib.request.urlopen(request)
	except urllib.error.HTTPError:
		print(f"HTTP error getting {artist} cover jpg.")
		with open('output.csv', 'a', encoding='utf-8') as output:
			output_csv = csv.writer(output)
			output_csv.writerow([artist, title, 'Null'])
			return None

	return response
def get_image(url):
	binary_str = response.read()
	file_obj = open('images/' + image_id + '.jpg', 'wb')
	file_obj.write(binary_str)
	file_obj.close()

	with open('output.csv', 'a', encoding='utf-8') as output:
			csv_writer = csv.writer(output)
			csv_writer.writerow([artist, title, image_id])
			time.sleep(1.2)

if __name__ == '__main__':
	# First get authentication, details from login_details
	ds = dc.Client(user_agent, user_token=access_token)
	# then get param_dict(key=search param, value=column) from CSV file
	params = Params(input_file, delimiter=';', encoding='utf-8-sig')

	param_dict = params.get_param_dict()
	# We should confirm delimiter/encoding etc before this
	print(param_dict)

	with open(input_file, 'r', encoding='utf-8-sig') as file:
		csv_reader = csv.reader(file, delimiter=';')
		next(csv_reader)
		for line in csv_reader:
			image_url = get_url(line, param_dict)	
			image = get_image(image_url)


