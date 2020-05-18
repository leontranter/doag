class Dlevel:
	def __init__(self, entities, tiles, floor, explored=False):
		self.entities = entities
		self.tiles = tiles
		self.floor = floor
		self.explored = explored