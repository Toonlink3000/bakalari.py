from utils import BakalariModule

class TimetableModule(BakalariModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		load_stable_timetable()

	def load_stable_timetable():
		result = self.client.do_authenticated_request("/api/3/timetable/permanent", "get", head={"Content-Type": "application/x-www-form-urlencoded"})
		for item in result.keys():
			self.__dict__[item] = result["item"]

	def load_dated_timetable():
		pass