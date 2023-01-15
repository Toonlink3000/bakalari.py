import requests
import user_info
from exceptions import NotAuthenticatedError, UnauthorisedAccessError, IncorrectLoginError
from utils import authenticated_method


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

class Class():
	def __init__(self, json):
		self.id = json["Id"]
		self.abreviated = json["Abbrev"]
		self.name = json["Name"]

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

		client.get_user_info()
		return client

	@authenticated_method
	def get_user_info(self) -> None:
		head = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Authorization": f"Bearer {self.access_token}"
		}
		request = requests.get(self.api_adress, headers)
		if request.status == 200:
			self._user_json = request

		elif request.status == 401:
			self.authenticated = False
			raise UnauthorisedAccessError

	def _merge_data_into_object(self):
		pass

	def get_class(self) -> Class:
		return Class(self._user_json["Class"])

	def get_enabled_modules(self) -> dict:
		result = {}
		for element in self._user_json["EnabledModules"]:
			result[element["Module"]] = element["Rights"]
		