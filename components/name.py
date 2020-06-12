class Name:
	def __init__(self, true_name="", display_name=""):
		self.true_name = true_name
		if display_name == "":
			self.display_name = true_name
		else:
			self.display_name = display_name