import math
import tcod as libtcod
from render_functions import RenderOrder
from components.item import Item
from components.caster import Caster

class Entity:
	"""
	A generic object for anything
	"""
	def __init__(self, x, y, char, color, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None, caster=None, stats=None, defender=None, skills=None, melee_weapon=None, missile_weapon=None, name=None, identified=None, effects=None):
		self.x = x
		self.y = y
		self.char = char
		self.color = color
		self.blocks = blocks
		self.render_order = render_order
		self.fighter = fighter
		self.ai = ai
		self.item = item
		self.inventory = inventory
		self.stairs = stairs
		self.level = level
		self.equipment = equipment
		self.equippable = equippable
		self.caster = caster
		self.stats = stats
		self.defender = defender
		self.skills = skills
		self.melee_weapon = melee_weapon
		self.missile_weapon = missile_weapon
		self.name = name
		self.identified = identified
		self.effects = effects

		if self.fighter:
			self.fighter.owner = self
		if self.ai:
			self.ai.owner = self
		if self.item:
			self.item.owner = self
		if self.inventory:
			self.inventory.owner = self
		if self.stairs:
			self.stairs.owner = self
		if self.level:
			self.level.owner = self
		if self.equipment:
			self.equipment.owner = self
		if self.equippable:
			self.equippable.owner = self
			if not self.item:
				item = Item()
				self.item = item
				self.item.owner = self
		if caster:
			self.caster.owner = self
		if stats:
			self.stats.owner = self
		if defender:
			self.defender.owner = self
		if skills:
			self.skills.owner = self
		if melee_weapon:
			self.melee_weapon.owner = self
		if missile_weapon:
			self.missile_weapon.owner = self
		if name:
			self.name.owner = self
		if identified:
			self.identified.owner = self
		if self.effects:
			self.effects.owner = self

	def move(self, dx, dy):
		self.x += dx
		self.y += dy

	def move_towards(self, target_x, target_y, game_map, entities):
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)
		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
			self.move(dx, dy)

	def distance(self, x, y):
		return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

	def move_astar(self, target, entities, game_map):
		# createa FOV map that has the dimensions of the map
		fov = libtcod.map_new(game_map.width, game_map.height)
		#scan the current map each turn and set all the walls as unwalkable
		for y1 in range(game_map.height):
			for x1 in range(game_map.width):
				libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)
		#scan all the objects to see if there are objects to be navigated around
		# check also that the object isn'tself or the target
		# the AI class handles the situation if the self is next to the target
		for entity in entities:
			if entity.blocks and entity != self and entity != target:
				#set the tile as a wall so it must be navigated around
				libtcod.map_set_properties(fov, entity.x, entity.y, True, False)
		# allocate a A* path
		# the 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
		my_path = libtcod.path_new_using_map(fov, 1.41)
		#compute the path between self's coordinates and target's coordinates
		libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)
		#check if the path exists and the path is shorter than 25
		# path size matters if you want the monster to use alternative longer paths
		if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
			# find the next coordinates in the computed full path
			x, y, = libtcod.path_walk(my_path, True)
			if x or y:
				# set self's coordinates to the next path tile
				self.x = x
				self.y = y
		else:
			# keep the old move funtion as a backup so that if there are no paths
			# it will still try to move towards the player
			self.move_towards(target.x, target.y, game_map, entities)
		# delete the path to free memory
		libtcod.path_delete(my_path)


	def distance_to(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)



def get_blocking_entities_at_location(entities, destination_x, destination_y):
	for entity in entities:
		if entity.blocks and entity.x == destination_x and entity.y == destination_y:
			return entity