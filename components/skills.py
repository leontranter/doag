from systems.skill_manager import skill_check_lookups

class Skills:
	def __init__(self):
		self.skills = {}

	def get_skill_rank(self, skill):
		skill_rank = self.skills.get(skill) or 0
		return skill_rank

	def get_skill_check(self, skill):
		skill_check_function_1 = skill_check_lookups.get(skill)[0]
		skill_check_function_2 = skill_check_lookups.get(skill)[1]
		skill_check = int((skill_check_function_1(self.owner) + skill_check_function_2(self.owner)) / 2)
		if skill not in self.skills:
			skill_check -= skill_check_lookups.get(skill)[2]
		if self.get_skill_rank(skill) > 1:
			skill_check += self.get_skill_rank(skill) - 1
		return skill_check		

	def set_skill_rank(self, skill, rank):
		self.skills[skill] = rank