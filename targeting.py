class Targeting:
	def __init__(self):
		self.current_targeting_consumable = None
		self.current_targeting_spell = None
		self.current_targeting_missile = False

	def __str__(self):
		rep = ""
		for k, v in self.__dict__.items():
			rep += str(k) + ": " + str(v) + "\n"
		
		return rep