from utils import BakalariModule

class HomeworkModule(BakalariModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.load_homework()

	def load_homework():
		result = self.client.do_authenticated_request("/api/3/homeworks", "get", head={"Content-Type": "application/x-www-form-urlencoded"})
		for item in result.keys():
			self.__dict__[item] = result["item"]
