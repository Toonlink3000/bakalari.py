class NotAuthenticatedError(Exception):
	def __init__(self, cls, instance, function):
		self.cls = cls
		self.instance = instance
		self.function = function

	def __str__():
		return f"bakalari.py: Error: In {self.cls} instance '{self.instance}' in function '{self.function}, not authenticated or authentication timed out.'"

class ConnectionFailedError(Exception):
	pass

class UnauthorisedAccessError(Exception):
	def __str__(self):
		return "bakalari.py Error, invalid access token provided when connecting."
		
