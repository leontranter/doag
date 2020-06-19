class Name:
	def __init__(self, true_name="", equippable_name=""):
		self.true_name = true_name
		self.equippable_name = true_name
		if self.true_name == "Player":
			self.subject_name = "You"
			self.object_name = "you"
		else:
			self.subject_name = "The " + self.true_name
			self.object_name = "the " + self.true_name