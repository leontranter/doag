class Identified:
	#TODO: don't make the links optional... missing one of them makes stuff break all over the place
	def __init__(self, potion_links=None, scroll_links=None):
		self.identified_potions = []
		self.identified_scrolls = []
		self.potion_links = potion_links
		self.scroll_links = scroll_links