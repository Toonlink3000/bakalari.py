import requests
import user
from exceptions import NotAuthenticatedError

class authenticated_method():
	def __init__(self, func):
		self.func = func

	def __call__(self, parent_class, *args, **kwargs):
		if parent_class.authenticated == True:
			result = self.func(parent_class, *args, **kwargs)

		else:
			raise NotAuthenticatedError(type(parent_class).__name__, parent_class.__name__, self.func.__name__)
			raise

		return result

class test_decorator():
	def __init__(self, function):
		self.function = function

def get_city_json():
	request = requests.get("https://sluzby.bakalari.cz/api/v1/municipality", headers={"Accept":"application/json"})

	return request.json()

def get_school_json(city:str):
	request = requests.get("https://sluzby.bakalari.cz/api/v1/municipality/$mesto", headers={"Accept":"application/json"})

	return request.json()

def get_campaign_banners(location:str, category_code:str):
	url = "https://campaign.bakalari.cz/bannerinfo/${}/${}".format(location, category_code)
	request = requests.get(url)
	result = requests.json()

	if "banners" not in result.keys():
		return result

	return result["banners"]

class Client():
	authenticated = False

	@classmethod
	def login(cls, adress:str, username:str, password:str, login_path = "/api/login"):
		payload = {
			"client_id": "ANDR",
			"grant_type": "password",
			"username": username, 
			"password": password
		}

		request = requests.post( adress + login_path, data=payload)
		value = request.json()

		if "error" in value.keys():
			print(f'bakalari.py: Error: {value["error_description"]}')
			return

		client = cls()
		client.api_adress = adress

		if "bak:UserId" in value.keys():
			client.user_id = value["bak:UserId"]
			client.app_version = value["bak:AppVersion"]
			client.access_token = value["access_token"]
			client.refresh_tokben = value["refresh_token"]
			client.expiration_date = value["expires_in"]
			client.scope = value["scope"]

			client.authenticated = True

		return client

	@authenticated_method
	def get_user(self) -> user.User:
		head = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Authorization": f"Bearer {self.access_token}"
		}
		request = requests.get(self.api_adress, headers)

	def logout(self):
		pass