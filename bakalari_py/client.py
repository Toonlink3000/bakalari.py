import requests

def get_city_json():
	request = requests.get("https://sluzby.bakalari.cz/api/v1/municipality", headers={"Accept":"application/json"})

	return request.json()

def get_school_json(city:str):
	request = requests.get("https://sluzby.bakalari.cz/api/v1/municipality/$mesto", headers={"Accept":"application/json"})

	return request.json()

class Client():
	authenticated = False

	@classmethod
	def login(cls, adress:str, username:str, password:str, login_path = "/api/login"):
		payload = {
						"client_id": "ANDR",
						"grant_type": "password",
						"username":username, 
						"password": password
		}

		request = requests.post( adress + login_path, data=payload)
		value = request.json()

		if "error" in value.keys():
			print(f'bakalari.py: Error: {value["error_description"]}')
			return

		client = cls()

		if "bak:UserId" in value.keys():
			client.user_id = value["bak:UserId"]
			client.app_version = value["bak:AppVersion"]
			client.access_token = value["access_token"]
			client.refresh_token = value["refresh_token"]
			client.expiration_date = value["expires_in"]
			client.scope = value["scope"]

			client.authenticated = True

		return client

	def logout(self):
		pass