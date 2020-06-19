class Name:
	def __init__(self, true_name="", display_name=""):
		self.true_name = true_name
	
	@property
	# TODO: fix this - pretty terrible! need to refactor items completely (urgh)
	def display_name(self):
		if self.owner.item:
			if self.owner.item.use_function:
				# Check if player has identified this or not
				if true_name in self.owner.identified.identified_potions or true_name in self.owner.identified.identified_scrolls:
					display_name = self.true_name
				else:
					display_name = ""
			if self.owner.equippable:
				# Fix this later
				display_name = self.true_name
		else:
			display_name = self.true_name
		return display_name