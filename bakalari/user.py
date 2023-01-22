from utils import BakalariModule

class UserModule(BakalariModule):
	def __init__(self, parent):
		self.client = parent