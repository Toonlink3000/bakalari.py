import exceptions

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
