class Skills:
	def __init__(self):
		self.skills = {}

	def getSkill(self, skill):
		skillValue = self.skills.get(skill)
		# TODO: Put in defaults (link to global skill book)
		if skillValue == None:
			skillValue = 8
		return skillValue

	def setSkill(self, skill, amount):
		self.skills[skill] = amount