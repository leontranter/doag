from systems import skill_manager

class Skills:

	def __init__(self):
		self.skills = {}

	def get_skill_rank(self, skill):
		skill_rank = self.skills.get(skill) or 0
		return skill_rank

	def get_skill_check(self, skill):
		skill_check_function = skill_manager.skill_check_lookups.get(skill)[0]
		skill_check = skill_check_function(self.owner)
		if skill not in self.skills:
			skill_check -= skill_manager.skill_check_lookups.get(skill)[1]
		return skill_check		

	def set_skill_rank(self, skill, rank):
		self.skills[skill] = rank

	def learn_skill(self, skill, rank):
		self.skills[skill] = rank
