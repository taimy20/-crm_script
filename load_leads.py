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

def load_file_to_df(filepath):
	df = pd.read_csv(filepath)
	df.columns = [x.lower().strip() for x in df.columns]
	return df

def get_state_code(state_map, state_name):
	name_to_code = {}
	for index, row in state_map.iterrows():
		name_to_code[row['state']] = row['abbreviation']
	return name_to_code[state_name]

def create_payload_from_lead(state_map, lead):

	campaign = 199031354236960
	line_of_business = 'SMB Marketing'
	phone = lead['work phone'].strip()
	email = lead['email'].strip()
	company = lead['company name'].strip()
	countryCode = lead['country'].strip()

	if len(lead['state']) == 2:
		stateCode = lead['state'].upper().strip()
	else:
		stateCode = get_state_code(state_map, lead['state'].strip())

	city = lead['city'].strip()
	zipCode = lead['zip code']
	street = lead['street'].strip()
	firstname = lead['first name'].strip()
	lastname = lead['last name'].strip()
	jobtitle = lead['title'].strip()
	industry = lead['industry'].strip()
	employees = lead['company employees'].strip()
	# revenue = lead['']

	payload = 	{
					'qualification': 'HOT',
					'status': 'OPEN',
					'campaign':
						{
							'id': campaign,
						},
					'phone' : phone,
					'email': email,
					'relatedName': company,
					'address':
						{
							'countryCode': countryCode,
							'stateCode': stateCode,
							'cityName' : city,
							'street1' : street,
							'zipCode' : zipCode,
						},
					'customFields':
						{
							'ext_default_leadlob': line_of_business,
							'ext_default_leadsfirstname': firstname,
							'ext_default_leadslastname': lastname,
							'ext_default_leadsjobtitle': jobtitle,
							'ext_default_companyindustry': industry,
							'ext_default_companyemployees': employees,
							# 'ext_default_companyrevenue': revenue,
						}
				}

	return payload

def upload_leads_to_crm(leads):

	state_map = load_file_to_df('states.csv')

	counter = 1

	awclient = awClient()
	service = 'Leads'
	for index, lead in leads.iterrows():
		payload = create_payload_from_lead(state_map, lead)
		request = awclient.post_request(service, payload)
		if request.status_code != 201:
			print 'Lead ' + str(counter) + ': FAILURE'
			print request
		else:
			print 'Lead ' + str(counter) + ': OK'
		counter += 1

def usage():
  print "Usage: " + sys.argv[0] + " <filename>"
  sys.exit(1)

def main(filename):
  if filename[-4:] == '.csv':
  	filepath = filename
  else:
  	filepath = filename + '.csv'
  leads_df = load_file_to_df(filepath)
  upload_leads_to_crm(leads_df)

if __name__ == '__main__':
  if len(sys.argv) == 2:
  	filename = sys.argv[1].strip().lower()
  	main(filename)
  else:
  	usage()
