import requests
import json
import pandas as pd
import sys

class awClient:
	def __init__(self):
		self.access_token = self.get_token()

	def get_token(self):
		client_id = 'd0jBh6O3Is2uJGeFgefFtluj6iCy9cgQ'
		client_secret = '9YJqQz9VGmZvQCM46S2EtYD7fdTSrYLL'
		refresh_token = 'f7827d56-8999-4c74-9728-0eb871043af2'
		url = 'https://go.sapanywhere.com/oauth2/token'
		headers = {'Content-type': 'application/x-www-form-urlencoded'}
		data = {'client_id': client_id, 'client_secret': client_secret, 'grant_type': 'refresh_token', 'refresh_token': refresh_token}

		r = requests.post(url, data=data, headers=headers)

		if r.status_code == 200:
			access_token = r.json()['access_token']
			return access_token
		else:
			print "failed token request"
			sys.exit(0)

	def get_request(self, service):
		base_url = 'https://api.sapanywhere.com/v1/'
		headers = {'Content-type': 'application/json'}
		params = {'access_token': self.access_token}
		r = requests.get(base_url + service, params=params, headers=headers)
		print r.__dict__
		return r

	def post_request(self, service, payload):
		base_url = 'https://api.sapanywhere.com/v1/'
		headers = {'Content-type': 'application/json'}
		params = {'access_token': self.access_token}
		r = requests.post(base_url + service, params=params, data=json.dumps(payload), headers=headers)
		return r

	def patch_request(self, service, id, payload):
		base_url = 'https://api.sapanywhere.com/v1/'
		headers = {'Content-type': 'application/json'}
		params = {'access_token': self.access_token}
		r = requests.patch(base_url + service + '/' + str(id), params=params, data=json.dumps(payload), headers=headers)
		return r

awClient = awClient()

awClient.get_request('Campaigns')
